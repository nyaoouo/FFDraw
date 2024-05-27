import ctypes
import inspect

import imgui

from ff_draw.mem.utils import bit_field_property
from nylib.utils.imgui import ctx as imgui_ctx
from nylib.utils.win32 import memory as ny_mem
from ff_draw.mem import XivMem

address_size = ctypes.sizeof(ctypes.c_size_t)


def scan_val(sig, is_unique=True, res_idx=0):
    def _scan_point():
        from ffd_plus.api import Api
        res = list(Api.instance.scanner.find_vals(sig))
        if not res:
            raise KeyError(f'pattern is not found for sig {sig}')
        if not is_unique and len(res) > 1:
            raise KeyError(f'pattern is not unique, {len(res)} is found for sig {sig}')
        return res[0][res_idx]

    return _scan_point


def scan_straight(sig, is_unique=True):
    def _scan_straight():
        from ffd_plus.api import Api
        res = list(Api.instance.scanner.find_addresses(sig))
        if not res:
            raise KeyError(f'pattern is not found for sig {sig}')
        if not is_unique and len(res) > 1:
            raise KeyError(f'pattern is not unique, {len(res)} is found for sig {sig}')
        return res[0]

    return _scan_straight


def multiple_getter(*getters):
    def _multiple_getter():
        for getter in getters:
            try:
                return getter()
            except:
                pass
        raise KeyError(f'no getter is valid')

    return _multiple_getter


class StaticFunction:
    def __init__(self, addr_getter, res_type: str, *arg_types: str, main_loop=False):
        self.addr_getter = addr_getter
        self.res_type = res_type
        self.arg_types = arg_types
        self._addr = None
        self._payload = None
        self.main_loop = main_loop

    @property
    def callee(self):
        return XivMem.instance.call_once_game_main if self.main_loop else XivMem.instance.inject_handle.run

    @property
    def payload(self):
        if self._payload is None:
            self._payload = f'from ctypes import *\nres=CFUNCTYPE({self.res_type},{",".join(self.arg_types)})({self.address})(*args)'
        return self._payload

    @property
    def address(self):
        if self._addr is None:
            self._addr = self.addr_getter()
            delattr(self, 'addr_getter')
        return self._addr

    def __get__(self, instance, owner):
        if instance is None: return self
        return lambda *args: self.callee(self.payload, *args)


class ClassFunction(StaticFunction):
    @property
    def payload(self):
        if self._payload is None:
            self._payload = f'from ctypes import *\nres=CFUNCTYPE({self.res_type},c_void_p,{",".join(self.arg_types)})({self.address})(*args)'
        return self._payload

    def __get__(self, instance, owner):
        if instance is None: return self
        return lambda *args: self.callee(self.payload, instance.address, *args)


class VirtualFunction:
    def __init__(self, vt_idx, res_type: str, *arg_types: str, vt_attr: str = '_vtbl', main_loop=False):
        self.vt_idx = vt_idx
        self.vt_attr = vt_attr
        self.owner = None
        self.res_type = res_type
        self.arg_types = arg_types
        self._payload = None
        self.main_loop = main_loop

    def __set_name__(self, owner, name):
        self.owner = owner

    @property
    def callee(self):
        return XivMem.instance.call_once_game_main if self.main_loop else XivMem.instance.inject_handle.run

    @property
    def payload(self):
        if self._payload is None:
            self._payload = f'from ctypes import *\nres=CFUNCTYPE({self.res_type},c_void_p,{",".join(self.arg_types)})(args[0])(*args[1:])'
        return self._payload

    def get_address(self, instance):
        return ny_mem.read_address(
            instance.handle,
            ny_mem.read_address(
                instance.handle,
                instance.address + getattr(self.owner.offsets, self.vt_attr, 0)
            ) + self.vt_idx * address_size
        )

    def __get__(self, instance, owner):
        if instance is None: return self
        return lambda *args: self.callee(self.payload, self.get_address(instance), instance.address, *args)


class BitFieldData:
    def __init__(self, handle, address):
        self.handle = handle
        self.address = address

    def render_panel(self):
        with imgui_ctx.TreeNode(self.__class__.__name__) as n, n:
            num_field = []
            for name, bf in bit_field_property.obj_properties(self.__class__):
                if name.startswith('_'): continue
                if bf.data_size > 8:
                    num_field.append(name)
                else:
                    color = (0, 1, 0, 1) if getattr(self, name) else (1, 0, 0, 1)
                    imgui.text_colored(name, *color)
            for name in num_field:
                imgui.input_int(name, getattr(self, name), 0, 0, imgui.INPUT_TEXT_READ_ONLY)


class Offset:
    def __init__(self, off):
        self.off = off
        self.backup = None

    def __enter__(self):
        assert self.backup is None
        self.backup = set(inspect.stack()[1].frame.f_locals.keys())

    def __exit__(self, exc_type, exc_val, exc_tb):
        assert self.backup is not None
        f_local = inspect.stack()[1].frame.f_locals
        for k in set(f_local.keys()) - self.backup:
            if isinstance((val := f_local[k]), int):
                f_local[k] = val + self.off
        self.backup = None


class MemPad:
    def __init__(self, start=0, max_pad=0x10):
        self.ptr = start
        self.max_pad = max_pad

    def __call__(self, size):
        to_pad = min(self.max_pad, max(size, 1)) - 1
        self.ptr = (self.ptr + to_pad) & ~to_pad
        ret = self.ptr
        self.ptr += size
        return ret
