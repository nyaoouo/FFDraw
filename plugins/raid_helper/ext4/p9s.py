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
special_actions[34709] = raid_utils.fan_shape(180)
special_actions[34710] = raid_utils.fan_shape(180)

delay_until[33121] = 4

p9s = raid_utils.MapTrigger.get(1148)

center = glm.vec3(100, 0, 100)

logger = logging.getLogger('raid_helper/p9s')

is_enable = p9s.add_value(raid_utils.BoolCheckBox('default/enable', True))
enable_waypoints = p9s.add_value(raid_utils.BoolCheckBox('default/waypoints/1.enable', False))
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


pi = math.pi
pi2 = pi * 2
pi_2 = pi / 2
pi_4 = pi / 4
# mt, st, h1, h2, d1, d2, d3, d4
pos_rad_2 = [-pi_2, pi_2, -pi_2, pi_2, -pi_2, pi_2, -pi_2, pi_2, ]
pos_rad_4 = [pi, 0, -pi_2, pi_2, -pi_2, 0, pi, pi_2, ]  # type[+], for type[x] , add pi/4
pos_rad_8 = [pi, 0, -pi_2, pi_2, -pi_2 + pi_4, 0 + pi_4, pi + pi_4, pi_2 + pi_4, ]


class DualSpell:
    fire_omens: list[raid_utils.OmenGroup] = None
    lightning_omens: list[BaseOmen] = None
    ice_omen: BaseOmen = None
    dur = 12.8

    fire_type = p9s.add_value(raid_utils.Select('default/waypoints/2.DualSpellFireType', [('+', 0), ('x', 1), ], 0))
    PATTERN_ICE = 0
    PATTERN_FIRE = 2
    PATTERN_LIGHTNING = 4

    def __init__(self):
        p9s.on_effect(33058)(self.on_fire_sp)
        p9s.on_effect(33059)(self.on_ice_sp)
        p9s.on_effect(33116)(self.on_lightning_sp)
        p9s.on_cast(33108, 33156)(self.on_cast_fire_ice)
        p9s.on_cast(33109, 33157)(self.on_cast_ice_lightning)
        p9s.on_reset(self.on_reset)
        self.pattern = 0
        p9s.add_value(raid_utils.ClickButton('default/waypoints/test/DualSpell_fire_P_ice', raid_utils.new_thread(lambda: self.on_select_test(
            (1 << self.PATTERN_ICE) | (1 << self.PATTERN_FIRE) | (1 << (self.PATTERN_ICE + 1))
        ))))
        p9s.add_value(raid_utils.ClickButton('default/waypoints/test/DualSpell_P_fire_ice', raid_utils.new_thread(lambda: self.on_select_test(
            (1 << self.PATTERN_ICE) | (1 << self.PATTERN_FIRE) | (1 << (self.PATTERN_FIRE + 1))
        ))))
        p9s.add_value(raid_utils.ClickButton('default/waypoints/test/DualSpell_P_ice_lightning', raid_utils.new_thread(lambda: self.on_select_test(
            (1 << self.PATTERN_ICE) | (1 << self.PATTERN_LIGHTNING) | (1 << (self.PATTERN_ICE + 1))
        ))))
        p9s.add_value(raid_utils.ClickButton('default/waypoints/test/DualSpell_ice_P_lightning', raid_utils.new_thread(lambda: self.on_select_test(
            (1 << self.PATTERN_ICE) | (1 << self.PATTERN_LIGHTNING) | (1 << (self.PATTERN_LIGHTNING + 1))
        ))))

    def on_select_test(self, pattern, dur=5):
        self.pattern = 0
        self.dur = dur
        if pattern & (1 << self.PATTERN_FIRE):
            self.make_fires()
        if pattern & (1 << self.PATTERN_ICE):
            self.make_ice()
        if pattern & (1 << self.PATTERN_LIGHTNING):
            self.make_lightnings()
        self.add_wp()
        time.sleep(dur / 2)
        if pattern & (1 << (self.PATTERN_FIRE + 1)):
            self.on_fire_sp(None)
        if pattern & (1 << (self.PATTERN_ICE + 1)):
            self.on_ice_sp(None)
        if pattern & (1 << (self.PATTERN_LIGHTNING + 1)):
            self.on_lightning_sp(None)

    def get_way_point(self, w: raid_utils.Waypoint):
        if not self.pattern:
            w.pop()
            return center
        me = raid_utils.get_me()
        role_idx = raid_utils.role_idx(me.id)
        if role_idx == 99:  # fail to get role
            logger.warning('fail to get role idx when play waypoints on DualSpell')
            w.pop()
            return center
        if self.pattern & (1 << self.PATTERN_FIRE):
            rad = pos_rad_4[role_idx]
            if self.fire_type.value == 1:  # is type[x]
                rad += pi_4
        elif self.pattern & (1 << self.PATTERN_LIGHTNING):
            rad = pos_rad_8[role_idx]
        else:
            logger.warning(f'pattern is not fire or lightning when play waypoints on DualSpell, got {self.pattern:#b}')
            w.pop()
            return center
        # dis = 6.5 if self.pattern & (1 << (self.PATTERN_ICE + 1)) else 13
        dis = 13 if self.pattern & (1 << (self.PATTERN_FIRE + 1)) or self.pattern & (1 << (self.PATTERN_LIGHTNING + 1)) else 6.5
        return glm.vec3(math.sin(rad), 0, math.cos(rad)) * dis + center

    def add_wp(self):
        if enable_waypoints.value:
            raid_utils.raid_helper.waypoints.append_waypoint(self.get_way_point, auto_pop=self.dur)

    def on_reset(self, _):
        self.pattern = 0

    def on_cast_fire_ice(self, evt: 'raid_utils.NetworkMessage[zone_server.ActorCast]'):
        self.dur = 12.8 if evt.message.action_id == 33108 else 8.15
        self.pattern = 0
        self.make_fires(), self.make_ice(), self.add_wp()

    def on_cast_ice_lightning(self, evt: 'raid_utils.NetworkMessage[zone_server.ActorCast]'):
        self.dur = 12.8 if evt.message.action_id == 33109 else 8.15
        self.pattern = 0
        self.make_ice(), self.make_lightnings(), self.add_wp()

    def on_fire_sp(self, _):
        self.pattern |= 1 << (self.PATTERN_FIRE + 1)
        if not self.fire_omens: return
        for omen in self.fire_omens:
            omen[0].apply_effect(ScaleTo, glm.vec3(12, 1, 12))

    def on_ice_sp(self, _):
        self.pattern |= 1 << (self.PATTERN_ICE + 1)
        if not self.ice_omen: return
        self.ice_omen.apply_effect(ScaleTo, glm.vec3(40, 1, 40))

    def on_lightning_sp(self, _):
        self.pattern |= 1 << (self.PATTERN_LIGHTNING + 1)
        if not self.lightning_omens: return
        for omen in self.lightning_omens:
            omen.apply_effect(ScaleTo, glm.vec3(16, 1, 40))

    def make_fire(self, actor_id):
        actor = raid_utils.NActor.by_id(actor_id)
        color = glm.vec4(1, .3, .3, .1) if raid_utils.is_class_job_dps(actor.class_job) else glm.vec4(.3, .3, 1, .1)
        line_color = color + glm.vec4(0, 0, 0, .7)
        res = raid_utils.OmenGroup(
            raid_utils.draw_circle(radius=6, pos=actor, surface_color=color, line_color=line_color, duration=self.dur)
        ) + raid_utils.draw_share(radius=6, pos=actor, surface_color=color, line_color=line_color, duration=self.dur)
        for omen in res:
            omen.apply_effect(HideWhenActorDead, actor_id)
        return res

    def make_fires(self):
        self.pattern |= 1 << self.PATTERN_FIRE
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
        self.pattern |= 1 << self.PATTERN_LIGHTNING
        self.lightning_omens = [self.make_lightning(a.id) for a in raid_utils.iter_main_party(False)]

    def make_ice(self):
        self.pattern |= 1 << self.PATTERN_ICE
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
                facing=actor.facing + pi,
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


