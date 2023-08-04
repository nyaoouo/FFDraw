datetime_str = '%Y-%m-%d %H:%M:%S'
proto_name = [
    ('CD', 'chat down'),
    ('CU', 'chat up'),
    ('ZD', 'zone down'),
    ('ZU', 'zone up'),
]


class ActorDef:
    def __init__(self, entity_id: int, base_id: int, name: str):
        self.entity_id = entity_id
        self.base_id = base_id
        self.name = name
        self.str = f'{self.name}<{self.entity_id:X}>'
        if self.base_id: self.str += f'[{self.base_id}]'

    def __str__(self):
        return self.str


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
