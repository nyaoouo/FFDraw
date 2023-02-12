import logging
import typing
from functools import cache

import glm
from nylib.utils import safe_lazy
from . import omen as omen_module

if typing.TYPE_CHECKING:
    from ff_draw.main import FFDraw

glm_vec_map = '', 'glm.vec1', 'glm.vec2', 'glm.vec3', 'glm.vec4',


class ResMap:
    def __init__(self):
        self.counter = 0
        self.res_list = {}

    def add_res(self, data):
        k = f'res_{self.counter}'
        self.counter += 1
        self.res_list[k] = data
        return k


def actor_distance_func(actor):
    src_pos = actor.pos
    return lambda a: glm.distance(src_pos, a.pos)


def make_value(value, res: ResMap):
    if isinstance(value, list):
        args = (''.join(make_value(v, res) + ',' for v in value))
        return f'(safe_lazy({glm_vec_map[len(value)]},{args}_default=(lambda *a:a)))' if 0 < len(value) < 5 else f'({args})'
    if not isinstance(value, dict):
        return '(' + repr(value) + ')'
    match value.get('key'):
        case 'remain':
            return '(omen.remaining_time)'
        case 'progress':
            return "(omen.progress)"
        case 'eval':
            code_key = res.add_res(compile(value.get("code"), '<precompile>', 'eval', dont_inherit=True, optimize=2))
            args = "{'omen':omen,'glm':glm," + ','.join(f'{repr(k)}:{make_value(v, res)}' for k, v in value.get('args', {}).items()) + '}'
            return f'(eval({code_key},{args}))'
        case 'actor_pos':
            return f'(main.mem.actor_table.get_actor_by_id({make_value(value.get("id", 0), res)}).pos)'
        case 'actor_facing':
            return f'(main.mem.actor_table.get_actor_by_id({make_value(value.get("id", 0), res)}).facing)'
        case 'actor_exists':
            return f'(int(main.mem.actor_table.get_actor_by_id({make_value(value.get("id", 0), res)}) != None))'
        case 'actor_can_select':
            return f'(int(main.mem.actor_table.get_actor_by_id({make_value(value.get("id", 0), res)}).can_select))'
        case 'actor_is_visible':
            return f'(int(main.mem.actor_table.get_actor_by_id({make_value(value.get("id", 0), res)}).is_visible))'
        case 'actor_distance':
            return f'glm.distance(' \
                   f'main.mem.actor_table.get_actor_by_id({make_value(value.get("a1", 0), res)}).pos,' \
                   f'main.mem.actor_table.get_actor_by_id({make_value(value.get("a2", 0), res)}).pos' \
                   f')'
        case 'player_by_distance_idx':  # 慎用
            return f'(sorted((a for a in main.mem.actor_table.iter_actor_by_type(1)), key=actor_distance(main.mem.actor_table.get_actor_by_id({make_value(value.get("src", 0), res)})))[{make_value(value.get("idx", 0), res)}])'
        case 'actor_relative_facing':
            return f'glm.polar(' \
                   f'main.mem.actor_table.get_actor_by_id({make_value(value.get("dst", 0), res)}).pos-' \
                   f'main.mem.actor_table.get_actor_by_id({make_value(value.get("src", 0), res)}).pos' \
                   f').y'
        case 'me':
            return f'(main.mem.actor_table.me.id)'
        case 'target':
            return f'(main.mem.actor_table.get_actor_by_id({make_value(value.get("id", 0), res)}).target_id)'
        case 'fallback':
            return f'(safe_lazy((lambda : {make_value(value.get("expr"), res)}), _default=(lambda : {make_value(value.get("default"), res)})))'
        case 'if':
            ts = make_value(value.get('true', 0), res)
            fs = make_value(value.get('false', 0), res)
            cond = make_value(value.get('cond', 0), res)
            return f'(({ts}) if ({cond}) else ({fs}))'
        case 'gt':
            return f"(int({make_value(value.get('v1', 0), res)}>{make_value(value.get('v2', 0), res)}))"
        case 'lt':
            return f"(int({make_value(value.get('v1', 0), res)}<{make_value(value.get('v2', 0), res)}))"
        case 'gte':
            return f"(int({make_value(value.get('v1', 0), res)}>={make_value(value.get('v2', 0), res)}))"
        case 'lte':
            return f"(int({make_value(value.get('v1', 0), res)}<={make_value(value.get('v2', 0), res)}))"
        case 'add':
            return "(" + ("+".join(make_value(v, res) for v in value.get('values', []))) + ")"
        case 'mul':
            return "(" + ("*".join(make_value(v, res) for v in value.get('values', []))) + ")"
        case 'div':
            return "(" + ("/".join(make_value(v, res) for v in value.get('values', []))) + ")"
        case 'min':
            return "(min(" + (",".join(make_value(v, res) for v in value.get('values', []))) + "))"
        case 'max':
            return "(max(" + (",".join(make_value(v, res) for v in value.get('values', []))) + "))"
        case 'fan':
            return f"((0x50000|{make_value(value.get('deg', 0), res)}),({make_value(value.get('range', 0), res)},)*3)"
        case 'circle':
            return f"((0x10000),({make_value(value.get('range', 0), res)},)*3)"
        case 'rect':
            return f"((0x20000),({make_value(value.get('width', 0), res)},1,{make_value(value.get('range', 0), res)}))"
        case 'cross':
            return f"((0x20002),({make_value(value.get('width', 0), res)},1,{make_value(value.get('range', 0), res)}))"
        case 'donut':
            return f"((0x10000|int({make_value(value.get('inner', 0), res)}/{make_value(value.get('range', 0), res)}*0xffff)),({make_value(value.get('range', 0), res)},)*3)"
        case 'action_shape':
            return f"(action_shape_scale({make_value(value.get('id', 0), res)}))"