class UpliftAndArchaicRockBreaker:
    LIFT_TYPE_A = 1  # +
    LIFT_TYPE_B = 2  # x

    def __init__(self):
        p9s.on_map_effect(self.on_map_effect)
        p9s.on_cast(33119)(self.on_cast_archaic_rockbreaker)
        self.lift_type = 0
        p9s.add_value(raid_utils.ClickButton('default/waypoints/test/UpliftAndArchaicRockBreaker_A', raid_utils.new_thread(lambda: self.test(self.LIFT_TYPE_A))))
        p9s.add_value(raid_utils.ClickButton('default/waypoints/test/UpliftAndArchaicRockBreaker_B', raid_utils.new_thread(lambda: self.test(self.LIFT_TYPE_B))))

    def test(self, lift_type):
        self.lift_type = lift_type
        self._on_cast_archaic_rockbreaker(center, 5)

    def on_map_effect(self, msg: NetworkMessage[zone_server.MapEffect]):
        _msg = msg.message
        if _msg.state == 0x1 and _msg.play_state == 0x2:
            if _msg.index == 0x2:
                logger.debug('lift type A')
                self.lift_type = self.LIFT_TYPE_A
            elif _msg.index == 0x3:
                logger.debug('lift type B')
                self.lift_type = self.LIFT_TYPE_B

    def get_knock_way_point(self):
        role_idx = raid_utils.role_idx(raid_utils.get_me().id)
        if role_idx == 99:  # fail to get role
            raise Exception('fail to get role idx when play waypoints on UpliftAndArchaicRockBreaker')
        rad = pos_rad_2[role_idx]
        if self.lift_type == self.LIFT_TYPE_B:
            rad += pi_4
        return glm.vec3(math.sin(rad), 0, math.cos(rad)) * 7 + center

    def on_cast_archaic_rockbreaker(self, msg: NetworkMessage[zone_server.ActorCast]):
        self._on_cast_archaic_rockbreaker(msg.message.pos, msg.message.cast_time)

    def _on_cast_archaic_rockbreaker(self, pos, cast_time):
        def _draw_share(actor_id):
            actor = raid_utils.NActor.by_id(actor_id)
            color = glm.vec4(1, .3, .3, .1) if raid_utils.is_class_job_dps(actor.class_job) else glm.vec4(.3, .3, 1, .1)
            line_color = color + glm.vec4(0, 0, 0, .7)
            res = raid_utils.OmenGroup(
                raid_utils.draw_circle(radius=6, pos=actor, surface_color=color, line_color=line_color, duration=7.8)
            ) + raid_utils.draw_share(radius=6, pos=actor, surface_color=color, line_color=line_color, duration=7.8)
            for omen in res:
                omen.apply_effect(HideWhenActorDead, actor_id)
            return res

        if enable_waypoints.value:
            raid_utils.raid_helper.waypoints.append_waypoint(self.get_knock_way_point(), auto_pop=cast_time + 1.5)

        raid_utils.draw_knock_predict_circle(radius=4, pos=pos, knock_distance=21, duration=cast_time + 1.5)
        for a in raid_utils.iter_main_party(False):
            _draw_share(a.id)


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

    solve_type = p9s.add_value(raid_utils.Select('default/waypoints/3.Levinstrike', [('马拉松', 0), ('定点', 1), ], 0))

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
            self.push_wp(0, 9)

    def on_icemeld(self, evt: 'raid_utils.NetworkMessage[zone_server.ActionEffect]'):
        if not self.enable: return
        i = [33155, 33168, 33169].index(evt.message.action_id) + 1
        self.draw_ball(i, 3.36)
        self.draw_ice(i, 5.7)
        self.draw_fire(i, 5.7)
        self.push_wp(i, 5.7)

    def type_1_find_top(self, phase, near=True):
        a, b = self.ball[:2] if phase else self.ball[2:]  # 第一二次取球1,2 第三四次取球3,4
        rad_a = glm.polar(a - center).y
        rad_b = glm.polar(b - center).y
        center_a = (rad_a + rad_b) / 2
        center_b = center_a + pi
        center_a = (center_a + pi) % pi2 - pi
        center_b = (center_b + pi) % pi2 - pi
        dis_a = abs((center_a - rad_a)) % pi2
        dis_b = abs((center_b - rad_b)) % pi2
        return center_a if near == dis_a < dis_b else center_b

    def wp_ice_active(self, idx):
        if self.solve_type.value == 0:  # 马拉松
            ball = self.ball[idx]
            return glm.normalize(ball - center) * 2 + ball  # 球的位置往后退2
        else:  # 定点
            top = self.type_1_find_top(idx < 2)  # 去校正后的十二点 远端
            return glm.vec3(math.sin(top), 0, math.cos(top)) * 18 + center

    def wp_ice_idle(self, idx):
        if self.solve_type.value == 0:  # 马拉松
            return self.ball[(idx + 1) % 4]  # 下一个球的位置
        else:  # 定点
            rad = self.type_1_find_top(idx < 2, False)
            return glm.vec3(math.sin(rad), 0, math.cos(rad)) * 7 + center

    def wp_fire_active(self, idx):
        if self.solve_type.value == 0:  # 马拉松
            if ball_pos := self.ball[idx]:
                rad = glm.polar(center - ball_pos).y - pi_4  # 塔的位置顺时针旋转45度
                return glm.vec3(math.sin(rad), 0, math.cos(rad)) * 18 + center
        else:  # 定点
            rad = self.type_1_find_top(idx < 2, False)
            return glm.vec3(math.sin(rad), 0, math.cos(rad)) * 18 + center

    def wp_fire_tower(self, idx):
        if ball_pos := self.ball[idx]:
            return center + glm.normalize(center - ball_pos) * 16

    def wp_fire_idle(self, idx):
        if self.solve_type.value == 0:  # 马拉松
            if ball_pos := self.ball[idx]:  # 塔前面
                return center + glm.normalize(center - ball_pos) * 7
        else:  # 定点
            rad = self.type_1_find_top(idx < 2, False)
            return glm.vec3(math.sin(rad), 0, math.cos(rad)) * 7 + center

    def push_wp(self, idx, dur):
        if not enable_waypoints.value: return
        me_id = raid_utils.get_me().id
        if me_id in self.fire:
            fire_idx = self.fire.index(me_id)
            if fire_idx == idx:
                raid_utils.raid_helper.waypoints.append_waypoint(self.wp_fire_active(idx), auto_pop=dur)
            elif fire_idx == (idx + 2) % 4:
                raid_utils.raid_helper.waypoints.append_waypoint(self.wp_fire_tower(idx), auto_pop=dur)
            else:
                raid_utils.raid_helper.waypoints.append_waypoint(self.wp_fire_idle(idx), auto_pop=dur)
        elif self.ice[idx] == me_id:
            raid_utils.raid_helper.waypoints.append_waypoint(self.wp_ice_active(idx), auto_pop=dur)
        else:
            raid_utils.raid_helper.waypoints.append_waypoint(self.wp_ice_idle(idx), auto_pop=dur)

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


