import math
import threading

import glm

from raid_helper import utils as raid_utils
from raid_helper.utils.typing import *
from raid_helper.data import special_actions

map_ex = raid_utils.MapTrigger.get(1096)
center = glm.vec3(100, 0, 100)
is_enable = map_ex.add_value(raid_utils.BoolCheckBox('default/enable', True))
map_ex.decorators.append(lambda f: (lambda *args, **kwargs: f(*args, **kwargs) if is_enable.value else None))
# special_actions[31983] = 0x50000 | 60  # 转转转扇形
# 因为会手动提前绘制，所以禁用自动绘制
special_actions[31983] = 0  # 转转转扇形
special_actions[31984] = 0  # 转转转半场
special_actions[32032] = 0x50000 | 180  # 半场刀
special_actions[32033] = 0x50000 | 180  # 半场刀
special_actions[32037] = 0x10000 | int(.5 * 0xffff)  # 月环


@map_ex.on_cast(31998)
def on_cast_radial_flagration(msg: NetworkMessage[zone_server.ActorCast]):
    # Radial Flagration
    # 执行技能 31999
    # 从中心发出全体扇形aoe带易伤，延时.9s(885?)
    # 角度 30, 距离 21
    def play(target: raid_utils.NActor):  # 因为 for 会影响 lambda 里面 actor 的值，所以包一个函数
        raid_utils.draw_fan(degree=30, radius=21, pos=center, facing=lambda _: glm.polar(target.update().pos - center).y, duration=msg.message.cast_time + .9)

    for actor in raid_utils.iter_main_party(False):
        play(actor)


@map_ex.on_cast(32036, 32037)
def on_cast_radial_flagration(msg: NetworkMessage[zone_server.ActorCast]):
    # Scalding Signal|Scalding Ring => Scalding Fleet
    # 执行技能 32038
    # 钢铁月环后马上接全体矩形aoe，延时4s
    # 宽度 6, 距离 60
    def play(target: raid_utils.NActor):
        raid_utils.draw_rect(width=6, length=60, pos=center, facing=lambda _: glm.polar(target.update().pos - center).y, duration=msg.message.cast_time + 1.2)

    for actor in raid_utils.iter_main_party(False):
        play(actor)


@map_ex.on_set_channel(192)
def on_channel_ghastly_wind(msg: ActorControlMessage[actor_control.SetChanneling]):
    # Ghastly Wind
    # 执行技能 32011
    # 对连线角色发出扇形aoe，延时7.1s
    # 角度 60, 范围 40
    source_actor = raid_utils.NActor.by_id(msg.source_id)
    target_actor = raid_utils.NActor.by_id(msg.param.target_id)
    raid_utils.timeout_when_channeling_change(  # 这个函数会监听连线转移或者任意一个人消失或者 blablabla 的时候删除绘制
        raid_utils.draw_fan(degree=60, radius=40, pos=source_actor, facing=lambda _: glm.polar(target_actor.update().pos - source_actor.update().pos).y, duration=8),
        msg.source_id, msg.param.target_id, msg.param.idx  # 传监控参
    )


@map_ex.on_set_channel(84)
def on_channel_shattering_heat(msg: ActorControlMessage[actor_control.SetChanneling]):
    # Shattering Heat
    # 执行技能 32010
    # 对连线角色发出死刑级小范围圆形aoe，延时7.1s
    # 范围 3
    target_actor = raid_utils.NActor.by_id(msg.param.target_id)
    raid_utils.timeout_when_channeling_change(
        raid_utils.draw_circle(radius=3, pos=target_actor, duration=8),
        msg.source_id, msg.param.target_id, msg.param.idx
    )


@map_ex.on_add_status(3483)
def on_add_status_blooming_welt(msg: ActorControlMessage[actor_control.AddStatus]):
    # 12s
    # Blooming Welt
    # 执行技能 32020
    # 距离衰减伤害（12）
    t_actor = raid_utils.NActor.by_id(msg.source_id)
    if not raid_utils.assert_status(t_actor, 3483, 6): return  # 用来确认目标用户直到倒计时剩余6s的时候依然有这个buff (处理死人、掉buff等情况)
    raid_utils.draw_circle(radius=12, pos=t_actor, duration=6)  # 最大伤害圆
    raid_utils.draw_circle(  # 画一个扩散特效
        radius=lambda o: (o.remaining_time % 1) * 28 + 12,
        pos=t_actor,
        line_color=raid_utils.default_color(), alpha=lambda o: 1 - (o.remaining_time % 1),
        duration=6
    )


@map_ex.on_add_status(3484)
def on_add_status_furious_welt(msg: ActorControlMessage[actor_control.AddStatus]):
    # 12s
    # Furious Welt
    # 执行技能 32021
    # 分摊伤害
    # 范围 6
    t_actor = raid_utils.NActor.by_id(msg.source_id)
    if not raid_utils.assert_status(t_actor, 3484, 6): return
    raid_utils.draw_share(radius=6, pos=t_actor, duration=6)


