import glm
import imgui

from ff_draw.func_parser import action_type_to_shape_default
from ff_draw.plugins import FFDrawPlugin
from ff_draw.omen import BaseOmen
from ff_draw.mem.actor import Actor
from ff_draw.sniffer.enums import ZoneServer, ActorControlId
from ff_draw.sniffer.utils.message import NetworkMessage
from ff_draw.sniffer.message_structs.zone_server import ActorCast
from nylib.utils import serialize_data
from nylib.utils.win32 import memory as ny_mem
from .data import special_actions


class SimpleCast(FFDrawPlugin):
    actor_omens: dict[int, BaseOmen]

    def __init__(self, main):
        super().__init__(main)
        self.main.sniffer.on_zone_server_message[ZoneServer.ActorCast].append(self.on_cast)
        self.show_friend = self.data.setdefault('show_friend', True)
        self.show_imgui_window = True

        # TODO: 等统一接口
        self.main.sniffer.on_zone_server_message[ZoneServer.Effect].append(lambda m: self.remove_actor_omen(m.header.source_id))
        self.main.sniffer.on_zone_server_message[ZoneServer.AoeEffect8].append(lambda m: self.remove_actor_omen(m.header.source_id))
        self.main.sniffer.on_zone_server_message[ZoneServer.AoeEffect16].append(lambda m: self.remove_actor_omen(m.header.source_id))
        self.main.sniffer.on_zone_server_message[ZoneServer.AoeEffect24].append(lambda m: self.remove_actor_omen(m.header.source_id))
        self.main.sniffer.on_zone_server_message[ZoneServer.AoeEffect32].append(lambda m: self.remove_actor_omen(m.header.source_id))

        self.main.sniffer.on_actor_control[ActorControlId.CancelCast].append(lambda m: self.remove_actor_omen(m.source_id))

        self.actor_omens = {}
        self.bnpc_battalion_offset = self.main.mem.scanner.find_val('44 ? ? ? * * * * 4c 89 68 ? 4c 89 70')[0]
        self.logger.debug(f'bnpc b offset {self.bnpc_battalion_offset:x}')

    def remove_actor_omen(self, actor_id):
        if omen := self.actor_omens.pop(actor_id, None):
            omen.destroy()

    def get_battalion_key(self, actor: Actor, mode: int):
        # e8 * * * * 33 ? 48 ? ? 8b ? e8 ? ? ? ? 8b
        if mode == 1 and actor.actor_type == 1: return 0
        return ny_mem.read_ubyte(actor.handle, actor.address + self.bnpc_battalion_offset)

    def is_enemy(self, a1: Actor | None, a2: Actor | None):
        # e8 * * * * 84 ? 0f 85 ? ? ? ? 85 ? 74
        if not (a1 and a2): return True
        if a1.actor_type > 2 or a2.actor_type > 2: return False
        battalion_mode = self.main.sq_pack.sheets.territory_type_sheet[self.main.mem.territory_type].battalion_mode
        if battalion_mode == 0: return False
        return self.main.sq_pack.sheets.battalion_sheet[self.get_battalion_key(a1, battalion_mode)][self.get_battalion_key(a2, battalion_mode)]

    def on_cast(self, msg: NetworkMessage[ActorCast]):
        data = msg.message
        if data.action_kind != 1: return
        source_id = msg.header.source_id
        source = self.main.mem.actor_table.get_actor_by_id(source_id)
        self.remove_actor_omen(source_id)
        action_id = data.action_id
        action = self.main.sq_pack.sheets.action_sheet[action_id]
        effect_type = action.effect_type
        target = self.main.mem.actor_table.get_actor_by_id(data.target_id)
        effect_width = action.effect_width
        effect_range = action.effect_range
        if self.is_enemy(self.main.mem.actor_table.me, source):
            color = 'enemy'
        elif self.show_friend:
            color = 'friend'
        else:
            return
        if effect_type == 8:  # rect to target
            if not (source and target): return
            self.actor_omens[source_id] = BaseOmen(
                main=self.main,
                pos=lambda _: source.pos,
                shape=0x20000,
                scale=lambda _: glm.vec3(effect_width, 1, glm.distance(source.pos, target.pos)),
                facing=lambda _: glm.polar(target.pos - source.pos).y,
                surface_line_color=color,
                duration=data.cast_time + .5,
            )
        shape = special_actions[action_id] if action_id in special_actions else action_type_to_shape_default.get(effect_type)
        if not shape: return
        scale = glm.vec3(effect_width if shape == 0x20000 else effect_range, 1, effect_range)
        is_circle = shape >> 16 == 1
        pos = (lambda _: target.pos) if is_circle and target else (lambda _: source.pos)
        facing = 0 if is_circle else (lambda _: glm.polar(target.pos - source.pos).y)
        self.actor_omens[source_id] = BaseOmen(
            main=self.main,
            pos=pos,
            shape=shape,
            scale=scale,
            facing=facing,
            surface_line_color=color,
            duration=data.cast_time + .3,
        )

    def update(self, main):
        if self.show_imgui_window:
            expanded, self.show_imgui_window = imgui.begin('simple_cast', self.show_imgui_window)
            if expanded:
                clicked, self.show_friend = imgui.checkbox("show_friend", self.show_friend)
                if clicked:
                    self.data['show_friend'] = self.show_friend
                    self.storage.save()
            # if (me := main.mem.actor_table.me) and (tg := main.mem.actor_table.get_actor_by_id(me.target_id)):
            #     battalion_mode = self.main.sq_pack.sheets.territory_type_sheet[self.main.mem.territory_type].battalion_mode
            #     me_key = self.get_battalion_key(me, battalion_mode)
            #     tg_key = self.get_battalion_key(tg, battalion_mode)
            #     imgui.text(f'[{battalion_mode}]{me.name}({me_key}) => {tg.name}({tg_key}) {self.is_enemy(me, tg)}')
            imgui.end()
