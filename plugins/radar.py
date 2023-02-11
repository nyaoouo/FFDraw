import glm

from ff_draw.plugins import FFDrawPlugin


class Radar(FFDrawPlugin):
    def update(self, main):
        for actor in main.mem.actor_table:
            main.gui.add_3d_shape(
                0x90000,
                glm.translate(actor.pos),
                point_color=glm.vec4(1, 1, 1, .7),
            )
