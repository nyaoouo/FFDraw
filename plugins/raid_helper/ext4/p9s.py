import logging
import math
import time

import glm

from ff_draw.omen.effector import Effector, ScaleInEffector, FadeOutEffector

from raid_helper import utils as raid_utils
from raid_helper.utils.typing import *
from raid_helper.data import special_actions, delay_until

special_actions[33337] = 0
special_actions[33336] = 0
special_actions[33314] = 0
special_actions[33315] = 0
special_actions[33292] = 0
special_actions[33139] = 0
special_actions[33145] = 0

delay_until[33121] = 4

p9s = raid_utils.MapTrigger.get(1148)

center = glm.vec3(100, 0, 100)

logger = logging.getLogger('raid_helper/p9s')

is_enable = p9s.add_value(raid_utils.BoolCheckBox('default/enable', True))
p9s.decorators.append(lambda f: (lambda *args, **kwargs: f(*args, **kwargs) if is_enable.value else None))


class HideWhenActorDead(Effector):
    def __init__(self, omen, actor_id):
        super().__init__(omen)
        self.actor = raid_utils.NActor.by_id(actor_id)
        self.is_display = True

    def update(self):
        try:
            new_is_display = self.actor.update().current_hp > 0
        except KeyError:
            new_is_display = False
        if new_is_display != self.is_display:
            self.omen.apply_effect(ScaleInEffector if new_is_display else FadeOutEffector)
            self.is_display = new_is_display
        return True

    def display(self):
        return self.is_display


class ScaleTo(Effector):
    def __init__(self, omen, new_scale: glm.vec3, dur=.5):
        super().__init__(omen)
        self.new_scale = new_scale
        self.d_scale = (new_scale - omen.scale) / dur
        self.dur = dur
        self.delta = 0

    def update(self):
        self.delta = time.time() - self.start_at
        if self.delta >= self.dur:
            self.omen._scale = self.new_scale
            return False
        return True

    def scale(self, s: glm.vec3):
        return s + self.d_scale * self.delta


class DualSpell:
    fire_omens: list[raid_utils.OmenGroup] = None
    lightning_omens: list[BaseOmen] = None
    ice_omen: BaseOmen = None
    dur = 12.8

    def __init__(self):
        p9s.on_effect(33058)(self.on_fire_sp)
        p9s.on_effect(33059)(self.on_ice_sp)
        p9s.on_effect(33116)(self.on_lightning_sp)
        p9s.on_cast(33108, 33156)(self.on_cast_fire_ice)
        p9s.on_cast(33109, 33157)(self.on_cast_ice_lightning)

    def on_cast_fire_ice(self, evt: 'raid_utils.NetworkMessage[zone_server.ActorCast]'):
        self.dur = 12.8 if evt.message.action_id == 33108 else 8.15
        self.make_fires(), self.make_ice()

    def on_cast_ice_lightning(self, evt: 'raid_utils.NetworkMessage[zone_server.ActorCast]'):
        self.dur = 12.8 if evt.message.action_id == 33109 else 8.15
        self.make_ice(), self.make_lightnings()

    def on_fire_sp(self, _):
        if not self.fire_omens: return
        for omen in self.fire_omens:
            omen[0].apply_effect(ScaleTo, glm.vec3(12, 1, 12))

    def on_ice_sp(self, _):
        if not self.ice_omen: return
        self.ice_omen.apply_effect(ScaleTo, glm.vec3(40, 1, 40))

    def on_lightning_sp(self, _):
        if not self.lightning_omens: return
        for omen in self.lightning_omens:
            omen.apply_effect(ScaleTo, glm.vec3(16, 1, 40))

    def make_fire(self, actor_id):
        actor = raid_utils.NActor.by_id(actor_id)
        color = glm.vec4(1, .3, .3, .3) if raid_utils.is_class_job_dps(actor.class_job) else glm.vec4(.3, .3, 1, .3)
        line_color = color + glm.vec4(0, 0, 0, .5)
        res = raid_utils.OmenGroup(
            raid_utils.draw_circle(radius=6, pos=actor, surface_color=color, line_color=line_color, duration=self.dur)
        ) + raid_utils.draw_share(radius=6, pos=actor, surface_color=color, line_color=line_color, duration=self.dur)
        for omen in res:
            omen.apply_effect(HideWhenActorDead, actor_id)
        return res

    def make_fires(self):
        self.fire_omens = [self.make_fire(a.id) for a in raid_utils.iter_main_party(False)]

    def make_lightning(self, actor_id):
        actor = raid_utils.NActor.by_id(actor_id)
        return raid_utils.draw_rect(
            width=8, length=40,
            pos=glm.vec3(100, 0, 100),
            facing=lambda _: glm.polar(actor.update().pos - glm.vec3(100, 0, 100)).y,
            duration=self.dur,
        )

    def make_lightnings(self):
        self.lightning_omens = [self.make_lightning(a.id) for a in raid_utils.iter_main_party(False)]

    def make_ice(self):
        self.ice_omen = raid_utils.draw_circle(
            radius=70,
            pos=glm.vec3(100, 0, 100),
            inner_radius=14,
            duration=self.dur
        )


