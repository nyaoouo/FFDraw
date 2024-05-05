import math

from raid_helper import utils as raid_utils
from raid_helper.utils.typing import *
from raid_helper.data import special_actions, delay_until

special_actions[35623] = 0  # [1168]The Abyssal Fracture - The Abyssal Fracture:
special_actions[35624] = 0  # [1168]The Abyssal Fracture - The Abyssal Fracture:
special_actions[35625] = 0  # [1168]The Abyssal Fracture - The Abyssal Fracture:
special_actions[35626] = 0  # [1168]The Abyssal Fracture - The Abyssal Fracture:
special_actions[35627] = 0  # [1168]The Abyssal Fracture - The Abyssal Fracture:
special_actions[35628] = raid_utils.fan_shape(40)  # [1168]The Abyssal Fracture - The Abyssal Fracture: Chasmic Nails
special_actions[35629] = raid_utils.fan_shape(40)  # [1168]The Abyssal Fracture - The Abyssal Fracture: Chasmic Nails
special_actions[35630] = raid_utils.fan_shape(40)  # [1168]The Abyssal Fracture - The Abyssal Fracture: Chasmic Nails
special_actions[35631] = raid_utils.fan_shape(40)  # [1168]The Abyssal Fracture - The Abyssal Fracture: Chasmic Nails
special_actions[35632] = raid_utils.fan_shape(40)  # [1168]The Abyssal Fracture - The Abyssal Fracture: Chasmic Nails
special_actions[35623] = 0  # [1169]The Abyssal Fracture - The Abyssal Fracture (Extreme):
special_actions[35624] = 0  # [1169]The Abyssal Fracture - The Abyssal Fracture (Extreme):
special_actions[35625] = 0  # [1169]The Abyssal Fracture - The Abyssal Fracture (Extreme):
special_actions[35626] = 0  # [1169]The Abyssal Fracture - The Abyssal Fracture (Extreme):
special_actions[35627] = 0  # [1169]The Abyssal Fracture - The Abyssal Fracture (Extreme):
special_actions[35705] = raid_utils.fan_shape(40)  # [1169]The Abyssal Fracture - The Abyssal Fracture (Extreme): Chasmic Nails
special_actions[35706] = raid_utils.fan_shape(40)  # [1169]The Abyssal Fracture - The Abyssal Fracture (Extreme): Chasmic Nails
special_actions[35707] = raid_utils.fan_shape(40)  # [1169]The Abyssal Fracture - The Abyssal Fracture (Extreme): Chasmic Nails
special_actions[35708] = raid_utils.fan_shape(40)  # [1169]The Abyssal Fracture - The Abyssal Fracture (Extreme): Chasmic Nails
special_actions[35709] = raid_utils.fan_shape(40)  # [1169]The Abyssal Fracture - The Abyssal Fracture (Extreme): Chasmic Nails

special_actions[35676] = 0  # 陨石护眼
special_actions[35710] = 0  # 地面小AOE护眼 #我觉得这个是不必要的绘制
special_actions[35662] = 0  # 地面小AOE护眼 #我觉得这个是不必要的绘制
special_actions[36415] = 0  # 地面小AOE护眼 #我觉得这个是不必要的绘制
special_actions[36416] = 0  # 地面小AOE护眼 #我觉得这个是不必要的绘制


delay_until[35650] = 8

delay_until[35699] = 5
delay_until[35698] = 1
delay_until[35697] = 1
delay_until[35696] = 1
delay_until[35695] = 1
delay_until[35694] = 1
delay_until[35693] = 1
delay_until[35628] = 4
delay_until[35629] = 4
delay_until[35630] = 4
delay_until[35631] = 4
delay_until[35632] = 4
delay_until[35705] = 4
delay_until[35706] = 4
delay_until[35707] = 4
delay_until[35708] = 4
delay_until[35709] = 4

map_ex = raid_utils.MapTrigger.get(1169)

is_enable = map_ex.add_value(raid_utils.BoolCheckBox('default/enable', True))
map_ex.decorators.append(lambda f: (lambda *args, **kwargs: f(*args, **kwargs) if is_enable.value else None))


@map_ex.on_add_status(3799)
def on_status_forked_lightning(evt: ActorControlMessage[actor_control.AddStatus]):
    # 倒计时完成后触发闪电
    actor = raid_utils.NActor.by_id(evt.source_id)
    if not raid_utils.assert_status(actor, evt.param.status_id, 6): return
    remain = actor.status.find_status_remain(evt.param.status_id)


@map_ex.on_add_status(3762)
def on_status_divisive_dark(evt: ActorControlMessage[actor_control.AddStatus]):
    # 倒计时完成后触发需要分散的aoe
    actor = raid_utils.NActor.by_id(evt.source_id)
    if not raid_utils.assert_status(actor, evt.param.status_id, 6): return
    remain = actor.status.find_status_remain(evt.param.status_id)
    raid_utils.draw_circle(radius=5, pos=actor, duration=remain)


@map_ex.on_add_status(3794)
def on_status_beckoning_dark(evt: ActorControlMessage[actor_control.AddStatus]):
    # 倒计时完成后触发需要44分摊的aoe
    actor = raid_utils.NActor.by_id(evt.source_id)
    if not raid_utils.assert_status(actor, evt.param.status_id, 6): return
    remain = actor.status.find_status_remain(evt.param.status_id)
    raid_utils.draw_share(radius=5, pos=actor, duration=remain)


@map_ex.on_cast(35646)
def on_cast_fractured_eventide(evt: NetworkMessage[zone_server.ActorCast]):
    facing = evt.message.facing
    if facing > 0:
        facing -= math.pi / 2
    else:
        facing += math.pi / 2
    raid_utils.draw_fan(
        degree=180, radius=60,
        pos=evt.message.pos,
        facing=facing,
        duration=evt.message.cast_time,
    )

@map_ex.on_lockon(197)
def on_lockon_dualfire(msg: ActorControlMessage[actor_control.SetLockOn]):

    raid_utils.sleep(6.7)
    actor = raid_utils.NActor.by_id(msg.source_id)
    for i in range(5):
        raid_utils.draw_circle(radius=10, pos=actor.pos, duration=5)
        raid_utils.sleep(1)





map_ex.clear_decorators()
