import json
import math
import os
import typing

import glfw
import glm
import imgui

from nylib.utils.win32 import memory as ny_mem, process as ny_proc
from nylib.pefile import PE
from nylib.pattern import StaticPatternSearcher
from . import utils, actor, party, network_target, packet_fix, marking, territory_info, event_module, quest_info, storage

if typing.TYPE_CHECKING:
    from ff_draw.main import FFDraw


class XivMemPanel:
    def __init__(self, mem: 'XivMem'):
        self.main = mem.main
        self.mem = mem
        self.cached_tid = -1
        self.territory = ''
        self.cached = ''
        self.show_exit_process = False
        self.is_dev = False

    def render(self):
        mem = self.mem

        imgui.text(f'pid: {mem.pid}')
        imgui.same_line()
        if self.show_exit_process:
            if imgui.button(f'kill process!'):
                from nylib.utils.win32.winapi.kernel32 import TerminateProcess
                TerminateProcess(mem.handle, 0)
                os._exit(0)
        else:
            self.show_exit_process = imgui.button(f'kill process?')

        imgui.text(f'game_version: {mem.game_version}')
        imgui.text(f'game_build_date: {mem.game_build_date}')

        if me := mem.actor_table.me:
            imgui.text(f'me: {me.name}#{me.id:#x}')
            tinfo = mem.territory_info
            tid = tinfo.territory_id
            if tid != self.cached_tid:
                self.cached_tid = tid
                try:
                    territory = self.main.sq_pack.sheets.territory_type_sheet[tid]
                except KeyError:
                    self.territory = 'N/A'
                else:
                    self.territory = f'{territory.region.text_sgl}-{territory.sub_region.text_sgl}-{territory.area.text_sgl}'
            imgui.text(f'territory: {self.territory}')
            imgui.text(f'[Tid: {tid}][Layer: {tinfo.layer_id}][Weather: {tinfo.weather_id}/{tinfo.weather_is_content}]')
            imgui.text(f'pos: {me.pos}#{me.facing / math.pi:.2f}pi')
        else:
            imgui.text(f'me: N/A')

        if imgui.tree_node('EventModule'):
            if imgui.tree_node('ContentInfo'):
                try:
                    cinfo = mem.event_module.content_info
                    imgui.text(f'handler_id: {cinfo.handler_id:#X}')
                    imgui.text(f'content_id: {cinfo.content_id:#X}')
                    imgui.text(f'title: {cinfo.title}')
                    imgui.text(f'text1: {cinfo.text1}')
                    imgui.text(f'text2: {cinfo.text2}')
                    imgui.text('todo_list')
                    if imgui.tree_node('Todo List'):
                        try:
                            for todo in cinfo.todo_list:
                                if not todo.is_valid: break
                                imgui.text(f'[{todo.is_finished}]{todo.desc}')
                        except Exception as e:
                            imgui.text('N/A - ' + str(e))
                        imgui.tree_pop()
                except Exception as e:
                    imgui.text('N/A - ' + str(e))
                imgui.tree_pop()
            imgui.tree_pop()
        if imgui.tree_node(f'QuestInfo'):
            quest_sheet = self.main.sq_pack.sheets.quest_sheet
            try:
                for quest in mem.quest_info.quests():
                    try:
                        quest_data = quest_sheet[quest.id | 0x10000]
                    except KeyError:
                        imgui.text(f'N/A#{quest.id}[{quest.seq}]')
                    else:
                        imgui.text(f'{quest_data.text}#{quest.id}[{quest.seq}]')
            except Exception as e:
                imgui.text('N/A - ' + str(e))

            imgui.tree_pop()
        if not self.is_dev:
            io = imgui.get_io()
            if io.key_ctrl and io.key_shift and io.key_alt and io.keys_down[glfw.KEY_D]:
                self.is_dev = True
        else:
            _, self.mem.actor_table.use_brute_search = imgui.checkbox('actor_table use_brute_search', self.mem.actor_table.use_brute_search)


class CachedSigScanner(StaticPatternSearcher):
    def __init__(self, mem: 'XivMem', pe, base_address):
        super().__init__(pe, base_address)
        self.mem = mem
        self._cache_file = mem.main.app_data_path / 'sig_cache' / (mem.game_build_date + '.json')
        self._cache = self._load_cache()

    def find_address(self, pattern):
        cache = self._cache.setdefault('address', {})
        if pattern in cache:
            return cache[pattern] + self.base_address
        address = super().find_address(pattern)
        cache[pattern] = address - self.base_address
        self._save_cache()
        return address

    def find_point(self, pattern: str):
        cache = self._cache.setdefault('point', {})
        if pattern in cache:
            return [a + self.base_address for a in cache[pattern]]
        point = super().find_point(pattern)
        cache[pattern] = [a - self.base_address for a in point]
        self._save_cache()
        return point

    def find_val(self, pattern: str):
        cache = self._cache.setdefault('val', {})
        if pattern in cache:
            return cache[pattern]
        val = super().find_val(pattern)
        cache[pattern] = val
        self._save_cache()
        return val

    def _load_cache(self):
        if not self._cache_file.exists(): return {}
        try:
            with self._cache_file.open('r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return {}

    def _save_cache(self):
        self._cache_file.parent.mkdir(parents=True, exist_ok=True)
        with self._cache_file.open('w', encoding='utf-8') as f:
            json.dump(self._cache, f, indent=4, ensure_ascii=False)


class XivMem:
    def __init__(self, main: 'FFDraw', pid: int):
        self.main = main
        self.pid = pid
        self.handle = ny_proc.open_process(pid)
        self.base_module = ny_proc.get_base_module(self.handle)
        file_name = self.base_module.filename.decode(self.main.path_encoding)
        self.hwnd = utils.get_hwnd(self.pid)
        self.game_version, self.game_build_date = utils.get_game_version_info(file_name)
        self.scanner = CachedSigScanner(self, PE(file_name, fast_load=True), self.base_module.lpBaseOfDll)
        self.screen_address = self.scanner.find_point('48 ? ? * * * * e8 ? ? ? ? 42 ? ? ? 39 05')[0] + 0x1b4
        self.replay_flag_address = self.scanner.find_point('84 1d * * * * 74 ? 80 3d')[0]
        self._a_p_framework = self.scanner.find_point('48 ? ? * * * * 41 39 b1')[0]
        self.actor_table = actor.ActorTable(self)
        self.party = party.PartyManager(self)
        self.network_target = network_target.NetworkInfo(self)
        self.packet_fix = packet_fix.PacketFix(self)
        self.marking = marking.MarkingController(self)
        self.territory_info = territory_info.TerritoryInfo(self)
        self.event_module = event_module.EventModule(self)
        self.quest_info = quest_info.QuestInfo(self)
        self.storage = storage.StorageManager(self)
        self.panel = XivMemPanel(self)

    def load_screen(self):
        buf = ny_mem.read_bytes(self.handle, self.screen_address, 0x48)
        return glm.mat4.from_bytes(bytes(buf[:0x40])), glm.vec2.from_bytes(bytes(buf[0x40:]))

    @property
    def p_framework(self):
        return ny_mem.read_address(self.handle, self._a_p_framework)

    @property
    def is_in_replay(self):
        return (ny_mem.read_ubyte(self.handle, self.replay_flag_address) & 0b100) > 0
