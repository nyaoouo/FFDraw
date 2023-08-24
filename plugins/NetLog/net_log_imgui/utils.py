import glm

datetime_str = '%Y-%m-%d %H:%M:%S'
proto_name = [
    ('CD', 'chat down'),
    ('CU', 'chat up'),
    ('ZD', 'zone down'),
    ('ZU', 'zone up'),
]


class ActorDef:
    def __init__(self, entity_id: int, base_id: int, name: str, pos: glm.vec3 = None, facing: float = None):
        self.entity_id = entity_id
        self.base_id = base_id
        self.name = name
        self.pos = pos
        self.facing = facing
        self.str = f'{self.name}<{self.entity_id:X}>'
        if self.base_id: self.str += f'[{self.base_id}]'

    def __str__(self):
        res = self.str
        if pos := self.pos: res += f'(p:{pos.x:.1f}, {pos.y:.1f}, {pos.z:.1f})'
        if (facing := self.facing) is not None: res += f'(f:{facing:.1f})'
        return res


class ActorDefs:
    def __init__(self):
        self.actors = {}

    def get(self, source_id):
        if not source_id or source_id == 0xe0000000: return None
        return self.actors.get(source_id) or ActorDef(source_id, 0, "?")

    def update(self, source_id, npc_id, name):
        self.actors[source_id] = ActorDef(source_id, npc_id, name)

    def drop(self, source_id):
        self.actors.pop(source_id, None)