class EclipticMeteor:
    order_type = p9s.add_value(raid_utils.Select('default/waypoints/4.EclipticMeteorOrder', [('TN share first', 0), ('DPS share first', 1), ], 1))

    def __init__(self):
        p9s.on_cast(33145)(self.on_cast_thunderbolt)

        self.comets = {}
        p9s.on_npc_spawn(16090)(self.on_comet_spawn)
        p9s.on_actor_control(ActorControlId.SetTimelineModelSkin)(self.on_set_timeline_model_skin)
        p9s.on_cast(33140)(self.on_comet_cast_burst)
        p9s.on_reset(lambda _: self.comets.clear())

    def on_comet_cast_burst(self, evt: NetworkMessage[zone_server.ActorCast]):
        self.comets.pop(evt.header.source_id, None)
        logger.debug(f'comet burst: {evt.header.source_id:x}')
        logger.debug(';'.join(f'{k:x}:{v}' for k, v in self.comets.items()))

    def on_set_timeline_model_skin(self, evt: ActorControlMessage[actor_control.SetTimelineModelSkin]):
        if evt.source_id in self.comets:
            self.comets[evt.source_id] = 1  # should be 1
            logger.debug(f'comet skin: {evt.source_id:x}')
            logger.debug(';'.join(f'{k:x}:{v}' for k, v in self.comets.items()))

    def on_comet_spawn(self, evt: NetworkMessage[zone_server.NpcSpawn]):
        self.comets[evt.header.source_id] = 0
        logger.debug(f'comet spawn: {evt.header.source_id:x}')
        logger.debug(';'.join(f'{k:x}:{v}' for k, v in self.comets.items()))

    def get_wp_share(self):
        comet_pos_to_share = [actor.pos for actor in raid_utils.find_actor_by_base_id(16090) if self.comets.get(actor.id)]
        if not comet_pos_to_share:
            raise Exception('fail to find comet when play waypoints on EclipticMeteor')
        pos = max(comet_pos_to_share, key=(lambda pos: pi if (rad := glm.polar(pos - center).y) < (-pi - .1) else rad))
        return glm.normalize(pos - center) * 13 + center

    def get_wp_fan(self):
        role_idx = raid_utils.role_idx(raid_utils.get_me().id)
        if role_idx == 99:  # fail to get role
            raise Exception('fail to get role idx when play waypoints on UpliftAndArchaicRockBreaker')
        rad = pos_rad_2[role_idx]
        is_x = glm.polar(next(raid_utils.find_actor_by_base_id(16090)).pos - center).y % pi_2 > .5
        if is_x: rad += pi_4
        return glm.vec3(math.sin(rad), 0, math.cos(rad)) * 6.5 + center

    def push_wp(self, dur_fan, dur_share):
        if enable_waypoints.value:
            me = raid_utils.get_me()
            if me.status.has_status(3323):  # 暗属性耐性大幅降低/已吃分摊
                raid_utils.raid_helper.waypoints.append_waypoint(self.get_wp_fan(), auto_pop=dur_fan)
            elif me.status.has_status(33146):  # 雷属性耐性大幅降低/已吃扇形
                raid_utils.raid_helper.waypoints.append_waypoint(self.get_wp_share(), auto_pop=dur_share)
            elif raid_utils.is_class_job_dps(me.class_job) == (self.order_type.value == 1):  # dps share first and me is dps/ tn share first and me is tn
                raid_utils.raid_helper.waypoints.append_waypoint(self.get_wp_share(), auto_pop=dur_share)
            else:
                raid_utils.raid_helper.waypoints.append_waypoint(self.get_wp_fan(), auto_pop=dur_fan)

    def on_cast_thunderbolt(self, evt: NetworkMessage[zone_server.ActorCast]):
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
        self.push_wp(evt.message.cast_time, share_cast)
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


