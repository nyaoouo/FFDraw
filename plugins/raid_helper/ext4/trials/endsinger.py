import time

from raid_helper import utils as raid_utils
from raid_helper.utils.typing import *
from raid_helper.data import special_actions

special_actions[28668] = raid_utils.fan_shape(180)
special_actions[28678] = raid_utils.fan_shape(180)
special_actions[28682] = raid_utils.donut_shape(5, 15)
special_actions[28691] = raid_utils.donut_shape(5, 15)

# 因为会接管提前绘制，所以不画这里
special_actions[28700] = 0  # 音游？
special_actions[28696] = 0  # 钢铁2s
special_actions[28698] = 0  # 分摊2s
special_actions[28695] = 0  # 月环2s
special_actions[28697] = 0  # 扩散2s


class Timer:
    def __init__(self):
        self.now = time.time()

    def get(self):
        current = time.time()
        delta = current - self.now
        self.now = current
        return delta


map_ex = raid_utils.MapTrigger.get(998)
is_enable = map_ex.add_value(raid_utils.BoolCheckBox('default/enable', True))
map_ex.decorators.append(lambda f: (lambda *args, **kwargs: f(*args, **kwargs) if is_enable.value else None))

save_cast = {28668, 28678, 28681, 28682}
cast_stack: dict[int, list] = dict()
cast_timer = Timer()
icon_stack: dict[int, list] = dict()
icon_timer = Timer()


@map_ex.on_cast(28667, 28677)
def on_cast_star_knock(evt: NetworkMessage[zone_server.ActorCast]):
    raid_utils.draw_knock_predict_circle(radius=40, pos=evt.message.pos, duration=evt.message.cast_time, knock_distance=19)


@map_ex.on_cast(28668, 28678, 28681, 28682)
def on_store_save_cast(evt: NetworkMessage[zone_server.ActorCast]):
    # 28668/28678: 分离 fan(20,180°)
    # 28681: 致死腐烂毒素飞散 circle(15)
    # 28682: 疾病激流 donut(15, 5)
    if cast_timer.get() > 10:
        cast_stack.clear()
    actor = raid_utils.NActor.by_id(evt.header.source_id)
    match evt.message.action_id:
        case 28668 | 28678:
            cb = lambda: raid_utils.draw_fan(degree=180, radius=20, pos=actor, facing=evt.message.facing, duration=20)
        case 28681:
            cb = lambda: raid_utils.draw_circle(radius=15, pos=actor, duration=20)
        case 28682:
            cb = lambda: raid_utils.draw_circle(inner_radius=5, radius=15, pos=actor, duration=20)
        case _:
            return
    cast_stack.setdefault(evt.header.source_id, []).append(cb)


@map_ex.on_lockon(328, 318, 322, 327)
def on_store_save_icon(evt: ActorControlMessage[actor_control.SetLockOn]):
    # 328: 28692: 钢铁 circle(10)
    # 318: 28694: 分摊 circle(6)
    # 322: 28691: 月环 donut(15, 5)
    # 327: 28693: 扩散 circle(40/15)
    if icon_timer.get() > 30:
        icon_stack.clear()
    actor = raid_utils.NActor.by_id(evt.source_id)
    match evt.param.lockon_id:
        case 328:
            cb = lambda: raid_utils.draw_circle(radius=10, pos=actor, duration=13)
        case 318:
            cb = lambda: raid_utils.draw_share(radius=6, pos=actor, duration=13)
        case 322:
            cb = lambda: raid_utils.draw_circle(inner_radius=5, radius=15, pos=actor, duration=13)
        case 327:
            cb = lambda: raid_utils.draw_decay(radius=40, pos=actor, duration=13)
        case _:
            return
    icon_stack.setdefault(evt.source_id, []).append(cb)


@map_ex.on_add_status(2056)
def on_call_save_cast(evt: ActorControlMessage[actor_control.AddStatus]):
    raid_utils.timeout_when_cancel(cast_stack[evt.source_id][375 - evt.param.param](), evt.source_id)


@map_ex.on_add_status(2397)
def on_call_save_cast(evt: ActorControlMessage[actor_control.AddStatus]):
    # print(icon_stack)
    icon_stack[evt.source_id][379 - evt.param.param]()


@map_ex.on_set_channel(189, 181)
def tether(evt: ActorControlMessage[actor_control.SetChanneling]) -> None:
    # 28700: 绝望轮唱 circle(15)
    # 连线189是从boss到小鸟，181是小鸟间传递
    duration = 9.1 if evt.param.channel_id == 189 else 8.1
    raid_utils.draw_circle(radius=15, pos=raid_utils.NActor.by_id(evt.source_id), duration=duration)


map_ex.clear_decorators()
