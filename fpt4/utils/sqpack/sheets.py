from typing import TYPE_CHECKING
from functools import cached_property
from .exd.row import SubDataRow
from .exd.sheet import Sheet
from .exd import define

if TYPE_CHECKING:
    from . import SqPack


class Sheets:
    def __init__(self, pack: 'SqPack'):
        self.pack = pack
        self.get_sheet = pack.exd.get_sheet

    @cached_property
    def aoz_arrangement_sheet(self) -> Sheet[SubDataRow[define.AOZArrangement]]:
        return self.get_sheet(define.AOZArrangement)

    @cached_property
    def aoz_boss_sheet(self) -> Sheet[define.AOZBoss]:
        return self.get_sheet(define.AOZBoss)

    @cached_property
    def aoz_content_sheet(self) -> Sheet[define.AOZContent]:
        return self.get_sheet(define.AOZContent)

    @cached_property
    def aoz_content_briefing_b_npc_sheet(self) -> Sheet[define.AOZContentBriefingBNpc]:
        return self.get_sheet(define.AOZContentBriefingBNpc)

    @cached_property
    def aoz_report_sheet(self) -> Sheet[define.AOZReport]:
        return self.get_sheet(define.AOZReport)

    @cached_property
    def aoz_report_reward_sheet(self) -> Sheet[define.AOZReportReward]:
        return self.get_sheet(define.AOZReportReward)

    @cached_property
    def aoz_score_sheet(self) -> Sheet[define.AOZScore]:
        return self.get_sheet(define.AOZScore)

    @cached_property
    def aoz_weekly_reward_sheet(self) -> Sheet[define.AOZWeeklyReward]:
        return self.get_sheet(define.AOZWeeklyReward)

    @cached_property
    def achievement_sheet(self) -> Sheet[define.Achievement]:
        return self.get_sheet(define.Achievement)

    @cached_property
    def achievement_category_sheet(self) -> Sheet[define.AchievementCategory]:
        return self.get_sheet(define.AchievementCategory)

    @cached_property
    def achievement_hide_condition_sheet(self) -> Sheet[define.AchievementHideCondition]:
        return self.get_sheet(define.AchievementHideCondition)

    @cached_property
    def achievement_kind_sheet(self) -> Sheet[define.AchievementKind]:
        return self.get_sheet(define.AchievementKind)

    @cached_property
    def achievement_target_sheet(self) -> Sheet[define.AchievementTarget]:
        return self.get_sheet(define.AchievementTarget)

    @cached_property
    def action_sheet(self) -> Sheet[define.Action]:
        return self.get_sheet(define.Action)

    @cached_property
    def action_cast_timeline_sheet(self) -> Sheet[define.ActionCastTimeline]:
        return self.get_sheet(define.ActionCastTimeline)

    @cached_property
    def action_cast_vfx_sheet(self) -> Sheet[define.ActionCastVFX]:
        return self.get_sheet(define.ActionCastVFX)

    @cached_property
    def action_category_sheet(self) -> Sheet[define.ActionCategory]:
        return self.get_sheet(define.ActionCategory)

    @cached_property
    def action_combo_route_sheet(self) -> Sheet[define.ActionComboRoute]:
        return self.get_sheet(define.ActionComboRoute)

    @cached_property
    def action_combo_route_transient_sheet(self) -> Sheet[define.ActionComboRouteTransient]:
        return self.get_sheet(define.ActionComboRouteTransient)

    @cached_property
    def action_cost_type_sheet(self) -> Sheet[define.ActionCostType]:
        return self.get_sheet(define.ActionCostType)

    @cached_property
    def action_indirection_sheet(self) -> Sheet[define.ActionIndirection]:
        return self.get_sheet(define.ActionIndirection)

    @cached_property
    def action_init_sheet(self) -> Sheet[define.ActionInit]:
        return self.get_sheet(define.ActionInit)

    @cached_property
    def action_param_sheet(self) -> Sheet[define.ActionParam]:
        return self.get_sheet(define.ActionParam)

    @cached_property
    def action_proc_status_sheet(self) -> Sheet[define.ActionProcStatus]:
        return self.get_sheet(define.ActionProcStatus)

    @cached_property
    def action_timeline_sheet(self) -> Sheet[define.ActionTimeline]:
        return self.get_sheet(define.ActionTimeline)

    @cached_property
    def action_timeline_move_sheet(self) -> Sheet[define.ActionTimelineMove]:
        return self.get_sheet(define.ActionTimelineMove)

    @cached_property
    def action_timeline_replace_sheet(self) -> Sheet[define.ActionTimelineReplace]:
        return self.get_sheet(define.ActionTimelineReplace)

    @cached_property
    def action_transient_sheet(self) -> Sheet[define.ActionTransient]:
        return self.get_sheet(define.ActionTransient)

    @cached_property
    def activity_feed_buttons_sheet(self) -> Sheet[define.ActivityFeedButtons]:
        return self.get_sheet(define.ActivityFeedButtons)

    @cached_property
    def activity_feed_captions_sheet(self) -> Sheet[define.ActivityFeedCaptions]:
        return self.get_sheet(define.ActivityFeedCaptions)

    @cached_property
    def activity_feed_group_captions_sheet(self) -> Sheet[define.ActivityFeedGroupCaptions]:
        return self.get_sheet(define.ActivityFeedGroupCaptions)

    @cached_property
    def activity_feed_images_sheet(self) -> Sheet[define.ActivityFeedImages]:
        return self.get_sheet(define.ActivityFeedImages)

    @cached_property
    def addon_sheet(self) -> Sheet[define.Addon]:
        return self.get_sheet(define.Addon)

    @cached_property
    def addon_hud_size_sheet(self) -> Sheet[define.AddonHudSize]:
        return self.get_sheet(define.AddonHudSize)

    @cached_property
    def addon_layout_sheet(self) -> Sheet[define.AddonLayout]:
        return self.get_sheet(define.AddonLayout)

    @cached_property
    def addon_param_sheet(self) -> Sheet[define.AddonParam]:
        return self.get_sheet(define.AddonParam)

    @cached_property
    def addon_talk_param_sheet(self) -> Sheet[define.AddonTalkParam]:
        return self.get_sheet(define.AddonTalkParam)

    @cached_property
    def addon_transient_sheet(self) -> Sheet[define.AddonTransient]:
        return self.get_sheet(define.AddonTransient)

    @cached_property
    def advanced_vibration_sheet(self) -> Sheet[define.AdvancedVibration]:
        return self.get_sheet(define.AdvancedVibration)

    @cached_property
    def adventure_sheet(self) -> Sheet[define.Adventure]:
        return self.get_sheet(define.Adventure)

    @cached_property
    def adventure_ex_phase_sheet(self) -> Sheet[define.AdventureExPhase]:
        return self.get_sheet(define.AdventureExPhase)

    @cached_property
    def aether_current_sheet(self) -> Sheet[define.AetherCurrent]:
        return self.get_sheet(define.AetherCurrent)

    @cached_property
    def aether_current_comp_flg_set_sheet(self) -> Sheet[define.AetherCurrentCompFlgSet]:
        return self.get_sheet(define.AetherCurrentCompFlgSet)

    @cached_property
    def aetherial_wheel_sheet(self) -> Sheet[define.AetherialWheel]:
        return self.get_sheet(define.AetherialWheel)

    @cached_property
    def aetheryte_sheet(self) -> Sheet[define.Aetheryte]:
        return self.get_sheet(define.Aetheryte)

    @cached_property
    def aetheryte_system_define_sheet(self) -> Sheet[define.AetheryteSystemDefine]:
        return self.get_sheet(define.AetheryteSystemDefine)

    @cached_property
    def aetheryte_transient_sheet(self) -> Sheet[define.AetheryteTransient]:
        return self.get_sheet(define.AetheryteTransient)

    @cached_property
    def airship_exploration_level_sheet(self) -> Sheet[define.AirshipExplorationLevel]:
        return self.get_sheet(define.AirshipExplorationLevel)

    @cached_property
    def airship_exploration_log_sheet(self) -> Sheet[define.AirshipExplorationLog]:
        return self.get_sheet(define.AirshipExplorationLog)

    @cached_property
    def airship_exploration_param_type_sheet(self) -> Sheet[define.AirshipExplorationParamType]:
        return self.get_sheet(define.AirshipExplorationParamType)

    @cached_property
    def airship_exploration_part_sheet(self) -> Sheet[define.AirshipExplorationPart]:
        return self.get_sheet(define.AirshipExplorationPart)

    @cached_property
    def airship_exploration_point_sheet(self) -> Sheet[define.AirshipExplorationPoint]:
        return self.get_sheet(define.AirshipExplorationPoint)

    @cached_property
    def airship_sky_island_sheet(self) -> Sheet[define.AirshipSkyIsland]:
        return self.get_sheet(define.AirshipSkyIsland)

    @cached_property
    def akatsuki_note_sheet(self) -> Sheet[SubDataRow[define.AkatsukiNote]]:
        return self.get_sheet(define.AkatsukiNote)

    @cached_property
    def akatsuki_note_string_sheet(self) -> Sheet[define.AkatsukiNoteString]:
        return self.get_sheet(define.AkatsukiNoteString)

    @cached_property
    def anima_weapon5_sheet(self) -> Sheet[define.AnimaWeapon5]:
        return self.get_sheet(define.AnimaWeapon5)

    @cached_property
    def anima_weapon5_param_sheet(self) -> Sheet[define.AnimaWeapon5Param]:
        return self.get_sheet(define.AnimaWeapon5Param)

    @cached_property
    def anima_weapon5_pattern_group_sheet(self) -> Sheet[define.AnimaWeapon5PatternGroup]:
        return self.get_sheet(define.AnimaWeapon5PatternGroup)

    @cached_property
    def anima_weapon5_spirit_talk_sheet(self) -> Sheet[SubDataRow[define.AnimaWeapon5SpiritTalk]]:
        return self.get_sheet(define.AnimaWeapon5SpiritTalk)

    @cached_property
    def anima_weapon5_spirit_talk_param_sheet(self) -> Sheet[define.AnimaWeapon5SpiritTalkParam]:
        return self.get_sheet(define.AnimaWeapon5SpiritTalkParam)

    @cached_property
    def anima_weapon5_spirit_talk_type_sheet(self) -> Sheet[define.AnimaWeapon5SpiritTalkType]:
        return self.get_sheet(define.AnimaWeapon5SpiritTalkType)

    @cached_property
    def anima_weapon5_trade_item_sheet(self) -> Sheet[define.AnimaWeapon5TradeItem]:
        return self.get_sheet(define.AnimaWeapon5TradeItem)

    @cached_property
    def anima_weapon_fui_talk_sheet(self) -> Sheet[SubDataRow[define.AnimaWeaponFUITalk]]:
        return self.get_sheet(define.AnimaWeaponFUITalk)

    @cached_property
    def anima_weapon_fui_talk_param_sheet(self) -> Sheet[define.AnimaWeaponFUITalkParam]:
        return self.get_sheet(define.AnimaWeaponFUITalkParam)

    @cached_property
    def anima_weapon_icon_sheet(self) -> Sheet[define.AnimaWeaponIcon]:
        return self.get_sheet(define.AnimaWeaponIcon)

    @cached_property
    def anima_weapon_item_sheet(self) -> Sheet[define.AnimaWeaponItem]:
        return self.get_sheet(define.AnimaWeaponItem)

    @cached_property
    def animation_lod_sheet(self) -> Sheet[define.AnimationLOD]:
        return self.get_sheet(define.AnimationLOD)

    @cached_property
    def aoz_action_sheet(self) -> Sheet[define.AozAction]:
        return self.get_sheet(define.AozAction)

    @cached_property
    def aoz_action_transient_sheet(self) -> Sheet[define.AozActionTransient]:
        return self.get_sheet(define.AozActionTransient)

    @cached_property
    def aquarium_fish_sheet(self) -> Sheet[define.AquariumFish]:
        return self.get_sheet(define.AquariumFish)

    @cached_property
    def aquarium_water_sheet(self) -> Sheet[define.AquariumWater]:
        return self.get_sheet(define.AquariumWater)

    @cached_property
    def archive_item_sheet(self) -> Sheet[SubDataRow[define.ArchiveItem]]:
        return self.get_sheet(define.ArchiveItem)

    @cached_property
    def array_event_handler_sheet(self) -> Sheet[define.ArrayEventHandler]:
        return self.get_sheet(define.ArrayEventHandler)

    @cached_property
    def attack_type_sheet(self) -> Sheet[define.AttackType]:
        return self.get_sheet(define.AttackType)

    @cached_property
    def attract_sheet(self) -> Sheet[define.Attract]:
        return self.get_sheet(define.Attract)

    @cached_property
    def attributive_sheet(self) -> Sheet[define.Attributive]:
        return self.get_sheet(define.Attributive)

    @cached_property
    def bgm_sheet(self) -> Sheet[define.BGM]:
        return self.get_sheet(define.BGM)

    @cached_property
    def bgm_fade_sheet(self) -> Sheet[define.BGMFade]:
        return self.get_sheet(define.BGMFade)

    @cached_property
    def bgm_fade_type_sheet(self) -> Sheet[define.BGMFadeType]:
        return self.get_sheet(define.BGMFadeType)

    @cached_property
    def bgm_scene_sheet(self) -> Sheet[define.BGMScene]:
        return self.get_sheet(define.BGMScene)

    @cached_property
    def bgm_situation_sheet(self) -> Sheet[define.BGMSituation]:
        return self.get_sheet(define.BGMSituation)

    @cached_property
    def bgm_switch_sheet(self) -> Sheet[SubDataRow[define.BGMSwitch]]:
        return self.get_sheet(define.BGMSwitch)

    @cached_property
    def bgm_system_define_sheet(self) -> Sheet[define.BGMSystemDefine]:
        return self.get_sheet(define.BGMSystemDefine)

    @cached_property
    def bkje_obj_sheet(self) -> Sheet[define.BKJEObj]:
        return self.get_sheet(define.BKJEObj)

    @cached_property
    def bkj_livestock_sheet(self) -> Sheet[define.BKJLivestock]:
        return self.get_sheet(define.BKJLivestock)

    @cached_property
    def bkj_pouch_sheet(self) -> Sheet[define.BKJPouch]:
        return self.get_sheet(define.BKJPouch)

    @cached_property
    def bkj_seed_sheet(self) -> Sheet[define.BKJSeed]:
        return self.get_sheet(define.BKJSeed)

    @cached_property
    def bkj_shipment_sheet(self) -> Sheet[define.BKJShipment]:
        return self.get_sheet(define.BKJShipment)

    @cached_property
    def bkj_specialty_goods_sheet(self) -> Sheet[define.BKJSpecialtyGoods]:
        return self.get_sheet(define.BKJSpecialtyGoods)

    @cached_property
    def b_npc_announce_icon_sheet(self) -> Sheet[define.BNpcAnnounceIcon]:
        return self.get_sheet(define.BNpcAnnounceIcon)

    @cached_property
    def b_npc_base_sheet(self) -> Sheet[define.BNpcBase]:
        return self.get_sheet(define.BNpcBase)

    @cached_property
    def b_npc_base_pop_vfx_sheet(self) -> Sheet[define.BNpcBasePopVfx]:
        return self.get_sheet(define.BNpcBasePopVfx)

    @cached_property
    def b_npc_customize_sheet(self) -> Sheet[define.BNpcCustomize]:
        return self.get_sheet(define.BNpcCustomize)

    @cached_property
    def b_npc_name_sheet(self) -> Sheet[define.BNpcName]:
        return self.get_sheet(define.BNpcName)

    @cached_property
    def b_npc_parts_sheet(self) -> Sheet[define.BNpcParts]:
        return self.get_sheet(define.BNpcParts)

    @cached_property
    def b_npc_state_sheet(self) -> Sheet[define.BNpcState]:
        return self.get_sheet(define.BNpcState)

    @cached_property
    def backlight_color_sheet(self) -> Sheet[define.BacklightColor]:
        return self.get_sheet(define.BacklightColor)

    @cached_property
    def ballista_sheet(self) -> Sheet[define.Ballista]:
        return self.get_sheet(define.Ballista)

    @cached_property
    def balloon_sheet(self) -> Sheet[define.Balloon]:
        return self.get_sheet(define.Balloon)

    @cached_property
    def banner_bg_sheet(self) -> Sheet[define.BannerBg]:
        return self.get_sheet(define.BannerBg)

    @cached_property
    def banner_condition_sheet(self) -> Sheet[define.BannerCondition]:
        return self.get_sheet(define.BannerCondition)

    @cached_property
    def banner_decoration_sheet(self) -> Sheet[define.BannerDecoration]:
        return self.get_sheet(define.BannerDecoration)

    @cached_property
    def banner_design_preset_sheet(self) -> Sheet[define.BannerDesignPreset]:
        return self.get_sheet(define.BannerDesignPreset)

    @cached_property
    def banner_facial_sheet(self) -> Sheet[define.BannerFacial]:
        return self.get_sheet(define.BannerFacial)

    @cached_property
    def banner_frame_sheet(self) -> Sheet[define.BannerFrame]:
        return self.get_sheet(define.BannerFrame)

    @cached_property
    def banner_obtain_hint_type_sheet(self) -> Sheet[define.BannerObtainHintType]:
        return self.get_sheet(define.BannerObtainHintType)

    @cached_property
    def banner_preset_sheet(self) -> Sheet[define.BannerPreset]:
        return self.get_sheet(define.BannerPreset)

    @cached_property
    def banner_timeline_sheet(self) -> Sheet[define.BannerTimeline]:
        return self.get_sheet(define.BannerTimeline)

    @cached_property
    def base_param_sheet(self) -> Sheet[define.BaseParam]:
        return self.get_sheet(define.BaseParam)

    @cached_property
    def battalion_sheet(self) -> Sheet[define.Battalion]:
        return self.get_sheet(define.Battalion)

    @cached_property
    def battle_leve_sheet(self) -> Sheet[define.BattleLeve]:
        return self.get_sheet(define.BattleLeve)

    @cached_property
    def battle_leve_rule_sheet(self) -> Sheet[define.BattleLeveRule]:
        return self.get_sheet(define.BattleLeveRule)

    @cached_property
    def beast_rank_bonus_sheet(self) -> Sheet[define.BeastRankBonus]:
        return self.get_sheet(define.BeastRankBonus)

    @cached_property
    def beast_reputation_rank_sheet(self) -> Sheet[define.BeastReputationRank]:
        return self.get_sheet(define.BeastReputationRank)

    @cached_property
    def beast_tribe_sheet(self) -> Sheet[define.BeastTribe]:
        return self.get_sheet(define.BeastTribe)

    @cached_property
    def behavior_sheet(self) -> Sheet[SubDataRow[define.Behavior]]:
        return self.get_sheet(define.Behavior)

    @cached_property
    def behavior_move_sheet(self) -> Sheet[define.BehaviorMove]:
        return self.get_sheet(define.BehaviorMove)

    @cached_property
    def behavior_path_sheet(self) -> Sheet[define.BehaviorPath]:
        return self.get_sheet(define.BehaviorPath)

    @cached_property
    def benchmark_cut_scene_table_sheet(self) -> Sheet[define.BenchmarkCutSceneTable]:
        return self.get_sheet(define.BenchmarkCutSceneTable)

    @cached_property
    def benchmark_override_equipment_sheet(self) -> Sheet[define.BenchmarkOverrideEquipment]:
        return self.get_sheet(define.BenchmarkOverrideEquipment)

    @cached_property
    def bgc_army_action_sheet(self) -> Sheet[define.BgcArmyAction]:
        return self.get_sheet(define.BgcArmyAction)

    @cached_property
    def bgc_army_action_transient_sheet(self) -> Sheet[define.BgcArmyActionTransient]:
        return self.get_sheet(define.BgcArmyActionTransient)

    @cached_property
    def booster_sheet(self) -> Sheet[define.Booster]:
        return self.get_sheet(define.Booster)

    @cached_property
    def buddy_sheet(self) -> Sheet[define.Buddy]:
        return self.get_sheet(define.Buddy)

    @cached_property
    def buddy_action_sheet(self) -> Sheet[define.BuddyAction]:
        return self.get_sheet(define.BuddyAction)

    @cached_property
    def buddy_equip_sheet(self) -> Sheet[define.BuddyEquip]:
        return self.get_sheet(define.BuddyEquip)

    @cached_property
    def buddy_item_sheet(self) -> Sheet[define.BuddyItem]:
        return self.get_sheet(define.BuddyItem)

    @cached_property
    def buddy_rank_sheet(self) -> Sheet[define.BuddyRank]:
        return self.get_sheet(define.BuddyRank)

    @cached_property
    def buddy_skill_sheet(self) -> Sheet[define.BuddySkill]:
        return self.get_sheet(define.BuddySkill)

    @cached_property
    def cabinet_sheet(self) -> Sheet[define.Cabinet]:
        return self.get_sheet(define.Cabinet)

    @cached_property
    def cabinet_category_sheet(self) -> Sheet[define.CabinetCategory]:
        return self.get_sheet(define.CabinetCategory)

    @cached_property
    def calendar_sheet(self) -> Sheet[define.Calendar]:
        return self.get_sheet(define.Calendar)

    @cached_property
    def carry_sheet(self) -> Sheet[define.Carry]:
        return self.get_sheet(define.Carry)

    @cached_property
    def channeling_sheet(self) -> Sheet[define.Channeling]:
        return self.get_sheet(define.Channeling)

    @cached_property
    def chara_card_base_sheet(self) -> Sheet[define.CharaCardBase]:
        return self.get_sheet(define.CharaCardBase)

    @cached_property
    def chara_card_decoration_sheet(self) -> Sheet[define.CharaCardDecoration]:
        return self.get_sheet(define.CharaCardDecoration)

    @cached_property
    def chara_card_design_preset_sheet(self) -> Sheet[define.CharaCardDesignPreset]:
        return self.get_sheet(define.CharaCardDesignPreset)

    @cached_property
    def chara_card_design_type_sheet(self) -> Sheet[define.CharaCardDesignType]:
        return self.get_sheet(define.CharaCardDesignType)

    @cached_property
    def chara_card_header_sheet(self) -> Sheet[define.CharaCardHeader]:
        return self.get_sheet(define.CharaCardHeader)

    @cached_property
    def chara_card_play_style_sheet(self) -> Sheet[define.CharaCardPlayStyle]:
        return self.get_sheet(define.CharaCardPlayStyle)

    @cached_property
    def chara_make_class_equip_sheet(self) -> Sheet[define.CharaMakeClassEquip]:
        return self.get_sheet(define.CharaMakeClassEquip)

    @cached_property
    def chara_make_customize_sheet(self) -> Sheet[define.CharaMakeCustomize]:
        return self.get_sheet(define.CharaMakeCustomize)

    @cached_property
    def chara_make_name_sheet(self) -> Sheet[define.CharaMakeName]:
        return self.get_sheet(define.CharaMakeName)

    @cached_property
    def chara_make_type_sheet(self) -> Sheet[define.CharaMakeType]:
        return self.get_sheet(define.CharaMakeType)

    @cached_property
    def chocobo_race_sheet(self) -> Sheet[define.ChocoboRace]:
        return self.get_sheet(define.ChocoboRace)

    @cached_property
    def chocobo_race_ability_sheet(self) -> Sheet[define.ChocoboRaceAbility]:
        return self.get_sheet(define.ChocoboRaceAbility)

    @cached_property
    def chocobo_race_ability_type_sheet(self) -> Sheet[define.ChocoboRaceAbilityType]:
        return self.get_sheet(define.ChocoboRaceAbilityType)

    @cached_property
    def chocobo_race_calculate_param_sheet(self) -> Sheet[define.ChocoboRaceCalculateParam]:
        return self.get_sheet(define.ChocoboRaceCalculateParam)

    @cached_property
    def chocobo_race_challenge_sheet(self) -> Sheet[define.ChocoboRaceChallenge]:
        return self.get_sheet(define.ChocoboRaceChallenge)

    @cached_property
    def chocobo_race_item_sheet(self) -> Sheet[define.ChocoboRaceItem]:
        return self.get_sheet(define.ChocoboRaceItem)

    @cached_property
    def chocobo_race_rank_sheet(self) -> Sheet[define.ChocoboRaceRank]:
        return self.get_sheet(define.ChocoboRaceRank)

    @cached_property
    def chocobo_race_ranking_sheet(self) -> Sheet[define.ChocoboRaceRanking]:
        return self.get_sheet(define.ChocoboRaceRanking)

    @cached_property
    def chocobo_race_status_sheet(self) -> Sheet[define.ChocoboRaceStatus]:
        return self.get_sheet(define.ChocoboRaceStatus)

    @cached_property
    def chocobo_race_territory_sheet(self) -> Sheet[define.ChocoboRaceTerritory]:
        return self.get_sheet(define.ChocoboRaceTerritory)

    @cached_property
    def chocobo_race_tutorial_sheet(self) -> Sheet[define.ChocoboRaceTutorial]:
        return self.get_sheet(define.ChocoboRaceTutorial)

    @cached_property
    def chocobo_race_weather_sheet(self) -> Sheet[define.ChocoboRaceWeather]:
        return self.get_sheet(define.ChocoboRaceWeather)

    @cached_property
    def chocobo_taxi_sheet(self) -> Sheet[define.ChocoboTaxi]:
        return self.get_sheet(define.ChocoboTaxi)

    @cached_property
    def chocobo_taxi_stand_sheet(self) -> Sheet[define.ChocoboTaxiStand]:
        return self.get_sheet(define.ChocoboTaxiStand)

    @cached_property
    def circle_activity_sheet(self) -> Sheet[define.CircleActivity]:
        return self.get_sheet(define.CircleActivity)

    @cached_property
    def class_job_sheet(self) -> Sheet[define.ClassJob]:
        return self.get_sheet(define.ClassJob)

    @cached_property
    def class_job_action_sort_sheet(self) -> Sheet[define.ClassJobActionSort]:
        return self.get_sheet(define.ClassJobActionSort)

    @cached_property
    def class_job_category_sheet(self) -> Sheet[define.ClassJobCategory]:
        return self.get_sheet(define.ClassJobCategory)

    @cached_property
    def class_job_resident_sheet(self) -> Sheet[SubDataRow[define.ClassJobResident]]:
        return self.get_sheet(define.ClassJobResident)

    @cached_property
    def collectables_shop_sheet(self) -> Sheet[define.CollectablesShop]:
        return self.get_sheet(define.CollectablesShop)

    @cached_property
    def collectables_shop_item_sheet(self) -> Sheet[SubDataRow[define.CollectablesShopItem]]:
        return self.get_sheet(define.CollectablesShopItem)

    @cached_property
    def collectables_shop_item_group_sheet(self) -> Sheet[define.CollectablesShopItemGroup]:
        return self.get_sheet(define.CollectablesShopItemGroup)

    @cached_property
    def collectables_shop_refine_sheet(self) -> Sheet[define.CollectablesShopRefine]:
        return self.get_sheet(define.CollectablesShopRefine)

    @cached_property
    def collectables_shop_reward_item_sheet(self) -> Sheet[define.CollectablesShopRewardItem]:
        return self.get_sheet(define.CollectablesShopRewardItem)

    @cached_property
    def collectables_shop_reward_scrip_sheet(self) -> Sheet[define.CollectablesShopRewardScrip]:
        return self.get_sheet(define.CollectablesShopRewardScrip)

    @cached_property
    def collision_id_pallet_sheet(self) -> Sheet[define.CollisionIdPallet]:
        return self.get_sheet(define.CollisionIdPallet)

    @cached_property
    def color_filter_sheet(self) -> Sheet[define.ColorFilter]:
        return self.get_sheet(define.ColorFilter)

    @cached_property
    def colosseum_sheet(self) -> Sheet[define.Colosseum]:
        return self.get_sheet(define.Colosseum)

    @cached_property
    def colosseum_match_rank_sheet(self) -> Sheet[define.ColosseumMatchRank]:
        return self.get_sheet(define.ColosseumMatchRank)

    @cached_property
    def companion_sheet(self) -> Sheet[define.Companion]:
        return self.get_sheet(define.Companion)

    @cached_property
    def companion_move_sheet(self) -> Sheet[define.CompanionMove]:
        return self.get_sheet(define.CompanionMove)

    @cached_property
    def companion_transient_sheet(self) -> Sheet[define.CompanionTransient]:
        return self.get_sheet(define.CompanionTransient)

    @cached_property
    def company_action_sheet(self) -> Sheet[define.CompanyAction]:
        return self.get_sheet(define.CompanyAction)

    @cached_property
    def company_craft_draft_sheet(self) -> Sheet[define.CompanyCraftDraft]:
        return self.get_sheet(define.CompanyCraftDraft)

    @cached_property
    def company_craft_draft_category_sheet(self) -> Sheet[define.CompanyCraftDraftCategory]:
        return self.get_sheet(define.CompanyCraftDraftCategory)

    @cached_property
    def company_craft_manufactory_state_sheet(self) -> Sheet[define.CompanyCraftManufactoryState]:
        return self.get_sheet(define.CompanyCraftManufactoryState)

    @cached_property
    def company_craft_part_sheet(self) -> Sheet[define.CompanyCraftPart]:
        return self.get_sheet(define.CompanyCraftPart)

    @cached_property
    def company_craft_process_sheet(self) -> Sheet[define.CompanyCraftProcess]:
        return self.get_sheet(define.CompanyCraftProcess)

    @cached_property
    def company_craft_sequence_sheet(self) -> Sheet[define.CompanyCraftSequence]:
        return self.get_sheet(define.CompanyCraftSequence)

    @cached_property
    def company_craft_supply_item_sheet(self) -> Sheet[define.CompanyCraftSupplyItem]:
        return self.get_sheet(define.CompanyCraftSupplyItem)

    @cached_property
    def company_craft_type_sheet(self) -> Sheet[define.CompanyCraftType]:
        return self.get_sheet(define.CompanyCraftType)

    @cached_property
    def company_leve_sheet(self) -> Sheet[define.CompanyLeve]:
        return self.get_sheet(define.CompanyLeve)

    @cached_property
    def company_leve_rule_sheet(self) -> Sheet[define.CompanyLeveRule]:
        return self.get_sheet(define.CompanyLeveRule)

    @cached_property
    def complete_journal_sheet(self) -> Sheet[define.CompleteJournal]:
        return self.get_sheet(define.CompleteJournal)

    @cached_property
    def complete_journal_category_sheet(self) -> Sheet[define.CompleteJournalCategory]:
        return self.get_sheet(define.CompleteJournalCategory)

    @cached_property
    def completion_sheet(self) -> Sheet[define.Completion]:
        return self.get_sheet(define.Completion)

    @cached_property
    def condition_sheet(self) -> Sheet[define.Condition]:
        return self.get_sheet(define.Condition)

    @cached_property
    def config_key_sheet(self) -> Sheet[define.ConfigKey]:
        return self.get_sheet(define.ConfigKey)

    @cached_property
    def content_attribute_rect_sheet(self) -> Sheet[define.ContentAttributeRect]:
        return self.get_sheet(define.ContentAttributeRect)

    @cached_property
    def content_close_cycle_sheet(self) -> Sheet[define.ContentCloseCycle]:
        return self.get_sheet(define.ContentCloseCycle)

    @cached_property
    def content_director_managed_sg_sheet(self) -> Sheet[SubDataRow[define.ContentDirectorManagedSG]]:
        return self.get_sheet(define.ContentDirectorManagedSG)

    @cached_property
    def content_effective_time_sheet(self) -> Sheet[define.ContentEffectiveTime]:
        return self.get_sheet(define.ContentEffectiveTime)

    @cached_property
    def content_entry_sheet(self) -> Sheet[define.ContentEntry]:
        return self.get_sheet(define.ContentEntry)

    @cached_property
    def content_event_item_sheet(self) -> Sheet[SubDataRow[define.ContentEventItem]]:
        return self.get_sheet(define.ContentEventItem)

    @cached_property
    def content_ex_action_sheet(self) -> Sheet[define.ContentExAction]:
        return self.get_sheet(define.ContentExAction)

    @cached_property
    def content_finder_condition_sheet(self) -> Sheet[define.ContentFinderCondition]:
        return self.get_sheet(define.ContentFinderCondition)

    @cached_property
    def content_finder_condition_transient_sheet(self) -> Sheet[define.ContentFinderConditionTransient]:
        return self.get_sheet(define.ContentFinderConditionTransient)

    @cached_property
    def content_gauge_sheet(self) -> Sheet[define.ContentGauge]:
        return self.get_sheet(define.ContentGauge)

    @cached_property
    def content_gauge_color_sheet(self) -> Sheet[define.ContentGaugeColor]:
        return self.get_sheet(define.ContentGaugeColor)

    @cached_property
    def content_member_type_sheet(self) -> Sheet[define.ContentMemberType]:
        return self.get_sheet(define.ContentMemberType)

    @cached_property
    def content_npc_talk_sheet(self) -> Sheet[define.ContentNpcTalk]:
        return self.get_sheet(define.ContentNpcTalk)

    @cached_property
    def content_random_select_sheet(self) -> Sheet[SubDataRow[define.ContentRandomSelect]]:
        return self.get_sheet(define.ContentRandomSelect)

    @cached_property
    def content_reward_condition_sheet(self) -> Sheet[define.ContentRewardCondition]:
        return self.get_sheet(define.ContentRewardCondition)

    @cached_property
    def content_roulette_sheet(self) -> Sheet[define.ContentRoulette]:
        return self.get_sheet(define.ContentRoulette)

    @cached_property
    def content_roulette_open_rule_sheet(self) -> Sheet[define.ContentRouletteOpenRule]:
        return self.get_sheet(define.ContentRouletteOpenRule)

    @cached_property
    def content_roulette_role_bonus_sheet(self) -> Sheet[define.ContentRouletteRoleBonus]:
        return self.get_sheet(define.ContentRouletteRoleBonus)

    @cached_property
    def content_talk_sheet(self) -> Sheet[define.ContentTalk]:
        return self.get_sheet(define.ContentTalk)

    @cached_property
    def content_talk_param_sheet(self) -> Sheet[define.ContentTalkParam]:
        return self.get_sheet(define.ContentTalkParam)

    @cached_property
    def content_todo_sheet(self) -> Sheet[SubDataRow[define.ContentTodo]]:
        return self.get_sheet(define.ContentTodo)

    @cached_property
    def content_tourism_construct_sheet(self) -> Sheet[SubDataRow[define.ContentTourismConstruct]]:
        return self.get_sheet(define.ContentTourismConstruct)

    @cached_property
    def content_type_sheet(self) -> Sheet[define.ContentType]:
        return self.get_sheet(define.ContentType)

    @cached_property
    def content_ui_category_sheet(self) -> Sheet[define.ContentUICategory]:
        return self.get_sheet(define.ContentUICategory)

    @cached_property
    def contents_note_sheet(self) -> Sheet[define.ContentsNote]:
        return self.get_sheet(define.ContentsNote)

    @cached_property
    def contents_note_category_sheet(self) -> Sheet[define.ContentsNoteCategory]:
        return self.get_sheet(define.ContentsNoteCategory)

    @cached_property
    def contents_note_level_sheet(self) -> Sheet[define.ContentsNoteLevel]:
        return self.get_sheet(define.ContentsNoteLevel)

    @cached_property
    def contents_note_reward_eureka_exp_sheet(self) -> Sheet[define.ContentsNoteRewardEurekaEXP]:
        return self.get_sheet(define.ContentsNoteRewardEurekaEXP)

    @cached_property
    def contents_tutorial_sheet(self) -> Sheet[define.ContentsTutorial]:
        return self.get_sheet(define.ContentsTutorial)

    @cached_property
    def contents_tutorial_page_sheet(self) -> Sheet[define.ContentsTutorialPage]:
        return self.get_sheet(define.ContentsTutorialPage)

    @cached_property
    def craft_action_sheet(self) -> Sheet[define.CraftAction]:
        return self.get_sheet(define.CraftAction)

    @cached_property
    def craft_leve_sheet(self) -> Sheet[define.CraftLeve]:
        return self.get_sheet(define.CraftLeve)

    @cached_property
    def craft_leve_talk_sheet(self) -> Sheet[define.CraftLeveTalk]:
        return self.get_sheet(define.CraftLeveTalk)

    @cached_property
    def craft_level_difference_sheet(self) -> Sheet[define.CraftLevelDifference]:
        return self.get_sheet(define.CraftLevelDifference)

    @cached_property
    def craft_type_sheet(self) -> Sheet[define.CraftType]:
        return self.get_sheet(define.CraftType)

    @cached_property
    def credit_sheet(self) -> Sheet[SubDataRow[define.Credit]]:
        return self.get_sheet(define.Credit)

    @cached_property
    def credit_back_image_sheet(self) -> Sheet[SubDataRow[define.CreditBackImage]]:
        return self.get_sheet(define.CreditBackImage)

    @cached_property
    def credit_cast_sheet(self) -> Sheet[define.CreditCast]:
        return self.get_sheet(define.CreditCast)

    @cached_property
    def credit_data_set_sheet(self) -> Sheet[define.CreditDataSet]:
        return self.get_sheet(define.CreditDataSet)

    @cached_property
    def credit_font_sheet(self) -> Sheet[define.CreditFont]:
        return self.get_sheet(define.CreditFont)

    @cached_property
    def credit_list_sheet(self) -> Sheet[SubDataRow[define.CreditList]]:
        return self.get_sheet(define.CreditList)

    @cached_property
    def credit_list_text_sheet(self) -> Sheet[define.CreditListText]:
        return self.get_sheet(define.CreditListText)

    @cached_property
    def credit_version_sheet(self) -> Sheet[define.CreditVersion]:
        return self.get_sheet(define.CreditVersion)

    @cached_property
    def currency_scrip_convert_sheet(self) -> Sheet[define.CurrencyScripConvert]:
        return self.get_sheet(define.CurrencyScripConvert)

    @cached_property
    def custom_talk_sheet(self) -> Sheet[define.CustomTalk]:
        return self.get_sheet(define.CustomTalk)

    @cached_property
    def custom_talk_nest_handlers_sheet(self) -> Sheet[SubDataRow[define.CustomTalkNestHandlers]]:
        return self.get_sheet(define.CustomTalkNestHandlers)

    @cached_property
    def custom_talk_resident_sheet(self) -> Sheet[define.CustomTalkResident]:
        return self.get_sheet(define.CustomTalkResident)

    @cached_property
    def cut_action_timeline_sheet(self) -> Sheet[define.CutActionTimeline]:
        return self.get_sheet(define.CutActionTimeline)

    @cached_property
    def cut_scene_incomp_quest_sheet(self) -> Sheet[SubDataRow[define.CutSceneIncompQuest]]:
        return self.get_sheet(define.CutSceneIncompQuest)

    @cached_property
    def cut_screen_image_sheet(self) -> Sheet[define.CutScreenImage]:
        return self.get_sheet(define.CutScreenImage)

    @cached_property
    def cutscene_sheet(self) -> Sheet[define.Cutscene]:
        return self.get_sheet(define.Cutscene)

    @cached_property
    def cutscene_actor_size_sheet(self) -> Sheet[define.CutsceneActorSize]:
        return self.get_sheet(define.CutsceneActorSize)

    @cached_property
    def cutscene_event_motion_sheet(self) -> Sheet[define.CutsceneEventMotion]:
        return self.get_sheet(define.CutsceneEventMotion)

    @cached_property
    def cutscene_motion_sheet(self) -> Sheet[define.CutsceneMotion]:
        return self.get_sheet(define.CutsceneMotion)

    @cached_property
    def cutscene_name_sheet(self) -> Sheet[define.CutsceneName]:
        return self.get_sheet(define.CutsceneName)

    @cached_property
    def cutscene_work_index_sheet(self) -> Sheet[define.CutsceneWorkIndex]:
        return self.get_sheet(define.CutsceneWorkIndex)

    @cached_property
    def cycle_time_sheet(self) -> Sheet[define.CycleTime]:
        return self.get_sheet(define.CycleTime)

    @cached_property
    def daily_supply_item_sheet(self) -> Sheet[define.DailySupplyItem]:
        return self.get_sheet(define.DailySupplyItem)

    @cached_property
    def dawn_content_sheet(self) -> Sheet[define.DawnContent]:
        return self.get_sheet(define.DawnContent)

    @cached_property
    def dawn_content_participable_sheet(self) -> Sheet[SubDataRow[define.DawnContentParticipable]]:
        return self.get_sheet(define.DawnContentParticipable)

    @cached_property
    def dawn_grow_member_sheet(self) -> Sheet[define.DawnGrowMember]:
        return self.get_sheet(define.DawnGrowMember)

    @cached_property
    def dawn_member_sheet(self) -> Sheet[define.DawnMember]:
        return self.get_sheet(define.DawnMember)

    @cached_property
    def dawn_member_ui_param_sheet(self) -> Sheet[define.DawnMemberUIParam]:
        return self.get_sheet(define.DawnMemberUIParam)

    @cached_property
    def dawn_quest_member_sheet(self) -> Sheet[define.DawnQuestMember]:
        return self.get_sheet(define.DawnQuestMember)

    @cached_property
    def deep_dungeon_sheet(self) -> Sheet[define.DeepDungeon]:
        return self.get_sheet(define.DeepDungeon)

    @cached_property
    def deep_dungeon_ban_sheet(self) -> Sheet[define.DeepDungeonBan]:
        return self.get_sheet(define.DeepDungeonBan)

    @cached_property
    def deep_dungeon_danger_sheet(self) -> Sheet[define.DeepDungeonDanger]:
        return self.get_sheet(define.DeepDungeonDanger)

    @cached_property
    def deep_dungeon_equipment_sheet(self) -> Sheet[define.DeepDungeonEquipment]:
        return self.get_sheet(define.DeepDungeonEquipment)

    @cached_property
    def deep_dungeon_floor_effect_ui_sheet(self) -> Sheet[define.DeepDungeonFloorEffectUI]:
        return self.get_sheet(define.DeepDungeonFloorEffectUI)

    @cached_property
    def deep_dungeon_grow_data_sheet(self) -> Sheet[define.DeepDungeonGrowData]:
        return self.get_sheet(define.DeepDungeonGrowData)

    @cached_property
    def deep_dungeon_item_sheet(self) -> Sheet[define.DeepDungeonItem]:
        return self.get_sheet(define.DeepDungeonItem)

    @cached_property
    def deep_dungeon_layer_sheet(self) -> Sheet[define.DeepDungeonLayer]:
        return self.get_sheet(define.DeepDungeonLayer)

    @cached_property
    def deep_dungeon_magic_stone_sheet(self) -> Sheet[define.DeepDungeonMagicStone]:
        return self.get_sheet(define.DeepDungeonMagicStone)

    @cached_property
    def deep_dungeon_map5_x_sheet(self) -> Sheet[SubDataRow[define.DeepDungeonMap5X]]:
        return self.get_sheet(define.DeepDungeonMap5X)

    @cached_property
    def deep_dungeon_room_sheet(self) -> Sheet[define.DeepDungeonRoom]:
        return self.get_sheet(define.DeepDungeonRoom)

    @cached_property
    def deep_dungeon_status_sheet(self) -> Sheet[define.DeepDungeonStatus]:
        return self.get_sheet(define.DeepDungeonStatus)

    @cached_property
    def default_talk_sheet(self) -> Sheet[define.DefaultTalk]:
        return self.get_sheet(define.DefaultTalk)

    @cached_property
    def default_talk_lip_sync_type_sheet(self) -> Sheet[define.DefaultTalkLipSyncType]:
        return self.get_sheet(define.DefaultTalkLipSyncType)

    @cached_property
    def delivery_quest_sheet(self) -> Sheet[define.DeliveryQuest]:
        return self.get_sheet(define.DeliveryQuest)

    @cached_property
    def description_sheet(self) -> Sheet[define.Description]:
        return self.get_sheet(define.Description)

    @cached_property
    def description_page_sheet(self) -> Sheet[SubDataRow[define.DescriptionPage]]:
        return self.get_sheet(define.DescriptionPage)

    @cached_property
    def description_section_sheet(self) -> Sheet[SubDataRow[define.DescriptionSection]]:
        return self.get_sheet(define.DescriptionSection)

    @cached_property
    def description_stand_alone_sheet(self) -> Sheet[define.DescriptionStandAlone]:
        return self.get_sheet(define.DescriptionStandAlone)

    @cached_property
    def description_stand_alone_transient_sheet(self) -> Sheet[define.DescriptionStandAloneTransient]:
        return self.get_sheet(define.DescriptionStandAloneTransient)

    @cached_property
    def description_string_sheet(self) -> Sheet[define.DescriptionString]:
        return self.get_sheet(define.DescriptionString)

    @cached_property
    def director_system_define_sheet(self) -> Sheet[define.DirectorSystemDefine]:
        return self.get_sheet(define.DirectorSystemDefine)

    @cached_property
    def director_type_sheet(self) -> Sheet[define.DirectorType]:
        return self.get_sheet(define.DirectorType)

    @cached_property
    def disposal_shop_sheet(self) -> Sheet[define.DisposalShop]:
        return self.get_sheet(define.DisposalShop)

    @cached_property
    def disposal_shop_filter_type_sheet(self) -> Sheet[define.DisposalShopFilterType]:
        return self.get_sheet(define.DisposalShopFilterType)

    @cached_property
    def disposal_shop_item_sheet(self) -> Sheet[SubDataRow[define.DisposalShopItem]]:
        return self.get_sheet(define.DisposalShopItem)

    @cached_property
    def doma_story_progress_sheet(self) -> Sheet[define.DomaStoryProgress]:
        return self.get_sheet(define.DomaStoryProgress)

    @cached_property
    def dps_challenge_sheet(self) -> Sheet[define.DpsChallenge]:
        return self.get_sheet(define.DpsChallenge)

    @cached_property
    def dps_challenge_officer_sheet(self) -> Sheet[define.DpsChallengeOfficer]:
        return self.get_sheet(define.DpsChallengeOfficer)

    @cached_property
    def dps_challenge_transient_sheet(self) -> Sheet[define.DpsChallengeTransient]:
        return self.get_sheet(define.DpsChallengeTransient)

    @cached_property
    def dynamic_event_sheet(self) -> Sheet[define.DynamicEvent]:
        return self.get_sheet(define.DynamicEvent)

    @cached_property
    def dynamic_event_enemy_type_sheet(self) -> Sheet[define.DynamicEventEnemyType]:
        return self.get_sheet(define.DynamicEventEnemyType)

    @cached_property
    def dynamic_event_manager_sheet(self) -> Sheet[define.DynamicEventManager]:
        return self.get_sheet(define.DynamicEventManager)

    @cached_property
    def dynamic_event_set_sheet(self) -> Sheet[SubDataRow[define.DynamicEventSet]]:
        return self.get_sheet(define.DynamicEventSet)

    @cached_property
    def dynamic_event_single_battle_sheet(self) -> Sheet[define.DynamicEventSingleBattle]:
        return self.get_sheet(define.DynamicEventSingleBattle)

    @cached_property
    def dynamic_event_type_sheet(self) -> Sheet[define.DynamicEventType]:
        return self.get_sheet(define.DynamicEventType)

    @cached_property
    def e_npc_base_sheet(self) -> Sheet[define.ENpcBase]:
        return self.get_sheet(define.ENpcBase)

    @cached_property
    def e_npc_dress_up_sheet(self) -> Sheet[define.ENpcDressUp]:
        return self.get_sheet(define.ENpcDressUp)

    @cached_property
    def e_npc_dress_up_dress_sheet(self) -> Sheet[SubDataRow[define.ENpcDressUpDress]]:
        return self.get_sheet(define.ENpcDressUpDress)

    @cached_property
    def e_npc_resident_sheet(self) -> Sheet[define.ENpcResident]:
        return self.get_sheet(define.ENpcResident)

    @cached_property
    def e_obj_sheet(self) -> Sheet[define.EObj]:
        return self.get_sheet(define.EObj)

    @cached_property
    def e_obj_name_sheet(self) -> Sheet[define.EObjName]:
        return self.get_sheet(define.EObjName)

    @cached_property
    def emj_addon_sheet(self) -> Sheet[define.EmjAddon]:
        return self.get_sheet(define.EmjAddon)

    @cached_property
    def emj_chara_view_camera_sheet(self) -> Sheet[define.EmjCharaViewCamera]:
        return self.get_sheet(define.EmjCharaViewCamera)

    @cached_property
    def emj_dani_sheet(self) -> Sheet[define.EmjDani]:
        return self.get_sheet(define.EmjDani)

    @cached_property
    def emote_sheet(self) -> Sheet[define.Emote]:
        return self.get_sheet(define.Emote)

    @cached_property
    def emote_category_sheet(self) -> Sheet[define.EmoteCategory]:
        return self.get_sheet(define.EmoteCategory)

    @cached_property
    def emote_mode_sheet(self) -> Sheet[define.EmoteMode]:
        return self.get_sheet(define.EmoteMode)

    @cached_property
    def emote_transient_sheet(self) -> Sheet[define.EmoteTransient]:
        return self.get_sheet(define.EmoteTransient)

    @cached_property
    def equip_race_category_sheet(self) -> Sheet[define.EquipRaceCategory]:
        return self.get_sheet(define.EquipRaceCategory)

    @cached_property
    def equip_slot_category_sheet(self) -> Sheet[define.EquipSlotCategory]:
        return self.get_sheet(define.EquipSlotCategory)

    @cached_property
    def error_sheet(self) -> Sheet[define.Error]:
        return self.get_sheet(define.Error)

    @cached_property
    def eureka_sheet(self) -> Sheet[define.Eureka]:
        return self.get_sheet(define.Eureka)

    @cached_property
    def eureka_aether_item_sheet(self) -> Sheet[define.EurekaAetherItem]:
        return self.get_sheet(define.EurekaAetherItem)

    @cached_property
    def eureka_aethernet_sheet(self) -> Sheet[define.EurekaAethernet]:
        return self.get_sheet(define.EurekaAethernet)

    @cached_property
    def eureka_dungeon_portal_sheet(self) -> Sheet[SubDataRow[define.EurekaDungeonPortal]]:
        return self.get_sheet(define.EurekaDungeonPortal)

    @cached_property
    def eureka_grow_data_sheet(self) -> Sheet[define.EurekaGrowData]:
        return self.get_sheet(define.EurekaGrowData)

    @cached_property
    def eureka_logos_mixer_probability_sheet(self) -> Sheet[define.EurekaLogosMixerProbability]:
        return self.get_sheet(define.EurekaLogosMixerProbability)

    @cached_property
    def eureka_magia_action_sheet(self) -> Sheet[define.EurekaMagiaAction]:
        return self.get_sheet(define.EurekaMagiaAction)

    @cached_property
    def eureka_magicite_item_sheet(self) -> Sheet[define.EurekaMagiciteItem]:
        return self.get_sheet(define.EurekaMagiciteItem)

    @cached_property
    def eureka_magicite_item_type_sheet(self) -> Sheet[define.EurekaMagiciteItemType]:
        return self.get_sheet(define.EurekaMagiciteItemType)

    @cached_property
    def eureka_sphere_element_adjust_sheet(self) -> Sheet[define.EurekaSphereElementAdjust]:
        return self.get_sheet(define.EurekaSphereElementAdjust)

    @cached_property
    def eureka_story_progress_sheet(self) -> Sheet[define.EurekaStoryProgress]:
        return self.get_sheet(define.EurekaStoryProgress)

    @cached_property
    def event_action_sheet(self) -> Sheet[define.EventAction]:
        return self.get_sheet(define.EventAction)

    @cached_property
    def event_custom_icon_type_sheet(self) -> Sheet[define.EventCustomIconType]:
        return self.get_sheet(define.EventCustomIconType)

    @cached_property
    def event_icon_priority_sheet(self) -> Sheet[define.EventIconPriority]:
        return self.get_sheet(define.EventIconPriority)

    @cached_property
    def event_icon_type_sheet(self) -> Sheet[define.EventIconType]:
        return self.get_sheet(define.EventIconType)

    @cached_property
    def event_item_sheet(self) -> Sheet[define.EventItem]:
        return self.get_sheet(define.EventItem)

    @cached_property
    def event_item_cast_timeline_sheet(self) -> Sheet[define.EventItemCastTimeline]:
        return self.get_sheet(define.EventItemCastTimeline)

    @cached_property
    def event_item_category_sheet(self) -> Sheet[define.EventItemCategory]:
        return self.get_sheet(define.EventItemCategory)

    @cached_property
    def event_item_help_sheet(self) -> Sheet[define.EventItemHelp]:
        return self.get_sheet(define.EventItemHelp)

    @cached_property
    def event_item_timeline_sheet(self) -> Sheet[define.EventItemTimeline]:
        return self.get_sheet(define.EventItemTimeline)

    @cached_property
    def event_path_move_sheet(self) -> Sheet[define.EventPathMove]:
        return self.get_sheet(define.EventPathMove)

    @cached_property
    def event_situation_icon_tooltip_sheet(self) -> Sheet[define.EventSituationIconTooltip]:
        return self.get_sheet(define.EventSituationIconTooltip)

    @cached_property
    def event_system_define_sheet(self) -> Sheet[define.EventSystemDefine]:
        return self.get_sheet(define.EventSystemDefine)

    @cached_property
    def event_vfx_sheet(self) -> Sheet[define.EventVfx]:
        return self.get_sheet(define.EventVfx)

    @cached_property
    def ex_hotbar_crossbar_index_type_sheet(self) -> Sheet[define.ExHotbarCrossbarIndexType]:
        return self.get_sheet(define.ExHotbarCrossbarIndexType)

    @cached_property
    def ex_version_sheet(self) -> Sheet[define.ExVersion]:
        return self.get_sheet(define.ExVersion)

    @cached_property
    def exported_gathering_point_sheet(self) -> Sheet[define.ExportedGatheringPoint]:
        return self.get_sheet(define.ExportedGatheringPoint)

    @cached_property
    def exported_sg_sheet(self) -> Sheet[define.ExportedSG]:
        return self.get_sheet(define.ExportedSG)

    @cached_property
    def extra_command_sheet(self) -> Sheet[define.ExtraCommand]:
        return self.get_sheet(define.ExtraCommand)

    @cached_property
    def fc_activity_sheet(self) -> Sheet[define.FCActivity]:
        return self.get_sheet(define.FCActivity)

    @cached_property
    def fc_activity_category_sheet(self) -> Sheet[define.FCActivityCategory]:
        return self.get_sheet(define.FCActivityCategory)

    @cached_property
    def fc_authority_sheet(self) -> Sheet[define.FCAuthority]:
        return self.get_sheet(define.FCAuthority)

    @cached_property
    def fc_authority_category_sheet(self) -> Sheet[define.FCAuthorityCategory]:
        return self.get_sheet(define.FCAuthorityCategory)

    @cached_property
    def fc_chest_name_sheet(self) -> Sheet[define.FCChestName]:
        return self.get_sheet(define.FCChestName)

    @cached_property
    def fc_crest_symbol_sheet(self) -> Sheet[define.FCCrestSymbol]:
        return self.get_sheet(define.FCCrestSymbol)

    @cached_property
    def fc_define_sheet(self) -> Sheet[define.FCDefine]:
        return self.get_sheet(define.FCDefine)

    @cached_property
    def fc_hierarchy_sheet(self) -> Sheet[define.FCHierarchy]:
        return self.get_sheet(define.FCHierarchy)

    @cached_property
    def fc_profile_sheet(self) -> Sheet[define.FCProfile]:
        return self.get_sheet(define.FCProfile)

    @cached_property
    def fc_rank_sheet(self) -> Sheet[define.FCRank]:
        return self.get_sheet(define.FCRank)

    @cached_property
    def fc_reputation_sheet(self) -> Sheet[define.FCReputation]:
        return self.get_sheet(define.FCReputation)

    @cached_property
    def fc_rights_sheet(self) -> Sheet[define.FCRights]:
        return self.get_sheet(define.FCRights)

    @cached_property
    def fashion_check_theme_category_sheet(self) -> Sheet[define.FashionCheckThemeCategory]:
        return self.get_sheet(define.FashionCheckThemeCategory)

    @cached_property
    def fashion_check_weekly_theme_sheet(self) -> Sheet[define.FashionCheckWeeklyTheme]:
        return self.get_sheet(define.FashionCheckWeeklyTheme)

    @cached_property
    def fate_sheet(self) -> Sheet[define.Fate]:
        return self.get_sheet(define.Fate)

    @cached_property
    def fate_event_sheet(self) -> Sheet[define.FateEvent]:
        return self.get_sheet(define.FateEvent)

    @cached_property
    def fate_mode_sheet(self) -> Sheet[define.FateMode]:
        return self.get_sheet(define.FateMode)

    @cached_property
    def fate_progress_ui_sheet(self) -> Sheet[define.FateProgressUI]:
        return self.get_sheet(define.FateProgressUI)

    @cached_property
    def fate_rule_ex_sheet(self) -> Sheet[define.FateRuleEx]:
        return self.get_sheet(define.FateRuleEx)

    @cached_property
    def fate_shop_sheet(self) -> Sheet[define.FateShop]:
        return self.get_sheet(define.FateShop)

    @cached_property
    def fate_token_type_sheet(self) -> Sheet[define.FateTokenType]:
        return self.get_sheet(define.FateTokenType)

    @cached_property
    def fcc_shop_sheet(self) -> Sheet[define.FccShop]:
        return self.get_sheet(define.FccShop)

    @cached_property
    def festival_sheet(self) -> Sheet[define.Festival]:
        return self.get_sheet(define.Festival)

    @cached_property
    def field_marker_sheet(self) -> Sheet[define.FieldMarker]:
        return self.get_sheet(define.FieldMarker)

    @cached_property
    def fish_parameter_sheet(self) -> Sheet[define.FishParameter]:
        return self.get_sheet(define.FishParameter)

    @cached_property
    def fish_parameter_reverse_sheet(self) -> Sheet[define.FishParameterReverse]:
        return self.get_sheet(define.FishParameterReverse)

    @cached_property
    def fishing_record_type_sheet(self) -> Sheet[define.FishingRecordType]:
        return self.get_sheet(define.FishingRecordType)

    @cached_property
    def fishing_record_type_transient_sheet(self) -> Sheet[define.FishingRecordTypeTransient]:
        return self.get_sheet(define.FishingRecordTypeTransient)

    @cached_property
    def fishing_spot_sheet(self) -> Sheet[define.FishingSpot]:
        return self.get_sheet(define.FishingSpot)

    @cached_property
    def fitting_shop_sheet(self) -> Sheet[define.FittingShop]:
        return self.get_sheet(define.FittingShop)

    @cached_property
    def fitting_shop_category_sheet(self) -> Sheet[define.FittingShopCategory]:
        return self.get_sheet(define.FittingShopCategory)

    @cached_property
    def fitting_shop_category_item_sheet(self) -> Sheet[SubDataRow[define.FittingShopCategoryItem]]:
        return self.get_sheet(define.FittingShopCategoryItem)

    @cached_property
    def fitting_shop_item_set_sheet(self) -> Sheet[define.FittingShopItemSet]:
        return self.get_sheet(define.FittingShopItemSet)

    @cached_property
    def frontline_sheet(self) -> Sheet[define.Frontline]:
        return self.get_sheet(define.Frontline)

    @cached_property
    def frontline01_sheet(self) -> Sheet[define.Frontline01]:
        return self.get_sheet(define.Frontline01)

    @cached_property
    def frontline02_sheet(self) -> Sheet[define.Frontline02]:
        return self.get_sheet(define.Frontline02)

    @cached_property
    def frontline03_sheet(self) -> Sheet[define.Frontline03]:
        return self.get_sheet(define.Frontline03)

    @cached_property
    def frontline04_sheet(self) -> Sheet[define.Frontline04]:
        return self.get_sheet(define.Frontline04)

    @cached_property
    def furniture_catalog_category_sheet(self) -> Sheet[define.FurnitureCatalogCategory]:
        return self.get_sheet(define.FurnitureCatalogCategory)

    @cached_property
    def furniture_catalog_item_list_sheet(self) -> Sheet[define.FurnitureCatalogItemList]:
        return self.get_sheet(define.FurnitureCatalogItemList)

    @cached_property
    def gc_rank_gridania_female_text_sheet(self) -> Sheet[define.GCRankGridaniaFemaleText]:
        return self.get_sheet(define.GCRankGridaniaFemaleText)

    @cached_property
    def gc_rank_gridania_male_text_sheet(self) -> Sheet[define.GCRankGridaniaMaleText]:
        return self.get_sheet(define.GCRankGridaniaMaleText)

    @cached_property
    def gc_rank_limsa_female_text_sheet(self) -> Sheet[define.GCRankLimsaFemaleText]:
        return self.get_sheet(define.GCRankLimsaFemaleText)

    @cached_property
    def gc_rank_limsa_male_text_sheet(self) -> Sheet[define.GCRankLimsaMaleText]:
        return self.get_sheet(define.GCRankLimsaMaleText)

    @cached_property
    def gc_rank_uldah_female_text_sheet(self) -> Sheet[define.GCRankUldahFemaleText]:
        return self.get_sheet(define.GCRankUldahFemaleText)

    @cached_property
    def gc_rank_uldah_male_text_sheet(self) -> Sheet[define.GCRankUldahMaleText]:
        return self.get_sheet(define.GCRankUldahMaleText)

    @cached_property
    def gc_scrip_shop_category_sheet(self) -> Sheet[define.GCScripShopCategory]:
        return self.get_sheet(define.GCScripShopCategory)

    @cached_property
    def gc_scrip_shop_item_sheet(self) -> Sheet[SubDataRow[define.GCScripShopItem]]:
        return self.get_sheet(define.GCScripShopItem)

    @cached_property
    def gc_shop_sheet(self) -> Sheet[define.GCShop]:
        return self.get_sheet(define.GCShop)

    @cached_property
    def gc_shop_item_category_sheet(self) -> Sheet[define.GCShopItemCategory]:
        return self.get_sheet(define.GCShopItemCategory)

    @cached_property
    def gc_supply_define_sheet(self) -> Sheet[define.GCSupplyDefine]:
        return self.get_sheet(define.GCSupplyDefine)

    @cached_property
    def gc_supply_duty_sheet(self) -> Sheet[define.GCSupplyDuty]:
        return self.get_sheet(define.GCSupplyDuty)

    @cached_property
    def gc_supply_duty_reward_sheet(self) -> Sheet[define.GCSupplyDutyReward]:
        return self.get_sheet(define.GCSupplyDutyReward)

    @cached_property
    def gfate_sheet(self) -> Sheet[define.GFATE]:
        return self.get_sheet(define.GFATE)

    @cached_property
    def g_fate_climbing_sheet(self) -> Sheet[define.GFateClimbing]:
        return self.get_sheet(define.GFateClimbing)

    @cached_property
    def g_fate_climbing2_sheet(self) -> Sheet[define.GFateClimbing2]:
        return self.get_sheet(define.GFateClimbing2)

    @cached_property
    def g_fate_climbing2_content_sheet(self) -> Sheet[define.GFateClimbing2Content]:
        return self.get_sheet(define.GFateClimbing2Content)

    @cached_property
    def g_fate_climbing2_totem_type_sheet(self) -> Sheet[define.GFateClimbing2TotemType]:
        return self.get_sheet(define.GFateClimbing2TotemType)

    @cached_property
    def g_fate_dance_sheet(self) -> Sheet[define.GFateDance]:
        return self.get_sheet(define.GFateDance)

    @cached_property
    def g_fate_hidden_object_sheet(self) -> Sheet[define.GFateHiddenObject]:
        return self.get_sheet(define.GFateHiddenObject)

    @cached_property
    def g_fate_ride_shooting_sheet(self) -> Sheet[define.GFateRideShooting]:
        return self.get_sheet(define.GFateRideShooting)

    @cached_property
    def g_fate_roulette_sheet(self) -> Sheet[define.GFateRoulette]:
        return self.get_sheet(define.GFateRoulette)

    @cached_property
    def g_fate_stelth_sheet(self) -> Sheet[define.GFateStelth]:
        return self.get_sheet(define.GFateStelth)

    @cached_property
    def game_reward_obtain_type_sheet(self) -> Sheet[define.GameRewardObtainType]:
        return self.get_sheet(define.GameRewardObtainType)

    @cached_property
    def gardening_seed_sheet(self) -> Sheet[define.GardeningSeed]:
        return self.get_sheet(define.GardeningSeed)

    @cached_property
    def gathering_condition_sheet(self) -> Sheet[define.GatheringCondition]:
        return self.get_sheet(define.GatheringCondition)

    @cached_property
    def gathering_exp_sheet(self) -> Sheet[define.GatheringExp]:
        return self.get_sheet(define.GatheringExp)

    @cached_property
    def gathering_item_sheet(self) -> Sheet[define.GatheringItem]:
        return self.get_sheet(define.GatheringItem)

    @cached_property
    def gathering_item_level_convert_table_sheet(self) -> Sheet[define.GatheringItemLevelConvertTable]:
        return self.get_sheet(define.GatheringItemLevelConvertTable)

    @cached_property
    def gathering_item_point_sheet(self) -> Sheet[SubDataRow[define.GatheringItemPoint]]:
        return self.get_sheet(define.GatheringItemPoint)

    @cached_property
    def gathering_leve_sheet(self) -> Sheet[define.GatheringLeve]:
        return self.get_sheet(define.GatheringLeve)

    @cached_property
    def gathering_leve_b_npc_entry_sheet(self) -> Sheet[define.GatheringLeveBNpcEntry]:
        return self.get_sheet(define.GatheringLeveBNpcEntry)

    @cached_property
    def gathering_leve_route_sheet(self) -> Sheet[define.GatheringLeveRoute]:
        return self.get_sheet(define.GatheringLeveRoute)

    @cached_property
    def gathering_leve_rule_sheet(self) -> Sheet[define.GatheringLeveRule]:
        return self.get_sheet(define.GatheringLeveRule)

    @cached_property
    def gathering_notebook_item_sheet(self) -> Sheet[define.GatheringNotebookItem]:
        return self.get_sheet(define.GatheringNotebookItem)

    @cached_property
    def gathering_notebook_list_sheet(self) -> Sheet[define.GatheringNotebookList]:
        return self.get_sheet(define.GatheringNotebookList)

    @cached_property
    def gathering_point_sheet(self) -> Sheet[define.GatheringPoint]:
        return self.get_sheet(define.GatheringPoint)

    @cached_property
    def gathering_point_base_sheet(self) -> Sheet[define.GatheringPointBase]:
        return self.get_sheet(define.GatheringPointBase)

    @cached_property
    def gathering_point_bonus_sheet(self) -> Sheet[define.GatheringPointBonus]:
        return self.get_sheet(define.GatheringPointBonus)

    @cached_property
    def gathering_point_bonus_type_sheet(self) -> Sheet[define.GatheringPointBonusType]:
        return self.get_sheet(define.GatheringPointBonusType)

    @cached_property
    def gathering_point_name_sheet(self) -> Sheet[define.GatheringPointName]:
        return self.get_sheet(define.GatheringPointName)

    @cached_property
    def gathering_point_transient_sheet(self) -> Sheet[define.GatheringPointTransient]:
        return self.get_sheet(define.GatheringPointTransient)

    @cached_property
    def gathering_rare_pop_time_table_sheet(self) -> Sheet[define.GatheringRarePopTimeTable]:
        return self.get_sheet(define.GatheringRarePopTimeTable)

    @cached_property
    def gathering_sub_category_sheet(self) -> Sheet[define.GatheringSubCategory]:
        return self.get_sheet(define.GatheringSubCategory)

    @cached_property
    def gathering_type_sheet(self) -> Sheet[define.GatheringType]:
        return self.get_sheet(define.GatheringType)

    @cached_property
    def gc_army_candidate_category_sheet(self) -> Sheet[define.GcArmyCandidateCategory]:
        return self.get_sheet(define.GcArmyCandidateCategory)

    @cached_property
    def gc_army_capture_sheet(self) -> Sheet[define.GcArmyCapture]:
        return self.get_sheet(define.GcArmyCapture)

    @cached_property
    def gc_army_capture_tactics_sheet(self) -> Sheet[define.GcArmyCaptureTactics]:
        return self.get_sheet(define.GcArmyCaptureTactics)

    @cached_property
    def gc_army_equip_preset_sheet(self) -> Sheet[define.GcArmyEquipPreset]:
        return self.get_sheet(define.GcArmyEquipPreset)

    @cached_property
    def gc_army_expedition_sheet(self) -> Sheet[define.GcArmyExpedition]:
        return self.get_sheet(define.GcArmyExpedition)

    @cached_property
    def gc_army_expedition_member_bonus_sheet(self) -> Sheet[define.GcArmyExpeditionMemberBonus]:
        return self.get_sheet(define.GcArmyExpeditionMemberBonus)

    @cached_property
    def gc_army_expedition_trait_sheet(self) -> Sheet[define.GcArmyExpeditionTrait]:
        return self.get_sheet(define.GcArmyExpeditionTrait)

    @cached_property
    def gc_army_expedition_trait_cond_sheet(self) -> Sheet[define.GcArmyExpeditionTraitCond]:
        return self.get_sheet(define.GcArmyExpeditionTraitCond)

    @cached_property
    def gc_army_expedition_type_sheet(self) -> Sheet[define.GcArmyExpeditionType]:
        return self.get_sheet(define.GcArmyExpeditionType)

    @cached_property
    def gc_army_member_sheet(self) -> Sheet[define.GcArmyMember]:
        return self.get_sheet(define.GcArmyMember)

    @cached_property
    def gc_army_member_grow_sheet(self) -> Sheet[define.GcArmyMemberGrow]:
        return self.get_sheet(define.GcArmyMemberGrow)

    @cached_property
    def gc_army_member_grow_exp_sheet(self) -> Sheet[define.GcArmyMemberGrowExp]:
        return self.get_sheet(define.GcArmyMemberGrowExp)

    @cached_property
    def gc_army_progress_sheet(self) -> Sheet[define.GcArmyProgress]:
        return self.get_sheet(define.GcArmyProgress)

    @cached_property
    def gc_army_training_sheet(self) -> Sheet[define.GcArmyTraining]:
        return self.get_sheet(define.GcArmyTraining)

    @cached_property
    def general_action_sheet(self) -> Sheet[define.GeneralAction]:
        return self.get_sheet(define.GeneralAction)

    @cached_property
    def gil_shop_sheet(self) -> Sheet[define.GilShop]:
        return self.get_sheet(define.GilShop)

    @cached_property
    def gil_shop_info_sheet(self) -> Sheet[define.GilShopInfo]:
        return self.get_sheet(define.GilShopInfo)

    @cached_property
    def gil_shop_item_sheet(self) -> Sheet[SubDataRow[define.GilShopItem]]:
        return self.get_sheet(define.GilShopItem)

    @cached_property
    def gimmick_accessor_sheet(self) -> Sheet[define.GimmickAccessor]:
        return self.get_sheet(define.GimmickAccessor)

    @cached_property
    def gimmick_bill_sheet(self) -> Sheet[define.GimmickBill]:
        return self.get_sheet(define.GimmickBill)

    @cached_property
    def gimmick_jump_sheet(self) -> Sheet[define.GimmickJump]:
        return self.get_sheet(define.GimmickJump)

    @cached_property
    def gimmick_rect_sheet(self) -> Sheet[define.GimmickRect]:
        return self.get_sheet(define.GimmickRect)

    @cached_property
    def gimmick_talk_sheet(self) -> Sheet[define.GimmickTalk]:
        return self.get_sheet(define.GimmickTalk)

    @cached_property
    def gimmick_yes_no_sheet(self) -> Sheet[define.GimmickYesNo]:
        return self.get_sheet(define.GimmickYesNo)

    @cached_property
    def gold_saucer_arcade_machine_sheet(self) -> Sheet[define.GoldSaucerArcadeMachine]:
        return self.get_sheet(define.GoldSaucerArcadeMachine)

    @cached_property
    def gold_saucer_content_sheet(self) -> Sheet[define.GoldSaucerContent]:
        return self.get_sheet(define.GoldSaucerContent)

    @cached_property
    def gold_saucer_talk_sheet(self) -> Sheet[define.GoldSaucerTalk]:
        return self.get_sheet(define.GoldSaucerTalk)

    @cached_property
    def gold_saucer_text_data_sheet(self) -> Sheet[define.GoldSaucerTextData]:
        return self.get_sheet(define.GoldSaucerTextData)

    @cached_property
    def grand_company_sheet(self) -> Sheet[define.GrandCompany]:
        return self.get_sheet(define.GrandCompany)

    @cached_property
    def grand_company_rank_sheet(self) -> Sheet[define.GrandCompanyRank]:
        return self.get_sheet(define.GrandCompanyRank)

    @cached_property
    def group_pose_chara_status_sheet(self) -> Sheet[define.GroupPoseCharaStatus]:
        return self.get_sheet(define.GroupPoseCharaStatus)

    @cached_property
    def group_pose_character_show_preset_sheet(self) -> Sheet[define.GroupPoseCharacterShowPreset]:
        return self.get_sheet(define.GroupPoseCharacterShowPreset)

    @cached_property
    def group_pose_frame_sheet(self) -> Sheet[define.GroupPoseFrame]:
        return self.get_sheet(define.GroupPoseFrame)

    @cached_property
    def group_pose_stamp_sheet(self) -> Sheet[define.GroupPoseStamp]:
        return self.get_sheet(define.GroupPoseStamp)

    @cached_property
    def group_pose_stamp_category_sheet(self) -> Sheet[define.GroupPoseStampCategory]:
        return self.get_sheet(define.GroupPoseStampCategory)

    @cached_property
    def group_pose_stamp_font_color_sheet(self) -> Sheet[define.GroupPoseStampFontColor]:
        return self.get_sheet(define.GroupPoseStampFontColor)

    @cached_property
    def guardian_deity_sheet(self) -> Sheet[define.GuardianDeity]:
        return self.get_sheet(define.GuardianDeity)

    @cached_property
    def guide_sheet(self) -> Sheet[define.Guide]:
        return self.get_sheet(define.Guide)

    @cached_property
    def guide_page_sheet(self) -> Sheet[SubDataRow[define.GuidePage]]:
        return self.get_sheet(define.GuidePage)

    @cached_property
    def guide_page_string_sheet(self) -> Sheet[define.GuidePageString]:
        return self.get_sheet(define.GuidePageString)

    @cached_property
    def guide_title_sheet(self) -> Sheet[define.GuideTitle]:
        return self.get_sheet(define.GuideTitle)

    @cached_property
    def guild_order_sheet(self) -> Sheet[define.GuildOrder]:
        return self.get_sheet(define.GuildOrder)

    @cached_property
    def guild_order_guide_sheet(self) -> Sheet[define.GuildOrderGuide]:
        return self.get_sheet(define.GuildOrderGuide)

    @cached_property
    def guild_order_officer_sheet(self) -> Sheet[define.GuildOrderOfficer]:
        return self.get_sheet(define.GuildOrderOfficer)

    @cached_property
    def guildleve_assignment_sheet(self) -> Sheet[define.GuildleveAssignment]:
        return self.get_sheet(define.GuildleveAssignment)

    @cached_property
    def guildleve_assignment_category_sheet(self) -> Sheet[define.GuildleveAssignmentCategory]:
        return self.get_sheet(define.GuildleveAssignmentCategory)

    @cached_property
    def guildleve_assignment_talk_sheet(self) -> Sheet[define.GuildleveAssignmentTalk]:
        return self.get_sheet(define.GuildleveAssignmentTalk)

    @cached_property
    def guildleve_evaluation_sheet(self) -> Sheet[define.GuildleveEvaluation]:
        return self.get_sheet(define.GuildleveEvaluation)

    @cached_property
    def hwd_announce_sheet(self) -> Sheet[define.HWDAnnounce]:
        return self.get_sheet(define.HWDAnnounce)

    @cached_property
    def hwd_crafter_supply_sheet(self) -> Sheet[define.HWDCrafterSupply]:
        return self.get_sheet(define.HWDCrafterSupply)

    @cached_property
    def hwd_crafter_supply_reward_sheet(self) -> Sheet[define.HWDCrafterSupplyReward]:
        return self.get_sheet(define.HWDCrafterSupplyReward)

    @cached_property
    def hwd_crafter_supply_term_sheet(self) -> Sheet[define.HWDCrafterSupplyTerm]:
        return self.get_sheet(define.HWDCrafterSupplyTerm)

    @cached_property
    def hwd_dev_layer_control_sheet(self) -> Sheet[define.HWDDevLayerControl]:
        return self.get_sheet(define.HWDDevLayerControl)

    @cached_property
    def hwd_dev_level_ui_sheet(self) -> Sheet[define.HWDDevLevelUI]:
        return self.get_sheet(define.HWDDevLevelUI)

    @cached_property
    def hwd_dev_level_web_text_sheet(self) -> Sheet[define.HWDDevLevelWebText]:
        return self.get_sheet(define.HWDDevLevelWebText)

    @cached_property
    def hwd_dev_lively_sheet(self) -> Sheet[SubDataRow[define.HWDDevLively]]:
        return self.get_sheet(define.HWDDevLively)

    @cached_property
    def hwd_dev_progress_sheet(self) -> Sheet[define.HWDDevProgress]:
        return self.get_sheet(define.HWDDevProgress)

    @cached_property
    def hwd_gathere_inspect_term_sheet(self) -> Sheet[define.HWDGathereInspectTerm]:
        return self.get_sheet(define.HWDGathereInspectTerm)

    @cached_property
    def hwd_gatherer_inspection_sheet(self) -> Sheet[define.HWDGathererInspection]:
        return self.get_sheet(define.HWDGathererInspection)

    @cached_property
    def hwd_gatherer_inspection_reward_sheet(self) -> Sheet[define.HWDGathererInspectionReward]:
        return self.get_sheet(define.HWDGathererInspectionReward)

    @cached_property
    def hwd_info_board_article_sheet(self) -> Sheet[define.HWDInfoBoardArticle]:
        return self.get_sheet(define.HWDInfoBoardArticle)

    @cached_property
    def hwd_info_board_article_transient_sheet(self) -> Sheet[define.HWDInfoBoardArticleTransient]:
        return self.get_sheet(define.HWDInfoBoardArticleTransient)

    @cached_property
    def hwd_info_board_article_type_sheet(self) -> Sheet[define.HWDInfoBoardArticleType]:
        return self.get_sheet(define.HWDInfoBoardArticleType)

    @cached_property
    def hwd_info_board_back_number_sheet(self) -> Sheet[define.HWDInfoBoardBackNumber]:
        return self.get_sheet(define.HWDInfoBoardBackNumber)

    @cached_property
    def hwd_level_change_deception_sheet(self) -> Sheet[define.HWDLevelChangeDeception]:
        return self.get_sheet(define.HWDLevelChangeDeception)

    @cached_property
    def hwd_shared_group_sheet(self) -> Sheet[SubDataRow[define.HWDSharedGroup]]:
        return self.get_sheet(define.HWDSharedGroup)

    @cached_property
    def hwd_shared_group_control_param_sheet(self) -> Sheet[SubDataRow[define.HWDSharedGroupControlParam]]:
        return self.get_sheet(define.HWDSharedGroupControlParam)

    @cached_property
    def hair_make_type_sheet(self) -> Sheet[define.HairMakeType]:
        return self.get_sheet(define.HairMakeType)

    @cached_property
    def house_retainer_pose_sheet(self) -> Sheet[define.HouseRetainerPose]:
        return self.get_sheet(define.HouseRetainerPose)

    @cached_property
    def housing_aethernet_sheet(self) -> Sheet[define.HousingAethernet]:
        return self.get_sheet(define.HousingAethernet)

    @cached_property
    def housing_appeal_sheet(self) -> Sheet[define.HousingAppeal]:
        return self.get_sheet(define.HousingAppeal)

    @cached_property
    def housing_employment_npc_list_sheet(self) -> Sheet[SubDataRow[define.HousingEmploymentNpcList]]:
        return self.get_sheet(define.HousingEmploymentNpcList)

    @cached_property
    def housing_employment_npc_race_sheet(self) -> Sheet[define.HousingEmploymentNpcRace]:
        return self.get_sheet(define.HousingEmploymentNpcRace)

    @cached_property
    def housing_exterior_sheet(self) -> Sheet[define.HousingExterior]:
        return self.get_sheet(define.HousingExterior)

    @cached_property
    def housing_furniture_sheet(self) -> Sheet[define.HousingFurniture]:
        return self.get_sheet(define.HousingFurniture)

    @cached_property
    def housing_interior_sheet(self) -> Sheet[define.HousingInterior]:
        return self.get_sheet(define.HousingInterior)

    @cached_property
    def housing_land_set_sheet(self) -> Sheet[define.HousingLandSet]:
        return self.get_sheet(define.HousingLandSet)

    @cached_property
    def housing_map_marker_info_sheet(self) -> Sheet[SubDataRow[define.HousingMapMarkerInfo]]:
        return self.get_sheet(define.HousingMapMarkerInfo)

    @cached_property
    def housing_mate_authority_sheet(self) -> Sheet[define.HousingMateAuthority]:
        return self.get_sheet(define.HousingMateAuthority)

    @cached_property
    def housing_merchant_pose_sheet(self) -> Sheet[define.HousingMerchantPose]:
        return self.get_sheet(define.HousingMerchantPose)

    @cached_property
    def housing_pile_limit_sheet(self) -> Sheet[define.HousingPileLimit]:
        return self.get_sheet(define.HousingPileLimit)

    @cached_property
    def housing_placement_sheet(self) -> Sheet[define.HousingPlacement]:
        return self.get_sheet(define.HousingPlacement)

    @cached_property
    def housing_preset_sheet(self) -> Sheet[define.HousingPreset]:
        return self.get_sheet(define.HousingPreset)

    @cached_property
    def housing_training_doll_sheet(self) -> Sheet[define.HousingTrainingDoll]:
        return self.get_sheet(define.HousingTrainingDoll)

    @cached_property
    def housing_united_exterior_sheet(self) -> Sheet[define.HousingUnitedExterior]:
        return self.get_sheet(define.HousingUnitedExterior)

    @cached_property
    def housing_unplacement_sheet(self) -> Sheet[define.HousingUnplacement]:
        return self.get_sheet(define.HousingUnplacement)

    @cached_property
    def housing_yard_object_sheet(self) -> Sheet[define.HousingYardObject]:
        return self.get_sheet(define.HousingYardObject)

    @cached_property
    def how_to_sheet(self) -> Sheet[define.HowTo]:
        return self.get_sheet(define.HowTo)

    @cached_property
    def how_to_category_sheet(self) -> Sheet[define.HowToCategory]:
        return self.get_sheet(define.HowToCategory)

    @cached_property
    def how_to_page_sheet(self) -> Sheet[define.HowToPage]:
        return self.get_sheet(define.HowToPage)

    @cached_property
    def hud_sheet(self) -> Sheet[define.Hud]:
        return self.get_sheet(define.Hud)

    @cached_property
    def hud_transient_sheet(self) -> Sheet[define.HudTransient]:
        return self.get_sheet(define.HudTransient)

    @cached_property
    def huge_craftworks_npc_sheet(self) -> Sheet[define.HugeCraftworksNpc]:
        return self.get_sheet(define.HugeCraftworksNpc)

    @cached_property
    def huge_craftworks_rank_sheet(self) -> Sheet[define.HugeCraftworksRank]:
        return self.get_sheet(define.HugeCraftworksRank)

    @cached_property
    def ikd_content_bonus_sheet(self) -> Sheet[define.IKDContentBonus]:
        return self.get_sheet(define.IKDContentBonus)

    @cached_property
    def ikd_fish_param_sheet(self) -> Sheet[define.IKDFishParam]:
        return self.get_sheet(define.IKDFishParam)

    @cached_property
    def ikd_player_mission_condition_sheet(self) -> Sheet[define.IKDPlayerMissionCondition]:
        return self.get_sheet(define.IKDPlayerMissionCondition)

    @cached_property
    def ikd_route_sheet(self) -> Sheet[define.IKDRoute]:
        return self.get_sheet(define.IKDRoute)

    @cached_property
    def ikd_route_table_sheet(self) -> Sheet[define.IKDRouteTable]:
        return self.get_sheet(define.IKDRouteTable)

    @cached_property
    def ikd_spot_sheet(self) -> Sheet[define.IKDSpot]:
        return self.get_sheet(define.IKDSpot)

    @cached_property
    def ikd_time_define_sheet(self) -> Sheet[define.IKDTimeDefine]:
        return self.get_sheet(define.IKDTimeDefine)

    @cached_property
    def icon_language_sheet(self) -> Sheet[define.IconLanguage]:
        return self.get_sheet(define.IconLanguage)

    @cached_property
    def inclusion_shop_sheet(self) -> Sheet[define.InclusionShop]:
        return self.get_sheet(define.InclusionShop)

    @cached_property
    def inclusion_shop_category_sheet(self) -> Sheet[define.InclusionShopCategory]:
        return self.get_sheet(define.InclusionShopCategory)

    @cached_property
    def inclusion_shop_series_sheet(self) -> Sheet[SubDataRow[define.InclusionShopSeries]]:
        return self.get_sheet(define.InclusionShopSeries)

    @cached_property
    def inclusion_shop_welcom_sheet(self) -> Sheet[define.InclusionShopWelcom]:
        return self.get_sheet(define.InclusionShopWelcom)

    @cached_property
    def inclusion_shop_welcom_text_sheet(self) -> Sheet[define.InclusionShopWelcomText]:
        return self.get_sheet(define.InclusionShopWelcomText)

    @cached_property
    def individual_weather_sheet(self) -> Sheet[define.IndividualWeather]:
        return self.get_sheet(define.IndividualWeather)

    @cached_property
    def instance_content_sheet(self) -> Sheet[define.InstanceContent]:
        return self.get_sheet(define.InstanceContent)

    @cached_property
    def instance_content_buff_sheet(self) -> Sheet[define.InstanceContentBuff]:
        return self.get_sheet(define.InstanceContentBuff)

    @cached_property
    def instance_content_cs_bonus_sheet(self) -> Sheet[define.InstanceContentCSBonus]:
        return self.get_sheet(define.InstanceContentCSBonus)

    @cached_property
    def instance_content_guide_sheet(self) -> Sheet[define.InstanceContentGuide]:
        return self.get_sheet(define.InstanceContentGuide)

    @cached_property
    def instance_content_qic_data_sheet(self) -> Sheet[define.InstanceContentQICData]:
        return self.get_sheet(define.InstanceContentQICData)

    @cached_property
    def instance_content_reward_item_sheet(self) -> Sheet[define.InstanceContentRewardItem]:
        return self.get_sheet(define.InstanceContentRewardItem)

    @cached_property
    def instance_content_text_data_sheet(self) -> Sheet[define.InstanceContentTextData]:
        return self.get_sheet(define.InstanceContentTextData)

    @cached_property
    def instance_content_type_sheet(self) -> Sheet[define.InstanceContentType]:
        return self.get_sheet(define.InstanceContentType)

    @cached_property
    def item_sheet(self) -> Sheet[define.Item]:
        return self.get_sheet(define.Item)

    @cached_property
    def item_action_sheet(self) -> Sheet[define.ItemAction]:
        return self.get_sheet(define.ItemAction)

    @cached_property
    def item_action_telepo_sheet(self) -> Sheet[define.ItemActionTelepo]:
        return self.get_sheet(define.ItemActionTelepo)

    @cached_property
    def item_barter_check_sheet(self) -> Sheet[SubDataRow[define.ItemBarterCheck]]:
        return self.get_sheet(define.ItemBarterCheck)

    @cached_property
    def item_food_sheet(self) -> Sheet[define.ItemFood]:
        return self.get_sheet(define.ItemFood)

    @cached_property
    def item_level_sheet(self) -> Sheet[define.ItemLevel]:
        return self.get_sheet(define.ItemLevel)

    @cached_property
    def item_once_hq_masterpiece_sheet(self) -> Sheet[define.ItemOnceHqMasterpiece]:
        return self.get_sheet(define.ItemOnceHqMasterpiece)

    @cached_property
    def item_repair_price_sheet(self) -> Sheet[define.ItemRepairPrice]:
        return self.get_sheet(define.ItemRepairPrice)

    @cached_property
    def item_repair_resource_sheet(self) -> Sheet[define.ItemRepairResource]:
        return self.get_sheet(define.ItemRepairResource)

    @cached_property
    def item_retainer_level_up_sheet(self) -> Sheet[define.ItemRetainerLevelUp]:
        return self.get_sheet(define.ItemRetainerLevelUp)

    @cached_property
    def item_search_category_sheet(self) -> Sheet[define.ItemSearchCategory]:
        return self.get_sheet(define.ItemSearchCategory)

    @cached_property
    def item_series_sheet(self) -> Sheet[define.ItemSeries]:
        return self.get_sheet(define.ItemSeries)

    @cached_property
    def item_sort_category_sheet(self) -> Sheet[define.ItemSortCategory]:
        return self.get_sheet(define.ItemSortCategory)

    @cached_property
    def item_special_bonus_sheet(self) -> Sheet[define.ItemSpecialBonus]:
        return self.get_sheet(define.ItemSpecialBonus)

    @cached_property
    def item_stain_condition_sheet(self) -> Sheet[define.ItemStainCondition]:
        return self.get_sheet(define.ItemStainCondition)

    @cached_property
    def item_ui_category_sheet(self) -> Sheet[define.ItemUICategory]:
        return self.get_sheet(define.ItemUICategory)

    @cached_property
    def jigsaw_score_sheet(self) -> Sheet[define.JigsawScore]:
        return self.get_sheet(define.JigsawScore)

    @cached_property
    def jigsaw_time_bonus_sheet(self) -> Sheet[define.JigsawTimeBonus]:
        return self.get_sheet(define.JigsawTimeBonus)

    @cached_property
    def jingle_sheet(self) -> Sheet[define.Jingle]:
        return self.get_sheet(define.Jingle)

    @cached_property
    def job_hud_manual_sheet(self) -> Sheet[define.JobHudManual]:
        return self.get_sheet(define.JobHudManual)

    @cached_property
    def job_hud_manual_priority_sheet(self) -> Sheet[define.JobHudManualPriority]:
        return self.get_sheet(define.JobHudManualPriority)

    @cached_property
    def journal_category_sheet(self) -> Sheet[define.JournalCategory]:
        return self.get_sheet(define.JournalCategory)

    @cached_property
    def journal_genre_sheet(self) -> Sheet[define.JournalGenre]:
        return self.get_sheet(define.JournalGenre)

    @cached_property
    def journal_section_sheet(self) -> Sheet[define.JournalSection]:
        return self.get_sheet(define.JournalSection)

    @cached_property
    def knockback_sheet(self) -> Sheet[define.Knockback]:
        return self.get_sheet(define.Knockback)

    @cached_property
    def lfg_extension_content_sheet(self) -> Sheet[define.LFGExtensionContent]:
        return self.get_sheet(define.LFGExtensionContent)

    @cached_property
    def legacy_quest_sheet(self) -> Sheet[define.LegacyQuest]:
        return self.get_sheet(define.LegacyQuest)

    @cached_property
    def leve_sheet(self) -> Sheet[define.Leve]:
        return self.get_sheet(define.Leve)

    @cached_property
    def leve_assignment_type_sheet(self) -> Sheet[define.LeveAssignmentType]:
        return self.get_sheet(define.LeveAssignmentType)

    @cached_property
    def leve_client_sheet(self) -> Sheet[define.LeveClient]:
        return self.get_sheet(define.LeveClient)

    @cached_property
    def leve_reward_item_sheet(self) -> Sheet[define.LeveRewardItem]:
        return self.get_sheet(define.LeveRewardItem)

    @cached_property
    def leve_reward_item_group_sheet(self) -> Sheet[define.LeveRewardItemGroup]:
        return self.get_sheet(define.LeveRewardItemGroup)

    @cached_property
    def leve_string_sheet(self) -> Sheet[define.LeveString]:
        return self.get_sheet(define.LeveString)

    @cached_property
    def leve_system_define_sheet(self) -> Sheet[define.LeveSystemDefine]:
        return self.get_sheet(define.LeveSystemDefine)

    @cached_property
    def leve_vfx_sheet(self) -> Sheet[define.LeveVfx]:
        return self.get_sheet(define.LeveVfx)

    @cached_property
    def level_sheet(self) -> Sheet[define.Level]:
        return self.get_sheet(define.Level)

    @cached_property
    def link_race_sheet(self) -> Sheet[define.LinkRace]:
        return self.get_sheet(define.LinkRace)

    @cached_property
    def loading_image_sheet(self) -> Sheet[define.LoadingImage]:
        return self.get_sheet(define.LoadingImage)

    @cached_property
    def loading_tips_sheet(self) -> Sheet[define.LoadingTips]:
        return self.get_sheet(define.LoadingTips)

    @cached_property
    def loading_tips_sub_sheet(self) -> Sheet[define.LoadingTipsSub]:
        return self.get_sheet(define.LoadingTipsSub)

    @cached_property
    def lobby_sheet(self) -> Sheet[define.Lobby]:
        return self.get_sheet(define.Lobby)

    @cached_property
    def lockon_sheet(self) -> Sheet[define.Lockon]:
        return self.get_sheet(define.Lockon)

    @cached_property
    def log_filter_sheet(self) -> Sheet[define.LogFilter]:
        return self.get_sheet(define.LogFilter)

    @cached_property
    def log_kind_sheet(self) -> Sheet[define.LogKind]:
        return self.get_sheet(define.LogKind)

    @cached_property
    def log_message_sheet(self) -> Sheet[define.LogMessage]:
        return self.get_sheet(define.LogMessage)

    @cached_property
    def loot_mode_type_sheet(self) -> Sheet[define.LootModeType]:
        return self.get_sheet(define.LootModeType)

    @cached_property
    def lottery_exchange_shop_sheet(self) -> Sheet[define.LotteryExchangeShop]:
        return self.get_sheet(define.LotteryExchangeShop)

    @cached_property
    def mji_animals_sheet(self) -> Sheet[define.MJIAnimals]:
        return self.get_sheet(define.MJIAnimals)

    @cached_property
    def mji_building_sheet(self) -> Sheet[SubDataRow[define.MJIBuilding]]:
        return self.get_sheet(define.MJIBuilding)

    @cached_property
    def mji_building_place_sheet(self) -> Sheet[define.MJIBuildingPlace]:
        return self.get_sheet(define.MJIBuildingPlace)

    @cached_property
    def mji_craftworks_object_sheet(self) -> Sheet[define.MJICraftworksObject]:
        return self.get_sheet(define.MJICraftworksObject)

    @cached_property
    def mji_craftworks_object_theme_sheet(self) -> Sheet[define.MJICraftworksObjectTheme]:
        return self.get_sheet(define.MJICraftworksObjectTheme)

    @cached_property
    def mji_craftworks_popularity_sheet(self) -> Sheet[define.MJICraftworksPopularity]:
        return self.get_sheet(define.MJICraftworksPopularity)

    @cached_property
    def mji_craftworks_popularity_type_sheet(self) -> Sheet[define.MJICraftworksPopularityType]:
        return self.get_sheet(define.MJICraftworksPopularityType)

    @cached_property
    def mji_craftworks_rank_ratio_sheet(self) -> Sheet[define.MJICraftworksRankRatio]:
        return self.get_sheet(define.MJICraftworksRankRatio)

    @cached_property
    def mji_craftworks_supply_define_sheet(self) -> Sheet[define.MJICraftworksSupplyDefine]:
        return self.get_sheet(define.MJICraftworksSupplyDefine)

    @cached_property
    def mji_craftworks_tension_sheet(self) -> Sheet[define.MJICraftworksTension]:
        return self.get_sheet(define.MJICraftworksTension)

    @cached_property
    def mji_crop_seed_sheet(self) -> Sheet[define.MJICropSeed]:
        return self.get_sheet(define.MJICropSeed)

    @cached_property
    def mji_disposal_shop_item_sheet(self) -> Sheet[define.MJIDisposalShopItem]:
        return self.get_sheet(define.MJIDisposalShopItem)

    @cached_property
    def mji_disposal_shop_ui_category_sheet(self) -> Sheet[define.MJIDisposalShopUICategory]:
        return self.get_sheet(define.MJIDisposalShopUICategory)

    @cached_property
    def mji_farm_pasture_rank_sheet(self) -> Sheet[define.MJIFarmPastureRank]:
        return self.get_sheet(define.MJIFarmPastureRank)

    @cached_property
    def mji_function_sheet(self) -> Sheet[define.MJIFunction]:
        return self.get_sheet(define.MJIFunction)

    @cached_property
    def mji_gathering_sheet(self) -> Sheet[define.MJIGathering]:
        return self.get_sheet(define.MJIGathering)

    @cached_property
    def mji_gathering_item_sheet(self) -> Sheet[define.MJIGatheringItem]:
        return self.get_sheet(define.MJIGatheringItem)

    @cached_property
    def mji_gathering_object_sheet(self) -> Sheet[define.MJIGatheringObject]:
        return self.get_sheet(define.MJIGatheringObject)

    @cached_property
    def mji_gathering_tool_sheet(self) -> Sheet[define.MJIGatheringTool]:
        return self.get_sheet(define.MJIGatheringTool)

    @cached_property
    def mji_hud_mode_sheet(self) -> Sheet[define.MJIHudMode]:
        return self.get_sheet(define.MJIHudMode)

    @cached_property
    def mji_item_category_sheet(self) -> Sheet[define.MJIItemCategory]:
        return self.get_sheet(define.MJIItemCategory)

    @cached_property
    def mji_item_pouch_sheet(self) -> Sheet[define.MJIItemPouch]:
        return self.get_sheet(define.MJIItemPouch)

    @cached_property
    def mji_key_item_sheet(self) -> Sheet[define.MJIKeyItem]:
        return self.get_sheet(define.MJIKeyItem)

    @cached_property
    def mji_landmark_sheet(self) -> Sheet[define.MJILandmark]:
        return self.get_sheet(define.MJILandmark)

    @cached_property
    def mji_landmark_place_sheet(self) -> Sheet[define.MJILandmarkPlace]:
        return self.get_sheet(define.MJILandmarkPlace)

    @cached_property
    def mji_lively_actor_sheet(self) -> Sheet[SubDataRow[define.MJILivelyActor]]:
        return self.get_sheet(define.MJILivelyActor)

    @cached_property
    def mji_minion_pop_areas_sheet(self) -> Sheet[define.MJIMinionPopAreas]:
        return self.get_sheet(define.MJIMinionPopAreas)

    @cached_property
    def mji_progress_sheet(self) -> Sheet[define.MJIProgress]:
        return self.get_sheet(define.MJIProgress)

    @cached_property
    def mji_rank_sheet(self) -> Sheet[define.MJIRank]:
        return self.get_sheet(define.MJIRank)

    @cached_property
    def mji_recipe_sheet(self) -> Sheet[define.MJIRecipe]:
        return self.get_sheet(define.MJIRecipe)

    @cached_property
    def mji_recipe_material_sheet(self) -> Sheet[define.MJIRecipeMaterial]:
        return self.get_sheet(define.MJIRecipeMaterial)

    @cached_property
    def mji_stockyard_management_area_sheet(self) -> Sheet[define.MJIStockyardManagementArea]:
        return self.get_sheet(define.MJIStockyardManagementArea)

    @cached_property
    def mji_stockyard_management_table_sheet(self) -> Sheet[SubDataRow[define.MJIStockyardManagementTable]]:
        return self.get_sheet(define.MJIStockyardManagementTable)

    @cached_property
    def mji_text_sheet(self) -> Sheet[define.MJIText]:
        return self.get_sheet(define.MJIText)

    @cached_property
    def mji_village_appearance_sg_sheet(self) -> Sheet[define.MJIVillageAppearanceSG]:
        return self.get_sheet(define.MJIVillageAppearanceSG)

    @cached_property
    def mji_village_appearance_ui_sheet(self) -> Sheet[SubDataRow[define.MJIVillageAppearanceUI]]:
        return self.get_sheet(define.MJIVillageAppearanceUI)

    @cached_property
    def mji_village_development_sheet(self) -> Sheet[define.MJIVillageDevelopment]:
        return self.get_sheet(define.MJIVillageDevelopment)

    @cached_property
    def myc_temporary_item_sheet(self) -> Sheet[define.MYCTemporaryItem]:
        return self.get_sheet(define.MYCTemporaryItem)

    @cached_property
    def myc_temporary_item_ui_category_sheet(self) -> Sheet[define.MYCTemporaryItemUICategory]:
        return self.get_sheet(define.MYCTemporaryItemUICategory)

    @cached_property
    def myc_war_result_notebook_sheet(self) -> Sheet[define.MYCWarResultNotebook]:
        return self.get_sheet(define.MYCWarResultNotebook)

    @cached_property
    def macro_icon_sheet(self) -> Sheet[define.MacroIcon]:
        return self.get_sheet(define.MacroIcon)

    @cached_property
    def macro_icon_redirect_old_sheet(self) -> Sheet[define.MacroIconRedirectOld]:
        return self.get_sheet(define.MacroIconRedirectOld)

    @cached_property
    def main_command_sheet(self) -> Sheet[define.MainCommand]:
        return self.get_sheet(define.MainCommand)

    @cached_property
    def main_command_category_sheet(self) -> Sheet[define.MainCommandCategory]:
        return self.get_sheet(define.MainCommandCategory)

    @cached_property
    def maneuvers_sheet(self) -> Sheet[define.Maneuvers]:
        return self.get_sheet(define.Maneuvers)

    @cached_property
    def maneuvers_armor_sheet(self) -> Sheet[define.ManeuversArmor]:
        return self.get_sheet(define.ManeuversArmor)

    @cached_property
    def map_sheet(self) -> Sheet[define.Map]:
        return self.get_sheet(define.Map)

    @cached_property
    def map_condition_sheet(self) -> Sheet[define.MapCondition]:
        return self.get_sheet(define.MapCondition)

    @cached_property
    def map_exclusive_sheet(self) -> Sheet[define.MapExclusive]:
        return self.get_sheet(define.MapExclusive)

    @cached_property
    def map_marker_sheet(self) -> Sheet[SubDataRow[define.MapMarker]]:
        return self.get_sheet(define.MapMarker)

    @cached_property
    def map_marker_region_sheet(self) -> Sheet[define.MapMarkerRegion]:
        return self.get_sheet(define.MapMarkerRegion)

    @cached_property
    def map_symbol_sheet(self) -> Sheet[define.MapSymbol]:
        return self.get_sheet(define.MapSymbol)

    @cached_property
    def map_transient_pvp_map_sheet(self) -> Sheet[define.MapTransientPvPMap]:
        return self.get_sheet(define.MapTransientPvPMap)

    @cached_property
    def map_type_sheet(self) -> Sheet[define.MapType]:
        return self.get_sheet(define.MapType)

    @cached_property
    def marker_sheet(self) -> Sheet[define.Marker]:
        return self.get_sheet(define.Marker)

    @cached_property
    def mate_authority_category_sheet(self) -> Sheet[define.MateAuthorityCategory]:
        return self.get_sheet(define.MateAuthorityCategory)

    @cached_property
    def materia_sheet(self) -> Sheet[define.Materia]:
        return self.get_sheet(define.Materia)

    @cached_property
    def materia_grade_sheet(self) -> Sheet[define.MateriaGrade]:
        return self.get_sheet(define.MateriaGrade)

    @cached_property
    def materia_join_rate_sheet(self) -> Sheet[define.MateriaJoinRate]:
        return self.get_sheet(define.MateriaJoinRate)

    @cached_property
    def materia_join_rate_gather_craft_sheet(self) -> Sheet[define.MateriaJoinRateGatherCraft]:
        return self.get_sheet(define.MateriaJoinRateGatherCraft)

    @cached_property
    def materia_param_sheet(self) -> Sheet[define.MateriaParam]:
        return self.get_sheet(define.MateriaParam)

    @cached_property
    def materia_tomestone_rate_sheet(self) -> Sheet[define.MateriaTomestoneRate]:
        return self.get_sheet(define.MateriaTomestoneRate)

    @cached_property
    def mc_guffin_sheet(self) -> Sheet[define.McGuffin]:
        return self.get_sheet(define.McGuffin)

    @cached_property
    def mc_guffin_ui_data_sheet(self) -> Sheet[define.McGuffinUIData]:
        return self.get_sheet(define.McGuffinUIData)

    @cached_property
    def mini_game_ra_sheet(self) -> Sheet[define.MiniGameRA]:
        return self.get_sheet(define.MiniGameRA)

    @cached_property
    def mini_game_ra_notes_sheet(self) -> Sheet[SubDataRow[define.MiniGameRANotes]]:
        return self.get_sheet(define.MiniGameRANotes)

    @cached_property
    def minion_race_sheet(self) -> Sheet[define.MinionRace]:
        return self.get_sheet(define.MinionRace)

    @cached_property
    def minion_rules_sheet(self) -> Sheet[define.MinionRules]:
        return self.get_sheet(define.MinionRules)

    @cached_property
    def minion_skill_type_sheet(self) -> Sheet[define.MinionSkillType]:
        return self.get_sheet(define.MinionSkillType)

    @cached_property
    def minion_stage_sheet(self) -> Sheet[define.MinionStage]:
        return self.get_sheet(define.MinionStage)

    @cached_property
    def mob_hunt_order_sheet(self) -> Sheet[SubDataRow[define.MobHuntOrder]]:
        return self.get_sheet(define.MobHuntOrder)

    @cached_property
    def mob_hunt_order_type_sheet(self) -> Sheet[define.MobHuntOrderType]:
        return self.get_sheet(define.MobHuntOrderType)

    @cached_property
    def mob_hunt_reward_sheet(self) -> Sheet[define.MobHuntReward]:
        return self.get_sheet(define.MobHuntReward)

    @cached_property
    def mob_hunt_reward_cap_sheet(self) -> Sheet[define.MobHuntRewardCap]:
        return self.get_sheet(define.MobHuntRewardCap)

    @cached_property
    def mob_hunt_target_sheet(self) -> Sheet[define.MobHuntTarget]:
        return self.get_sheet(define.MobHuntTarget)

    @cached_property
    def model_attribute_sheet(self) -> Sheet[define.ModelAttribute]:
        return self.get_sheet(define.ModelAttribute)

    @cached_property
    def model_chara_sheet(self) -> Sheet[define.ModelChara]:
        return self.get_sheet(define.ModelChara)

    @cached_property
    def model_scale_sheet(self) -> Sheet[define.ModelScale]:
        return self.get_sheet(define.ModelScale)

    @cached_property
    def model_skeleton_sheet(self) -> Sheet[define.ModelSkeleton]:
        return self.get_sheet(define.ModelSkeleton)

    @cached_property
    def model_state_sheet(self) -> Sheet[define.ModelState]:
        return self.get_sheet(define.ModelState)

    @cached_property
    def monster_note_sheet(self) -> Sheet[define.MonsterNote]:
        return self.get_sheet(define.MonsterNote)

    @cached_property
    def monster_note_target_sheet(self) -> Sheet[define.MonsterNoteTarget]:
        return self.get_sheet(define.MonsterNoteTarget)

    @cached_property
    def motion_timeline_sheet(self) -> Sheet[define.MotionTimeline]:
        return self.get_sheet(define.MotionTimeline)

    @cached_property
    def motion_timeline_advance_blend_sheet(self) -> Sheet[define.MotionTimelineAdvanceBlend]:
        return self.get_sheet(define.MotionTimelineAdvanceBlend)

    @cached_property
    def motion_timeline_blend_table_sheet(self) -> Sheet[define.MotionTimelineBlendTable]:
        return self.get_sheet(define.MotionTimelineBlendTable)

    @cached_property
    def mount_sheet(self) -> Sheet[define.Mount]:
        return self.get_sheet(define.Mount)

    @cached_property
    def mount_action_sheet(self) -> Sheet[define.MountAction]:
        return self.get_sheet(define.MountAction)

    @cached_property
    def mount_customize_sheet(self) -> Sheet[define.MountCustomize]:
        return self.get_sheet(define.MountCustomize)

    @cached_property
    def mount_flying_condition_sheet(self) -> Sheet[define.MountFlyingCondition]:
        return self.get_sheet(define.MountFlyingCondition)

    @cached_property
    def mount_speed_sheet(self) -> Sheet[define.MountSpeed]:
        return self.get_sheet(define.MountSpeed)

    @cached_property
    def mount_transient_sheet(self) -> Sheet[define.MountTransient]:
        return self.get_sheet(define.MountTransient)

    @cached_property
    def move_control_sheet(self) -> Sheet[define.MoveControl]:
        return self.get_sheet(define.MoveControl)

    @cached_property
    def move_timeline_sheet(self) -> Sheet[define.MoveTimeline]:
        return self.get_sheet(define.MoveTimeline)

    @cached_property
    def move_vfx_sheet(self) -> Sheet[define.MoveVfx]:
        return self.get_sheet(define.MoveVfx)

    @cached_property
    def movie_staff_list_sheet(self) -> Sheet[define.MovieStaffList]:
        return self.get_sheet(define.MovieStaffList)

    @cached_property
    def movie_subtitle_sheet(self) -> Sheet[define.MovieSubtitle]:
        return self.get_sheet(define.MovieSubtitle)

    @cached_property
    def movie_subtitle500_sheet(self) -> Sheet[define.MovieSubtitle500]:
        return self.get_sheet(define.MovieSubtitle500)

    @cached_property
    def movie_subtitle_voyage_sheet(self) -> Sheet[define.MovieSubtitleVoyage]:
        return self.get_sheet(define.MovieSubtitleVoyage)

    @cached_property
    def notebook_division_sheet(self) -> Sheet[define.NotebookDivision]:
        return self.get_sheet(define.NotebookDivision)

    @cached_property
    def notebook_division_category_sheet(self) -> Sheet[define.NotebookDivisionCategory]:
        return self.get_sheet(define.NotebookDivisionCategory)

    @cached_property
    def notebook_list_sheet(self) -> Sheet[define.NotebookList]:
        return self.get_sheet(define.NotebookList)

    @cached_property
    def notorious_monster_sheet(self) -> Sheet[define.NotoriousMonster]:
        return self.get_sheet(define.NotoriousMonster)

    @cached_property
    def notorious_monster_territory_sheet(self) -> Sheet[define.NotoriousMonsterTerritory]:
        return self.get_sheet(define.NotoriousMonsterTerritory)

    @cached_property
    def npc_equip_sheet(self) -> Sheet[define.NpcEquip]:
        return self.get_sheet(define.NpcEquip)

    @cached_property
    def npc_yell_sheet(self) -> Sheet[define.NpcYell]:
        return self.get_sheet(define.NpcYell)

    @cached_property
    def omen_sheet(self) -> Sheet[define.Omen]:
        return self.get_sheet(define.Omen)

    @cached_property
    def omikuji_sheet(self) -> Sheet[define.Omikuji]:
        return self.get_sheet(define.Omikuji)

    @cached_property
    def omikuji_guidance_sheet(self) -> Sheet[define.OmikujiGuidance]:
        return self.get_sheet(define.OmikujiGuidance)

    @cached_property
    def online_status_sheet(self) -> Sheet[define.OnlineStatus]:
        return self.get_sheet(define.OnlineStatus)

    @cached_property
    def open_content_sheet(self) -> Sheet[define.OpenContent]:
        return self.get_sheet(define.OpenContent)

    @cached_property
    def open_content_candidate_name_sheet(self) -> Sheet[define.OpenContentCandidateName]:
        return self.get_sheet(define.OpenContentCandidateName)

    @cached_property
    def open_lua_ui_sheet(self) -> Sheet[define.OpenLuaUI]:
        return self.get_sheet(define.OpenLuaUI)

    @cached_property
    def opening_sheet(self) -> Sheet[define.Opening]:
        return self.get_sheet(define.Opening)

    @cached_property
    def opening_system_define_sheet(self) -> Sheet[define.OpeningSystemDefine]:
        return self.get_sheet(define.OpeningSystemDefine)

    @cached_property
    def orchestrion_sheet(self) -> Sheet[define.Orchestrion]:
        return self.get_sheet(define.Orchestrion)

    @cached_property
    def orchestrion_category_sheet(self) -> Sheet[define.OrchestrionCategory]:
        return self.get_sheet(define.OrchestrionCategory)

    @cached_property
    def orchestrion_path_sheet(self) -> Sheet[define.OrchestrionPath]:
        return self.get_sheet(define.OrchestrionPath)

    @cached_property
    def orchestrion_uiparam_sheet(self) -> Sheet[define.OrchestrionUiparam]:
        return self.get_sheet(define.OrchestrionUiparam)

    @cached_property
    def ornament_sheet(self) -> Sheet[define.Ornament]:
        return self.get_sheet(define.Ornament)

    @cached_property
    def ornament_action_sheet(self) -> Sheet[define.OrnamentAction]:
        return self.get_sheet(define.OrnamentAction)

    @cached_property
    def ornament_customize_sheet(self) -> Sheet[define.OrnamentCustomize]:
        return self.get_sheet(define.OrnamentCustomize)

    @cached_property
    def ornament_customize_group_sheet(self) -> Sheet[define.OrnamentCustomizeGroup]:
        return self.get_sheet(define.OrnamentCustomizeGroup)

    @cached_property
    def ornament_transient_sheet(self) -> Sheet[define.OrnamentTransient]:
        return self.get_sheet(define.OrnamentTransient)

    @cached_property
    def param_grow_sheet(self) -> Sheet[define.ParamGrow]:
        return self.get_sheet(define.ParamGrow)

    @cached_property
    def party_content_sheet(self) -> Sheet[define.PartyContent]:
        return self.get_sheet(define.PartyContent)

    @cached_property
    def party_content_cutscene_sheet(self) -> Sheet[define.PartyContentCutscene]:
        return self.get_sheet(define.PartyContentCutscene)

    @cached_property
    def party_content_text_data_sheet(self) -> Sheet[define.PartyContentTextData]:
        return self.get_sheet(define.PartyContentTextData)

    @cached_property
    def party_content_transient_sheet(self) -> Sheet[define.PartyContentTransient]:
        return self.get_sheet(define.PartyContentTransient)

    @cached_property
    def patch_mark_sheet(self) -> Sheet[define.PatchMark]:
        return self.get_sheet(define.PatchMark)

    @cached_property
    def perform_sheet(self) -> Sheet[define.Perform]:
        return self.get_sheet(define.Perform)

    @cached_property
    def perform_group_sheet(self) -> Sheet[define.PerformGroup]:
        return self.get_sheet(define.PerformGroup)

    @cached_property
    def perform_guide_score_sheet(self) -> Sheet[define.PerformGuideScore]:
        return self.get_sheet(define.PerformGuideScore)

    @cached_property
    def perform_transient_sheet(self) -> Sheet[define.PerformTransient]:
        return self.get_sheet(define.PerformTransient)

    @cached_property
    def permission_sheet(self) -> Sheet[define.Permission]:
        return self.get_sheet(define.Permission)

    @cached_property
    def pet_sheet(self) -> Sheet[define.Pet]:
        return self.get_sheet(define.Pet)

    @cached_property
    def pet_action_sheet(self) -> Sheet[define.PetAction]:
        return self.get_sheet(define.PetAction)

    @cached_property
    def pet_mirage_sheet(self) -> Sheet[define.PetMirage]:
        return self.get_sheet(define.PetMirage)

    @cached_property
    def physics_group_sheet(self) -> Sheet[define.PhysicsGroup]:
        return self.get_sheet(define.PhysicsGroup)

    @cached_property
    def physics_off_group_sheet(self) -> Sheet[define.PhysicsOffGroup]:
        return self.get_sheet(define.PhysicsOffGroup)

    @cached_property
    def physics_wind_sheet(self) -> Sheet[define.PhysicsWind]:
        return self.get_sheet(define.PhysicsWind)

    @cached_property
    def picture_sheet(self) -> Sheet[define.Picture]:
        return self.get_sheet(define.Picture)

    @cached_property
    def place_name_sheet(self) -> Sheet[define.PlaceName]:
        return self.get_sheet(define.PlaceName)

    @cached_property
    def plant_pot_flower_seed_sheet(self) -> Sheet[define.PlantPotFlowerSeed]:
        return self.get_sheet(define.PlantPotFlowerSeed)

    @cached_property
    def player_search_location_sheet(self) -> Sheet[define.PlayerSearchLocation]:
        return self.get_sheet(define.PlayerSearchLocation)

    @cached_property
    def player_search_sub_location_sheet(self) -> Sheet[define.PlayerSearchSubLocation]:
        return self.get_sheet(define.PlayerSearchSubLocation)

    @cached_property
    def pre_handler_sheet(self) -> Sheet[define.PreHandler]:
        return self.get_sheet(define.PreHandler)

    @cached_property
    def pre_handler_movement_sheet(self) -> Sheet[define.PreHandlerMovement]:
        return self.get_sheet(define.PreHandlerMovement)

    @cached_property
    def preset_camera_sheet(self) -> Sheet[define.PresetCamera]:
        return self.get_sheet(define.PresetCamera)

    @cached_property
    def preset_camera_adjust_sheet(self) -> Sheet[define.PresetCameraAdjust]:
        return self.get_sheet(define.PresetCameraAdjust)

    @cached_property
    def public_content_sheet(self) -> Sheet[define.PublicContent]:
        return self.get_sheet(define.PublicContent)

    @cached_property
    def public_content_cutscene_sheet(self) -> Sheet[define.PublicContentCutscene]:
        return self.get_sheet(define.PublicContentCutscene)

    @cached_property
    def public_content_text_data_sheet(self) -> Sheet[define.PublicContentTextData]:
        return self.get_sheet(define.PublicContentTextData)

    @cached_property
    def public_content_type_sheet(self) -> Sheet[define.PublicContentType]:
        return self.get_sheet(define.PublicContentType)

    @cached_property
    def pvp_action_sheet(self) -> Sheet[define.PvPAction]:
        return self.get_sheet(define.PvPAction)

    @cached_property
    def pvp_action_sort_sheet(self) -> Sheet[SubDataRow[define.PvPActionSort]]:
        return self.get_sheet(define.PvPActionSort)

    @cached_property
    def pvp_initial_select_action_trait_sheet(self) -> Sheet[define.PvPInitialSelectActionTrait]:
        return self.get_sheet(define.PvPInitialSelectActionTrait)

    @cached_property
    def pvp_rank_sheet(self) -> Sheet[define.PvPRank]:
        return self.get_sheet(define.PvPRank)

    @cached_property
    def pvp_rank_transient_sheet(self) -> Sheet[define.PvPRankTransient]:
        return self.get_sheet(define.PvPRankTransient)

    @cached_property
    def pvp_select_trait_sheet(self) -> Sheet[define.PvPSelectTrait]:
        return self.get_sheet(define.PvPSelectTrait)

    @cached_property
    def pvp_select_trait_transient_sheet(self) -> Sheet[define.PvPSelectTraitTransient]:
        return self.get_sheet(define.PvPSelectTraitTransient)

    @cached_property
    def pvp_series_sheet(self) -> Sheet[define.PvPSeries]:
        return self.get_sheet(define.PvPSeries)

    @cached_property
    def pvp_series_level_sheet(self) -> Sheet[define.PvPSeriesLevel]:
        return self.get_sheet(define.PvPSeriesLevel)

    @cached_property
    def pvp_trait_sheet(self) -> Sheet[define.PvPTrait]:
        return self.get_sheet(define.PvPTrait)

    @cached_property
    def qte_sheet(self) -> Sheet[define.QTE]:
        return self.get_sheet(define.QTE)

    @cached_property
    def quest_sheet(self) -> Sheet[define.Quest]:
        return self.get_sheet(define.Quest)

    @cached_property
    def quest_accept_addition_condition_sheet(self) -> Sheet[define.QuestAcceptAdditionCondition]:
        return self.get_sheet(define.QuestAcceptAdditionCondition)

    @cached_property
    def quest_battle_sheet(self) -> Sheet[define.QuestBattle]:
        return self.get_sheet(define.QuestBattle)

    @cached_property
    def quest_battle_resident_sheet(self) -> Sheet[define.QuestBattleResident]:
        return self.get_sheet(define.QuestBattleResident)

    @cached_property
    def quest_battle_system_define_sheet(self) -> Sheet[define.QuestBattleSystemDefine]:
        return self.get_sheet(define.QuestBattleSystemDefine)

    @cached_property
    def quest_chapter_sheet(self) -> Sheet[define.QuestChapter]:
        return self.get_sheet(define.QuestChapter)

    @cached_property
    def quest_class_job_reward_sheet(self) -> Sheet[SubDataRow[define.QuestClassJobReward]]:
        return self.get_sheet(define.QuestClassJobReward)

    @cached_property
    def quest_class_job_supply_sheet(self) -> Sheet[SubDataRow[define.QuestClassJobSupply]]:
        return self.get_sheet(define.QuestClassJobSupply)

    @cached_property
    def quest_custom_todo_sheet(self) -> Sheet[define.QuestCustomTodo]:
        return self.get_sheet(define.QuestCustomTodo)

    @cached_property
    def quest_derived_class_sheet(self) -> Sheet[define.QuestDerivedClass]:
        return self.get_sheet(define.QuestDerivedClass)

    @cached_property
    def quest_effect_sheet(self) -> Sheet[define.QuestEffect]:
        return self.get_sheet(define.QuestEffect)

    @cached_property
    def quest_effect_define_sheet(self) -> Sheet[SubDataRow[define.QuestEffectDefine]]:
        return self.get_sheet(define.QuestEffectDefine)

    @cached_property
    def quest_effect_type_sheet(self) -> Sheet[define.QuestEffectType]:
        return self.get_sheet(define.QuestEffectType)

    @cached_property
    def quest_equip_model_sheet(self) -> Sheet[define.QuestEquipModel]:
        return self.get_sheet(define.QuestEquipModel)

    @cached_property
    def quest_hide_reward_sheet(self) -> Sheet[define.QuestHideReward]:
        return self.get_sheet(define.QuestHideReward)

    @cached_property
    def quest_recomplete_sheet(self) -> Sheet[define.QuestRecomplete]:
        return self.get_sheet(define.QuestRecomplete)

    @cached_property
    def quest_redo_sheet(self) -> Sheet[define.QuestRedo]:
        return self.get_sheet(define.QuestRedo)

    @cached_property
    def quest_redo_chapter_sheet(self) -> Sheet[define.QuestRedoChapter]:
        return self.get_sheet(define.QuestRedoChapter)

    @cached_property
    def quest_redo_chapter_ui_sheet(self) -> Sheet[define.QuestRedoChapterUI]:
        return self.get_sheet(define.QuestRedoChapterUI)

    @cached_property
    def quest_redo_chapter_ui_category_sheet(self) -> Sheet[define.QuestRedoChapterUICategory]:
        return self.get_sheet(define.QuestRedoChapterUICategory)

    @cached_property
    def quest_redo_chapter_ui_tab_sheet(self) -> Sheet[define.QuestRedoChapterUITab]:
        return self.get_sheet(define.QuestRedoChapterUITab)

    @cached_property
    def quest_redo_incomp_chapter_sheet(self) -> Sheet[SubDataRow[define.QuestRedoIncompChapter]]:
        return self.get_sheet(define.QuestRedoIncompChapter)

    @cached_property
    def quest_repeat_flag_sheet(self) -> Sheet[define.QuestRepeatFlag]:
        return self.get_sheet(define.QuestRepeatFlag)

    @cached_property
    def quest_reward_other_sheet(self) -> Sheet[define.QuestRewardOther]:
        return self.get_sheet(define.QuestRewardOther)

    @cached_property
    def quest_set_define_sheet(self) -> Sheet[SubDataRow[define.QuestSetDefine]]:
        return self.get_sheet(define.QuestSetDefine)

    @cached_property
    def quest_status_param_sheet(self) -> Sheet[define.QuestStatusParam]:
        return self.get_sheet(define.QuestStatusParam)

    @cached_property
    def quest_system_define_sheet(self) -> Sheet[define.QuestSystemDefine]:
        return self.get_sheet(define.QuestSystemDefine)

    @cached_property
    def quick_chat_sheet(self) -> Sheet[define.QuickChat]:
        return self.get_sheet(define.QuickChat)

    @cached_property
    def quick_chat_transient_sheet(self) -> Sheet[define.QuickChatTransient]:
        return self.get_sheet(define.QuickChatTransient)

    @cached_property
    def rp_parameter_sheet(self) -> Sheet[define.RPParameter]:
        return self.get_sheet(define.RPParameter)

    @cached_property
    def race_sheet(self) -> Sheet[define.Race]:
        return self.get_sheet(define.Race)

    @cached_property
    def racing_chocobo_grade_sheet(self) -> Sheet[define.RacingChocoboGrade]:
        return self.get_sheet(define.RacingChocoboGrade)

    @cached_property
    def racing_chocobo_item_sheet(self) -> Sheet[define.RacingChocoboItem]:
        return self.get_sheet(define.RacingChocoboItem)

    @cached_property
    def racing_chocobo_name_sheet(self) -> Sheet[define.RacingChocoboName]:
        return self.get_sheet(define.RacingChocoboName)

    @cached_property
    def racing_chocobo_name_category_sheet(self) -> Sheet[define.RacingChocoboNameCategory]:
        return self.get_sheet(define.RacingChocoboNameCategory)

    @cached_property
    def racing_chocobo_name_info_sheet(self) -> Sheet[define.RacingChocoboNameInfo]:
        return self.get_sheet(define.RacingChocoboNameInfo)

    @cached_property
    def racing_chocobo_param_sheet(self) -> Sheet[define.RacingChocoboParam]:
        return self.get_sheet(define.RacingChocoboParam)

    @cached_property
    def raid_finder_param_sheet(self) -> Sheet[SubDataRow[define.RaidFinderParam]]:
        return self.get_sheet(define.RaidFinderParam)

    @cached_property
    def reaction_event_object_sheet(self) -> Sheet[SubDataRow[define.ReactionEventObject]]:
        return self.get_sheet(define.ReactionEventObject)

    @cached_property
    def reaction_event_object_info_sheet(self) -> Sheet[SubDataRow[define.ReactionEventObjectInfo]]:
        return self.get_sheet(define.ReactionEventObjectInfo)

    @cached_property
    def recast_navimesh_sheet(self) -> Sheet[define.RecastNavimesh]:
        return self.get_sheet(define.RecastNavimesh)

    @cached_property
    def recipe_sheet(self) -> Sheet[define.Recipe]:
        return self.get_sheet(define.Recipe)

    @cached_property
    def recipe_level_table_sheet(self) -> Sheet[define.RecipeLevelTable]:
        return self.get_sheet(define.RecipeLevelTable)

    @cached_property
    def recipe_lookup_sheet(self) -> Sheet[define.RecipeLookup]:
        return self.get_sheet(define.RecipeLookup)

    @cached_property
    def recipe_notebook_list_sheet(self) -> Sheet[define.RecipeNotebookList]:
        return self.get_sheet(define.RecipeNotebookList)

    @cached_property
    def recommend_contents_sheet(self) -> Sheet[define.RecommendContents]:
        return self.get_sheet(define.RecommendContents)

    @cached_property
    def relic_sheet(self) -> Sheet[define.Relic]:
        return self.get_sheet(define.Relic)

    @cached_property
    def relic3_sheet(self) -> Sheet[define.Relic3]:
        return self.get_sheet(define.Relic3)

    @cached_property
    def relic3_materia_sheet(self) -> Sheet[define.Relic3Materia]:
        return self.get_sheet(define.Relic3Materia)

    @cached_property
    def relic3_rate_sheet(self) -> Sheet[define.Relic3Rate]:
        return self.get_sheet(define.Relic3Rate)

    @cached_property
    def relic3_rate_pattern_sheet(self) -> Sheet[define.Relic3RatePattern]:
        return self.get_sheet(define.Relic3RatePattern)

    @cached_property
    def relic6_magicite_sheet(self) -> Sheet[define.Relic6Magicite]:
        return self.get_sheet(define.Relic6Magicite)

    @cached_property
    def relic_item_sheet(self) -> Sheet[define.RelicItem]:
        return self.get_sheet(define.RelicItem)

    @cached_property
    def relic_materia_sheet(self) -> Sheet[define.RelicMateria]:
        return self.get_sheet(define.RelicMateria)

    @cached_property
    def relic_note_sheet(self) -> Sheet[define.RelicNote]:
        return self.get_sheet(define.RelicNote)

    @cached_property
    def relic_note_category_sheet(self) -> Sheet[define.RelicNoteCategory]:
        return self.get_sheet(define.RelicNoteCategory)

    @cached_property
    def resident_sheet(self) -> Sheet[SubDataRow[define.Resident]]:
        return self.get_sheet(define.Resident)

    @cached_property
    def resident_motion_type_sheet(self) -> Sheet[define.ResidentMotionType]:
        return self.get_sheet(define.ResidentMotionType)

    @cached_property
    def resistance_weapon_adjust_sheet(self) -> Sheet[define.ResistanceWeaponAdjust]:
        return self.get_sheet(define.ResistanceWeaponAdjust)

    @cached_property
    def retainer_fortune_reward_range_sheet(self) -> Sheet[define.RetainerFortuneRewardRange]:
        return self.get_sheet(define.RetainerFortuneRewardRange)

    @cached_property
    def retainer_task_sheet(self) -> Sheet[define.RetainerTask]:
        return self.get_sheet(define.RetainerTask)

    @cached_property
    def retainer_task_lv_range_sheet(self) -> Sheet[define.RetainerTaskLvRange]:
        return self.get_sheet(define.RetainerTaskLvRange)

    @cached_property
    def retainer_task_normal_sheet(self) -> Sheet[define.RetainerTaskNormal]:
        return self.get_sheet(define.RetainerTaskNormal)

    @cached_property
    def retainer_task_parameter_sheet(self) -> Sheet[define.RetainerTaskParameter]:
        return self.get_sheet(define.RetainerTaskParameter)

    @cached_property
    def retainer_task_parameter_lv_diff_sheet(self) -> Sheet[define.RetainerTaskParameterLvDiff]:
        return self.get_sheet(define.RetainerTaskParameterLvDiff)

    @cached_property
    def retainer_task_random_sheet(self) -> Sheet[define.RetainerTaskRandom]:
        return self.get_sheet(define.RetainerTaskRandom)

    @cached_property
    def ride_shooting_sheet(self) -> Sheet[define.RideShooting]:
        return self.get_sheet(define.RideShooting)

    @cached_property
    def ride_shooting_scheduler_sheet(self) -> Sheet[SubDataRow[define.RideShootingScheduler]]:
        return self.get_sheet(define.RideShootingScheduler)

    @cached_property
    def ride_shooting_target_sheet(self) -> Sheet[define.RideShootingTarget]:
        return self.get_sheet(define.RideShootingTarget)

    @cached_property
    def ride_shooting_target_scheduler_sheet(self) -> Sheet[SubDataRow[define.RideShootingTargetScheduler]]:
        return self.get_sheet(define.RideShootingTargetScheduler)

    @cached_property
    def ride_shooting_target_type_sheet(self) -> Sheet[define.RideShootingTargetType]:
        return self.get_sheet(define.RideShootingTargetType)

    @cached_property
    def ride_shooting_text_data_sheet(self) -> Sheet[define.RideShootingTextData]:
        return self.get_sheet(define.RideShootingTextData)

    @cached_property
    def role_sheet(self) -> Sheet[define.Role]:
        return self.get_sheet(define.Role)

    @cached_property
    def se_sheet(self) -> Sheet[define.SE]:
        return self.get_sheet(define.SE)

    @cached_property
    def se_battle_sheet(self) -> Sheet[define.SEBattle]:
        return self.get_sheet(define.SEBattle)

    @cached_property
    def satisfaction_arbitration_sheet(self) -> Sheet[SubDataRow[define.SatisfactionArbitration]]:
        return self.get_sheet(define.SatisfactionArbitration)

    @cached_property
    def satisfaction_npc_sheet(self) -> Sheet[define.SatisfactionNpc]:
        return self.get_sheet(define.SatisfactionNpc)

    @cached_property
    def satisfaction_supply_sheet(self) -> Sheet[SubDataRow[define.SatisfactionSupply]]:
        return self.get_sheet(define.SatisfactionSupply)

    @cached_property
    def satisfaction_supply_reward_sheet(self) -> Sheet[define.SatisfactionSupplyReward]:
        return self.get_sheet(define.SatisfactionSupplyReward)

    @cached_property
    def satisfaction_supply_reward_exp_sheet(self) -> Sheet[SubDataRow[define.SatisfactionSupplyRewardExp]]:
        return self.get_sheet(define.SatisfactionSupplyRewardExp)

    @cached_property
    def scenario_tree_sheet(self) -> Sheet[define.ScenarioTree]:
        return self.get_sheet(define.ScenarioTree)

    @cached_property
    def scenario_tree_tips_sheet(self) -> Sheet[define.ScenarioTreeTips]:
        return self.get_sheet(define.ScenarioTreeTips)

    @cached_property
    def scenario_tree_tips_class_quest_sheet(self) -> Sheet[SubDataRow[define.ScenarioTreeTipsClassQuest]]:
        return self.get_sheet(define.ScenarioTreeTipsClassQuest)

    @cached_property
    def scenario_type_sheet(self) -> Sheet[define.ScenarioType]:
        return self.get_sheet(define.ScenarioType)

    @cached_property
    def screen_image_sheet(self) -> Sheet[define.ScreenImage]:
        return self.get_sheet(define.ScreenImage)

    @cached_property
    def secret_recipe_book_sheet(self) -> Sheet[define.SecretRecipeBook]:
        return self.get_sheet(define.SecretRecipeBook)

    @cached_property
    def sequential_event_sheet(self) -> Sheet[define.SequentialEvent]:
        return self.get_sheet(define.SequentialEvent)

    @cached_property
    def sequential_event_multiple_range_sheet(self) -> Sheet[SubDataRow[define.SequentialEventMultipleRange]]:
        return self.get_sheet(define.SequentialEventMultipleRange)

    @cached_property
    def sharlayan_craft_works_sheet(self) -> Sheet[define.SharlayanCraftWorks]:
        return self.get_sheet(define.SharlayanCraftWorks)

    @cached_property
    def sharlayan_craft_works_supply_sheet(self) -> Sheet[define.SharlayanCraftWorksSupply]:
        return self.get_sheet(define.SharlayanCraftWorksSupply)

    @cached_property
    def skirmish_sheet(self) -> Sheet[define.Skirmish]:
        return self.get_sheet(define.Skirmish)

    @cached_property
    def sky_island_sheet(self) -> Sheet[define.SkyIsland]:
        return self.get_sheet(define.SkyIsland)

    @cached_property
    def sky_island2_sheet(self) -> Sheet[define.SkyIsland2]:
        return self.get_sheet(define.SkyIsland2)

    @cached_property
    def sky_island2_mission_sheet(self) -> Sheet[define.SkyIsland2Mission]:
        return self.get_sheet(define.SkyIsland2Mission)

    @cached_property
    def sky_island2_mission_detail_sheet(self) -> Sheet[define.SkyIsland2MissionDetail]:
        return self.get_sheet(define.SkyIsland2MissionDetail)

    @cached_property
    def sky_island2_mission_type_sheet(self) -> Sheet[define.SkyIsland2MissionType]:
        return self.get_sheet(define.SkyIsland2MissionType)

    @cached_property
    def sky_island2_range_type_sheet(self) -> Sheet[define.SkyIsland2RangeType]:
        return self.get_sheet(define.SkyIsland2RangeType)

    @cached_property
    def sky_island_map_marker_sheet(self) -> Sheet[define.SkyIslandMapMarker]:
        return self.get_sheet(define.SkyIslandMapMarker)

    @cached_property
    def sky_island_subject_sheet(self) -> Sheet[define.SkyIslandSubject]:
        return self.get_sheet(define.SkyIslandSubject)

    @cached_property
    def snipe_sheet(self) -> Sheet[define.Snipe]:
        return self.get_sheet(define.Snipe)

    @cached_property
    def snipe_collision_sheet(self) -> Sheet[define.SnipeCollision]:
        return self.get_sheet(define.SnipeCollision)

    @cached_property
    def snipe_element_id_sheet(self) -> Sheet[define.SnipeElementId]:
        return self.get_sheet(define.SnipeElementId)

    @cached_property
    def snipe_hit_event_sheet(self) -> Sheet[SubDataRow[define.SnipeHitEvent]]:
        return self.get_sheet(define.SnipeHitEvent)

    @cached_property
    def snipe_performance_camera_sheet(self) -> Sheet[define.SnipePerformanceCamera]:
        return self.get_sheet(define.SnipePerformanceCamera)

    @cached_property
    def snipe_talk_sheet(self) -> Sheet[define.SnipeTalk]:
        return self.get_sheet(define.SnipeTalk)

    @cached_property
    def snipe_talk_name_sheet(self) -> Sheet[define.SnipeTalkName]:
        return self.get_sheet(define.SnipeTalkName)

    @cached_property
    def spearfishing_combo_target_sheet(self) -> Sheet[define.SpearfishingComboTarget]:
        return self.get_sheet(define.SpearfishingComboTarget)

    @cached_property
    def spearfishing_ecology_sheet(self) -> Sheet[define.SpearfishingEcology]:
        return self.get_sheet(define.SpearfishingEcology)

    @cached_property
    def spearfishing_item_sheet(self) -> Sheet[define.SpearfishingItem]:
        return self.get_sheet(define.SpearfishingItem)

    @cached_property
    def spearfishing_item_reverse_sheet(self) -> Sheet[define.SpearfishingItemReverse]:
        return self.get_sheet(define.SpearfishingItemReverse)

    @cached_property
    def spearfishing_notebook_sheet(self) -> Sheet[define.SpearfishingNotebook]:
        return self.get_sheet(define.SpearfishingNotebook)

    @cached_property
    def spearfishing_record_page_sheet(self) -> Sheet[define.SpearfishingRecordPage]:
        return self.get_sheet(define.SpearfishingRecordPage)

    @cached_property
    def spearfishing_silhouette_sheet(self) -> Sheet[define.SpearfishingSilhouette]:
        return self.get_sheet(define.SpearfishingSilhouette)

    @cached_property
    def special_shop_sheet(self) -> Sheet[define.SpecialShop]:
        return self.get_sheet(define.SpecialShop)

    @cached_property
    def special_shop_item_category_sheet(self) -> Sheet[define.SpecialShopItemCategory]:
        return self.get_sheet(define.SpecialShopItemCategory)

    @cached_property
    def spectator_sheet(self) -> Sheet[define.Spectator]:
        return self.get_sheet(define.Spectator)

    @cached_property
    def stain_sheet(self) -> Sheet[define.Stain]:
        return self.get_sheet(define.Stain)

    @cached_property
    def stain_transient_sheet(self) -> Sheet[define.StainTransient]:
        return self.get_sheet(define.StainTransient)

    @cached_property
    def stance_change_sheet(self) -> Sheet[define.StanceChange]:
        return self.get_sheet(define.StanceChange)

    @cached_property
    def status_sheet(self) -> Sheet[define.Status]:
        return self.get_sheet(define.Status)

    @cached_property
    def status_hit_effect_sheet(self) -> Sheet[define.StatusHitEffect]:
        return self.get_sheet(define.StatusHitEffect)

    @cached_property
    def status_loop_vfx_sheet(self) -> Sheet[define.StatusLoopVFX]:
        return self.get_sheet(define.StatusLoopVFX)

    @cached_property
    def story_sheet(self) -> Sheet[define.Story]:
        return self.get_sheet(define.Story)

    @cached_property
    def story_system_define_sheet(self) -> Sheet[define.StorySystemDefine]:
        return self.get_sheet(define.StorySystemDefine)

    @cached_property
    def submarine_exploration_sheet(self) -> Sheet[define.SubmarineExploration]:
        return self.get_sheet(define.SubmarineExploration)

    @cached_property
    def submarine_exploration_log_sheet(self) -> Sheet[define.SubmarineExplorationLog]:
        return self.get_sheet(define.SubmarineExplorationLog)

    @cached_property
    def submarine_map_sheet(self) -> Sheet[define.SubmarineMap]:
        return self.get_sheet(define.SubmarineMap)

    @cached_property
    def submarine_part_sheet(self) -> Sheet[define.SubmarinePart]:
        return self.get_sheet(define.SubmarinePart)

    @cached_property
    def submarine_rank_sheet(self) -> Sheet[define.SubmarineRank]:
        return self.get_sheet(define.SubmarineRank)

    @cached_property
    def submarine_spec_category_sheet(self) -> Sheet[define.SubmarineSpecCategory]:
        return self.get_sheet(define.SubmarineSpecCategory)

    @cached_property
    def switch_talk_sheet(self) -> Sheet[define.SwitchTalk]:
        return self.get_sheet(define.SwitchTalk)

    @cached_property
    def switch_talk_variation_sheet(self) -> Sheet[SubDataRow[define.SwitchTalkVariation]]:
        return self.get_sheet(define.SwitchTalkVariation)

    @cached_property
    def system_graphic_preset_sheet(self) -> Sheet[SubDataRow[define.SystemGraphicPreset]]:
        return self.get_sheet(define.SystemGraphicPreset)

    @cached_property
    def telepo_relay_sheet(self) -> Sheet[define.TelepoRelay]:
        return self.get_sheet(define.TelepoRelay)

    @cached_property
    def territory_chat_rule_sheet(self) -> Sheet[define.TerritoryChatRule]:
        return self.get_sheet(define.TerritoryChatRule)

    @cached_property
    def territory_intended_use_sheet(self) -> Sheet[define.TerritoryIntendedUse]:
        return self.get_sheet(define.TerritoryIntendedUse)

    @cached_property
    def territory_type_sheet(self) -> Sheet[define.TerritoryType]:
        return self.get_sheet(define.TerritoryType)

    @cached_property
    def territory_type_telepo_sheet(self) -> Sheet[define.TerritoryTypeTelepo]:
        return self.get_sheet(define.TerritoryTypeTelepo)

    @cached_property
    def territory_type_transient_sheet(self) -> Sheet[define.TerritoryTypeTransient]:
        return self.get_sheet(define.TerritoryTypeTransient)

    @cached_property
    def text_command_sheet(self) -> Sheet[define.TextCommand]:
        return self.get_sheet(define.TextCommand)

    @cached_property
    def text_command_param_sheet(self) -> Sheet[define.TextCommandParam]:
        return self.get_sheet(define.TextCommandParam)

    @cached_property
    def title_sheet(self) -> Sheet[define.Title]:
        return self.get_sheet(define.Title)

    @cached_property
    def tomestone_convert_sheet(self) -> Sheet[define.TomestoneConvert]:
        return self.get_sheet(define.TomestoneConvert)

    @cached_property
    def tomestones_sheet(self) -> Sheet[define.Tomestones]:
        return self.get_sheet(define.Tomestones)

    @cached_property
    def tomestones_item_sheet(self) -> Sheet[define.TomestonesItem]:
        return self.get_sheet(define.TomestonesItem)

    @cached_property
    def topic_select_sheet(self) -> Sheet[define.TopicSelect]:
        return self.get_sheet(define.TopicSelect)

    @cached_property
    def town_sheet(self) -> Sheet[define.Town]:
        return self.get_sheet(define.Town)

    @cached_property
    def trait_sheet(self) -> Sheet[define.Trait]:
        return self.get_sheet(define.Trait)

    @cached_property
    def trait_recast_sheet(self) -> Sheet[define.TraitRecast]:
        return self.get_sheet(define.TraitRecast)

    @cached_property
    def trait_transient_sheet(self) -> Sheet[define.TraitTransient]:
        return self.get_sheet(define.TraitTransient)

    @cached_property
    def transformation_sheet(self) -> Sheet[define.Transformation]:
        return self.get_sheet(define.Transformation)

    @cached_property
    def treasure_sheet(self) -> Sheet[define.Treasure]:
        return self.get_sheet(define.Treasure)

    @cached_property
    def treasure_hunt_rank_sheet(self) -> Sheet[define.TreasureHuntRank]:
        return self.get_sheet(define.TreasureHuntRank)

    @cached_property
    def treasure_hunt_texture_sheet(self) -> Sheet[define.TreasureHuntTexture]:
        return self.get_sheet(define.TreasureHuntTexture)

    @cached_property
    def treasure_model_sheet(self) -> Sheet[define.TreasureModel]:
        return self.get_sheet(define.TreasureModel)

    @cached_property
    def treasure_spot_sheet(self) -> Sheet[SubDataRow[define.TreasureSpot]]:
        return self.get_sheet(define.TreasureSpot)

    @cached_property
    def tribe_sheet(self) -> Sheet[define.Tribe]:
        return self.get_sheet(define.Tribe)

    @cached_property
    def trigger_effect_sheet(self) -> Sheet[define.TriggerEffect]:
        return self.get_sheet(define.TriggerEffect)

    @cached_property
    def triple_triad_sheet(self) -> Sheet[define.TripleTriad]:
        return self.get_sheet(define.TripleTriad)

    @cached_property
    def triple_triad_card_sheet(self) -> Sheet[define.TripleTriadCard]:
        return self.get_sheet(define.TripleTriadCard)

    @cached_property
    def triple_triad_card_obtain_sheet(self) -> Sheet[define.TripleTriadCardObtain]:
        return self.get_sheet(define.TripleTriadCardObtain)

    @cached_property
    def triple_triad_card_rarity_sheet(self) -> Sheet[define.TripleTriadCardRarity]:
        return self.get_sheet(define.TripleTriadCardRarity)

    @cached_property
    def triple_triad_card_resident_sheet(self) -> Sheet[define.TripleTriadCardResident]:
        return self.get_sheet(define.TripleTriadCardResident)

    @cached_property
    def triple_triad_card_type_sheet(self) -> Sheet[define.TripleTriadCardType]:
        return self.get_sheet(define.TripleTriadCardType)

    @cached_property
    def triple_triad_competition_sheet(self) -> Sheet[define.TripleTriadCompetition]:
        return self.get_sheet(define.TripleTriadCompetition)

    @cached_property
    def triple_triad_define_sheet(self) -> Sheet[define.TripleTriadDefine]:
        return self.get_sheet(define.TripleTriadDefine)

    @cached_property
    def triple_triad_resident_sheet(self) -> Sheet[define.TripleTriadResident]:
        return self.get_sheet(define.TripleTriadResident)

    @cached_property
    def triple_triad_rule_sheet(self) -> Sheet[define.TripleTriadRule]:
        return self.get_sheet(define.TripleTriadRule)

    @cached_property
    def triple_triad_tournament_sheet(self) -> Sheet[define.TripleTriadTournament]:
        return self.get_sheet(define.TripleTriadTournament)

    @cached_property
    def tutorial_sheet(self) -> Sheet[define.Tutorial]:
        return self.get_sheet(define.Tutorial)

    @cached_property
    def tutorial_dps_sheet(self) -> Sheet[define.TutorialDPS]:
        return self.get_sheet(define.TutorialDPS)

    @cached_property
    def tutorial_healer_sheet(self) -> Sheet[define.TutorialHealer]:
        return self.get_sheet(define.TutorialHealer)

    @cached_property
    def tutorial_tank_sheet(self) -> Sheet[define.TutorialTank]:
        return self.get_sheet(define.TutorialTank)

    @cached_property
    def uds__event_sheet(self) -> Sheet[define.UDS_Event]:
        return self.get_sheet(define.UDS_Event)

    @cached_property
    def uds__object_sheet(self) -> Sheet[define.UDS_Object]:
        return self.get_sheet(define.UDS_Object)

    @cached_property
    def uds__property_sheet(self) -> Sheet[define.UDS_Property]:
        return self.get_sheet(define.UDS_Property)

    @cached_property
    def uds__stats_sheet(self) -> Sheet[define.UDS_Stats]:
        return self.get_sheet(define.UDS_Stats)

    @cached_property
    def ui_color_sheet(self) -> Sheet[define.UIColor]:
        return self.get_sheet(define.UIColor)

    @cached_property
    def ui_const_sheet(self) -> Sheet[define.UIConst]:
        return self.get_sheet(define.UIConst)

    @cached_property
    def vfx_sheet(self) -> Sheet[define.VFX]:
        return self.get_sheet(define.VFX)

    @cached_property
    def vvd_data_sheet(self) -> Sheet[define.VVDData]:
        return self.get_sheet(define.VVDData)

    @cached_property
    def vvd_notebook_contents_sheet(self) -> Sheet[define.VVDNotebookContents]:
        return self.get_sheet(define.VVDNotebookContents)

    @cached_property
    def vvd_notebook_series_sheet(self) -> Sheet[define.VVDNotebookSeries]:
        return self.get_sheet(define.VVDNotebookSeries)

    @cached_property
    def vvd_route_data_sheet(self) -> Sheet[SubDataRow[define.VVDRouteData]]:
        return self.get_sheet(define.VVDRouteData)

    @cached_property
    def vvd_variant_action_sheet(self) -> Sheet[define.VVDVariantAction]:
        return self.get_sheet(define.VVDVariantAction)

    @cached_property
    def vase_sheet(self) -> Sheet[define.Vase]:
        return self.get_sheet(define.Vase)

    @cached_property
    def vase_flower_sheet(self) -> Sheet[define.VaseFlower]:
        return self.get_sheet(define.VaseFlower)

    @cached_property
    def warp_sheet(self) -> Sheet[define.Warp]:
        return self.get_sheet(define.Warp)

    @cached_property
    def warp_condition_sheet(self) -> Sheet[define.WarpCondition]:
        return self.get_sheet(define.WarpCondition)

    @cached_property
    def warp_logic_sheet(self) -> Sheet[define.WarpLogic]:
        return self.get_sheet(define.WarpLogic)

    @cached_property
    def weapon_timeline_sheet(self) -> Sheet[define.WeaponTimeline]:
        return self.get_sheet(define.WeaponTimeline)

    @cached_property
    def weather_sheet(self) -> Sheet[define.Weather]:
        return self.get_sheet(define.Weather)

    @cached_property
    def weather_group_sheet(self) -> Sheet[SubDataRow[define.WeatherGroup]]:
        return self.get_sheet(define.WeatherGroup)

    @cached_property
    def weather_rate_sheet(self) -> Sheet[define.WeatherRate]:
        return self.get_sheet(define.WeatherRate)

    @cached_property
    def weather_report_replace_sheet(self) -> Sheet[define.WeatherReportReplace]:
        return self.get_sheet(define.WeatherReportReplace)

    @cached_property
    def web_guidance_sheet(self) -> Sheet[define.WebGuidance]:
        return self.get_sheet(define.WebGuidance)

    @cached_property
    def web_url_sheet(self) -> Sheet[define.WebURL]:
        return self.get_sheet(define.WebURL)

    @cached_property
    def wedding_bgm_sheet(self) -> Sheet[define.WeddingBGM]:
        return self.get_sheet(define.WeddingBGM)

    @cached_property
    def wedding_flower_color_sheet(self) -> Sheet[define.WeddingFlowerColor]:
        return self.get_sheet(define.WeddingFlowerColor)

    @cached_property
    def wedding_plan_sheet(self) -> Sheet[define.WeddingPlan]:
        return self.get_sheet(define.WeddingPlan)

    @cached_property
    def weekly_bingo_order_data_sheet(self) -> Sheet[define.WeeklyBingoOrderData]:
        return self.get_sheet(define.WeeklyBingoOrderData)

    @cached_property
    def weekly_bingo_reward_data_sheet(self) -> Sheet[define.WeeklyBingoRewardData]:
        return self.get_sheet(define.WeeklyBingoRewardData)

    @cached_property
    def weekly_bingo_text_sheet(self) -> Sheet[define.WeeklyBingoText]:
        return self.get_sheet(define.WeeklyBingoText)

    @cached_property
    def weekly_lot_bonus_sheet(self) -> Sheet[define.WeeklyLotBonus]:
        return self.get_sheet(define.WeeklyLotBonus)

    @cached_property
    def weekly_lot_bonus_threshold_sheet(self) -> Sheet[define.WeeklyLotBonusThreshold]:
        return self.get_sheet(define.WeeklyLotBonusThreshold)

    @cached_property
    def world_sheet(self) -> Sheet[define.World]:
        return self.get_sheet(define.World)

    @cached_property
    def world_dc_group_type_sheet(self) -> Sheet[define.WorldDCGroupType]:
        return self.get_sheet(define.WorldDCGroupType)

    @cached_property
    def x_pvp_group_activity_sheet(self) -> Sheet[define.XPVPGroupActivity]:
        return self.get_sheet(define.XPVPGroupActivity)

    @cached_property
    def ykw_sheet(self) -> Sheet[define.YKW]:
        return self.get_sheet(define.YKW)

    @cached_property
    def yard_catalog_category_sheet(self) -> Sheet[define.YardCatalogCategory]:
        return self.get_sheet(define.YardCatalogCategory)

    @cached_property
    def yard_catalog_item_list_sheet(self) -> Sheet[define.YardCatalogItemList]:
        return self.get_sheet(define.YardCatalogItemList)

    @cached_property
    def zone_shared_group_sheet(self) -> Sheet[SubDataRow[define.ZoneSharedGroup]]:
        return self.get_sheet(define.ZoneSharedGroup)

    @cached_property
    def zone_timeline_sheet(self) -> Sheet[SubDataRow[define.ZoneTimeline]]:
        return self.get_sheet(define.ZoneTimeline)
