import logging
import math
import threading

import glm

from raid_helper import utils as raid_utils
from raid_helper.utils.typing import *
from raid_helper.data import special_actions, delay_until, omen_color

# light rect 482
# light circle 483
# dark rect 484
# dark circle 485

# 33276 判定 连锁 光 share range 6 # 双奶 4人
# 33277 判定 连锁 暗 share range 3 # d 2人

# 33254 读条 八方 光
# 33255 读条 八方 暗
# 33256 判定 八方 光 rect range 50 width 8
# 33257 判定 八方 暗 rect range 50 width 8
# 33258 二段 八方 光 circle range 5 # 有读条
# 33259 二段 八方 暗 circle range 9 ignore 2 # 有读条

# 34771 读条 点名 光
# 34772 读条 点名 暗
# 33266 判定 点名 光 share range 6
# 33267 判定 点名 暗 circle range 13
# 33270 二段 点名 光 circle range 13 # 有读条
# 33271 二段 点名 暗 circle range 50 ignore 8 # 有读条

# 33260 读条 前后 光
# 33261 读条 前后 暗
# 33262 判定 前后 rect range 46 width 16 # 有读条
# 33263 二段 前后 光 rect range 46 width 26 # 有读条
# 33264 二段 前后 暗 rect range 46 width 16 # 有读条
# 33265 二段 前后 暗 rect range 46 width 16 # 有读条

# 一运
# 34694 判定 圆心击退 光 knock 11 # 有读条
# 34695 判定 圆心击退 暗 knock 11 # 有读条
# 34696 判定 圆心击退 二段 光 circle range 13 # 有读条
# 34697 判定 圆心击退 二段 暗 circle range 50 ignore 8 # 有读条
# 33293 读条 魔法阵1 光
# 33294 读条 魔法阵1 暗
# 33299 判定 魔法阵 光 rect range 50 width 8 # 有读条
# 33300 判定 魔法阵 暗 rect range 50 width 8 # 有读条

# 二运
# 33306 读条 边刀 光
# 33307 读条 边刀 暗
# 33308 判定 边刀 一段 rect range 46 width 16 # 有读条
# 33309 判定 边刀 二段 光 rect range 46 width 26 # 有读条
# 33310 判定 边刀 二段 暗 rect range 46 width 16 # 有读条
# 33311 判定 边刀 二段 暗 rect range 46 width 16 # 有读条
# 34739 读条 中刀 光
# 34740 读条 中刀 暗
# 34741 判定 中刀 一段 rect range 46 width 16 # 有读条
# 34742 判定 中刀 二段 光 rect range 46 width 26 # 有读条
# 34743 判定 中刀 二段 暗 rect range 46 width 16 # 有读条
# 34744 判定 中刀 二段 暗 rect range 46 width 16 # 有读条
# channel 249 点名引导
# 34768 读条 点名 光
# 34769 读条 点名 暗
# 33312 判定 点名 光 share range 6
# 33313 判定 点名 暗 circle range 13
# 33316 二段 点名 光 circle range 13 # 有读条
# 33317 二段 点名 暗 circle range 50 ignore 8 # 有读条

# 转转转
# 33283 读条 转圈
# lockon 156 顺时针
# lockon 157 逆时针
# 33287 判定 激光 rect range 50 width 10 # 有读条
# 33288 判定 激光 后续 rect range 50 width 10

# network_map_effect|100186b8|800375b3|16|32|2 地火
# 33284 读条 地火
# 33289 判定 地火1 circle range 8 # 有读条
# 33290 判定 地火 circle range 8
# 33321 读条 分散
# 33322 判定 分散 circle range 6

# 33297 读条 魔法阵3 光
# 33298 读条 魔法阵3 暗
# 33301 判定 魔法阵3 球 光 circle range 15 # 有读条
# 33302 判定 魔法阵3 球 暗 circle range 15 # 有读条

special_actions[33259] = raid_utils.donut_shape(2, 9)
special_actions[33271] = raid_utils.donut_shape(8, 50)
special_actions[34697] = raid_utils.donut_shape(8, 50)
special_actions[33317] = raid_utils.donut_shape(8, 50)
special_actions[34694] = 0
special_actions[34695] = 0
delay_until[33263] = 8
delay_until[33264] = 8
delay_until[33265] = 8
delay_until[33309] = 8
delay_until[33310] = 8
delay_until[33311] = 8
delay_until[34742] = 8
delay_until[34743] = 8
delay_until[34744] = 8

