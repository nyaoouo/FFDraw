import logging
import math
import typing
from functools import cache

import glm
from nylib.utils import safe_lazy
from . import omen as omen_module

if typing.TYPE_CHECKING:
    from ff_draw.main import FFDraw

glm_vec_map = '', 'glm.vec1', 'glm.vec2', 'glm.vec3', 'glm.vec4',


class ResMap:
    def __init__(self, enable_eval=False):
        self.counter = 0
        self.res_list = {}
        self.enable_eval = enable_eval

    def add_res(self, data):
        k = f'res_{self.counter}'
        self.counter += 1
        self.res_list[k] = data
        return k

    def add_eval_code(self, code):
        if not self.enable_eval: raise Exception('eval is not enabled')
        return self.add_res(compile(code, '<precompile>', 'eval', dont_inherit=True, optimize=2))


def actor_distance_func(actor):
    src_pos = actor.pos
    return lambda a: glm.distance(src_pos, a.pos)


# TODO: to jump map
def make_value(parser: 'FuncParser', value, res: ResMap, args: dict[str, typing.Any]):
    if isinstance(value, list):
        value_args = (''.join(make_value(parser, v, res, args) + ',' for v in value))
        return f'(safe_lazy({glm_vec_map[len(value)]},{value_args}_default=(lambda *a:a)))' if 0 < len(value) < 5 else f'({value_args})'
    if not isinstance(value, dict):
        return '(' + repr(value) + ')'
    match value.get('key'):
        case 'pi':
            val = ('*' + make_value(parser, val, res, args)) if (val := value.get("val", 1)) != 1 else ''
            return "(math.pi" + val + ")"
        case 'rad_deg':
            if 'rad' in value:
                return f'(math.degrees({make_value(parser, value["rad"], res, args)}))'
            elif 'deg' in value:
                return f'(math.radians({make_value(parser, value["deg"], res, args)}))'
            else:
                return '(0)'
        case 'now':
            return "(" + res.add_res(parser.parse_value(value.get('value'), args)) + ")"
        case 'arg':
            return args[value.get('name', 'v')]
        case 'remain':
            return '(omen.remaining_time)'
        case 'is_hit':
            return f'(int(omen.is_hit({make_value(parser, value.get("pos"), res, args)})))'
        case 'count_hit_actor':
            return f'(sum(int(omen.is_hit(_a.pos)) for _a in (main.mem.actor_table.get_actor_by_id(_i) for _i in ({make_value(parser, value.get("ids"), res, args)})) if _a))'
        case 'progress':
            return "(omen.progress)"
        case 'destroy_omen':
            return "(setattr(omen,'working',False))"
        case 'eval':
            code_key = res.add_eval_code(value.get("code"))
            value_args = "{'omen':omen,'glm':glm," + ','.join(f'{repr(k)}:{make_value(parser, v, res, args)}' for k, v in value.get('args', {}).items()) + '}'
            return f'(eval({code_key},{value_args}))'
        case 'actor_pos':
            return f'(main.mem.actor_table.get_actor_by_id({make_value(parser, value.get("id", 0), res, args)}).pos)'
        case 'actor_facing':
            return f'(main.mem.actor_table.get_actor_by_id({make_value(parser, value.get("id", 0), res, args)}).facing)'
        case 'actor_has_status':
            return f'(int(main.mem.actor_table.get_actor_by_id({make_value(parser, value.get("id", 0), res, args)}).status.has_status({make_value(parser, value.get("status_id", 0), res, args)},{make_value(parser, value.get("source_id", 0), res, args)})))'
        case 'actor_status_remain':
            return f'(main.mem.actor_table.get_actor_by_id({make_value(parser, value.get("id", 0), res, args)}).status.find_status_remain({make_value(parser, value.get("status_id", 0), res, args)},{make_value(parser, value.get("source_id", 0), res, args)}))'
        case 'actor_status_param':
            return f'(main.mem.actor_table.get_actor_by_id({make_value(parser, value.get("id", 0), res, args)}).status.find_status_param({make_value(parser, value.get("status_id", 0), res, args)},{make_value(parser, value.get("source_id", 0), res, args)}))'
        case 'actor_status_source':
            return f'(main.mem.actor_table.get_actor_by_id({make_value(parser, value.get("id", 0), res, args)}).status.find_status_source({make_value(parser, value.get("status_id", 0), res, args)}))'
        case 'actor_exists':
            return f'(int(main.mem.actor_table.get_actor_by_id({make_value(parser, value.get("id", 0), res, args)}) != None))'
        case 'actor_can_select':
            return f'(int(main.mem.actor_table.get_actor_by_id({make_value(parser, value.get("id", 0), res, args)}).can_select))'
        case 'actor_is_visible':
            return f'(int(main.mem.actor_table.get_actor_by_id({make_value(parser, value.get("id", 0), res, args)}).is_visible))'
        case 'actor_distance':
            return f'glm.distance(' \
                   f'main.mem.actor_table.get_actor_by_id({make_value(parser, value.get("a1", 0), res, args)}).pos,' \
                   f'main.mem.actor_table.get_actor_by_id({make_value(parser, value.get("a2", 0), res, args)}).pos' \
                   f')'
        case 'player_by_distance_idx':  # 慎用
            return f'(sorted((a for a in main.mem.actor_table.iter_actor_by_type(1)), key=actor_distance(main.mem.actor_table.get_actor_by_id({make_value(parser, value.get("src", 0), res, args)})))[{make_value(parser, value.get("idx", 0), res, args)}])'
        case 'actor_relative_facing':
            return f'glm.polar(' \
                   f'main.mem.actor_table.get_actor_by_id({make_value(parser, value.get("dst", 0), res, args)}).pos-' \
                   f'main.mem.actor_table.get_actor_by_id({make_value(parser, value.get("src", 0), res, args)}).pos' \
                   f').y'
        case 'me':
            return f'(main.mem.actor_table.me.id)'
        case 'target':
            return f'(main.mem.actor_table.get_actor_by_id({make_value(parser, value.get("id", 0), res, args)}).target_id)'
        case 'fallback':
            return f'(safe_lazy((lambda : {make_value(parser, value.get("expr"), res, args)}), _default=(lambda : {make_value(parser, value.get("default"), res, args)})))'
        case 'if':
            ts = make_value(parser, value.get('true', 0), res, args)
            fs = make_value(parser, value.get('false', 0), res, args)
            cond = make_value(parser, value.get('cond', 0), res, args)
            return f'(({ts})if({cond})else({fs}))'
        case 'gt':
            return f"(int({make_value(parser, value.get('v1', 0), res, args)}>{make_value(parser, value.get('v2', 0), res, args)}))"
        case 'lt':
            return f"(int({make_value(parser, value.get('v1', 0), res, args)}<{make_value(parser, value.get('v2', 0), res, args)}))"
        case 'gte':
            return f"(int({make_value(parser, value.get('v1', 0), res, args)}>={make_value(parser, value.get('v2', 0), res, args)}))"
        case 'lte':
            return f"(int({make_value(parser, value.get('v1', 0), res, args)}<={make_value(parser, value.get('v2', 0), res, args)}))"
        case 'add':
            return "(" + ("+".join(make_value(parser, v, res, args) for v in value.get('values', []))) + ")"
        case 'mul':
            return "(" + ("*".join(make_value(parser, v, res, args) for v in value.get('values', []))) + ")"
        case 'div':
            return "(" + ("/".join(make_value(parser, v, res, args) for v in value.get('values', []))) + ")"
        case 'min':
            return "(min(" + (",".join(make_value(parser, v, res, args) for v in value.get('values', []))) + "))"
        case 'max':
            return "(max(" + (",".join(make_value(parser, v, res, args) for v in value.get('values', []))) + "))"
        case 'string_format':
            return f"({make_value(parser, value.get('format', []), res, args)}.format({','.join(make_value(parser, v, res, args) for v in value.get('args', []))}))"
        case 'fan':
            return f"((0x50000|{make_value(parser, value.get('deg', 0), res, args)}),({make_value(parser, value.get('range', 0), res, args)},)*3)"
        case 'circle':
            return f"((0x10000),({make_value(parser, value.get('range', 0), res, args)},)*3)"
        case 'rect':
            return f"((0x20000),({make_value(parser, value.get('width', 0), res, args)},1,{make_value(parser, value.get('range', 0), res, args)}))"
        case 'cross':
            return f"((0x20002),({make_value(parser, value.get('width', 0), res, args)},1,{make_value(parser, value.get('range', 0), res, args)}))"
        case 'donut':
            return f"((0x10000|int({make_value(parser, value.get('inner', 0), res, args)}/{make_value(parser, value.get('range', 0), res, args)}*0xffff)),({make_value(parser, value.get('range', 0), res, args)},)*3)"
        case 'action_shape':
            return f"(action_shape_scale({make_value(parser, value.get('id', 0), res, args)}))"
        case 'actors_by_type':
            return f"([a.id for a in main.mem.actor_table if a.actor_type == ({make_value(parser, value.get('type', 0), res, args)})])"
        case 'actors_by_base_id':
            return f"([a.id for a in main.mem.actor_table if a.base_id == ({make_value(parser, value.get('id', 0), res, args)})])"
        case 'actors_in_party':
            return f"([m.id for m in main.mem.party.party_list])"


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
            'actor_distance': actor_distance_func, 'action_shape_scale': self.action_shape_scale, 'math': math
        }
        compile_config = self.main.config.setdefault('compile', {})
        self.print_compile = compile_config.setdefault('print_debug', {}).setdefault('enable', False)
        self.enable_eval = compile_config.setdefault('enable_eval', False)
        if self.enable_eval and not self.main.rpc_password:
            self.logger.warning(r'enable_eval is set as true but there is no rpc password, please set a rpc password to enable eval function')
            self.enable_eval = False

    @cache
    def action_shape_scale(self, action_id):
        action = self.action_sheet[action_id]
        if not (shape := action_type_to_shape_default.get(action.effect_type)): return None
        if shape >> 16 == 2:
            scale = glm.vec3(action.effect_width, 1, action.effect_range)
        else:
            scale = glm.vec3(action.effect_range, 1, action.effect_range)
        return shape, scale

    def parse_value_lambda(self, value, args):
        code = optimize_code(make_value(self, value, res := ResMap(enable_eval=self.enable_eval), args))
        if self.print_compile: self.logger.debug(f'compile_debug:{value}=>{code}')
        return eval(f'lambda omen:({code})', res.res_list | self.parse_name_space)

    def parse_value(self, value, args):
        code = optimize_code(make_value(self, value, res := ResMap(enable_eval=self.enable_eval), args))
        if self.print_compile: self.logger.debug(f'compile_debug:{value}=>{code}')
        return eval(code, res.res_list | self.parse_name_space)

    def parse_func(self, command, args=None):
        assert isinstance(command, dict)
        if args is None: args = {}
        match command.get('cmd'):
            case 'with_args':
                return self.parse_func(command.get('func'), args | {k: self.parse_value(v, args) for k, v in command.get('args', {}).items()})
            case 'foreach':
                return [self.parse_func(command.get('func'), args | {command.get('name', 'v'): v}) for v in self.parse_value(command.get('values'), args)]
            case 'add_line':
                width = self.parse_value_lambda(command.get('width',3), args)
                color = self.parse_value_lambda(command.get('color'), args)
                src = self.parse_value_lambda(command.get('src'), args)
                dst = self.parse_value_lambda(command.get('dst'), args)
                return omen_module.Line(
                    main=self.main,
                    src=src, dst=dst,
                    line_color=color,
                    line_width=width,
                    label=self.parse_value_lambda(command.get('label', ''), args),
                    label_color=self.parse_value_lambda(command.get('label_color', [0, 0, 0]), args),
                    label_scale=self.parse_value_lambda(command.get('label_scale', 1), args),
                    label_at=self.parse_value_lambda(command.get('label_at', 1), args),
                    duration=command.get('duration', 0),
                ).oid
            case 'add_omen':
                if 'shape_scale' in command:
                    shape = scale = None
                    shape_scale = self.parse_value_lambda(command.get('shape_scale'), args)
                else:
                    shape = self.parse_value_lambda(command.get('shape'), args)
                    scale = self.parse_value_lambda(command.get('scale'), args)
                    shape_scale = None
                if 'color' in command:
                    surface_color = line_color = None
                    surface_line = self.parse_value_lambda(command.get('color'), args)
                else:
                    surface_color = self.parse_value_lambda(command.get('surface'), args)
                    line_color = self.parse_value_lambda(command.get('line'), args)
                    surface_line = None

                return omen_module.BaseOmen(
                    main=self.main,
                    pos=self.parse_value_lambda(command.get('pos'), args),
                    scale=scale, shape=shape, shape_scale=shape_scale,
                    facing=self.parse_value_lambda(command.get('facing'), args),
                    surface_color=surface_color,
                    line_color=line_color,
                    surface_line_color=surface_line,
                    label=self.parse_value_lambda(command.get('label', ''), args),
                    label_color=self.parse_value_lambda(command.get('label_color', [0, 0, 0]), args),
                    label_scale=self.parse_value_lambda(command.get('label_scale', 1), args),
                    label_at=self.parse_value_lambda(command.get('label_at', 1), args),
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
