from __future__ import annotations
import json
from ff_draw.plugins import FFDrawPlugin
import imgui
import requests


def hex_to_rgba(hex_color: str, alpha: int = 1):
    """16进制颜色格式颜色转换为RGBA格式"""
    r = int(hex_color[1:3], 16) / 255
    g = int(hex_color[3:5], 16) / 255
    b = int(hex_color[5:7], 16) / 255
    rgb = [r, g, b, alpha]
    return rgb


# class Instance:
#     """实例类"""
#
#     def __init__(self, name):
#         self.id:int|None = None
#         self.name: str = name
#         self.show: bool = True
#         self.selected: bool = False
#
#         self.cmd = {
#             'index': 0,
#             'key': ['add_omen', 'add_line'],
#             'translate': ['绘制图形', '绘制线条']
#         }
#         self.shape_scale = {
#             'index': 0,
#             'key': ['circle', 'fan', 'donut', 'rect', 'cross', 'action_shape'],
#             'translate': ['圆形', '扇形','月环','矩形','十字','技能图形'],
#             'circle': {
#                 'range': 5
#             },
#             'fan': {
#                 'deg': 90,
#                 'range': 5
#             },
#             'donut': {
#                 'inner': 3,
#                 'range': 5,
#             },
#             'rect': {
#                 'width': 3,
#                 'range': 15
#             },
#             'cross': {
#                 'width': 3,
#                 'range': 15
#             },
#             'action_shape': {
#                 'id': 21866
#             }
#         }
#
#     def to_dict(self):
#         """返回字典数据"""
#         data = {'cmd': self.cmd['key'][self.cmd['index']]}
#         match data['cmd']:
#             case 'add_omen':
#                 data['shape_scale'] = {'key':self.shape_scale['key'][self.shape_scale['index']]}
#                 temp = self.shape_scale[data['shape_scale']['key']]
#
#     def to_json(self):
#         """返回json数据"""
#         pass
#
#
# class Dev(FFDrawPlugin):
#     """画图调试"""
#
#     def __init__(self, main):
#         super().__init__(main)
#         self.instances = []
#         self.current_instance: int | None = None
#
#     def draw_panel(self):
#         """imgui界面"""
#
#         # 实例选择子窗口
#         imgui.begin_child("instance selection", 200, 0, border=True)
#         add = imgui.button('+', 175 / 2)
#         imgui.same_line(spacing=10)
#         sub = imgui.button('-', 175 / 2)
#
#         if add:  # 添加新实例
#             self.instances.append(Instance(f'新的实例{len(self.instances) + 1}'))
#         if sub:  # 删除实例
#             if self.current_instance is not None:
#                 del self.instances[self.current_instance]
#                 self.current_instance = None  # 取消设置当前选中实例的索引
#
#         for i, e in enumerate(self.instances):  # 绘制全部实例
#             clicked, e.selected = imgui.selectable(e.name, e.selected)
#             if e.selected:
#                 self.current_instance = i  # 设置当前选中实例的索引
#                 # 单选
#                 for j in range(len(self.instances)):
#                     self.instances[j].selected = False
#                 e.selected = True
#             if clicked and not e.selected:
#                 self.current_instance = None  # 取消设置当前选中实例的索引
#
#         imgui.end_child()
#
#         # div
#         imgui.same_line(spacing=30)
#         imgui.begin_child("div", 0, 0, border=False)
#
#         # 主窗口
#         self.main_child_window()
#
#         # 不变窗口
#         imgui.begin_child("other", 0, 0, border=False)
#         imgui.begin_child("div2", 300, 0, border=False)
#         imgui.end_child()
#         imgui.same_line()
#         # 发送窗口
#         imgui.begin_child("post", 0, 0, border=False)
#         items = ['item1', 'item2', 'item3']
#         current_item = 0
#         if imgui.combo('Select an item:', current_item, items):
#             pass
#         if imgui.button('发送POST'):
#             if self.current_instance is not None:
#                 json_data = self.get_current_instance().to_json()
#                 send_post(json_data)
#         imgui.end_child()
#         imgui.end_child()
#         imgui.end_child()
#
#     def main_child_window(self):
#         """主窗口分开写"""
#         current = self.get_current_instance()  # 获取当前实例
#         imgui.begin_child("main", 0, -90, border=False)
#         if self.current_instance is not None:
#             _, current.name = imgui.input_text('名称', current.name, 120)  # 名称
#             imgui.same_line(spacing=50)
#             _, current.show = imgui.checkbox("启用", current.show)  # 启用
#             _, current.cmd['index'] = imgui.combo("指令", current.cmd['index'], current.cmd['translate'])  # cmd
#             match self.get_combo_text(current.cmd['key'],current.cmd['index']):
#                 case 'add_omen':
#                     _, current.shape_scale['index'] = imgui.combo("形状", current.shape_scale['index'], current.shape_scale['translate'])  # 形状
#                     match self.get_combo_text(current.shape_scale['key'], current.shape_scale['index']):
#                         case 'circle':
#                             current.shape_scale['circle']['range'] = self.number_input('半径',current.shape_scale['circle']['range'])
#                         case 'fan':
#                             current.shape_scale['fan']['deg'] = self.number_input('夹角',current.shape_scale['fan']['deg'],max_value=360,change_speed=0.5)
#                             current.shape_scale['fan']['range'] = self.number_input('半径',current.shape_scale['fan']['range'])
#                         case 'donut':
#                             pass
#                         case 'rect':
#                             pass
#                         case 'cross':
#                             pass
#                         case 'action_shape':
#                             pass
#                 case 'add_line':
#                     pass
#
#         imgui.end_child()
#
#     def get_current_instance(self) -> Instance | None:
#         """获取当前实例对象的引用"""
#         if self.current_instance is not None:
#             return self.instances[self.current_instance]
#         else:
#             return None
#
#     @staticmethod
#     def get_combo_text(item_list, index) -> str:
#         """获取combo控件的选中文本"""
#         return item_list[index]
#
#     @staticmethod
#     def number_input(name,value,min_value=0.0, max_value=30.0,format="%.1f",change_speed=0.05):
#         """数字输入"""
#         _,re = imgui.drag_float(name,value,min_value=min_value, max_value=max_value,format=format,change_speed=change_speed)
#         return re


class ActorList(FFDrawPlugin):
    """实体信息表格"""

    def __init__(self, main):
        super().__init__(main)
        self.actor_list = main.mem.actor_table
        self.current_omen_id = None
        self.show = self.data.setdefault('show', False)

    def send_post(self, json_data: dict):
        res = requests.post(f'http://127.0.0.1:{self.main.http_port}/rpc', json=json_data)
        return int(json.loads(res.text)['res'])

    def draw_panel(self):
        imgui.text("")
        clicked, self.show = imgui.checkbox("开启", self.show)
        imgui.same_line(spacing=50)
        self.check_button(self.actor_list.me, 1)
        imgui.same_line(spacing=15)
        if imgui.button("取消选中绘制"):
            if self.current_omen_id is not None:
                _data = {
                    'cmd': 'destroy_omen',
                    'id': self.current_omen_id
                }
                self.send_post(_data)

        if self.show:
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
                self.check_button(actor)
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
        radius = float(actor.radius)
        if imgui.button(id_16, 80):  # 选中按钮
            # 取消之前的绘制
            if self.current_omen_id is not None:
                _data = {
                    'cmd': 'destroy_omen',
                    'id': self.current_omen_id
                }
                self.send_post(_data)
                self.current_omen_id = None
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
                    'id': actor.id,
                },
            }
            self.current_omen_id = self.send_post(_data)
