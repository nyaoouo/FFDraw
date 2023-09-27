import functools
import time
import typing

import glm
import itertools

import imgui

from ff_draw.plugins import FFDrawPlugin
from ff_draw.sniffer.message_structs.zone_server import ActorCast
from nylib.utils.win32 import memory as ny_mem
from .data import special_actions, delay_until, omen_color
from . import utils as raid_utils
from .utils import party_role


@functools.cache
def get_shape_default_by_action_type(t):
    return {
        2: raid_utils.circle_shape(),  # circle
        3: raid_utils.fan_shape(90),  # fan
        4: raid_utils.rect_shape(),  # rect
        5: raid_utils.circle_shape(),  # circle
        6: raid_utils.circle_shape(),  # circle
        7: raid_utils.circle_shape(),  # circle
        # 8: 0x20000,  # rect to target
        10: raid_utils.donut_shape(1, 2),  # donut
        11: raid_utils.rect_shape(2),  # cross
        12: raid_utils.rect_shape(),  # rect
        13: raid_utils.fan_shape(90),  # fan
    }.get(t, 0)


def set_raid_helper_instance(raid_helper: 'RaidHelper'):
    from . import utils
    from .utils import trigger, logic, drawings
    utils.raid_helper = trigger.raid_helper = logic.raid_helper = drawings.raid_helper = RaidHelper.instance = raid_helper
    for t_val_cb in trigger.TValue._cache_need_init:
        t_val_cb()


def load_triggers():
    import pkgutil, os, importlib

    for i, mod in enumerate(pkgutil.iter_modules([os.path.dirname(__file__)])):
        if not mod.ispkg: continue
        if mod.name != 'utils':
            ext_name = f'{__name__}.{mod.name}'
            for mod_ in pkgutil.iter_modules([os.path.dirname(importlib.import_module(ext_name).__file__)]):
                importlib.import_module(f'{ext_name}.{mod_.name}')


class HookCall:
    def __init__(self):
        self.common = []
        self.by_map = {}

    def play(self, msg):
        for c in self.common: c(msg)
        for c in self.by_map.get(raid_utils.FFDraw.instance.mem.territory_info.territory_id, ()): c(msg)


def delay_until_dec(action_id, shape):
    if (delay_until_ := delay_until.get(action_id)) and delay_until_ > 0:
        return lambda o: 0 if o.remaining_time > delay_until_ else shape
    return shape


class HookMap2:
    call_map: dict[int, HookCall]
    hook_map: dict[int, raid_utils.BroadcastHook]

    def __init__(self):
        self.call_map = {}
        self.hook_map = {}

    def get_call(self, hook: raid_utils.BroadcastHook):
        self.hook_map[hid := id(hook)] = hook
        if hid not in self.call_map:
            self.call_map[hid] = res = HookCall()
            return res
        return self.call_map[hid]

    def iter(self):
        for i, h in self.hook_map.items():
            yield h, self.call_map[i]