@map_ex.on_add_status(3485)
def on_add_status_stinging_welt(msg: ActorControlMessage[actor_control.AddStatus]):
    # 15s
    # Stinging Welt
    # 执行技能 32022
    # 带易伤的分散
    # 范围 6
    t_actor = raid_utils.NActor.by_id(msg.source_id)
    if not raid_utils.assert_status(t_actor, 3485, 6): return
    raid_utils.draw_circle(radius=6, pos=t_actor, duration=6)


@map_ex.on_lockon(230)
def on_lockon_dualfire(msg: ActorControlMessage[actor_control.SetLockOn]):
    # Dualfire
    # 执行技能 32047
    # 扇形死刑
    # 角度 120, 范围 60
    rubicante = next(raid_utils.find_actor_by_base_id(0x3d8c))
    t_actor = raid_utils.NActor.by_id(msg.source_id)
    raid_utils.draw_fan(degree=120, radius=60, pos=rubicante, facing=lambda _: glm.polar(t_actor.update().pos - rubicante.update().pos).y, duration=6)


class HopeAbandonYe:
    middle_route = [0, 0, None, -1, 0, +1, None, 0]
    omens: 'list[raid_utils.BaseOmen|None]'

    def __init__(self):
        self.fix = [0, 0, 0]
        self.outer = [0 for _ in range(8)]
        self.middle_rotate = 0
        self.inner = ()
        self.omens = [None, None]
        self.lock = threading.Lock()
        map_ex.on_add_status(2056)(self.on_add_status)
        map_ex.on_actor_play_action_timeline(4561)(self.update_outer)
        map_ex.on_map_effect(self.on_map_event)

    def on_add_status(self, msg: ActorControlMessage[actor_control.AddStatus]):
        round_facing = round(raid_utils.NActor.by_id(msg.source_id).facing / (math.pi / 4))
        match msg.param.param:
            case 542:
                self.inner = round_facing,
            case 543:
                self.inner = round_facing, round_facing - 2
            case 544:
                self.inner = round_facing, round_facing - 4
            case 545:
                self.middle_rotate = round_facing

    def update_outer(self, msg: PlayActionTimelineMessage):
        actor = raid_utils.NActor.by_id(msg.id)
        self.outer[round(actor.facing / (math.pi / 4)) % 8] = actor.base_id - 15758

    def on_map_event(self, msg: NetworkMessage[zone_server.MapEffect]):
        # 1|2|1 = 内顺
        # 1|2|2 = 中顺
        # 1|2|3 = 外顺
        # 16|32|1 = 内逆
        # 16|32|2 = 中逆
        # 16|32|3 = 外逆
        state = msg.message.state
        index = msg.message.index

        if 0 < index < 4 and (state == 1 or state == 16):
            self.fix[index - 1] = -1 if state == 1 else 1
            with self.lock: self.exec()
            return
        self.fix = [0, 0, 0]

    def exec(self):
        for o in self.omens:
            if o:
                o.timeout()
        # res = []
        for i, s in enumerate(self.inner):
            s += self.fix[0]
            if (m_fix := self.middle_route[(s - (self.middle_rotate + self.fix[1])) % 8]) is None: continue
            d = (s + m_fix) % 8
            _r = d * math.pi / 4
            pos = center + glm.euclidean(glm.vec2(0, _r)) * 20
            if self.outer[(d - self.fix[2]) % 8] == 1:
                shape = 0x50000 | 60
                scale = glm.vec3(60, 1, 60)
            else:
                shape = 0x20000
                scale = glm.vec3(40, 0, 20)
            self.omens[i] = raid_utils.create_game_omen(
                shape=shape, pos=pos, scale=scale, facing=_r - math.pi,
                duration=18
            )


class FlamespireClaw:
    # Flamespire Claw
    # 依次对点名使用 32371
    # 角度 130，范围 20
    prev_action: 'raid_utils.BaseOmen|None' = None

    def __init__(self):
        self.queue = []
        map_ex.on_lockon(*range(79, 87))(raid_utils.DelayCallOnce(self._process_on_icon, .3))
        map_ex.on_effect(32371)(self.pop)

    def _process_on_icon(self, data: 'list[tuple[ActorControlMessage[actor_control.SetLockOn]]]'):
        self.queue = [actor for _, actor in sorted(
            (msg.param.lockon_id, raid_utils.NActor.by_id(msg.source_id)) for msg, in data
        )]
        self.pop()

    def pop(self, _=None):
        if self.prev_action:
            self.prev_action.timeout()
            self.prev_action = None
        if self.queue:
            actor = next(iter(raid_utils.find_actor_by_base_id(0x3d8c)))
            t_actor = self.queue.pop(0)
            self.prev_action = raid_utils.draw_fan(
                degree=130, radius=20, pos=actor.pos,
                facing=lambda _: glm.polar(t_actor.update().pos - actor.update().pos).y, duration=20,
                surface_color=glm.vec4(1, .6, .6, .5), line_color=glm.vec4(1, .6, .6, .9)
            )


flamespire_claw = FlamespireClaw()
hope_abandon_ye = HopeAbandonYe()

map_ex.clear_decorators()
