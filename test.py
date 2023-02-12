from requests import post

# 对自己目标的一个 5s 30度 20距离 扇形，使用预设队友颜色
# {'key': 'me'} 可以替换为任意角色 id
demo_1 = {
    'cmd': 'add_omen',
    'color': 'friend',
    'shape_scale': {
        'key': 'fan',
        'deg': 30,
        'range': 20,
    },
    'pos': {
        'key': 'actor_pos',
        'id': {'key': 'me'},
    },
    'facing': {
        'key': 'fallback',
        'expr': {
            'key': 'actor_relative_facing',
            'src': {'key': 'me'},
            'dst': {'key': 'target', 'id': {'key': 'me'}},
        },
        'default': {
            'key': 'actor_facing',
            'id': {'key': 'me'},
        },
    },
    'duration': 10,
}
# 如果有选中目标，对目标标红圈月环，否则对自己标绿月环
demo_2 = {
    'cmd': 'add_omen',
    'color': {
        'key': 'if',
        'cond': {
            'key': 'actor_exists',
            'id': {'key': 'target', 'id': {'key': 'me'}},
        },
        'true': 'g_enemy',
        'false': 'g_friend',
    },
    'shape_scale': {
        'key': 'donut',
        'inner': 10,
        'range': 15,
    },
    'pos': {
        'key': 'fallback',
        'expr': {
            'key': 'actor_pos',
            'id': {'key': 'target', 'id': {'key': 'me'}},
        },
        'default': {
            'key': 'actor_pos',
            'id': {'key': 'me'},
        },
    },
    'duration': 10,
}

# 从显示开始每1s缩小2m直到剩余5s时锁定为5m
demo_3 = {
    'cmd': 'add_omen',
    'color': 'enemy',
    'shape_scale': {
        'key': 'circle',
        'range': {'key': 'add', 'values': [{'key': 'mul', 'values': [{'key': 'max', 'values': [{'key': 'add', 'values': [{'key': 'remain'}, -5]}, 0]}, 2]}, 5]}
    },
    'pos': {
        'key': 'actor_pos',
        'id': {'key': 'me'},
    },
    'duration': 10,
}

# 可变长度十字（仅当选中目标）
demo_4 = {
    'cmd': 'add_omen',
    'color': 'friend',
    'shape_scale': {
        'key': 'if',
        'cond': {
            'key': 'actor_exists',
            'id': {'key': 'target', 'id': {'key': 'me'}},
        },
        'true': {
            'key': 'cross',
            'width': 4,
            'range': {'key': 'actor_distance', 'a1': {'key': 'me'}, 'a2': {'key': 'target', 'id': {'key': 'me'}}}
        },
        'false': 0,
    },
    'pos': {
        'key': 'actor_pos',
        'id': {'key': 'target', 'id': {'key': 'me'}},
    },
    'facing': {
        'key': 'actor_relative_facing',
        'src': {'key': 'me'},
        'dst': {'key': 'target', 'id': {'key': 'me'}},
    },
    'duration': 10,
}
# 恩惠终结：贰，使用自定义颜色
demo_5 = {
    'cmd': 'add_omen',
    'surface': [1, .1, .5, .3],
    'line': [1, .1, .5, .7],
    'shape_scale': {
        'key': 'action_shape',
        'id': 21866,
    },
    'pos': {
        'key': 'actor_pos',
        'id': {'key': 'me'},
    },
    'facing': {
        'key': 'actor_facing',
        'id': {'key': 'me'},
    },
    'duration': 10,
}

print(post(f'http://127.0.0.1:8001/rpc', json=demo_5).text)
