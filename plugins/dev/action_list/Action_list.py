import imgui
from dev.i18n import *


def tab_action_list(self):
    clicked, self.show_action_list = imgui.checkbox(i18n(Enable), self.show_action_list)
    imgui.same_line(spacing=50)
    check_button(self, self.actor_list.me, 1)
    imgui.same_line(spacing=15)
    if imgui.button("取消选中绘制"):
        if self.action_list_current_omen_id is not None:
            _data = {
                'cmd': 'destroy_omen',
                'id': self.action_list_current_omen_id
            }
            self.send_post(_data)

    if self.show_action_list:
        imgui.text("")

        # 表格
        imgui.columns(7, "Actor List")
        imgui.separator()
        imgui.text("Name")
        imgui.next_column()
        imgui.text("Id")
        imgui.next_column()
        imgui.text("Id 十六进制")
        imgui.next_column()
        imgui.text("BaseId")
        imgui.next_column()
        imgui.text("HP")
        imgui.next_column()
        imgui.text("可见")
        imgui.next_column()
        imgui.text("可选中")
        imgui.next_column()
        imgui.separator()

        for actor in self.actor_list:
            is_visible = False
            try:
                if actor.is_visible:
                    is_visible = True
            except Exception as e:
                pass

            imgui.text_wrapped(str(actor.name))
            imgui.next_column()
            imgui.text_wrapped(str(actor.id))
            imgui.next_column()
            check_button(self, actor)
            imgui.next_column()
            imgui.text_wrapped(str(actor.base_id))
            imgui.next_column()
            imgui.text_wrapped(str(actor.current_hp))
            imgui.next_column()
            imgui.text_wrapped(str(is_visible))
            imgui.next_column()
            imgui.text_wrapped(str(actor.can_select))
            imgui.next_column()

        imgui.separator()
        imgui.columns(1)

    imgui.text("")
    imgui.text('调试时可以设置绘制一直可见，在主页面中勾选 "always_draw" ')
    imgui.text("")


def check_button(self, actor, tittle=0):
    """选中绘制按钮"""
    if tittle == 0:
        id_16 = f"{actor.id:#x}"
        id_16 = id_16[2:].upper()
    else:
        id_16 = '选中自己'
    if imgui.button(id_16):  # 选中按钮
        radius = float(actor.radius) if hasattr(actor, 'radius') else 0
        actor_id = actor.id
        # 取消之前的绘制
        if self.action_list_current_omen_id is not None:
            _data = {
                'cmd': 'destroy_omen',
                'id': self.action_list_current_omen_id
            }
            self.send_post(_data)
            self.action_list_current_omen_id = None
        # 新增绘制
        _data = {
            'cmd': 'add_omen',
            'surface': hex_to_rgba('#FF058B', 0),
            'line': hex_to_rgba('#FF058B'),
            'shape_scale': {
                'key': 'circle',
                'range': radius,
            },
            'pos': {
                'key': 'actor_pos',
                'id': actor_id,
            },
        }
        self.action_list_current_omen_id = self.send_post(_data)


def hex_to_rgba(hex_color: str, alpha: int = 1):
    """16进制颜色格式颜色转换为RGBA格式"""
    r = int(hex_color[1:3], 16) / 255
    g = int(hex_color[3:5], 16) / 255
    b = int(hex_color[5:7], 16) / 255
    rgb = [r, g, b, alpha]
    return rgb
