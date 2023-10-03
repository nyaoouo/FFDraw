import glm

from raid_helper import utils as raid_utils
from raid_helper.utils.typing import *
from raid_helper.data import special_actions, delay_until

special_actions[34523] = raid_utils.fan_shape(180)
special_actions[34535] = raid_utils.fan_shape(180)
special_actions[34541] = raid_utils.donut_shape(6, 22)
special_actions[34543] = raid_utils.fan_shape(180)
special_actions[34546] = raid_utils.fan_shape(180)

delay_until[34546] = 4
delay_until[34540] = 4
delay_until[34541] = 4
delay_until[34543] = 4
delay_until[33880] = 4
delay_until[33881] = 4
delay_until[33882] = 4
delay_until[33883] = 4

map_ex = raid_utils.MapTrigger.get(1141)

is_enable = map_ex.add_value(raid_utils.BoolCheckBox('default/enable', True))
map_ex.decorators.append(lambda f: (lambda *args, **kwargs: f(*args, **kwargs) if is_enable.value else None))


@map_ex.on_set_channel(17)
def on_cauterize(msg: ActorControlMessage[actor_control.SetChanneling]):
    source_actor = raid_utils.NActor.by_id(msg.source_id)
    target_actor = raid_utils.NActor.by_id(msg.param.target_id)
    raid_utils.timeout_when_channeling_change(
        raid_utils.draw_rect(width=12, length=50, pos=source_actor, facing=lambda _: glm.polar(target_actor.update().pos - source_actor.update().pos).y, duration=20),
        msg.source_id, msg.param.target_id, msg.param.idx
    )


@map_ex.on_lockon(0x1da)
def on_dragons_descent_lockon(msg: ActorControlMessage[actor_control.SetLockOn]):
    if raid_utils.is_me_id(msg.source_id): return
    source_actor = raid_utils.NActor.by_id(msg.source_id)
    raid_utils.draw_knock_predict_circle(
        radius=45,
        pos=lambda: source_actor.update().pos,
        duration=8.5,
        knock_distance=12
    )


map_ex.clear_decorators()
