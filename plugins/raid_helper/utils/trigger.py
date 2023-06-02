import functools
import threading
import typing

import glm
import imgui

from nylib.utils import BroadcastHook
from ff_draw.main import FFDraw
from ff_draw.gui import i18n
from .typing import *

if typing.TYPE_CHECKING:
    from .. import RaidHelper

main = FFDraw.instance
raid_helper: 'RaidHelper|None' = None


class TValue:
    _cache_need_init = []
    _cache_value: typing.Any

    def __init__(self, key: str, label: str, default_value=None, on_change=None):
        self.key = key
        self.label = label
        self.default_value = default_value
        if isinstance(on_change, list):
            self.on_change = on_change
        elif callable(on_change):
            self.on_change = [on_change]
        else:
            self.on_change = []

    def val_serialize(self, v):
        return v

    def val_deserialize(self, v):
        return v

    @property
    def value(self):
        if hasattr(self, '_cache_value'): return self._cache_value
        val = self.val_deserialize(raid_helper.data.setdefault('values', {}).get(self.key, self.default_value))
        self._cache_value = val
        return val

    @value.setter
    def value(self, v):
        raid_helper.data.setdefault('values', {})[self.key] = v
        raid_helper.storage.save()
        for f in self.on_change: f(v)
        self._cache_value = v

    def reset(self):
        raid_helper.data.setdefault('values', {}).pop(self.key, None)
        raid_helper.storage.save()
        self._cache_value = self.default_value
        for f in self.on_change: f(self.default_value)


    def do_render(self):
        imgui.text(self.label + ': ')
        self.render()

    def render(self):
        imgui.same_line()
        changed, value = imgui.input_text('##' + self.key, self.value, 256, imgui.COLOR_EDIT_NO_LABEL)
        if changed: self.value = value

    def __init_cb(self, f):
        def cb():
            if self.key in (vals := raid_helper.data.setdefault('values', {})):
                f(vals[self.key])

        return cb

    def listen_change(self, f):
        self.on_change.append(f)
        cb = self.__init_cb(f)
        if raid_helper:
            cb()
        else:
            self._cache_need_init.append(cb)
        return f


class IntSlider(TValue):
    def __init__(self, key: str, min_value, max_value, default_value):
        super(IntSlider, self).__init__(key + ':int', key.rsplit('/', 1)[-1], default_value)
        self.min_value = min_value
        self.max_value = max_value

    def render(self):
        imgui.same_line()
        changed, value = imgui.slider_int('##' + self.key, self.value, self.min_value, self.max_value)
        if changed: self.value = value


class BoolCheckBox(TValue):
    def __init__(self, key: str, default_value):
        super(BoolCheckBox, self).__init__(key + ':bool', key.rsplit('/', 1)[-1], default_value)

    def render(self):
        imgui.same_line()
        changed, value = imgui.checkbox('##' + self.key, self.value)
        if changed: self.value = value


class Color4f(TValue):
    def __init__(self, key: str, default_value, flags=0):
        self.flags = flags
        super(Color4f, self).__init__(key + ':color4f', key.rsplit('/', 1)[-1], list(default_value))

    def val_serialize(self, v):
        assert len(v) == 4
        return list(v)

    def val_deserialize(self, v):
        assert len(v) == 4
        return glm.vec4(*v)

    def render(self):
        imgui.same_line()
        changed, value = imgui.color_edit4('##' + self.key, *self.value, self.flags)
        if changed: self.value = value
        imgui.same_line()
        if imgui.button(i18n.i18n(i18n.Reset) + '##reset_btn' + self.key):
            self.reset()


class Color3f(TValue):
    def __init__(self, key: str, default_value, flags=0):
        self.flags = flags
        super(Color3f, self).__init__(key + ':color3f', key.rsplit('/', 1)[-1], list(default_value))

    def val_serialize(self, v):
        assert len(v) == 3
        return list(v)

    def val_deserialize(self, v):
        assert len(v) == 3
        return glm.vec3(*v)

    def render(self):
        imgui.same_line()
        changed, value = imgui.color_edit3('##' + self.key, *self.value, self.flags)
        if changed: self.value = value
        imgui.same_line()
        if imgui.button(i18n.i18n(i18n.Reset) + '##reset_btn' + self.key):
            self.reset()