class Combination:
    # 内置omen1有偏差，因此也画
    # cast: 31:10.303
    # 1: 31:17.27 7s
    # 2: 31:20.37 3s
    # 3: 31:23.304 3s
    circle = 0  # 33336
    donut = 1  # 33337
    front = 2  # 33314
    back = 3  # 33315

    data = {
        33127: (circle, front, donut),
        33128: (donut, front, circle),
        33129: (circle, back, donut),
        33130: (donut, back, circle),
    }

    def __init__(self):
        p9s.on_cast(*self.data.keys())(self.on_cast)

    def draw(self, actor: raid_utils.NActor, draw_type, dur):
        actor_pos = actor.pos
        if draw_type == self.circle:
            return raid_utils.draw_circle(
                radius=12,
                pos=actor_pos,
                duration=dur,
            )
        elif draw_type == self.donut:
            return raid_utils.draw_circle(
                radius=20,
                pos=actor_pos,
                inner_radius=8,
                duration=dur,
            )
        elif draw_type == self.front:
            return raid_utils.draw_fan(
                degree=180,
                radius=40,
                pos=actor_pos,
                facing=actor.facing,
                duration=dur,
            )
        elif draw_type == self.back:
            return raid_utils.draw_fan(
                degree=180,
                radius=40,
                pos=actor_pos,
                facing=actor.facing + math.pi,
                duration=dur,
            )

    def on_cast(self, msg: NetworkMessage[zone_server.ActorCast]):
        actor_id = msg.header.source_id
        cast_id = msg.message.action_id
        if cast_id not in self.data: return
        actor = raid_utils.NActor.by_id(actor_id)
        a1, a2, a3 = self.data[cast_id]
        self.draw(actor, a1, 7)
        time.sleep(6)
        self.draw(actor, a2, 4)
        time.sleep(3)
        self.draw(actor, a3, 4)


@p9s.on_cast(33119)
def on_cast_archaic_rockbreaker(_):
    def _draw(actor_id):
        actor = raid_utils.NActor.by_id(actor_id)
        color = glm.vec4(1, .3, .3, .3) if raid_utils.is_class_job_dps(actor.class_job) else glm.vec4(.3, .3, 1, .3)
        line_color = color + glm.vec4(0, 0, 0, .5)
        res = raid_utils.OmenGroup(
            raid_utils.draw_circle(radius=6, pos=actor, surface_color=color, line_color=line_color, duration=7.8)
        ) + raid_utils.draw_share(radius=6, pos=actor, surface_color=color, line_color=line_color, duration=7.8)
        for omen in res:
            omen.apply_effect(HideWhenActorDead, actor_id)
        return res

    for a in raid_utils.iter_main_party(False):
        _draw(a.id)