def optimize_code(code: str):
    code = code.replace('main.mem.actor_table.get_actor_by_id((main.mem.actor_table.me.id))', 'main.mem.actor_table.me')
    return code


action_type_to_shape_default = {
    2: 0x10000,  # circle
    3: 0x50000 | 90,  # fan
    4: 0x20000,  # rect
    5: 0x10000,  # circle
    6: 0x10000,  # circle
    7: 0x10000,  # circle
    # 8: 0x20000,  # rect to target
    10: 0x10000 | int(.5 * 0xffff),  # donut
    11: 0x20002,  # cross
    12: 0x20000,  # rect
    13: 0x50000 | 90,  # fan
}


class FuncParser:
    logger = logging.getLogger('FuncParser')

    def __init__(self, main: 'FFDraw'):
        self.main = main
        self.action_sheet = main.sq_pack.sheets.action_sheet
        self.parse_name_space = {
            'glm': glm, 'main': self.main, 'safe_lazy': safe_lazy,
            'actor_distance': actor_distance_func, 'action_shape_scale': self.action_shape_scale
        }

    @cache
    def action_shape_scale(self, action_id):
        action = self.action_sheet[action_id]
        if not (shape := action_type_to_shape_default.get(action.effect_type)): return None
        if shape >> 16 == 2:
            scale = glm.vec3(action.effect_width, 1, action.effect_range)
        else:
            scale = glm.vec3(action.effect_range, 1, action.effect_range)
        return shape, scale

    def parse_value(self, omen: omen_module.BaseOmen, value):
        if isinstance(value, list):
            return glm_vec_map[len(value)](*(self.parse_value(omen, v) for v in value))
        if not isinstance(value, dict):
            return value
        match value.get('key'):
            case 'remain':
                return omen.remaining_time
            case 'progress':
                return omen.progress
            case 'eval':
                return eval(value.get('code'), {'omen': omen, 'glm': glm, **{k: self.parse_value(omen, v) for k, v in value.get('args', {}).items()}})
            case 'actor_pos':
                return self.main.mem.actor_table.get_actor_by_id(self.parse_value(omen, value.get('id', 0))).pos
            case 'actor_facing':
                return self.main.mem.actor_table.get_actor_by_id(self.parse_value(omen, value.get('id', 0))).facing
            case 'actor_relative_facing':
                return glm.polar(
                    self.main.mem.actor_table.get_actor_by_id(self.parse_value(omen, value.get('dst', 0))).pos -
                    self.main.mem.actor_table.get_actor_by_id(self.parse_value(omen, value.get('src', 0))).pos
                ).y
            case 'me':
                return self.main.mem.actor_table.me.id
            case 'target':
                return self.main.mem.actor_table.get_actor_by_id(self.parse_value(omen, value.get('id', 0))).target_id
            case 'fallback':
                return safe_lazy((lambda _: self.parse_value(omen, value.get('expr', 0))), _default=(lambda _: self.parse_value(omen, value.get('default', 0))))

    def parse_value_lambda(self, value):
        # return lambda o: self.parse_value(o, value)
        code = optimize_code(make_value(value, res := ResMap()))
        self.logger.debug(code)
        return eval(f'lambda omen:({code})', res.res_list | self.parse_name_space)

    def parse_func(self, command):
        assert isinstance(command, dict)
        match command.get('cmd'):
            case 'add_omen':
                if 'shape_scale' in command:
                    shape = scale = None
                    shape_scale = self.parse_value_lambda(command.get('shape_scale'))
                else:
                    shape = self.parse_value_lambda(command.get('shape'))
                    scale = self.parse_value_lambda(command.get('scale'))
                    shape_scale = None
                if 'color' in command:
                    surface_color = line_color = None
                    surface_line = self.parse_value_lambda(command.get('color'))
                else:
                    surface_color = self.parse_value_lambda(command.get('surface'))
                    line_color = self.parse_value_lambda(command.get('line'))
                    surface_line = None

                return omen_module.BaseOmen(
                    main=self.main,
                    pos=self.parse_value_lambda(command.get('pos')),
                    scale=scale, shape=shape, shape_scale=shape_scale,
                    facing=self.parse_value_lambda(command.get('facing')),
                    surface_color=surface_color,
                    line_color=line_color,
                    surface_line_color=surface_line,
                    duration=command.get('duration', 0),
                ).oid
            case 'destroy_omen':
                oid = command.get('id')
                omens = self.main.omens
                if oid == -1:
                    cnt = 0
                    while omens:
                        if _omen := omens.pop(next(iter(omens.keys()), None)):
                            _omen.destroy()
                            cnt += 1
                    return cnt
                elif _omen := self.main.omens.get(oid):
                    _omen.destroy()
                    return 1
                return 0
            case unk:
                for plugin in self.main.plugins:
                    if plugin.process_command(command):
                        break
                else:
                    raise Exception(f'unhandled command {unk}')
