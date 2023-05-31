from ff_draw.gui.default_style import text_tip
from .i18n import *
from raid_helper.utils import *
from pprint import pprint


def tab_code_debug(self):
    code = self.code_debug_code

    changed, code = imgui.input_text_multiline("##codeEdit", code, width=-30, height=-100)
    if changed: self.code_debug_code = code

    imgui.new_line()
    imgui.begin_child("##", width=-150)
    text_tip(i18n(Code_tip))
    imgui.end_child()

    imgui.same_line()
    if imgui.button(i18n(Run), width=-30):
        try:
            print('\n' + code)
            exec(code)
        except Exception as e:
            print('\033[91m' + f'Error: {e}' + '\033[0m')


def d(i):
    if hasattr(i, '__dict__'):
        # 对象类型
        print('\n'.join(['\033[93m{0}\033[0m: {1}'.format(item[0], item[1]) for item in i.__dict__.items()]))
        return
    elif isinstance(i, dict):
        # 字典类型
        pprint(i)
        return

    print(i)
