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
# 恩惠终结：贰，使用自定义颜色和显示文字
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
    'label': '恩惠终结：贰',
    'label_at': 3,
    'duration': 10,
}
# 给所有玩家画一个小扇形
demo_6 = {
    'cmd': 'foreach',
    'name': 'target_id',
    'values': {'key': 'actors_by_type', 'type': 1},
    'func': {
        'cmd': 'add_omen',
        'surface': [1, .1, .5, .3],
        'line': [1, .1, .5, .7],
        'shape_scale': {
            'key': 'fan',
            'deg': 90,
            'range': .5,
        },
        'pos': {
            'key': 'actor_pos',
            'id': {'key': 'arg', 'name': 'target_id'},
        },
        'facing': {
            'key': 'actor_facing',
            'id': {'key': 'arg', 'name': 'target_id'},
        },
        'duration': 10,
    }
}
# 如果身上有再生并且剩余时间小于13则画一个小圈圈
demo_7 = {
    'cmd': 'add_omen',
    'color': 'g_friend',
    'shape_scale': {
        'key': 'if',
        'cond': {
            'key': 'actor_has_status',
            'id': {'key': 'me'},
            'status_id': 158,
        },
        'true': {
            'key': 'if',
            'cond': {
                'key': 'lt',
                'v1': {
                    'key': 'actor_status_remain',
                    'id': {'key': 'me'},
                    'status_id': 158,
                },
                'v2': 13,
            },
            'true': {
                'key': 'circle',
                'range': 5,
            },
            'false': 0,
        },
        'false': 0,
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

# 在脚下生成一个omen，如果人在里面会显示为红色，否则为绿色
demo_8 = {
    'cmd': 'add_omen',
    'color': {
        'key': 'if',
        'cond': {
            'key': 'is_hit',
            'pos': {
                'key': 'actor_pos',
                'id': {'key': 'me'},
            }
        },
        'true': 'enemy',
        'false': 'friend',
    },
    # 'shape_scale': {'key': 'fan', 'deg': 60, 'range': 5, },
    'shape_scale': {'key': 'cross', 'width': 5, 'range': 10, },
    'pos': {
        'key': 'now',
        'value': {
            'key': 'actor_pos',
            'id': {'key': 'me'},
        },
    },
    'facing': {
        'key': 'now',
        'value': {
            'key': 'actor_facing',
            'id': {'key': 'me'},
        },
    },
    'duration': 10,
}
# 在脚下生成一个omen，并且label里面有多少玩家
demo_9 = {
    'cmd': 'add_omen',
    'color': 'friend',
    # 'shape_scale': {'key': 'fan', 'deg': 60, 'range': 5, },
    'shape_scale': {'key': 'circle', 'range': 5, },
    'pos': {
        'key': 'actor_pos',
        'id': {'key': 'me'},
    },
    'facing': {
        'key': 'actor_facing',
        'id': {'key': 'me'},
    },
    'duration': 10,
    'label': {
        'key': 'string_format',
        'format': 'hit:{}',
        'args': [{
            'key': 'count_hit_actor',
            'ids': {'key': 'actors_by_type', 'type': 1},
        }],
    },
}
# 画一条和目标的连线
demo_10 = {
    'cmd': 'add_line',
    'color': 'enemy',
    'src': {
        'key': 'actor_pos',
        'id': {'key': 'me'},
    },
    'dst': {
        'key': 'fallback',
        'expr': {
            'key': 'actor_pos',
            'id': {'key': 'target', 'id': {'key': 'me'}},
        },
        'default': None,
    },
    'duration': 10,
}
print(post(f'http://127.0.0.1:8001/rpc', json=demo_10).text)