dark_violet_surface = glm.vec4(0.58, 0.0, 0.83, .2)
dark_violet_line = dark_violet_surface + glm.vec4(-.05, 0, -.05, .5)
pale_goldenrod_surface = glm.vec4(0.93, 0.91, 0.66, .2)
pale_goldenrod_line = pale_goldenrod_surface + glm.vec4(.05, .05, .05, .5)

_light_actions = [33258, 33263, 34696, 33309, 34742, 33316]
_dark_actions = [33259, 33271, 33264, 33265, 34697, 33310, 33311, 34743, 34744, 33317]

for _a in _light_actions:
    omen_color[_a] = pale_goldenrod_surface, pale_goldenrod_line

for _a in _dark_actions:
    omen_color[_a] = dark_violet_surface, dark_violet_line

pBs = raid_utils.MapTrigger(1152)
center = glm.vec3(100, 0, 100)
logger = logging.getLogger('raid_helper/pBs')

is_enable = pBs.add_value(raid_utils.BoolCheckBox('default/enable', True))
pBs.decorators.append(lambda f: (lambda *args, **kwargs: f(*args, **kwargs) if is_enable.value else None))

light_surface = pBs.add_value(raid_utils.Color4f('default/light_surface', pale_goldenrod_surface))
dark_surface = pBs.add_value(raid_utils.Color4f('default/dark_surface', dark_violet_surface))
light_line = pBs.add_value(raid_utils.Color4f('default/light_line', pale_goldenrod_line))
dark_line = pBs.add_value(raid_utils.Color4f('default/dark_line', dark_violet_line))


@light_surface.listen_change
def on_light_surface_change(value):
    for _a in _light_actions:
        omen_color[_a] = value, light_line.value


@light_line.listen_change
def on_light_line_change(value):
    for _a in _light_actions:
        omen_color[_a] = light_surface.value, value


@dark_surface.listen_change
def on_dark_surface_change(value):
    for _a in _dark_actions:
        omen_color[_a] = value, dark_line.value


@dark_line.listen_change
def on_dark_line_change(value):
    for _a in _dark_actions:
        omen_color[_a] = dark_surface.value, value


class CallOnce:
    def __init__(self, func):
        self.lock = threading.Lock()
        self.func = func

    def _run(self, *args, **kwargs):
        try:
            self.func(*args, **kwargs)
        finally:
            self.lock.release()

    def __call__(self, *args, **kwargs):
        if self.lock.acquire(False):
            threading.Thread(target=self._run, args=args, kwargs=kwargs).start()


@pBs.on_cast(33258, 33270, 33263, 34696, 34742)
@CallOnce
def on_cast_light_combo(evt: 'NetworkMessage[zone_server.ActorCast]'):
    raid_utils.sleep(evt.message.cast_time - 4)
    cast_time = min(evt.message.cast_time, 4)
    for actor in raid_utils.iter_main_party(False):
        if raid_utils.is_class_job_healer(actor.class_job):
            raid_utils.draw_share(radius=6, pos=actor, duration=cast_time, line_color=light_line.value, surface_color=light_surface.value)
            raid_utils.draw_circle(radius=6, pos=actor, duration=cast_time, line_color=light_line.value, surface_color=light_surface.value)


@pBs.on_cast(33259, 33271, 33264, 34697, 34743)
@CallOnce
def on_cast_dark_combo(evt: 'NetworkMessage[zone_server.ActorCast]'):
    raid_utils.sleep(evt.message.cast_time - 4)
    cast_time = min(evt.message.cast_time, 4)
    for actor in raid_utils.iter_main_party(False):
        if raid_utils.is_class_job_dps(actor.class_job):
            raid_utils.draw_share(radius=3, pos=actor, duration=cast_time, line_color=dark_line.value, surface_color=dark_surface.value)
            raid_utils.draw_circle(radius=3, pos=actor, duration=cast_time, line_color=dark_line.value, surface_color=dark_surface.value)