class Select(TValue):
    def __init__(self, key: str, options: list[tuple[str, typing.Any]], default_value):
        super(Select, self).__init__(key + ':any', key.rsplit('/', 1)[-1], default_value)
        self.options = options

    def render(self):
        imgui.same_line()
        imgui.push_id(self.key)
        current_value = self.value
        try:
            selected_key = next(k for k, v in self.options if v == current_value)
        except StopIteration:
            selected_key = 'Select...'
        if imgui.button(selected_key):
            imgui.open_popup("select")
        if imgui.begin_popup("select"):
            imgui.push_id('select')
            for k, v in self.options:
                if imgui.selectable(k)[1]:
                    self.value = v
            imgui.pop_id()
            imgui.end_popup()
        imgui.pop_id()


pair_all = (None,)


class HookMap:
    def __init__(self):
        self.call_map = {}
        self.hook_map = {}

    def get(self, hook: BroadcastHook):
        return self.call_map.get(id(hook), [])

    def set(self, hook: BroadcastHook, call):
        self.hook_map[id(hook)] = hook
        if call not in (call_list := self.call_map.setdefault(id(hook), [])):
            call_list.append(call)

    def iter(self):
        for i, h in self.hook_map.items():
            yield h, self.call_map.get(i, [])


def call_safe(func, *args):
    return raid_helper.create_mission(func, *args, _log_exception=True)


