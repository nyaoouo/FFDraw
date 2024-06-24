import ctypes
import struct

from .utils import InstanceObject
from . import ct_character, game_object, helper_object, trigger_box, pop_range, bg, vfx, shared_group
from . import env
from ..utils import AssetType

# TODO

instance_object_map = {
    AssetType.BG.value: bg.BGInstanceObject,
    AssetType.Attribute.value: None,
    AssetType.LayLight.value: None,
    AssetType.VFX.value: vfx.VFXInstanceObject,
    AssetType.PositionMarker.value: None,
    AssetType.SharedGroup.value: shared_group.SGInstanceObject,
    AssetType.Sound.value: None,
    AssetType.EventNPC.value: game_object.ENPCInstanceObject,
    AssetType.BattleNPC.value: game_object.BNPCInstanceObject,
    AssetType.RoutePath.value: None,
    AssetType.Character.value: ct_character.CTCharacter,
    AssetType.Aetheryte.value: game_object.AetheryteInstanceObject,
    AssetType.EnvSet.value: env.EnvSetInstanceObject,
    AssetType.Gathering.value: game_object.GatheringInstanceObject,
    AssetType.HelperObject.value: helper_object.HelperObjInstanceObject,
    AssetType.Treasure.value: game_object.TreasureInstanceObject,
    AssetType.Clip.value: None,
    AssetType.ClipCtrlPoint.value: None,
    AssetType.ClipCamera.value: None,
    AssetType.ClipLight.value: None,
    AssetType.ClipPathCtrlPoint.value: None,
    AssetType.CutAssetOnlySelectable.value: None,
    AssetType.Player.value: ct_character.CTPlayer,
    AssetType.Monster.value: ct_character.CTMonster,
    AssetType.Weapon.value: ct_character.CTWeapon,
    AssetType.PopRange.value: pop_range.PopRangeInstanceObject,
    AssetType.ExitRange.value: trigger_box.ExitRangeInstanceObject,
    AssetType.LVB.value: None,
    AssetType.MapRange.value: trigger_box.MapRangeInstanceObject,
    AssetType.NavMeshRange.value: None,
    AssetType.EventObject.value: game_object.EventInstanceObject,
    AssetType.DemiHuman.value: ct_character.CTDemiHuman,
    AssetType.EnvLocation.value: env.EnvLocationInstanceObject,
    AssetType.ControlPoint.value: None,
    AssetType.EventRange.value: trigger_box.EventRangeInstanceObject,
    AssetType.RestBonusRange.value: trigger_box.RestBonusRangeInstanceObject,
    AssetType.QuestMarker.value: None,
    AssetType.Timeline.value: None,
    AssetType.ObjectBehaviorSet.value: None,
    AssetType.Movie.value: None,
    AssetType.ScenarioEXD.value: None,
    AssetType.ScenarioText.value: None,
    AssetType.CollisionBox.value: trigger_box.CollisionBoxInstanceObject,
    AssetType.DoorRange.value: trigger_box.DoorRangeInstanceObject,
    AssetType.LineVFX.value: None,
    AssetType.SoundEnvSet.value: None,
    AssetType.CutActionTimeline.value: None,
    AssetType.CharaScene.value: None,
    AssetType.CutAction.value: None,
    AssetType.EquipPreset.value: None,
    AssetType.ClientPath.value: None,
    AssetType.ServerPath.value: None,
    AssetType.GimmickRange.value: trigger_box.GimmickRangeInstanceObject,
    AssetType.TargetMarker.value: None,
    AssetType.ChairMarker.value: None,
    AssetType.ClickableRange.value: trigger_box.ClickableRangeInstanceObject,
    AssetType.PrefetchRange.value: trigger_box.PrefetchRangeInstanceObject,
    AssetType.FateRange.value: trigger_box.FateRangeInstanceObject,
    AssetType.PartyMember.value: None,
    AssetType.KeepRange.value: None,
    AssetType.SphereCastRange.value: trigger_box.SphereCastRangeInstanceObject,
    AssetType.IndoorObject.value: None,
    AssetType.OutdoorObject.value: None,
    AssetType.EditGroup.value: None,
    AssetType.StableChocobo.value: None,
    AssetType.GroomPlayer.value: None,
    AssetType.BridePlayer.value: None,
    AssetType.WeddingGuestPlayer.value: None,
    AssetType.Decal.value: None,
    AssetType.SystemActor.value: None,
    AssetType.CustomSharedGroup.value: None,
    AssetType.WaterRange.value: trigger_box.WaterRangeInstanceObject,
    AssetType.ShowHideRange.value: trigger_box.ShowHideRangeInstanceObject,
    AssetType.GameContentsRange.value: trigger_box.GameContentsRangeInstanceObject,
    AssetType.EventEffectRange.value: trigger_box.EventEffectRangeInstanceObject,
}


def get_instance_object(buf, off=0) -> InstanceObject:
    return (instance_object_map.get(struct.unpack_from(b'I', buf, off)[0]) or InstanceObject).from_buffer(buf, off)


def get_instance_object_from_addr(addr) -> InstanceObject:
    return (instance_object_map.get(ctypes.c_int32.from_address(addr).value) or InstanceObject).from_address(addr)
