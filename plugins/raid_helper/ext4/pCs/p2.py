import math
import threading

from .utils import *

special_actions[33613] = 0
special_actions[34435] = 0
special_actions[33569] = 0


class PalladianGrasp:
    left = glm.vec3(90, 0, 77)
    right = glm.vec3(110, 0, 77)

    def __init__(self):
        self.omen: raid_utils.BaseOmen | None = None
        pCs.on_cast(33562, 33563)(self.on_cast)
        pCs.on_effect(33562)(self.on_effect)

    def on_cast(self, evt: NetworkMessage[zone_server.ActorCast]):
        if self.omen: self.omen.destroy()
        t = raid_utils.NActor.by_id(
            raid_utils.NActor.by_id(
                evt.header.source_id
            ).target_id
        )
        self.omen = raid_utils.draw_rect(
            width=20, length=35,
            pos=lambda _: self.left if t.pos.x < 100 else self.right,
            facing=0,
            duration=evt.message.cast_time,
        )

    def on_effect(self, evt: NetworkMessage[zone_server.ActionEffect]):
        if self.omen: self.omen.destroy()
        self.omen = raid_utils.draw_rect(
            width=20, length=35,
            pos=lambda _: self.left if raid_utils.NActor.by_id(
                raid_utils.NActor.by_id(
                    evt.header.source_id
                ).target_id
            ).pos.x < 100 else self.right,
            facing=0,
            duration=2.5,
        )


@pCs.on_cast(33579)
def on_cast_geocentrism_horiz(evt: NetworkMessage[zone_server.ActorCast]):
    for z in range(85, 96, 5):
        raid_utils.draw_rect(
            width=4, length=20,
            pos=glm.vec3(90, 0, z),
            facing=math.pi / 2,
            duration=evt.message.cast_time,
        )


@pCs.on_cast(33577)
def on_cast_geocentrism_vert(evt: NetworkMessage[zone_server.ActorCast]):
    for x in range(90, 106, 5):
        raid_utils.draw_rect(
            width=4, length=20,
            pos=glm.vec3(x, 0, 80),
            facing=0,
            duration=evt.message.cast_time,
        )


@pCs.on_cast(33578)
def on_cast_geocentrism_round(evt: NetworkMessage[zone_server.ActorCast]):
    raid_utils.draw_circle(radius=2, pos=glm.vec3(100, 0, 90), duration=evt.message.cast_time)
    raid_utils.draw_circle(radius=7, inner_radius=3, pos=glm.vec3(100, 0, 90), duration=evt.message.cast_time)


@pCs.on_lockon(0x16)
def on_icon_divine_excoriation(evt: ActorControlMessage[actor_control.SetLockOn]):
    raid_utils.draw_circle(
        radius=1,
        pos=raid_utils.NActor.by_id(evt.source_id),
        duration=3,
    )


def m_dis(x1, y1, x2, y2):
    return round(abs(x1 - x2) + abs(y1 - y2))


class TheClassicalConcepts:
    unk = 0
    fire = 0x3f37
    water = 0x3f38
    ground = 0x3f39

    def __init__(self):
        self.lock = threading.Lock()
        self.reset()
        self.concept_count = 12
        self.waters = []
        self.fires = []
        self.grounds = []
        self.omens = []
        pCs.on_cast(33585)(self.reset)
        pCs.on_npc_spawn(self.fire, self.water, self.ground)(self.on_concept_spawn)
        pCs.on_cast(33590)(self.on_cast_panta_rhei)

    def reset(self, _=None):
        self.concept_count = 12
        self.waters = []
        self.fires = []
        self.grounds = []
        self.omens = []

    def on_concept_spawn(self, evt: NetworkMessage[zone_server.NpcSpawn]):
        x, _, y = evt.message.create_common.pos
        {
            self.fire: self.fires,
            self.water: self.waters,
            self.ground: self.grounds,
        }[evt.message.create_common.npc_id].append((
            round((x - 88) / 8), round((y - 84) / 8)
        ))
        with self.lock:
            self.concept_count -= 1
            if self.concept_count: return
        self.solve(17)

    def on_cast_panta_rhei(self, evt: NetworkMessage[zone_server.ActorCast]):
        self.waters = [(3 - x, 2 - y) for x, y in self.waters]
        self.fires = [(3 - x, 2 - y) for x, y in self.fires]
        self.grounds = [(3 - x, 2 - y) for x, y in self.grounds]
        self.solve(evt.message.cast_time)

    def solve(self, dur):
        for omen in self.omens: omen.destroy()
        self.omens.clear()

        fire_connect = {}
        ground_connect = {}
        result = {}
        for water in self.waters:
            [fire_connect.setdefault(fire, []).append(water) for fire in self.fires if m_dis(*water, *fire) == 1]
            [ground_connect.setdefault(ground, []).append(water) for ground in self.grounds if m_dis(*water, *ground) == 1]

        def parse_connect(connect: dict[tuple[int, int], list[tuple[int, int]]]):
            for _ in range(4):
                for element, connected_water in list(connect.items()):
                    if len(connected_water) == 1:
                        result.setdefault(connected_water[0], []).append(element)
                        connect.pop(element)
                        for _connected_water in connect.values():
                            try:
                                _connected_water.remove(connected_water[0])
                            except ValueError:
                                pass
                        break
            if connect:
                raise ValueError(f'connect cant be solved: {connect}')

        parse_connect(fire_connect)
        parse_connect(ground_connect)
        fire_color = glm.vec4(.7, .1, .1, 1)
        ground_color = glm.vec4(.7, .5, .1, 1)
        for (water_x, water_y), elements in result.items():
            for (el_x, el_y), color in zip(elements, [fire_color, ground_color]):
                self.omens.append(raid_utils.draw_line(
                    source=glm.vec3(el_x * 8 + 88, 1, el_y * 8 + 84),
                    target=glm.vec3(water_x * 8 + 88, 1, water_y * 8 + 84),
                    color=glm.vec4(.3, .3, .7, 1),
                    width=5,
                    duration=dur,
                ))


