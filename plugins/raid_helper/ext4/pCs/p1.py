import threading
import time

from .utils import *

special_actions[33505] = raid_utils.fan_shape(180)
special_actions[33506] = raid_utils.fan_shape(180)
special_actions[33511] = raid_utils.fan_shape(180)
special_actions[33512] = raid_utils.fan_shape(180)
special_actions[33500] = 0
special_actions[33499] = 0


class Anthropos:
    # Logou Idea base_id=0x3f2c pop_action_tid=9442 desc=场外固定直线aoe
    # Thymou Idea base_id=0x3f2e pop_action_tid=9443 desc=最近两人直线aoe
    # Epithymias Idea base_id=0x3f2f pop_action_tid=9444 desc=连线直线aoe
    Logou = 0
    Thymou = 1
    Epithymias = 2

    def __init__(self):
        self.idea_lock = threading.Lock()
        self.idea_stack = []
        self.last_idea_update = 0
        pCs.on_actor_play_action_timeline(9442, 9443, 9444)(self.on_idea_update)
        pCs.on_actor_play_action_timeline(7750)(self.on_anthropos_set)

    def on_idea_update(self, evt: PlayActionTimelineMessage):
        with self.idea_lock:
            current = time.time()
            if current - self.last_idea_update > 1:
                self.idea_stack.clear()
                logger.debug('idea update timeout')
            self.last_idea_update = current

        match evt.timeline_id:
            case 0x24e2:
                self.idea_stack.append(Anthropos.Logou)
            case 0x24e3:
                self.idea_stack.append(Anthropos.Thymou)
            case 0x24e4:
                self.idea_stack.append(Anthropos.Epithymias)

    def on_anthropos_set(self, evt: PlayActionTimelineMessage):
        actor = raid_utils.NActor.by_id(evt.id)
        if actor.base_id != 0x3f2c:
            return logger.warn(f'not anthropos {actor.base_id=:x}')
        time.sleep(1)
        if not self.idea_stack:
            return logger.warn('anthropos set but no idea')
        idea_type = self.idea_stack.pop(0)
        if idea_type == Anthropos.Logou:
            # self.on_logou_set(actor) # 自带omen
            pass
        elif idea_type == Anthropos.Thymou:
            self.on_thymou_set(actor)
        elif idea_type == Anthropos.Epithymias:
            # self.on_epithymias_set(actor) # 自带omen
            pass

    def on_thymou_set(self, source_actor: 'raid_utils.NActor'):
        raid_utils.sleep(4.5)
        raid_utils.draw_rect(
            width=4, length=100, pos=source_actor,
            facing=lambda _: source_actor.target_radian(raid_utils.get_actor_by_dis(source_actor, 0)),
            duration=5,
        )
        raid_utils.draw_rect(
            width=4, length=100, pos=source_actor,
            facing=lambda _: source_actor.target_radian(raid_utils.get_actor_by_dis(source_actor, 1)),
            duration=5,
        )


class TrinityOfSouls:
    LEFT = 0
    RIGHT = 1

    def __init__(self):
        self.lr_types = [0, 0, 0]
        self.top_first = False
        pCs.on_add_status(3572)(self.on_add_status_3572)
        pCs.on_effect(33505, 33506)(lambda evt: self.apply_omen(raid_utils.NActor.by_id(evt.header.source_id), False, 1))  # no_rev 1
        pCs.on_effect(33507, 33508)(lambda evt: self.apply_omen(raid_utils.NActor.by_id(evt.header.source_id), False, 2))  # no_rev
        pCs.on_effect(33511, 33512)(lambda evt: self.apply_omen(raid_utils.NActor.by_id(evt.header.source_id), True, 1))  # rev 1
        pCs.on_effect(33513, 33514)(lambda evt: self.apply_omen(raid_utils.NActor.by_id(evt.header.source_id), True, 0))  # rev 2

    def on_add_status_3572(self, evt: 'ActorControlMessage[actor_control.AddStatus]'):
        match evt.param.param:
            case 19:
                self.lr_types[0] = self.LEFT  # top left
            case 20:
                self.lr_types[0] = self.RIGHT  # top right
            case 21:
                self.lr_types[1] = self.LEFT  # mid left
            case 22:
                self.lr_types[1] = self.RIGHT  # mid right
            case 23:
                self.lr_types[2] = self.LEFT  # bottom left
            case 24:
                self.lr_types[2] = self.RIGHT  # bottom right

    def apply_omen(self, source_actor: 'raid_utils.NActor', is_reverse, next_idx, dur=2.6):
        facing = source_actor.facing + math.radians(90 if (self.lr_types[next_idx] == self.LEFT) != is_reverse else -90)
        raid_utils.draw_fan(degree=180, radius=60, pos=source_actor, facing=facing, duration=dur)