def calc_circle_intersect(center_a: glm.vec2, center_b: glm.vec2, ra: float, rb: float):
    dis = glm.distance(center_a, center_b)
    if dis > ra + rb or dis < abs(ra - rb) or dis == 0: return []
    a = (ra ** 2 - rb ** 2 + dis ** 2) / (2 * dis)
    h = (ra ** 2 - a ** 2) ** .5
    p0 = center_a + (center_b - center_a) * a / dis
    if h == 0: return [p0]
    i1 = glm.vec2(p0.x + h * (center_b.y - center_a.y) / dis, p0.y - h * (center_b.x - center_a.x) / dis)
    i2 = glm.vec2(p0.x - h * (center_b.y - center_a.y) / dis, p0.y + h * (center_b.x - center_a.x) / dis)
    return [i1, i2]


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
    guild_order = raid_utils.make_role_rule("h2h1d4d3d2d1stmt")

    def __init__(self):
        self.enable = False
        p9s.on_cast(33211)(self.on_start_cast)
        p9s.on_lockon(0x4f, 0x50, 0x51, 0x52)(self.on_lockon_ice)
        p9s.on_effect(33155, 33168, 33169)(self.on_icemeld)

    def get_wp_guide(self, min_dis=None, max_dis=None):
        def f(w: raid_utils.Waypoint):
            target = current_pos = raid_utils.get_me().pos
            try:
                boss_pos = next(raid_utils.find_actor_by_base_id(16087)).pos
            except StopIteration:
                w.pop()
                logger.warning('fail to find boss when play waypoints on ChimericSuccession')
                return
            distance = glm.distance(current_pos, boss_pos)
            fix_dis = 0
            if min_dis is not None and distance < min_dis:
                fix_dis = min_dis + 1
            elif max_dis is not None and distance > max_dis:
                fix_dis = max_dis - 1
            if fix_dis:
                target = boss_pos + glm.normalize(current_pos - boss_pos) * fix_dis
                # check that should not be too far to center
                if glm.distance(target, center) > 19:
                    _pts = calc_circle_intersect(center.xz, boss_pos.xz, 19, fix_dis)
                    pts = [glm.vec3(p.x, 0, p.y) for p in _pts]
                    target = min(pts, key=lambda p: glm.distance(p, current_pos))
            return target

        return f

    def set_guide_wp(self, dur):
        if enable_waypoints.value:
            guid_actors = sorted((a.id for a in raid_utils.iter_main_party(False)), key=lambda a_id: raid_utils.role_key(self.guild_order, a_id))
            try:
                me_idx = guid_actors.index(raid_utils.get_me().id)
            except ValueError:
                raise Exception(f"fail to find me in guid_actors: {guid_actors=}")
            match me_idx:
                case 0:  # dis {14,}
                    pos = self.get_wp_guide(min_dis=14)
                case 1:  # dis {11,13}
                    pos = self.get_wp_guide(min_dis=11, max_dis=13)
                case 2 | 3:  # dis {8,10}
                    pos = self.get_wp_guide(min_dis=8, max_dis=10)
                case _:  # dis {,7}
                    pos = self.get_wp_guide(max_dis=7)
            raid_utils.raid_helper.waypoints.append_waypoint(pos, auto_pop=dur)

    def on_start_cast(self, evt: NetworkMessage[zone_server.ActorCast]):
        self.enable = True
        levinstrike.enable = False
        self.ice = [None for _ in range(4)]
        self.set_guide_wp(evt.message.cast_time)

    def get_fire_wp(self, w: raid_utils.Waypoint):
        try:
            boss_pos = next(raid_utils.find_actor_by_base_id(16087)).pos
        except StopIteration:
            w.pop()
            logger.warning('fail to find boss when play waypoints on ChimericSuccession')
            return
        return glm.normalize(center - boss_pos) * 19 + center

    def set_fire_wp(self, dur=15):
        if not enable_waypoints.value: return
        me_id = raid_utils.get_me().id
        if me_id in self.ice: return
        raid_utils.raid_helper.waypoints.append_waypoint(self.get_fire_wp, auto_pop=dur)

    def on_lockon_ice(self, evt: 'raid_utils.ActorControlMessage[actor_control.SetLockOn]'):
        if not self.enable: return
        self.ice[i := evt.param.lockon_id - 0x4f] = evt.source_id
        if i == 0: self.draw_ice(0, 10)
        if all(self.ice):
            self.set_fire_wp()

    def on_icemeld(self, evt: 'raid_utils.NetworkMessage[zone_server.ActionEffect]'):
        if not self.enable: return
        self.draw_ice([33155, 33168, 33169].index(evt.message.action_id) + 1, 3)

    def get_ice_wp(self, w: raid_utils.Waypoint):
        me_pos = raid_utils.get_me().pos
        return glm.normalize(me_pos - center) * 19 + center

    def set_ice_wp(self, dur):
        if not enable_waypoints.value: return
        raid_utils.raid_helper.waypoints.append_waypoint(self.get_ice_wp, auto_pop=dur)

    def draw_ice(self, idx, dur):
        target_id = self.ice[idx]
        if not target_id:
            return logger.warning(f"ice[{idx}] is None: {target_id=:x}")
        if target_id == raid_utils.get_me().id:
            self.set_ice_wp(dur)
        return raid_utils.draw_circle(
            radius=20,
            pos=raid_utils.NActor.by_id(target_id),
            duration=dur,
        )


dual_spell = DualSpell()
combination = Combination()
up_lift_and_archaic_rock_breaker = UpliftAndArchaicRockBreaker()
levinstrike = Levinstrike()
ecliptic_meteor = EclipticMeteor()
chimeric_succession = ChimericSuccession()
p9s.clear_decorators()