class Levinstrike:
    # 18.60 cast start
    # 24.69 icon dice # 0x4f-0x56
    # 30.70 icon ice 1 # 0x14a
    # 36.43 icon ice 2 # 0x14a
    # 37.35 effect ball 1 # 33151
    # 39.64 effect fire 1 + ice 1 + tower 1 # 33152 + 33155 + 33153
    # 42.12 icon ice 3 # 0x14a
    # 43.02 effect ball 2 # 33151
    # 45.34 effect fire 2 + ice 2 + tower 2 # 33152 + 33168 + 33153
    # 47.82 icon ice 4 # 0x14a
    # 48.70 effect ball 3 # 33151
    # 51.02 effect fire 3 + ice 3 + tower 3 # 33152 + 33169 + 33153
    # 54.45 effect ball 4 # 33151
    # 56.74 effect fire 4 + ice 4 + tower 4 # 33152 + 33170 + 33153

    ball: list[glm.vec3 | None]
    fire: list[int | None]
    ice: list[int]

    def __init__(self):
        self.enable = False
        p9s.on_cast(33148)(self.on_start_cast)
        p9s.on_lockon(0x50, 0x52, 0x54, 0x56)(self.on_lockon_fire)
        p9s.on_lockon(0x4f, 0x51, 0x53, 0x55)(self.on_lockon_ball)
        p9s.on_lockon(0x14a)(self.on_lockon_ice)
        p9s.on_effect(33155, 33168, 33169)(self.on_icemeld)

        self.fire_counter = 0

    def on_start_cast(self, _):
        chimeric_succession.enable = False
        self.enable = True
        self.ball = [None for _ in range(4)]
        self.fire = [None for _ in range(4)]
        self.ice = []

    def on_lockon_fire(self, evt: 'raid_utils.ActorControlMessage[actor_control.SetLockOn]'):
        if not self.enable: return
        idx = (evt.param.lockon_id - 0x50) // 2
        logger.debug(f'fire[{idx}] = {evt.source_id:x}')
        self.fire[idx] = evt.source_id

    def on_lockon_ball(self, evt: 'raid_utils.ActorControlMessage[actor_control.SetLockOn]'):
        if not self.enable: return
        idx = (evt.param.lockon_id - 0x4f) // 2
        pos = raid_utils.main.mem.actor_table.get_actor_by_id(evt.source_id).pos
        logger.debug(f'ball[{idx}] = {pos}')
        self.ball[idx] = pos

    def on_lockon_ice(self, evt: 'raid_utils.ActorControlMessage[actor_control.SetLockOn]'):
        if not self.enable: return
        logger.debug(f'ice[{len(self.ice)}] = {evt.source_id:x}')
        self.ice.append(evt.source_id)
        if len(self.ice) == 1:
            self.draw_ball(0, 6.65)
            self.draw_ice(0, 9)
            self.draw_fire(0, 9)

    def on_icemeld(self, evt: 'raid_utils.NetworkMessage[zone_server.ActionEffect]'):
        if not self.enable: return
        i = [33155, 33168, 33169].index(evt.message.action_id) + 1
        self.draw_ball(i, 3.36)
        self.draw_ice(i, 5.7)
        self.draw_fire(i, 5.7)

    def draw_ball(self, idx, dur):
        source_pos = self.ball[idx]
        if source_pos is None:
            return logger.warning(f"ball[{idx}] is None: {source_pos=}")
        target_pos = center + glm.normalize(center - source_pos) * 16
        return raid_utils.draw_circle(radius=6, pos=target_pos, duration=dur)

    def draw_fire(self, idx, dur):
        source_pos = self.ball[idx]
        target_id = self.fire[idx]
        if source_pos is None or target_id is None:
            return logger.warning(f"fire[{idx}] is None or ball[{idx}] is None: {source_pos=} {target_id=}")
        target = raid_utils.NActor.by_id(target_id)
        if not target:
            return logger.warning(f"fire[{idx}] actor not_found: {target_id=:x}")
        source_pos = center + glm.normalize(source_pos - center) * 14
        return raid_utils.draw_distance_line(
            source_pos, target, min_distance=20, duration=dur
        ), raid_utils.draw_circle(
            radius=6, pos=target, duration=dur
        )

    def draw_ice(self, idx, dur):
        if idx >= len(self.ice): return
        return raid_utils.draw_circle(radius=20, pos=raid_utils.NActor.by_id(self.ice[idx]), duration=dur)


