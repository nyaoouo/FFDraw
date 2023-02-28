import functools
import typing

import imgui

from nylib.utils import BroadcastHook
from ff_draw.main import FFDraw
from .typing import *

if typing.TYPE_CHECKING:
    from .. import RaidHelper

main = FFDraw.instance
raid_helper: 'RaidHelper|None' = None


def _add_set(d, ids):
    def dec(f):
        for i in ids:
            d.setdefault(i, []).append(f)
        return f

    return dec


class TValue:
    def __init__(self, key: str, label: str, default_value=None):
        self.key = key
        self.label = label
        self.default_value = default_value

    @property
    def value(self):
        return raid_helper.data.setdefault('values', {}).get(self.key, self.default_value)

    @value.setter
    def value(self, v):
        raid_helper.data.setdefault('values', {})[self.key] = v
        raid_helper.storage.save()

    def do_render(self):
        imgui.text(self.label + ': ')
        self.render()

    def render(self):
        imgui.same_line()
        changed, value = imgui.input_text('##' + self.key, self.value, 256, imgui.COLOR_EDIT_NO_LABEL)
        if changed: self.value = value


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
    try:
        return func(*args)
    except Exception as e:
        raid_helper.logger.error('error in trigger call:', exc_info=e)


class TriggerGroup:
    def __init__(self, identifier: str, label=None):
        self.identifier = identifier
        self.label = label or identifier
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
        self._on_object_spawn = {}
        self._on_actor_delete = []
        self._on_actor_play_action_timeline = {}
        self._on_map_effect = []
        self._on_reset = []

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

    def render(self):
        if not self.values: return
        if imgui.tree_node(self.label):
            self._render_directory((), self.value_tree)
            imgui.tree_pop()

    # region on_lockon
    def _recv_on_lockon(self, msg: ActorControlMessage[actor_control.SetLockOn]):
        for c in self._on_lockon_map.get(msg.param.lockon_id, ()): call_safe(c, msg)
        for c in self._on_lockon_map.get(None, ()):  call_safe(c, msg)  # pair all

    def on_lockon(self, *icon_id):
        self.hook_map.set(main.sniffer.on_actor_control[ActorControlId.SetLockOn], self._recv_on_lockon)
        return _add_set(self._on_lockon_map, icon_id or pair_all)

    # endregion
    # region on_cast
    def _recv_on_cast(self, msg: NetworkMessage[zone_server.ActorCast]):
        if msg.message.action_kind != 1: return
        for c in self._on_cast_map.get(msg.message.action_id, ()): call_safe(c, msg)
        for c in self._on_cast_map.get(None, ()):  call_safe(c, msg)  # pair all

    def on_cast(self, *action_id):
        self.hook_map.set(main.sniffer.on_zone_server_message[ZoneServer.ActorCast], self._recv_on_cast)
        return _add_set(self._on_cast_map, action_id or pair_all)

    # endregion
    # region on_effect
    def _recv_on_effect(self, msg: NetworkMessage[zone_server.ActionEffect]):
        if msg.message.action_kind != 1: return
        for c in self._on_effect_map.get(msg.message.action_id, ()): call_safe(c, msg)
        for c in self._on_effect_map.get(None, ()):  call_safe(c, msg)  # pair all

    def on_effect(self, *action_id):
        self.hook_map.set(main.sniffer.on_action_effect, self._recv_on_effect)
        return _add_set(self._on_effect_map, action_id or pair_all)

    # endregion
    # region on_add_status
    def _recv_on_add_status(self, msg: ActorControlMessage[actor_control.AddStatus]):
        for c in self._on_add_status.get(msg.param.status_id, ()): call_safe(c, msg)
        for c in self._on_add_status.get(None, ()):  call_safe(c, msg)  # pair all

    def on_add_status(self, *status_id):
        self.hook_map.set(main.sniffer.on_actor_control[ActorControlId.AddStatus], self._recv_on_add_status)
        return _add_set(self._on_add_status, status_id or pair_all)

    # endregion
    # region on_npc_spawn
    def _recv_on_npc_spawn(self, msg: NetworkMessage[zone_server.NpcSpawn | zone_server.NpcSpawn2]):
        for c in self._on_npc_spawn.get(msg.message.create_common.npc_id, ()): call_safe(c, msg)
        for c in self._on_npc_spawn.get(None, ()):  call_safe(c, msg)  # pair all

    def on_npc_spawn(self, *base_id):
        self.hook_map.set(main.sniffer.on_zone_server_message[ZoneServer.NpcSpawn], self._recv_on_npc_spawn)
        self.hook_map.set(main.sniffer.on_zone_server_message[ZoneServer.NpcSpawn2], self._recv_on_npc_spawn)
        return _add_set(self._on_npc_spawn, base_id or pair_all)

    # endregion
    # region on_object_spawn
    def _recv_on_object_spawn(self, msg: NetworkMessage[zone_server.ObjectSpawn]):
        for c in self._on_object_spawn.get(msg.message.base_id, ()): call_safe(c, msg)
        for c in self._on_object_spawn.get(None, ()):  call_safe(c, msg)  # pair all

    def on_object_spawn(self, *base_id):
        self.hook_map.set(main.sniffer.on_zone_server_message[ZoneServer.ObjectSpawn], self._recv_on_object_spawn)
        return _add_set(self._on_object_spawn, base_id or pair_all)

    # endregion
    # region on_actor_delete
    def _recv_on_actor_delete(self, msg: NetworkMessage[zone_server.ActorDelete]):
        for c in self._on_actor_delete: call_safe(c, msg)

    def on_actor_delete(self, func):
        self.hook_map.set(main.sniffer.on_zone_server_message[ZoneServer.ActorDelete], self._recv_on_actor_delete)
        self._on_actor_delete.append(func)
        return func

    # endregion
    # region on_set_channel
    def _recv_on_set_channel(self, msg: ActorControlMessage[actor_control.SetChanneling]):
        for c in self._on_set_channel.get(msg.param.channel_id, ()): call_safe(c, msg)
        for c in self._on_set_channel.get(None, ()):  call_safe(c, msg)  # pair all

    def on_set_channel(self, *channel_id):
        self.hook_map.set(main.sniffer.on_actor_control[ActorControlId.SetChanneling], self._recv_on_set_channel)
        return _add_set(self._on_set_channel, channel_id or pair_all)

    # endregion
    # region on_cancel_channel
    def _recv_on_cancel_channel(self, msg: ActorControlMessage[actor_control.RemoveChanneling]):
        for c in self._on_cancel_channel.get(msg.param.channel_id, ()): call_safe(c, msg)
        for c in self._on_cancel_channel.get(None, ()):  call_safe(c, msg)  # pair all

    def on_cancel_channel(self, *channel_id):
        self.hook_map.set(main.sniffer.on_actor_control[ActorControlId.RemoveChanneling], self._recv_on_cancel_channel)
        return _add_set(self._on_cancel_channel, channel_id or pair_all)

    # endregion
    # region on_actor_play_action_timeline
    def _recv_on_actor_play_action_timeline(self, msg: PlayActionTimelineMessage):
        for c in self._on_actor_play_action_timeline.get(msg.timeline_id, ()): call_safe(c, msg)
        for c in self._on_actor_play_action_timeline.get(None, ()):  call_safe(c, msg)  # pair all

    def on_actor_play_action_timeline(self, *timeline_id):
        self.hook_map.set(main.sniffer.on_play_action_timeline, self._recv_on_actor_play_action_timeline)
        return _add_set(self._on_actor_play_action_timeline, timeline_id or pair_all)

    # endregion
    # region on_map_effect
    def _recv_on_map_effect(self, msg: NetworkMessage[zone_server.MapEffect]):
        for c in self._on_map_effect: call_safe(c, msg)

    def on_map_effect(self, func):
        self.hook_map.set(main.sniffer.on_zone_server_message[ZoneServer.MapEffect], self._recv_on_map_effect)
        self._on_map_effect.append(func)
        return func

    # endregion
    def on_reset(self, func):
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
            label = str(territory.area.text_sgl)
        super().__init__(f'@territory_{territory_id}', label)

    @classmethod
    def get(cls, territory_id: int):
        return MapTrigger.triggers.get(territory_id) or MapTrigger(territory_id)


common_trigger = TriggerGroup('#common', 'common')


def new_thread(f):
    @functools.wraps(f)
    def func(*args, **kwargs):
        return raid_helper.create_mission(f, *args, **kwargs)

    return func