class SuperchainTheory:
    # base_id 16176
    # base_id 16177 action_id 33499 circle range 7
    # base_id 16178 action_id 33500 donut range 70 ignore 6
    # base_id 16179 action_id 33501 fan range 100 angle 30 * 8
    # base_id 16180 action_id 33502 share fan range 100 angle 30 * 4

    def __init__(self):
        self.channel_record = {}
        pCs.on_npc_spawn(16177, 16178, 16179, 16180)(self.on_npc_create)
        pCs.on_add_status(2056)(self.on_add_start_status)

    def on_npc_create(self, evt: NetworkMessage[zone_server.NpcSpawn]):
        self.channel_record.setdefault(evt.message.create_common.channeling_target, []).append(evt.header.source_id)

    def on_add_start_status(self, evt: ActorControlMessage[actor_control.AddStatus]):
        if evt.param.param != 583: return
        core_actor = raid_utils.NActor.by_id(evt.source_id)
        if core_actor.base_id != 16176: return
        for aid in self.channel_record.get(core_actor.id, []):
            action_actor = raid_utils.NActor.by_id(aid)
            cast_time = action_actor.target_distance(core_actor) / 3 + 1
            match action_actor.base_id:
                case 16177:
                    raid_utils.new_thread(self.draw_circle)(core_actor, cast_time)
                case 16178:
                    raid_utils.new_thread(self.draw_donut)(core_actor, cast_time)
                case 16179:
                    raid_utils.new_thread(self.draw_fan)(core_actor, cast_time)
                case 16180:
                    raid_utils.new_thread(self.draw_share_fan)(core_actor, cast_time)
                case _:
                    logger.warning(f'unknown action {action_actor.base_id=:x}')
                    continue

    @staticmethod
    def draw_circle(core_actor: 'raid_utils.NActor', cast_time: float):
        raid_utils.sleep(cast_time - 4)
        raid_utils.draw_circle(pos=core_actor, radius=7, duration=min(cast_time, 4))

    @staticmethod
    def draw_donut(core_actor: 'raid_utils.NActor', cast_time: float):
        raid_utils.sleep(cast_time - 4)
        raid_utils.draw_circle(radius=70, inner_radius=6, pos=core_actor, duration=min(cast_time, 4), )

    @staticmethod
    def draw_fan(core_actor: 'raid_utils.NActor', cast_time: float):
        def _draw(target_actor: 'raid_utils.NActor', duration: float):
            return raid_utils.draw_fan(degree=30, radius=100, pos=core_actor, facing=lambda _: core_actor.target_radian(target_actor), duration=duration)

        raid_utils.sleep(cast_time - 4)
        for actor in raid_utils.iter_main_party(False):
            _draw(actor, min(cast_time, 4))

    @staticmethod
    def draw_share_fan(core_actor: 'raid_utils.Actor', cast_time: float):
        def _draw(target_actor: 'raid_utils.Actor', duration: float):
            color = glm.vec4(1, .3, .3, .3) if raid_utils.is_class_job_dps(actor.class_job) else glm.vec4(.3, .3, 1, .3)
            return raid_utils.draw_fan(
                degree=30,
                radius=100,
                pos=core_actor,
                facing=lambda _: core_actor.target_radian(target_actor),
                duration=duration,
                surface_color=color, line_color=color + glm.vec4(0, 0, 0, .5)
            )

        raid_utils.sleep(cast_time - 4)
        for actor in raid_utils.iter_main_party(False):
            _draw(actor, min(cast_time, 4))


