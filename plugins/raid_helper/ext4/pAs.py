import logging
import math

import glm

from raid_helper import utils as raid_utils
from raid_helper.utils.typing import *
from raid_helper.data import special_actions

special_actions[33430] = raid_utils.fan_shape(20)
special_actions[33415] = raid_utils.donut_shape(3, 8)
special_actions[33447] = raid_utils.donut_shape(12, 40)

pAs = raid_utils.MapTrigger(1150)

center = glm.vec3(100, 0, 100)

logger = logging.getLogger('raid_helper/pAs')

is_enable = pAs.add_value(raid_utils.BoolCheckBox('default/enable', True))
pAs.decorators.append(lambda f: (lambda *args, **kwargs: f(*args, **kwargs) if is_enable.value else None))


@pAs.on_set_channel(242)
def on_tether_dividing_wings(evt: 'ActorControlMessage[actor_control.SetChanneling]'):
    source_actor = raid_utils.NActor.by_id(evt.source_id)
    target_actor = raid_utils.NActor.by_id(evt.param.target_id)
    raid_utils.timeout_when_channeling_change(raid_utils.draw_fan(
        degree=120, radius=60, pos=source_actor,
        facing=lambda _: source_actor.target_radian(target_actor),
        duration=20,
    ), evt)


@pAs.on_cast(33434, 33435)
def on_cast_wicked_step(evt: 'NetworkMessage[zone_server.ActorCast]'):
    raid_utils.draw_knock_predict_circle(radius=4, pos=evt.message.pos, knock_distance=36, duration=evt.message.cast_time)


@pAs.on_add_status(3550)
def on_add_status_daemoniac_bonds(evt: 'ActorControlMessage[actor_control.AddStatus]'):
    actor = raid_utils.NActor.by_id(evt.source_id)
    if not raid_utils.assert_status(actor, 3550, 5.5): return
    remain = actor.status.find_status_remain(3550)
    raid_utils.draw_circle(radius=6, pos=actor, duration=remain)


@pAs.on_add_status(3551)
def on_add_status_duodaemoniac_bonds(evt: 'ActorControlMessage[actor_control.AddStatus]'):
    actor = raid_utils.NActor.by_id(evt.source_id)
    if not raid_utils.assert_status(actor, 3551, 5.5): return
    remain = actor.status.find_status_remain(3551)
    raid_utils.draw_share(radius=4, pos=actor, duration=remain)
    raid_utils.draw_circle(radius=4, pos=actor, duration=remain)


@pAs.on_add_status(3696)
def on_add_status_tetradaemoniac_bonds(evt: 'ActorControlMessage[actor_control.AddStatus]'):
    actor = raid_utils.NActor.by_id(evt.source_id)
    if not raid_utils.assert_status(actor, 3696, 5.5): return
    remain = actor.status.find_status_remain(3696)
    raid_utils.draw_share(radius=4, pos=actor, duration=remain)
    raid_utils.draw_circle(radius=4, pos=actor, duration=remain)


@pAs.on_lockon(0x17)
def on_lockon_pandaemoniac_meltdown_lazer(evt: 'ActorControlMessage[actor_control.SetLockOn]'):
    pandaemonium = next(raid_utils.find_actor_by_base_id(0x3f1d))
    target = raid_utils.NActor.by_id(evt.source_id)
    raid_utils.draw_rect(
        length=50, width=4, pos=pandaemonium,
        facing=lambda _: pandaemonium.target_radian(target),
        duration=5.7,
    )


@pAs.on_effect(26708)
def on_prepare_pandaemoniac_meltdown_share(evt: 'NetworkMessage[zone_server.ActionEffect]'):
    pandaemonium = next(raid_utils.find_actor_by_base_id(0x3f1d))
    target = raid_utils.NActor.by_id(evt.message.target_ids[0])
    raid_utils.draw_rect(
        length=50, width=4, pos=pandaemonium,
        facing=lambda _: pandaemonium.target_radian(target),
        duration=5.7,
    )


@pAs.on_add_status(2397)
def on_cast_peal_of_condemnation(evt: 'ActorControlMessage[actor_control.AddStatus]'):
    if evt.param.param != 601: return
    source_actor = raid_utils.NActor.by_id(evt.source_id)
    raid_utils.draw_rect(
        length=50, width=5, pos=source_actor,
        facing=lambda _: source_actor.target_radian(raid_utils.get_actor_by_dis(source_actor, 0)),
        duration=5.7,
    )


@pAs.on_npc_spawn(0x3f22)
def on_arcane_sphere(evt: 'NetworkMessage[zone_server.NpcSpawn]'):
    pos = evt.message.create_common.pos
    raid_utils.draw_rect(
        width=2, length=80, arg=1,
        pos=pos,
        facing=math.pi / 2,
        duration=3.5
    )


pAs.clear_decorators()