@p9s.on_cast(33133)
def on_cast_archaic_demolis(evt: 'raid_utils.NetworkMessage[zone_server.ActorCast]'):
    for actor in raid_utils.iter_main_party(False):
        if raid_utils.is_class_job_healer(actor.class_job):
            raid_utils.draw_share(
                radius=6,
                pos=actor,
                duration=evt.message.cast_time
            )


@p9s.on_cast(33145)
def on_cast_thunderbolt(evt: 'raid_utils.NetworkMessage[zone_server.ActorCast]'):
    source_actor = raid_utils.NActor.by_id(evt.header.source_id)

    def _draw(_i):
        raid_utils.draw_fan(
            degree=60, radius=40,
            pos=source_actor,
            facing=lambda _: glm.polar(raid_utils.get_actor_by_dis(source_actor, _i).pos - source_actor.update().pos).y,
            duration=evt.message.cast_time,
        )

    for i in range(4): _draw(i)

    share_cast = evt.message.cast_time + 2
    raid_utils.draw_circle(
        radius=6,
        pos=lambda _: raid_utils.get_actor_by_dis(source_actor, -1).pos,
        duration=share_cast,
    )
    raid_utils.sleep(share_cast - 5)
    raid_utils.draw_share(
        radius=6,
        pos=lambda _: raid_utils.get_actor_by_dis(source_actor, -1).pos,
        duration=min(share_cast, 5),
    )


class ChimericSuccession:
    # 00.631   icon dice # 0x4f - 0x52
    # 07.397   cast rear/front combo # 34703/34702
    # 10.698 effect ice 1 # 33155
    # 13.697 effect ice 2 # 33168
    # 15.814 effect ice 3 # 33169
    # 16.664 effect combo[0] fire share # 34707/34708
    # 17.931   cast combo[1] swing kick # 34709/34710 # has omen
    # 19.714 effect ice 4 # 33170
    # 20.881 effect combo[1] swing kick # 34709/34710
    ice: list[int | None]

    def __init__(self):
        self.enable = False
        p9s.on_cast(33211)(self.on_start_cast)
        p9s.on_lockon(0x4f, 0x50, 0x51, 0x52)(self.on_lockon_ice)
        p9s.on_effect(33155, 33168, 33169)(self.on_icemeld)

    def on_start_cast(self, _):
        self.enable = True
        levinstrike.enable = False
        self.ice = [None for _ in range(4)]

    def on_lockon_ice(self, evt: 'raid_utils.ActorControlMessage[actor_control.SetLockOn]'):
        if not self.enable: return
        self.ice[i := evt.param.lockon_id - 0x4f] = evt.source_id
        if i == 0: self.draw_ice(0, 10)

    def on_icemeld(self, evt: 'raid_utils.NetworkMessage[zone_server.ActionEffect]'):
        if not self.enable: return
        self.draw_ice([33155, 33168, 33169].index(evt.message.action_id) + 1, 3)

    def draw_ice(self, idx, dur):
        target_id = self.ice[idx]
        if not target_id:
            return logger.warning(f"ice[{idx}] is None: {target_id=:x}")
        return raid_utils.draw_circle(
            radius=20,
            pos=raid_utils.NActor.by_id(target_id),
            duration=dur,
        )


dual_spell = DualSpell()
combination = Combination()
levinstrike = Levinstrike()
chimeric_succession = ChimericSuccession()
p9s.clear_decorators()