@pCs.on_add_status(3578)
def on_add_status_heavensflame(evt: ActorControlMessage[actor_control.AddStatus]):
    actor = raid_utils.NActor.by_id(evt.source_id)
    if raid_utils.assert_status(actor, 3578, 5):
        raid_utils.draw_circle(radius=6, pos=actor, duration=5)


@pCs.on_add_status(3582, 3581)
def on_add_status_heavensflame_share(evt: ActorControlMessage[actor_control.AddStatus]):
    actor = raid_utils.NActor.by_id(evt.source_id)
    if raid_utils.assert_status(actor, evt.param.status_id, 5):
        athena = next(raid_utils.find_actor_by_base_id(0x3f2b))
        color = glm.vec4(.5, .1, 0, .3) if evt.param.status_id == 3582 else glm.vec4(.9, 1, 1, .3)
        raid_utils.draw_rect(
            width=6, length=100, pos=athena, facing=lambda _: athena.target_radian(actor), duration=5,
            surface_color=color, line_color=color + glm.vec4(0, 0, 0, .5)
        )


@pCs.on_cast(33534, 33535)
def on_cast_apodialogos_peridialogos(evt: NetworkMessage[zone_server.ActorCast]):
    source_actor = raid_utils.NActor.by_id(evt.header.source_id)
    tank_o, share_o = (0, -1) if evt.message.action_id == 33535 else (-1, 0)
    tank_color = glm.vec4(.5, 0, 0, .3)
    raid_utils.draw_share(
        radius=6,
        pos=lambda _: raid_utils.get_actor_by_dis(source_actor, tank_o).pos,
        duration=evt.message.cast_time + + 1,
    )
    raid_utils.draw_share(
        radius=6,
        pos=lambda _: raid_utils.get_actor_by_dis(source_actor, share_o).pos,
        duration=evt.message.cast_time + + 1,
        surface_color=tank_color, line_color=tank_color + glm.vec4(0, 0, 0, .5)
    )


