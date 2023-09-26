import functools
import math

import glm
import imgui
from ff_draw.gui.text import TextPosition
from ff_draw.mem.actor import Actor
from ff_draw.plugins import FFDrawPlugin
from .models import HitBox, TargetLine


def safe_cached_property(func, default=None):
    @functools.cached_property
    def wrapper(self):
        try:
            return func(self)
        except:
            return default

    return wrapper


class CActor:
    def __init__(self, actor: Actor):
        self._actor = actor

    id = safe_cached_property((lambda self: self._actor.id), 0)
    name = safe_cached_property((lambda self: self._actor.name), '')
    pos = safe_cached_property((lambda self: self._actor.pos), glm.vec3(0, 0, 0))
    facing = safe_cached_property((lambda self: self._actor.facing), 0)
    radius = safe_cached_property((lambda self: self._actor.radius), 0)
    actor_type = safe_cached_property((lambda self: self._actor.actor_type), 0)
    target_id = safe_cached_property((lambda self: self._actor.target_id), 0xe0000000)
    can_select = safe_cached_property((lambda self: self._actor.can_select), False)


y_axis = glm.vec3(0, 1, 0)
x_axis = glm.vec3(1, 0, 0)


def line_trans(start, end):
    distance = glm.distance(start, end)
    return glm.translate(start) * glm.rotate(glm.polar(end - start).y, y_axis) * glm.rotate(math.atan2(start.y - end.y, glm.distance(start.xz, end.xz)), x_axis) * glm.scale(glm.vec3(1,1,distance))


class Radar(FFDrawPlugin):
    def __init__(self, main):
        super().__init__(main)
        self.print_name = self.data.setdefault('print_name', True)
        self.show_hitbox = self.data.setdefault('show_hitbox', True)
        self.show_target = self.data.setdefault('show_target', True)

        self.colors_data = self.data.setdefault('colors', {})
        self.color_player = self.colors_data.setdefault('player', [0, 0, 1])
        self.color_npc = self.colors_data.setdefault('npc', [1, 1, 0])
        self.color_me = self.colors_data.setdefault('me', [0, 1, 0])
        self.color_focus = self.colors_data.setdefault('focus', [1, 0, 1])
        self.hit_box_model = None
        self.target_line_model = None

    def draw_panel(self):
        clicked, self.print_name = imgui.checkbox("show name", self.print_name)
        if clicked:
            self.data['print_name'] = self.print_name
            self.storage.save()
        clicked, self.show_hitbox = imgui.checkbox("show hitbox", self.show_hitbox)
        if clicked:
            self.data['show_hitbox'] = self.show_hitbox
            self.storage.save()
        clicked, self.show_target = imgui.checkbox("show target", self.show_target)
        if clicked:
            self.data['show_target'] = self.show_target
            self.storage.save()

    def update(self, main):
        if self.hit_box_model is None:
            self.hit_box_model = HitBox()
        if self.target_line_model is None:
            self.target_line_model = TargetLine()

        view = main.gui.get_view()
        me_color = glm.vec4(self.color_me, .2), glm.vec4(self.color_me, .7)
        player_color = glm.vec4(self.color_player, .2), glm.vec4(self.color_player, .7)
        npc_color = glm.vec4(self.color_npc, .2), glm.vec4(self.color_npc, .7)
        focus_color = glm.vec4(self.color_focus, .2), glm.vec4(self.color_focus, .7)
        actors = {a.id: a for a in (CActor(_a) for _a in main.mem.actor_table)}
        me_id = getattr(main.mem.actor_table.me, 'id', -1)
        me = actors.get(me_id)
        focus_id = getattr(main.mem.targets.focus, 'id', -1)

        for actor in actors.values():
            if actor.id == me_id:
                color = me_color
            elif actor.actor_type == 1:
                color = player_color
            else:
                color = npc_color

            is_focus = actor.id == focus_id

            main.gui.add_3d_shape(0x90000, glm.translate(actor.pos), point_color=color[1], )
            if self.print_name:
                text_pos, valid = view.world_to_screen(*actor.pos)
                if not valid: continue
                self.main.gui.render_text(actor.name, (text_pos * glm.vec2(1, -1) + 1) * view.screen_size / 2, color=color[1].xyz, at=TextPosition.center_bottom)
            if self.show_hitbox:
                self.hit_box_model.render(main.gui.program, glm.translate(actor.pos) * glm.rotate(actor.facing, y_axis) * glm.scale(glm.vec3(actor.radius)), view.projection_view, *(focus_color if is_focus else color), )
            if self.show_target and (target := actors.get(actor.target_id)):
                self.target_line_model.render(main.gui.program, line_trans(actor.pos, target.pos), view.projection_view, *color)
            if is_focus and me:
                self.target_line_model.render(main.gui.program, line_trans(me.pos, actor.pos), view.projection_view, *focus_color)