class TriggerGroup:
    def __init__(self, identifier: str, label=None):
        self.identifier = identifier
        self.label = label or identifier
        self._decorators = {}
        self.hook_map = HookMap()
        self.value_tree = {}
        self.values = {}

        self._on_lockon_map = {}
        self._on_cast_map = {}
        self._on_effect_map = {}
        self._on_add_status = {}
        self._on_set_channel = {}
        self._on_cancel_channel = {}
        self._on_npc_spawn = {}
        self._on_npc_yell = {}
        self._on_object_spawn = {}
        self._on_actor_delete = []
        self._on_actor_play_action_timeline = {}
        self._on_map_effect = []
        self._on_reset = []

    @property
    def decorators(self) -> list[typing.Callable[[typing.Callable], typing.Callable]]:
        return self._decorators.setdefault(threading.get_ident(), [])

    @decorators.setter
    def decorators(self, v: list[typing.Callable[[typing.Callable], typing.Callable]]):
        self._decorators[threading.get_ident()] = v

    def clear_decorators(self):
        self._decorators.pop(threading.get_ident(), None)

    def _add_set(self, d, ids):
        def dec(f):
            for _d in self._decorators.get(threading.get_ident(), []):
                f = _d(f)
            for i in ids:
                d.setdefault(i, []).append(f)
            return f

        return dec

    def add_value(self, v: TValue):
        key = v.key
        v.key = self.identifier + '/' + key
        vt = self.value_tree
        *directory, _key = key.split('/')
        for k in directory:
            vt = vt.setdefault(k, {})
        self.values.setdefault(tuple(directory), {})[_key] = v
        return v

    def _render_directory(self, p: tuple, vt: dict, ind=0):
        if p in self.values:
            for v in self.values.get(p, {}).values():
                v.do_render()
        for sub_directory, _vt in vt.items():
            if imgui.tree_node(sub_directory):
                self._render_directory(p + (sub_directory,), _vt, ind + 1)
                imgui.tree_pop()

    def get_index(self):
        return 0

    def render(self, highlight=None):
        if not self.values: return
        if highlight:
            imgui.push_style_color(imgui.COLOR_TEXT, *highlight)
        if imgui.tree_node(self.label):
            if highlight:
                imgui.pop_style_color()
            self._render_directory((), self.value_tree)
            imgui.tree_pop()
        elif highlight:
            imgui.pop_style_color()

    # region on_lockon
    def _recv_on_lockon(self, msg: ActorControlMessage[actor_control.SetLockOn]):
        for c in self._on_lockon_map.get(msg.param.lockon_id, ()): call_safe(c, msg)
        for c in self._on_lockon_map.get(None, ()):  call_safe(c, msg)  # pair all

    def on_lockon(self, *icon_id):
        self.hook_map.set(main.sniffer.on_actor_control[ActorControlId.SetLockOn], self._recv_on_lockon)
        return self._add_set(self._on_lockon_map, icon_id or pair_all)

    # endregion
    # region on_cast
    def _recv_on_cast(self, msg: NetworkMessage[zone_server.ActorCast]):
        if msg.message.action_kind != 1: return
        for c in self._on_cast_map.get(msg.message.action_id, ()): call_safe(c, msg)
        for c in self._on_cast_map.get(None, ()):  call_safe(c, msg)  # pair all

    def on_cast(self, *action_id):
        self.hook_map.set(main.sniffer.on_zone_server_message[ZoneServer.ActorCast], self._recv_on_cast)
        return self._add_set(self._on_cast_map, action_id or pair_all)

    # endregion
    # region on_effect
    def _recv_on_effect(self, msg: NetworkMessage[zone_server.ActionEffect]):
        if msg.message.action_kind != 1: return
        for c in self._on_effect_map.get(msg.message.action_id, ()): call_safe(c, msg)
        for c in self._on_effect_map.get(None, ()):  call_safe(c, msg)  # pair all

    def on_effect(self, *action_id):
        self.hook_map.set(main.sniffer.on_action_effect, self._recv_on_effect)
        return self._add_set(self._on_effect_map, action_id or pair_all)

    # endregion
    # region on_add_status
    def _recv_on_add_status(self, msg: ActorControlMessage[actor_control.AddStatus]):
        for c in self._on_add_status.get(msg.param.status_id, ()): call_safe(c, msg)
        for c in self._on_add_status.get(None, ()):  call_safe(c, msg)  # pair all

    def on_add_status(self, *status_id):
        self.hook_map.set(main.sniffer.on_actor_control[ActorControlId.AddStatus], self._recv_on_add_status)
        return self._add_set(self._on_add_status, status_id or pair_all)

    # endregion
    # region on_npc_spawn
    def _recv_on_npc_spawn(self, msg: NetworkMessage[zone_server.NpcSpawn | zone_server.NpcSpawn2]):
        for c in self._on_npc_spawn.get(msg.message.create_common.npc_id, ()): call_safe(c, msg)
        for c in self._on_npc_spawn.get(None, ()):  call_safe(c, msg)  # pair all

    def on_npc_spawn(self, *base_id):
        self.hook_map.set(main.sniffer.on_zone_server_message[ZoneServer.NpcSpawn], self._recv_on_npc_spawn)
        self.hook_map.set(main.sniffer.on_zone_server_message[ZoneServer.NpcSpawn2], self._recv_on_npc_spawn)
        return self._add_set(self._on_npc_spawn, base_id or pair_all)

    # endregion
    # region on_object_spawn
    def _recv_on_object_spawn(self, msg: NetworkMessage[zone_server.ObjectSpawn]):
        for c in self._on_object_spawn.get(msg.message.base_id, ()): call_safe(c, msg)
        for c in self._on_object_spawn.get(None, ()):  call_safe(c, msg)  # pair all

    def on_object_spawn(self, *base_id):
        self.hook_map.set(main.sniffer.on_zone_server_message[ZoneServer.ObjectSpawn], self._recv_on_object_spawn)
        return self._add_set(self._on_object_spawn, base_id or pair_all)

    # endregion
    # region on_actor_delete
    def _recv_on_actor_delete(self, msg: NetworkMessage[zone_server.ActorDelete]):
        for c in self._on_actor_delete: call_safe(c, msg)

    def on_actor_delete(self, func):
        for _d in self._decorators.get(threading.get_ident(), []): func = _d(func)
        self.hook_map.set(main.sniffer.on_zone_server_message[ZoneServer.ActorDelete], self._recv_on_actor_delete)
        self._on_actor_delete.append(func)
        return func

    # endregion
    # region on_actor_delete
    def _recv_on_npc_yell(self, msg: NetworkMessage[zone_server.NpcYell]):
        for c in self._on_npc_yell.get(msg.message.npc_yell_id, ()): call_safe(c, msg)
        for c in self._on_npc_yell.get(None, ()):  call_safe(c, msg)  # pair all

    def on_npc_yell(self, *npc_yell_id):
        self.hook_map.set(main.sniffer.on_zone_server_message[ZoneServer.NpcYell], self._recv_on_npc_yell)
        return self._add_set(self._on_npc_yell, npc_yell_id or pair_all)

    # endregion
    # region on_set_channel
    def _recv_on_set_channel(self, msg: ActorControlMessage[actor_control.SetChanneling]):
        for c in self._on_set_channel.get(msg.param.channel_id, ()): call_safe(c, msg)
        for c in self._on_set_channel.get(None, ()):  call_safe(c, msg)  # pair all

    def on_set_channel(self, *channel_id):
        self.hook_map.set(main.sniffer.on_actor_control[ActorControlId.SetChanneling], self._recv_on_set_channel)
        return self._add_set(self._on_set_channel, channel_id or pair_all)

    # endregion
    # region on_cancel_channel
    def _recv_on_cancel_channel(self, msg: ActorControlMessage[actor_control.RemoveChanneling]):
        for c in self._on_cancel_channel.get(msg.param.channel_id, ()): call_safe(c, msg)
        for c in self._on_cancel_channel.get(None, ()):  call_safe(c, msg)  # pair all

    def on_cancel_channel(self, *channel_id):
        self.hook_map.set(main.sniffer.on_actor_control[ActorControlId.RemoveChanneling], self._recv_on_cancel_channel)
        return self._add_set(self._on_cancel_channel, channel_id or pair_all)

    # endregion
    # region on_actor_play_action_timeline
    def _recv_on_actor_play_action_timeline(self, msg: PlayActionTimelineMessage):
        for c in self._on_actor_play_action_timeline.get(msg.timeline_id, ()): call_safe(c, msg)
        for c in self._on_actor_play_action_timeline.get(None, ()):  call_safe(c, msg)  # pair all

    def on_actor_play_action_timeline(self, *timeline_id):
        self.hook_map.set(main.sniffer.on_play_action_timeline, self._recv_on_actor_play_action_timeline)
        return self._add_set(self._on_actor_play_action_timeline, timeline_id or pair_all)

    # endregion
    # region on_map_effect
    def _recv_on_map_effect(self, msg: NetworkMessage[zone_server.MapEffect]):
        for c in self._on_map_effect: call_safe(c, msg)

    def on_map_effect(self, func):
        for _d in self._decorators.get(threading.get_ident(), []): func = _d(func)
        self.hook_map.set(main.sniffer.on_zone_server_message[ZoneServer.MapEffect], self._recv_on_map_effect)
        self._on_map_effect.append(func)
        return func

    # endregion
    def on_reset(self, func):
        for _d in self._decorators.get(threading.get_ident(), []): func = _d(func)
        self._on_reset.append(func)
        return func

    def on_hook(self, *hooks: BroadcastHook):
        def dec(func):
            for hook in hooks:
                self.hook_map.set(hook, func)
            return func

        return dec


class MapTrigger(TriggerGroup):
    triggers: 'dict[int,MapTrigger]' = {}

    def __init__(self, territory_id: int):
        assert territory_id not in MapTrigger.triggers
        MapTrigger.triggers[territory_id] = self
        self.territory_id = territory_id
        try:
            territory = main.sq_pack.sheets.territory_type_sheet[territory_id]
        except KeyError:
            label = f'unk_territory_{territory_id}'
        else:
            label = f'{territory.area.text_sgl} - {territory.content_finder_condition.text_name or "?"} [{territory_id}]'
        super().__init__(f'@territory_{territory_id}', label)

    def get_index(self):
        if main.mem.territory_info.territory_id == self.territory_id:
            return 1
        else:
            return -self.territory_id

    @classmethod
    def get(cls, territory_id: int):
        return MapTrigger.triggers.get(territory_id) or MapTrigger(territory_id)


common_trigger = TriggerGroup('#common', 'common')


def new_thread(f):
    @functools.wraps(f)
    def func(*args, **kwargs):
        return raid_helper.create_mission(f, *args, **kwargs)

    return func


def tts(msg):
    if tts_plugin := main.plugins.get("tts/TTS"):
        tts_plugin.speak(msg)