class Palladion:
    head_mark: list[raid_utils.NActor | None]

    def __init__(self):
        self.head_mark = [None for _ in range(8)]
        self.fix_pos = []
        self.anthropos_type = {}
        self.anthropos_order = [0 for _ in range(8)]
        pCs.on_effect(33524)(self.on_effect_ultima_blade)
        pCs.on_lockon(0x150, 0x151, 0x152, 0x153, 0x1b5, 0x1b6, 0x1b7, 0x1b8)(self.on_icon_dice)
        pCs.on_effect(33526)(self.on_effect_palladion)

        pCs.on_effect(33524)(self.on_effect_ultima_blade)
        pCs.on_actor_play_action_timeline(4564, 4563)(self.on_play_type_timeline)
        pCs.on_actor_play_action_timeline(7737)(self.on_add_fly)

    def on_effect_ultima_blade(self, _):
        self.head_mark = [None for _ in range(8)]
        self.fix_pos = []
        self.anthropos_order.clear()

    def on_icon_dice(self, evt: 'ActorControlMessage[actor_control.SetLockOn]'):
        source_actor = raid_utils.NActor.by_id(evt.source_id)
        match evt.param.lockon_id:
            case _i if 0x150 <= _i <= 0x153:
                self.head_mark[i := (_i - 0x150)] = source_actor
            case _i if 0x1b5 <= _i <= 0x1b8:
                self.head_mark[i := (_i - 0x1b5 + 4)] = source_actor
            case _:
                return
        if i == 0:
            self.draw_first(source_actor)

    def draw_first(self, target_actor, dur=8.5):
        athena = next(raid_utils.find_actor_by_base_id(0x3f2b))
        raid_utils.draw_rect(
            width=4, length=lambda _: athena.target_distance(target_actor),
            pos=athena, facing=lambda _: athena.target_radian(target_actor),
            duration=dur
        )
        raid_utils.draw_circle(radius=6, pos=target_actor, duration=dur)
        raid_utils.draw_share(radius=6, pos=target_actor, duration=dur)
        self.draw_anthropos(0, dur)
        sec_end = time.time() + dur + 3
        while (not self.head_mark[1] and time.time() < sec_end):
            time.sleep(.1)
        sec_dur = sec_end - time.time()
        if sec_dur > 0: self.draw_omen(1, sec_dur)

    def on_effect_palladion(self, evt: 'NetworkMessage[zone_server.ActionEffect]'):
        a_pos = evt.message.pos
        self.fix_pos.append(a_pos)
        if len(self.fix_pos) < 7:
            self.draw_omen(len(self.fix_pos) + 1, 6)
        if len(self.fix_pos) < 8:
            self.draw_anthropos(len(self.fix_pos), 3)

    def draw_anthropos(self, idx, dur):
        if len(self.anthropos_order) <= idx:
            return logger.warning(f'no anthropos type {idx=} {self.anthropos_order=}')
        if self.anthropos_order[idx] == 4564:  # light
            raid_utils.draw_rect(
                width=4, length=100,
                pos=center,
                facing=lambda _: glm.polar(raid_utils.get_actor_by_dis(center, 0).pos - center).y,
                duration=dur,
            )
            raid_utils.draw_rect(
                width=4, length=100,
                pos=center,
                facing=lambda _: glm.polar(raid_utils.get_actor_by_dis(center, 1).pos - center).y,
                duration=dur,
            )
        else:  # dark
            if idx % 2:
                f = math.pi / 2
            else:
                f = -math.pi / 2
            raid_utils.draw_fan(
                degree=270, radius=4,
                pos=center,
                facing=f,
                duration=dur,
            )

    def draw_omen(self, idx, dur):
        raid_utils.draw_rect(
            pos=lambda _: self.get_start_pos(idx),
            width=4, length=lambda _: glm.distance(self.get_start_pos(idx), self.get_end_pos(idx)),
            facing=lambda _: glm.polar(self.get_end_pos(idx) - self.get_start_pos(idx)).y,
            duration=dur,
        )
        raid_utils.draw_circle(radius=6, pos=lambda _: self.get_end_pos(idx), duration=dur)
        raid_utils.draw_share(radius=6, pos=lambda _: self.get_end_pos(idx), duration=dur)

    def get_start_pos(self, idx):
        i = idx - 1
        if len(self.fix_pos) > i:
            return self.fix_pos[i]
        else:
            return self.head_mark[i].pos

    def get_end_pos(self, idx):
        return self.head_mark[idx].pos

    def on_play_type_timeline(self, evt: PlayActionTimelineMessage):
        logger.debug(f'anthropos_type {evt.id=} {evt.timeline_id=}')
        self.anthropos_type[evt.id] = evt.timeline_id

    def on_add_fly(self, evt: PlayActionTimelineMessage):
        if len(self.anthropos_order) >= 8: return
        t = self.anthropos_type.pop(evt.id, 0)
        logger.debug(f'anthropos_fly {evt.id=} {t=}')
        self.anthropos_order.append(t)


@pCs.on_effect(33528)
def on_palladion_cut_ground(_):
    raid_utils.draw_rect(width=20, length=100, pos=glm.vec3(100, 0, 100), facing=math.pi / 2, duration=4, arg=1)


anthropos = Anthropos()
trinity_of_souls = TrinityOfSouls()
superchain_theory = SuperchainTheory()
palladion = Palladion()