@pCs.on_cast(33571)
def on_cast_palladian_ray(evt: NetworkMessage[zone_server.ActorCast]):
    p1 = glm.vec3(92, 0, 92)
    p2 = glm.vec3(108, 0, 92)

    def _draw(p, i):
        raid_utils.draw_fan(
            degree=30, radius=100,
            pos=p,
            facing=lambda _: glm.polar(raid_utils.get_actor_by_dis(p, i).pos - p).y,
            duration=evt.message.cast_time + 2.7,
        )

    for i in range(4):
        _draw(p1, i)
        _draw(p2, i)


@pCs.on_cast(33597)
def on_cast_caloric_theory(evt: NetworkMessage[zone_server.ActorCast]):
    raid_utils.draw_share(radius=4, pos=raid_utils.NActor.by_id(evt.message.target_id), duration=evt.message.cast_time)


@pCs.on_add_status(3590)
def on_add_status_pyrefaction(evt: 'ActorControlMessage[actor_control.AddStatus]'):
    actor = raid_utils.NActor.by_id(evt.source_id)
    if not raid_utils.assert_status(actor, 3590, 5): return
    raid_utils.draw_share(radius=4, pos=actor, duration=5)
    raid_utils.draw_circle(radius=4, pos=actor, duration=5)


@pCs.on_add_status(3591)
def on_add_status_atmosfaction(evt: 'ActorControlMessage[actor_control.AddStatus]'):  # 33595
    actor = raid_utils.NActor.by_id(evt.source_id)
    if not raid_utils.assert_status(actor, 3591, 5): return
    raid_utils.draw_circle(radius=7, pos=actor, duration=5)


def play_boa(x, y, z, r, cast_time, dif, dis, rad, times, show_time=4):
    raid_utils.sleep(dif + cast_time - show_time)
    for i in range(1, times):
        x += math.sin(r) * dis
        z += math.cos(r) * dis
        raid_utils.draw_circle(
            radius=rad,
            pos=glm.vec3(x, y, z),
            duration=show_time,
        )
        raid_utils.sleep(dif)


@raid_utils.new_thread
@raid_utils.delay_call_once(1)
def _draw_ekpyrosis_circle(_):  # 33570
    raid_utils.sleep(4)
    for a in raid_utils.iter_main_party():
        raid_utils.draw_circle(radius=6, pos=a, duration=5)


@pCs.on_cast(33567)
def on_cast_ekpyrosis(evt: NetworkMessage[zone_server.ActorCast]):
    _draw_ekpyrosis_circle()
    play_boa(*evt.message.pos, evt.message.facing, evt.message.cast_time, 2, 8, 6, 5)


@pCs.on_set_channel(1)
def on_tether_ekpyrosis(evt: 'ActorControlMessage[actor_control.SetChanneling]'):  # 33608
    source_actor = raid_utils.NActor.by_id(evt.source_id)
    target_actor = raid_utils.NActor.by_id(evt.param.target_id)
    if source_actor.base_id != 0x3f36: return
    raid_utils.draw_rect(
        width=6, length=20,
        pos=source_actor,
        facing=lambda _: target_actor.target_radian(source_actor),
        duration=8,
    )


the_classical_concepts = TheClassicalConcepts()
palladian_grasp = PalladianGrasp()