class RaidHelper(FFDrawPlugin):
    actor_omens: dict[int, raid_utils.BaseOmen]
    instance: 'RaidHelper' = None

    def __init__(self, main):
        super().__init__(main)
        set_raid_helper_instance(self)
        self.hook_map = HookMap2()
        self._init_hook_map()
        for h, c in self.hook_map.iter():
            # self.logger.debug(f"{h, c.by_map, c.common}")
            h.append(c.play)

        # simple cast
        self.cmn_cfg = self.data.setdefault('cmn_cfg', {})
        self.game_style = self.cmn_cfg.setdefault('game_style', False)

        self.simple_cast_cfg = self.data.setdefault('simple_cast', {})
        self.enable_simple_cast = self.simple_cast_cfg.setdefault('enable_simple_cast', True)
        self.show_friend = self.simple_cast_cfg.setdefault('show_friend', True)
        self.print_history = self.simple_cast_cfg.setdefault('print_history', False)

        self.main.sniffer.on_zone_server_message[raid_utils.ZoneServer.ActorCast].append(self.on_simple_cast)
        self.on_action_effect = lambda m: self.remove_actor_omen(m.header.source_id)
        self.main.sniffer.on_action_effect.append(self.on_action_effect)
        self.on_cancel_cast = lambda m: self.remove_actor_omen(m.source_id)
        self.main.sniffer.on_actor_control[raid_utils.ActorControlId.CancelCast].append(self.on_cancel_cast)

        # party_role
        self.party_role = party_role.PartyRole()
        self.main.sniffer.on_zone_server_message[raid_utils.ZoneServer.PartyUpdate].append(self.on_party_update)
        self.party_reload()

        self.actor_omens = {}
        self.bnpc_battalion_offset, = self.main.mem.scanner_v2.find_val('44 ? ? ? <? ? ? ?> 4c 89 68 ? 4c 89 70 ? 4c 89 78 ? 0f 29 70')
        self.logger.debug(f'bnpc b offset {self.bnpc_battalion_offset:x}')

        self.waypoints = raid_utils.WaypointList()

        self._panel_filter_string = ''

    def _init_hook_map(self):
        load_triggers()
        for hook, calls in raid_utils.common_trigger.hook_map.iter():
            self.hook_map.get_call(hook).common = calls
        for tid, mt in raid_utils.MapTrigger.triggers.items():
            for hook, calls in mt.hook_map.iter():
                self.hook_map.get_call(hook).by_map[tid] = calls

    def on_unload(self):
        for h, c in self.hook_map.iter(): h.remove(c.play)

        # simple cast
        self.main.sniffer.on_zone_server_message[raid_utils.ZoneServer.ActorCast].remove(self.on_simple_cast)
        self.main.sniffer.on_action_effect.remove(self.on_action_effect)
        self.main.sniffer.on_actor_control[raid_utils.ActorControlId.CancelCast].remove(self.on_cancel_cast)

        # party_role
        self.main.sniffer.on_zone_server_message[raid_utils.ZoneServer.PartyUpdate].remove(self.on_party_update)

    def on_party_update(self, evt: raid_utils.NetworkMessage[raid_utils.zone_server.PartyUpdate]):
        self.party_role.update([
            (m.name, m.home_world_id, m.actor_id, m.class_job,)
            for m in (evt.message.member[i] for i in range(evt.message.party_count))
        ], False)

    def party_reload(self, reload=False):
        if raid_utils.get_me():
            self.party_role.update([
                (m.name, m.home_world, m.id, m.class_job,)
                for m in raid_utils.iter_main_party(False)
            ], reload)

    # def test_waypoint_list(self):
    #     marking = self.main.mem.marking
    #     res = []
    #     for i in range(8):
    #         mark = marking.way_mark(i)
    #         if mark.is_enable:
    #             res.append(mark.pos)
    #     self.waypoints.set_waypoint(*res)

    def update(self, _):
        self.waypoints.update()
        self.waypoints.render_game()

    def draw_panel(self):
        imgui.text(f'has tts: {"tts/TTS" in self.main.plugins}')
        imgui.text(f'{self.waypoints}')
        # if imgui.button('test waypoint list'):
        #     self.test_waypoint_list()
        if imgui.tree_node('config'):
            clicked, self.game_style = imgui.checkbox("game_style", self.game_style)
            if clicked:
                self.cmn_cfg['game_style'] = self.game_style
                self.storage.save()
            imgui.tree_pop()
        if imgui.tree_node('simple cast'):
            clicked, self.enable_simple_cast = imgui.checkbox("enable_simple_cast", self.enable_simple_cast)
            if clicked:
                self.simple_cast_cfg['enable_simple_cast'] = self.enable_simple_cast
                self.storage.save()
            clicked, self.show_friend = imgui.checkbox("show_friend", self.show_friend)
            if clicked:
                self.simple_cast_cfg['show_friend'] = self.show_friend
                self.storage.save()
            clicked, self.print_history = imgui.checkbox("print_history", self.print_history)
            if clicked:
                self.simple_cast_cfg['print_history'] = self.print_history
                self.storage.save()
            imgui.tree_pop()
        if imgui.tree_node('party role'):
            role_datas = self.party_role.data
            for role in party_role.Role:
                if not (_d := role_datas[role.value]):
                    imgui.push_style_color(imgui.COLOR_BUTTON_HOVERED, *imgui.get_style_color_vec_4(imgui.COLOR_BUTTON))
                    imgui.push_style_color(imgui.COLOR_BUTTON_ACTIVE, *imgui.get_style_color_vec_4(imgui.COLOR_BUTTON))
                    imgui.button(f"{role.name}: None")
                    imgui.pop_style_color(2)
                    continue
                if imgui.button(f"{role.name}: {_d['name']}"):
                    imgui.open_popup(f"##select_role_{role.value}")
                if imgui.begin_popup(f"##select_role_{role.value}"):
                    imgui.push_id(f'select_role_{role.value}')
                    for _role in party_role.Role:
                        if role == _role: continue
                        if imgui.selectable(f'Set as {_role.name}')[1]:
                            role_datas[_role.value], role_datas[role.value] = role_datas[role.value], role_datas[_role.value]
                            self.party_role.update_role_map()
                    imgui.pop_id()
                    imgui.end_popup()
            imgui.tree_pop()
        if self._panel_filter_string:
            if imgui.button(' x '):
                self._panel_filter_string = ''
            imgui.same_line()
        _, self._panel_filter_string = imgui.input_text('filter', self._panel_filter_string, 256)

        for idx, tg in sorted(((tg.get_index(), tg) for tg in itertools.chain(raid_utils.MapTrigger.triggers.values(), [raid_utils.common_trigger]) if self._panel_filter_string in tg.label), reverse=True):
            if idx > 0:
                highlight = (.3, 1, .3, 1)
            else:
                highlight = None
            tg.render(highlight)

    def current_triggers(self) -> typing.Iterable[raid_utils.TriggerGroup]:
        yield raid_utils.common_trigger
        if t := raid_utils.MapTrigger.triggers.get(self.main.mem.territory_info.territory_id):
            yield t

    def remove_actor_omen(self, actor_id):
        if omen := self.actor_omens.pop(actor_id, None):
            omen.timeout()

    def get_battalion_key(self, actor: raid_utils.Actor, mode: int):
        # e8 * * * * 33 ? 48 ? ? 8b ? e8 ? ? ? ? 8b
        if mode == 1 and actor.actor_type == 1: return 0
        return ny_mem.read_ubyte(actor.handle, actor.address + self.bnpc_battalion_offset)

    def is_enemy(self, a1: raid_utils.Actor | None, a2: raid_utils.Actor | None):
        # e8 * * * * 84 ? 0f 85 ? ? ? ? 85 ? 74
        if not (a1 and a2): return True
        if a1.actor_type > 2 or a2.actor_type > 2: return False
        try:
            battalion_mode = self.main.sq_pack.sheets.territory_type_sheet[self.main.mem.territory_info.territory_id].battalion_mode
        except KeyError:
            return False
        if battalion_mode == 0: return False
        return self.main.sq_pack.sheets.battalion_sheet[self.get_battalion_key(a1, battalion_mode)][self.get_battalion_key(a2, battalion_mode)]

    def on_simple_cast(self, msg: raid_utils.NetworkMessage[ActorCast]):
        if not self.enable_simple_cast: return
        data = msg.message
        if data.action_kind != 1: return
        source_id = msg.header.source_id
        source = self.main.mem.actor_table.get_actor_by_id(source_id)
        self.remove_actor_omen(source_id)
        action_id = data.action_id
        action = self.main.sq_pack.sheets.action_sheet[action_id]
        effect_type = action.effect_type
        target = self.main.mem.actor_table.get_actor_by_id(data.target_id) if data.target_id != source_id else None
        effect_width = action.effect_width
        effect_range = action.effect_range
        if 3 <= action.effect_type <= 5: effect_range += source.radius  # deal fan = 3, laser = 4 , around = 5 with source radius extra
        color = surface_color = line_color = None
        if _color := omen_color.get(action_id):
            _line_color = None
            if isinstance(_color, tuple):
                surface_color, *_line_color = _color
            else:
                surface_color = _color
            line_color = _line_color[0] if _line_color else surface_color + glm.vec4(0, 0, 0, .5)
        elif self.is_enemy(self.main.mem.actor_table.me, source):
            color = raid_utils.default_color(True)
        elif self.show_friend:
            color = raid_utils.default_color(False)
        else:
            return
        if data.display_delay:
            delay = data.display_delay / 10
            alpha = lambda o: 1 if time.time() - o.start_at > delay else .7
        else:
            alpha = 1
        if effect_type == 8:  # rect to target
            if not (source and target): return
            if self.print_history:
                self.logger.debug(f'#simple_cast {source.name} cast laser {action.text}#{action_id} to with width {effect_width}')
            self.actor_omens[source_id] = raid_utils.BaseOmen(
                main=self.main,
                pos=lambda _: source.pos,
                shape=delay_until_dec(action_id, raid_utils.rect_shape()),
                scale=lambda _: glm.vec3(effect_width, 1, glm.distance(source.pos, target.pos)),
                facing=lambda _: glm.polar(target.pos - source.pos).y,
                surface_color=surface_color,
                line_color=line_color,
                surface_line_color=color,
                duration=data.cast_time + .5,
                alpha=alpha,
            )
        shape = special_actions[action_id] if action_id in special_actions else get_shape_default_by_action_type(effect_type)
        if not shape:
            # self.logger.debug(f'#simple_cast {source.name} cast {action.text}#{action_id} with unknown shape {effect_type} got {shape}')
            return
        scale = glm.vec3(effect_width if raid_utils.is_shape_rect(shape) else effect_range, 1, effect_range)
        is_circle = raid_utils.is_shape_circle(shape)
        pos = (lambda _: target.pos) if is_circle and target else data.pos
        facing = 0 if is_circle else (lambda _: glm.polar(target.pos - source.pos).y) if target else data.facing
        maybe_callable = lambda v: v(None) if callable(v) else v
        if self.print_history:
            shape_ = maybe_callable(shape)
            self.logger.debug(
                f'#simple_cast {source.name} cast {action.text}#{action_id} '
                f'shape:{hex(shape_) if isinstance(shape_, int) else shape_} time:{data.cast_time:.2f} '
                f'pos:{maybe_callable(pos)} facing:{maybe_callable(facing)} scale:{scale} '
                f'color:{color} line_color:{line_color} surface_color:{surface_color}'
            )
        self.actor_omens[source_id] = raid_utils.BaseOmen(
            main=self.main,
            pos=pos,
            shape=delay_until_dec(action_id, shape),
            scale=scale,
            facing=facing,
            surface_line_color=color,
            surface_color=surface_color,
            line_color=line_color,
            duration=data.cast_time + .3,
            alpha=alpha,
        )
