from ff_draw.omen import BaseOmen, Line
from nylib.utils import safe_lazy
from nylib.utils.win32.exception import WinAPIError
from .trigger import new_thread
from .typing import *
from .logic import *

main = FFDraw.instance


def default_color(is_enemy=True):
    if is_enemy:
        return 'enemy'
    else:
        return 'friend'


def pos_tracker(actor: Actor):
    if not isinstance(actor, NActor): actor = NActor(actor)
    return lambda o: safe_lazy(lambda: actor.update().pos, _default=o.timeout)


def facing_tracker(actor: Actor):
    if not isinstance(actor, NActor): actor = NActor(actor)
    return lambda o: safe_lazy(lambda: actor.update().facing, _default=o.timeout)


def draw_share(
        radius: typing.Callable[[BaseOmen], int] | int,
        pos: typing.Callable[[BaseOmen], glm.vec3] | glm.vec3 | Actor,
        facing: typing.Callable[[BaseOmen], float] | float | Actor = 0,
        color: typing.Callable[[BaseOmen], glm.vec4 | str] | glm.vec4 | str = None,
        surface_color: typing.Callable[[BaseOmen], glm.vec4 | str] | glm.vec4 | str = None,
        line_color: typing.Callable[[BaseOmen], glm.vec4 | str] | glm.vec4 | str = None,
        label: typing.Callable[[BaseOmen], str] | str = '',
        label_color: typing.Callable[[BaseOmen], tuple[float, float, float,]] | tuple[float, float, float,] = None,
        duration: float = 0,
        alpha: typing.Callable[[BaseOmen], float] | float = None,
):
    if isinstance(pos, Actor):
        pos = pos_tracker(pos)
    if isinstance(facing, Actor):
        facing = facing_tracker(facing)

    def play(f):
        def get_shape(o: BaseOmen):
            _radius = o.get_maybe_callable(radius)
            fac = o.get_maybe_callable(facing) + f
            dis = _radius * ((1 - (time.time() - o.start_at) % 1) * .4 + .8)
            o._pos = o.get_maybe_callable(pos) + glm.vec3(math.cos(fac) * dis, 2, -math.sin(fac) * dis)
            o._facing = fac - math.pi / 2
            o._scale = glm.vec3(_radius / 5, 1, _radius / 5)
            return 0x1010000

        return create_game_omen(
            pos=pos,
            shape=get_shape,
            facing=facing,
            scale=glm.vec3(1, 1, 1),
            surface_color=surface_color, line_color=line_color, color=color,
            duration=duration,
            alpha=alpha,
        )

    return [
        draw_circle(
            radius=radius, pos=lambda o: o.get_maybe_callable(pos) + glm.vec3(0, 2, 0),
            line_color=color or line_color or default_color(True),
            label=label, label_color=label_color,
            duration=duration, alpha=alpha
        ),
        *(play(i * math.pi / 2) for i in range(4))
    ]


def draw_circle(
        radius: typing.Callable[[BaseOmen], int] | int,
        pos: typing.Callable[[BaseOmen], glm.vec3] | glm.vec3 | Actor,
        color: typing.Callable[[BaseOmen], glm.vec4 | str] | glm.vec4 | str = None,
        surface_color: typing.Callable[[BaseOmen], glm.vec4 | str] | glm.vec4 | str = None,
        line_color: typing.Callable[[BaseOmen], glm.vec4 | str] | glm.vec4 | str = None,
        label: typing.Callable[[BaseOmen], str] | str = '',
        label_color: typing.Callable[[BaseOmen], tuple[float, float, float,]] | tuple[float, float, float,] = None,
        duration: float = 0,
        inner_radius: typing.Callable[[BaseOmen], int] | int = 0,
        alpha: typing.Callable[[BaseOmen], float] | float = None,
):
    if isinstance(radius, int):
        scale = glm.vec3(radius, 1, radius)
    else:
        def scale(o: BaseOmen):
            r = o.get_maybe_callable(radius)
            return glm.vec3(r, 1, r)
    if isinstance(radius, int) and isinstance(inner_radius, int):
        shape = 0x10000 | int(inner_radius / radius * 0xffff)
    else:
        def shape(o: BaseOmen):
            return 0x10000 | int(o.get_maybe_callable(inner_radius) / o.get_maybe_callable(radius) * 0xffff)

    return create_game_omen(
        pos=pos,
        shape=shape,
        scale=scale,
        surface_color=surface_color, line_color=line_color, color=color,
        label=label, label_color=label_color,
        duration=duration,
        alpha=alpha,
    )


