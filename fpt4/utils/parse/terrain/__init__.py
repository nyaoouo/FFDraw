import functools

from fpt4.utils.sqpack import SqPack
from .terrain_mesh import TerrainMesh
from .scene import Scene
from .layer_group import LayerGroup


class Terrain:

    @classmethod
    def get(cls, sq_pack: 'SqPack', terrain_id) -> 'Terrain':
        if (c := getattr(sq_pack, '__cached_terrain', None)) is None:
            setattr(sq_pack, '__cached_terrain', c := {})
        if terrain_id not in c: c[terrain_id] = cls(sq_pack, terrain_id)
        return c[terrain_id]

    __lv_scene = None

    def __init__(self, sq_pack: SqPack, terrain_id):
        self.sq_pack = sq_pack
        self.territory_data = sq_pack.sheets.territory_type_sheet[terrain_id]

    @functools.cached_property
    def lv_scene(self):
        return Scene.get(self.sq_pack, b'bg/%s.lvb' % self.territory_data.lvb.encode(), Scene.LV_SCENE)

    @functools.cached_property
    def mesh(self):
        return TerrainMesh.get(self.sq_pack, self.lv_scene.setting.terrain_asset_path + b'/collision')

    @functools.cached_property
    def layer_groups(self) -> dict[bytes, LayerGroup]:
        res = {}
        for p in self.lv_scene.lgb_asset_paths:
            lg = LayerGroup.get(self.sq_pack, p)
            assert (name := lg.name) not in res
            res[name] = lg
        return res