@pBs.on_cast(33254, 33255)
def on_cast_jury_overruling(evt: 'NetworkMessage[zone_server.ActorCast]'):
    colors = (light_surface.value, light_line.value) if evt.message.action_id == 33254 else (dark_surface.value, dark_line.value)
    source = raid_utils.NActor.by_id(evt.header.source_id)

    def _draw(actor: raid_utils.NActor):
        return raid_utils.draw_rect(
            width=8, length=50,
            pos=source,
            facing=lambda _: glm.polar(actor.update().pos - source.update().pos).y,
            duration=evt.message.cast_time,
            line_color=colors[1],
            surface_color=colors[0]
        )

    for a in raid_utils.iter_main_party(False):
        _draw(a)


@pBs.on_set_channel(249)
@pBs.on_cast(34771, 34772, 34768, 34769)
@raid_utils.delay_call_once(1)
def on_cast_upheld_ruling(data: 'list[NetworkMessage[zone_server.ActorCast]|ActorControlMessage[actor_control.SetChanneling]]'):
    channel_data = {}
    cast_data = {}
    cast_time = 0
    for evt, in data:
        if isinstance(evt, ActorControlMessage):
            evt: 'ActorControlMessage[actor_control.SetChanneling]'
            channel_data[evt.source_id] = evt.param.target_id
            logger.debug(f'channel {evt.source_id=:x} {evt.param.target_id=:x}')
        else:
            evt: 'NetworkMessage[zone_server.ActorCast]'
            cast_data[evt.header.source_id] = evt.message.action_id
            cast_time = evt.message.cast_time - 1
            logger.debug(f'cast {evt.header.source_id=:x} {evt.message.action_id=}')
    for source_id, target_id in channel_data.items():
        if not (cast_id := cast_data.get(source_id)):
            print(f'upheld_ruling: no cast data for {source_id:x}')
            continue
        target = raid_utils.NActor.by_id(target_id)
        if cast_id == 34771 or cast_id == 34768:  # light
            raid_utils.draw_circle(radius=6, pos=target, duration=cast_time, line_color=light_line.value, surface_color=light_surface.value)
            raid_utils.draw_share(radius=6, pos=target, duration=cast_time, line_color=light_line.value, surface_color=light_surface.value)
        elif cast_id == 34772 or cast_id == 34769:  # dark
            raid_utils.draw_circle(radius=13, pos=target, duration=cast_time, line_color=dark_line.value, surface_color=dark_surface.value)


@pBs.on_cast(34694, 34695)
def on_cast_dismissal_overruling(evt: 'NetworkMessage[zone_server.ActorCast]'):
    raid_utils.draw_knock_predict_circle(radius=11, pos=raid_utils.NActor.by_id(evt.header.source_id), duration=evt.message.cast_time, knock_distance=11)


upheld_ruling_rad = math.radians(10)


@pBs.on_lockon(156, 157)
def on_lockon_upheld_ruling(evt: 'ActorControlMessage[actor_control.SetLockOn]'):
    a_pos = raid_utils.NActor.by_id(evt.source_id).pos
    r = glm.polar(center - a_pos).y
    d_r = -upheld_ruling_rad if evt.param.lockon_id == 156 else upheld_ruling_rad
    for i in range(1, 6):
        raid_utils.draw_rect(
            width=10, length=50,
            pos=a_pos, facing=r + d_r * i,
            duration=7.7 + 1.1 * i,
        )


@pBs.on_map_effect
def on_dark_current(evt: 'NetworkMessage[zone_server.MapEffect]'):
    if evt.message.index == 2:
        start_rad = math.radians(90)
    elif evt.message.index == 1:
        start_rad = 0
    else:
        return
    if evt.message.state == 16:
        delta_rad = math.radians(-22.5)
    elif evt.message.state == 1:
        delta_rad = math.radians(22.5)
    else:
        return
    raid_utils.draw_circle(radius=8, pos=center, duration=14.7)
    raid_utils.sleep(7.7 + 1 - 4)
    for i in range(1, 8):
        rad = start_rad + delta_rad * i
        raid_utils.draw_circle(radius=8, pos=glm.vec3(math.sin(rad), 0, -math.cos(rad)) * 13 + center, duration=4)
        rad += math.pi
        raid_utils.draw_circle(radius=8, pos=glm.vec3(math.sin(rad), 0, -math.cos(rad)) * 13 + center, duration=4)
        raid_utils.sleep(1)


pBs.clear_decorators()