def draw_rect(
        width: typing.Callable[[BaseOmen], int] | int,
        length: typing.Callable[[BaseOmen], int] | int,
        pos: typing.Callable[[BaseOmen], glm.vec3] | glm.vec3 | Actor,
        facing: typing.Callable[[BaseOmen], float] | float | Actor = None,
        color: typing.Callable[[BaseOmen], glm.vec4 | str] | glm.vec4 | str = None,
        surface_color: typing.Callable[[BaseOmen], glm.vec4 | str] | glm.vec4 | str = None,
        line_color: typing.Callable[[BaseOmen], glm.vec4 | str] | glm.vec4 | str = None,
        label: typing.Callable[[BaseOmen], str] | str = '',
        label_color: typing.Callable[[BaseOmen], tuple[float, float, float,]] | tuple[float, float, float,] = None,
        duration: float = 0,
        arg=0,  # 0:normal, 1:include back, 2:cross
        alpha: typing.Callable[[BaseOmen], float] | float = None,
):
    if isinstance(width, int) and isinstance(length, int):
        scale = glm.vec3(width, 1, length)
    else:
        def scale(o: BaseOmen):
            return glm.vec3(o.get_maybe_callable(width), 1, o.get_maybe_callable(length))
    return create_game_omen(
        pos=pos,
        shape=0x20000 | arg,
        scale=scale,
        facing=facing,
        surface_color=surface_color, line_color=line_color, color=color,
        label=label, label_color=label_color,
        duration=duration,
        alpha=alpha,
    )


def draw_fan(
        degree: typing.Callable[[BaseOmen], int] | int,
        radius: typing.Callable[[BaseOmen], int] | int,
        pos: typing.Callable[[BaseOmen], glm.vec3] | glm.vec3 | Actor,
        facing: typing.Callable[[BaseOmen], float] | float | Actor = None,
        color: typing.Callable[[BaseOmen], glm.vec4 | str] | glm.vec4 | str = None,
        surface_color: typing.Callable[[BaseOmen], glm.vec4 | str] | glm.vec4 | str = None,
        line_color: typing.Callable[[BaseOmen], glm.vec4 | str] | glm.vec4 | str = None,
        label: typing.Callable[[BaseOmen], str] | str = '',
        label_color: typing.Callable[[BaseOmen], tuple[float, float, float,]] | tuple[float, float, float,] = None,
        duration: float = 0,
        alpha: typing.Callable[[BaseOmen], float] | float = None,
):
    if isinstance(radius, int):
        scale = glm.vec3(radius, 1, radius)
    else:
        def scale(o: BaseOmen):
            r = o.get_maybe_callable(radius)
            return glm.vec3(r, 1, r)

    if isinstance(degree, int):
        shape = 0x50000 | degree
    else:
        def shape(o: BaseOmen):
            return 0x50000 | o.get_maybe_callable(degree)

    return create_game_omen(
        pos=pos,
        shape=shape,
        scale=scale,
        facing=facing,
        surface_color=surface_color, line_color=line_color, color=color,
        label=label, label_color=label_color,
        duration=duration,
        alpha=alpha,
    )


def linear_trans(start_s, start_p, end_s, end_p, remain):
    return max(min((start_s - remain) / (start_s - end_s), 1), 0) * (end_p - start_p) + start_p


def create_game_omen(
        shape: typing.Callable[[BaseOmen], int] | int,
        scale: typing.Callable[[BaseOmen], glm.vec3] | glm.vec3,
        pos: typing.Callable[[BaseOmen], glm.vec3] | glm.vec3 | Actor,
        facing: typing.Callable[[BaseOmen], float] | float | Actor = None,
        color: typing.Callable[[BaseOmen], glm.vec4 | str] | glm.vec4 | str = None,
        surface_color: typing.Callable[[BaseOmen], glm.vec4 | str] | glm.vec4 | str = None,
        line_color: typing.Callable[[BaseOmen], glm.vec4 | str] | glm.vec4 | str = None,
        label: typing.Callable[[BaseOmen], str] | str = '',
        label_color: typing.Callable[[BaseOmen], tuple[float, float, float,]] | tuple[float, float, float,] = None,
        duration: float = 0,
        alpha: typing.Callable[[BaseOmen], float] | float = None,
):
    if surface_color is None and line_color is None and color is None:
        color = default_color(True)
    if isinstance(pos, Actor):
        if facing is None:
            facing = facing_tracker(pos)
        pos = pos_tracker(pos)
    elif facing is None:
        facing = 0
    return BaseOmen(
        main=main,
        pos=pos,
        shape=shape,
        scale=scale,
        facing=facing,
        surface_color=surface_color, line_color=line_color, surface_line_color=color,
        label=label, label_color=label_color,
        duration=duration,
        alpha=alpha
    )


def draw_line(
        source: Actor | glm.vec3 | typing.Callable[[BaseOmen], glm.vec3],
        target: Actor | glm.vec3 | typing.Callable[[BaseOmen], glm.vec3],
        color: glm.vec4,
        width: int = 3,
        duration=0
):
    if isinstance(source, Actor):
        source = pos_tracker(source)
    if isinstance(target, Actor):
        target = pos_tracker(target)
    return Line(
        main=main,
        src=source,
        dst=target,
        line_color=color,
        line_width=width,
        duration=duration
    )


def timeout_when_cancel(omen: BaseOmen, actor: Actor | int):
    if isinstance(actor, Actor): actor = actor.id

    on_net_msg = lambda m: remove(m.header.source_id)
    on_ac_msg = lambda m: remove(m.source_id)

    def remove(check_id=None):
        if check_id is not None and check_id != actor: return
        main.sniffer.on_action_effect.remove(on_net_msg)
        main.sniffer.on_zone_server_message[ZoneServer.ActorCast].remove(on_net_msg)
        main.sniffer.on_actor_control[ActorControlId.CancelCast].remove(on_ac_msg)
        omen.timeout()

    @new_thread
    def install():
        with main.sniffer.ipc_lock:
            main.sniffer.on_action_effect.append(on_net_msg)
            main.sniffer.on_zone_server_message[ZoneServer.ActorCast].append(on_net_msg)
            main.sniffer.on_actor_control[ActorControlId.CancelCast].append(on_ac_msg)

            old_shape = omen._shape
            omen._shape = lambda o: o.get_maybe_callable(old_shape) if main.mem.actor_table.get_actor_by_id(actor) else o.timeout()
            old_destroy = omen.destroy
            omen.destroy = lambda: (remove(), old_destroy())

    install()
    return omen


def timeout_when_channeling_change(omen: BaseOmen, source_id, target_id, idx=0):
    def on_channeling(msg: ActorControlMessage[actor_control.SetChanneling | actor_control.RemoveChanneling]):
        if msg.source_id == source_id and msg.param.idx == idx: remove()

    def remove():
        main.sniffer.on_actor_control[ActorControlId.SetChanneling].remove(on_channeling)
        main.sniffer.on_actor_control[ActorControlId.RemoveChanneling].remove(on_channeling)
        omen.timeout()

    @new_thread
    def install():
        with main.sniffer.ipc_lock:
            main.sniffer.on_actor_control[ActorControlId.SetChanneling].append(on_channeling)
            main.sniffer.on_actor_control[ActorControlId.RemoveChanneling].append(on_channeling)
            get_actor_by_id = main.mem.actor_table.get_actor_by_id

            old_shape = omen._shape
            omen._shape = lambda o: o.get_maybe_callable(old_shape) if get_actor_by_id(source_id) and get_actor_by_id(target_id) else o.timeout()
            old_destroy = omen.destroy
            omen.destroy = lambda: (remove(), old_destroy())

    install()
    return omen

