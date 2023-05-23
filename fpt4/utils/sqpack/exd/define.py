from typing import List
from nylib.utils import iter_repeat_add as ir
from fpt4.utils.sqpack.exd.data_row import RowData, RowForeign, ListData, Icon, IconRow
from fpt4.utils.sqpack.exd.row import DataRow
str_t, bool_t, float_t, int_t=str, bool, float, int

class AOZArrangement(DataRow):
    _sign = b'AOZArrangement|eJzLywMAAUwA3Q=='
    sheet_name = 'AOZArrangement'
    briefing_b_npc: 'AOZContentBriefingBNpc' = RowForeign(0, 'AOZContentBriefingBNpc')
    briefing_pos: int_t = RowData(1)


class AOZBoss(DataRow):
    _sign = b'AOZBoss|eJzLywMAAUwA3Q=='
    sheet_name = 'AOZBoss'
    _display = 'briefing_b_npc'
    briefing_b_npc: 'AOZContentBriefingBNpc' = RowForeign(0, 'AOZContentBriefingBNpc')
    briefing_pos: int_t = RowData(1)


class AOZContent(DataRow):
    _sign = b'AOZContent|eJzLy8MAAFG3CCs='
    sheet_name = 'AOZContent'
    clear_time: List[int_t] = ListData(ir((0, 2, 1)), RowData)
    type: List[int_t] = ListData(ir((2, 3, 4)), RowData)
    data: List[int_t] = ListData(ir((3, 3, 4)), RowData)
    map: List[int_t] = ListData(ir((4, 3, 4)), RowData)
    content_entry_key: 'ContentEntry' = RowForeign(14, 'ContentEntry')
    ui_index: int_t = RowData(15)
    reward_gil: int_t = RowData(16)
    reward_allied_seal: int_t = RowData(17)
    reward_tomestone_a: int_t = RowData(18)


class AOZContent(DataRow):
    _sign = b'AOZContent|eJzLy0MFADqABuE='
    sheet_name = 'AOZContent'
    clear_time: List[int_t] = ListData(ir((0, 2, 1)), RowData)
    type: List[int_t] = ListData(ir((2, 3, 3)), RowData)
    data: List[int_t] = ListData(ir((3, 3, 3)), RowData)
    map: List[int_t] = ListData(ir((4, 3, 3)), RowData)
    content_entry_key: 'ContentEntry' = RowForeign(11, 'ContentEntry')
    ui_index: int_t = RowData(12)
    reward_gil: int_t = RowData(13)
    reward_allied_seal: int_t = RowData(14)
    reward_tomestone_a: int_t = RowData(15)


class AOZContentBriefingBNpc(DataRow):
    _sign = b'AOZContentBriefingBNpc|eJzLy8tLy0OANDgAAIlXCmc='
    sheet_name = 'AOZContentBriefingBNpc'
    _display = 'name'
    name: 'BNpcName' = RowForeign(0, 'BNpcName')
    icon: 'Icon' = IconRow(1)
    icon_detail: 'Icon' = IconRow(2)
    mask_param: bool_t = RowData(3)
    hp_type: int_t = RowData(4)
    elem_def: List[int_t] = ListData(ir((5, 10, 1)), RowData)
    status_def_0: bool_t = RowData(15)
    status_def_1: bool_t = RowData(16)
    status_def_2: bool_t = RowData(17)
    status_def_3: bool_t = RowData(18)
    status_def_4: bool_t = RowData(19)
    status_def_5: bool_t = RowData(20)
    status_def_6: bool_t = RowData(21)
    status_def_7: bool_t = RowData(22)
    status_def_8: bool_t = RowData(23)
    status_def_9: bool_t = RowData(24)


class AOZContentBriefingObject(DataRow):
    _sign = b'AOZContentBriefingObject|eJzLywMAAUwA3Q=='
    sheet_name = 'AOZContentBriefingObject'


class AOZReport(DataRow):
    _sign = b'AOZReport|eJzLy8sDAAKXAUs='
    sheet_name = 'AOZReport'
    content_finder_condition_id: int_t = RowData(0)
    reward: 'AOZReportReward' = RowForeign(1, 'AOZReportReward')
    save_index: int_t = RowData(2)


class AOZReportReward(DataRow):
    _sign = b'AOZReportReward|eJzLywMBAAkMApU='
    sheet_name = 'AOZReportReward'
    first_gil: int_t = RowData(0)
    first_allied_seal: int_t = RowData(1)
    first_tomestone_a: int_t = RowData(2)
    normal_gil: int_t = RowData(3)
    normal_allied_seal: int_t = RowData(4)
    normal_tomestone_a: int_t = RowData(5)


class AOZScore(DataRow):
    _sign = b'AOZScore|eJxLyysuBgAEPwG7'
    sheet_name = 'AOZScore'
    _display = 'text_name'
    show_in_list: bool_t = RowData(0)
    point: int_t = RowData(1)
    text_name: str_t = RowData(2)
    text_help: str_t = RowData(3)


class AOZWeeklyReward(DataRow):
    _sign = b'AOZWeeklyReward|eJzLy8sDAAKXAUs='
    sheet_name = 'AOZWeeklyReward'
    gil: int_t = RowData(0)
    allied_seal: int_t = RowData(1)
    tomestone_a: int_t = RowData(2)


class Achievement(DataRow):
    _sign = b'Achievement|eJzLKy7Oww4Al+ELNw=='
    sheet_name = 'Achievement'
    _display = 'text_name'
    category: 'AchievementCategory' = RowForeign(0, 'AchievementCategory')
    text_name: str_t = RowData(1)
    text_help: str_t = RowData(2)
    target: 'AchievementTarget' = RowForeign(3, 'AchievementTarget')
    recommend_level: int_t = RowData(4)
    point: int_t = RowData(5)
    title: 'Title' = RowForeign(6, 'Title')
    item: 'Item' = RowForeign(7, 'Item')
    item_bit: int_t = RowData(8)
    new_item_bit: int_t = RowData(9)
    reward_genre: int_t = RowData(10)
    icon: 'Icon' = IconRow(11)
    detail: int_t = RowData(12)
    condition_type: int_t = RowData(13)
    condition_arg: List[int_t] = ListData(ir((14, 9, 1)), RowData)
    priority: int_t = RowData(23)
    activity_feed_image: int_t = RowData(24)
    show_complete: 'AchievementHideCondition' = RowForeign(25, 'AchievementHideCondition')


class AchievementCategory(DataRow):
    _sign = b'AchievementCategory|eJwrzktLywMABmgCHA=='
    sheet_name = 'AchievementCategory'
    _display = 'text'
    text: str_t = RowData(0)
    kind: 'AchievementKind' = RowForeign(1, 'AchievementKind')
    valid: bool_t = RowData(2)
    show_complete: bool_t = RowData(3)
    sort: int_t = RowData(4)


class AchievementHideCondition(DataRow):
    _sign = b'AchievementHideCondition|eJxLS0sDAAJnATM='
    sheet_name = 'AchievementHideCondition'
    hide_in_complete: bool_t = RowData(0)
    hide_name: bool_t = RowData(1)
    hide_help: bool_t = RowData(2)


class AchievementKind(DataRow):
    _sign = b'AchievementKind|eJwrzgMAAVYA4g=='
    sheet_name = 'AchievementKind'
    _display = 'text'
    text: str_t = RowData(0)
    sort: int_t = RowData(1)


class AchievementTarget(DataRow):
    _sign = b'AchievementTarget|eJzLywMAAUwA3Q=='
    sheet_name = 'AchievementTarget'
    _display = 'class_job_category'
    target_category: int_t = RowData(0)
    class_job_category: int_t = RowData(1)


class Action(DataRow):
    _sign = b'Action|eJwrTstDgLS8NBgAssACeXASoSotD0VdGgDXoRxW'
    sheet_name = 'Action'
    _display = 'text'
    text: str_t = RowData(0)
    help_dummy: bool_t = RowData(1)
    icon: 'Icon' = IconRow(2)
    category: 'ActionCategory' = RowForeign(3, 'ActionCategory')
    sub_category: int_t = RowData(4)
    cast_timeline: 'ActionCastTimeline' = RowForeign(5, 'ActionCastTimeline')
    cast_vfx: 'ActionCastVFX' = RowForeign(6, 'ActionCastVFX')
    timeline: 'ActionTimeline' = RowForeign(7, 'ActionTimeline')
    hit_timeline: 'ActionTimeline' = RowForeign(8, 'ActionTimeline')
    archer_timeline: int_t = RowData(9)
    learn: 'ClassJob' = RowForeign(10, 'ClassJob')
    action_timeline_move: int_t = RowData(11)
    level: int_t = RowData(12)
    is_additional: bool_t = RowData(13)
    select_range: int_t = RowData(14)
    select_myself: bool_t = RowData(15)
    select_party: bool_t = RowData(16)
    select_alliance: bool_t = RowData(17)
    select_enemy: bool_t = RowData(18)
    select_others: bool_t = RowData(19)
    select_e_npc: bool_t = RowData(20)
    select_ground: bool_t = RowData(21)
    select_my_pet: bool_t = RowData(22)
    select_party_pet: bool_t = RowData(23)
    select_corpse: int_t = RowData(24)
    lay: bool_t = RowData(25)
    check_dir: bool_t = RowData(26)
    effect_type: int_t = RowData(27)
    effect_range: int_t = RowData(28)
    effect_width: int_t = RowData(29)
    effect_enemy: bool_t = RowData(30)
    cost_type: int_t = RowData(31)
    cost_value: int_t = RowData(32)
    cond: int_t = RowData(33)
    cond_arg: int_t = RowData(34)
    combo_parent: 'Action' = RowForeign(35, 'Action')
    combo_continue: bool_t = RowData(36)
    cast_time: int_t = RowData(37)
    cast_disp_time_add: int_t = RowData(38)
    recast_time: int_t = RowData(39)
    recast_group: int_t = RowData(40)
    recast_group_sub: int_t = RowData(41)
    charge_num: int_t = RowData(42)
    attack_type: 'AttackType' = RowForeign(43, 'AttackType')
    element: int_t = RowData(44)
    proc_status: 'ActionProcStatus' = RowForeign(45, 'ActionProcStatus')
    hate_type: int_t = RowData(46)
    reset_status: 'Status' = RowForeign(47, 'Status')
    reward: int_t = RowData(48)
    use_class_job: 'ClassJobCategory' = RowForeign(49, 'ClassJobCategory')
    init: int_t = RowData(50)
    silence: bool_t = RowData(51)
    invalid_move: bool_t = RowData(52)
    omen: 'Omen' = RowForeign(53, 'Omen')
    debug_hit_omen: int_t = RowData(54)
    pvp_only: bool_t = RowData(55)
    is_avoid: bool_t = RowData(56)
    log_cast: bool_t = RowData(57)
    log_cast_myself: bool_t = RowData(58)
    log_miss: bool_t = RowData(59)
    log_exec: bool_t = RowData(60)
    force_vfx: bool_t = RowData(61)
    hide_cast_bar: bool_t = RowData(62)
    is_target_line: bool_t = RowData(63)
    normalize_action_group: int_t = RowData(64)
    valid_mount: bool_t = RowData(65)
    valid_swimming_or_diving_or_flying: bool_t = RowData(66)
    use_direction: bool_t = RowData(67)


class ActionCastTimeline(DataRow):
    _sign = b'ActionCastTimeline|eJzLywMAAUwA3Q=='
    sheet_name = 'ActionCastTimeline'
    _display = 'timeline'
    timeline: 'ActionTimeline' = RowForeign(0, 'ActionTimeline')
    weapon_vfx: 'VFX' = RowForeign(1, 'VFX')


class ActionCastVFX(DataRow):
    _sign = b'ActionCastVFX|eJzLAwAAbwBv'
    sheet_name = 'ActionCastVFX'
    _display = 'vfx'
    vfx: 'VFX' = RowForeign(0, 'VFX')


class ActionCategory(DataRow):
    _sign = b'ActionCategory|eJwrBgAAdAB0'
    sheet_name = 'ActionCategory'
    _display = 'text'
    text: str_t = RowData(0)


class ActionComboRoute(DataRow):
    _sign = b'ActionComboRoute|eJwrzoOCNAAX1gRK'
    sheet_name = 'ActionComboRoute'
    _display = 'text'
    text: str_t = RowData(0)
    route_index: int_t = RowData(1)
    action: List[int_t] = ListData(ir((2, 7, 1)), RowData)
    use_text_command: bool_t = RowData(9)


class ActionComboRouteTransient(DataRow):
    _sign = b'ActionComboRouteTransient|eJwrBgAAdAB0'
    sheet_name = 'ActionComboRouteTransient'
    text: str_t = RowData(0)


class ActionCostType(DataRow):
    _sign = b'ActionCostType|eJxLAwAAZwBn'
    sheet_name = 'ActionCostType'
    is_ui_disp: bool_t = RowData(0)


class ActionIndirection(DataRow):
    _sign = b'ActionIndirection|eJzLy8sDAAKXAUs='
    sheet_name = 'ActionIndirection'
    _display = 'action'
    action: 'Action' = RowForeign(0, 'Action')
    class_job: 'ClassJob' = RowForeign(1, 'ClassJob')
    replace_action: 'Action' = RowForeign(2, 'Action')


class ActionInit(DataRow):
    _sign = b'ActionInit|eJzLAwAAbwBv'
    sheet_name = 'ActionInit'
    drawn_sword: int_t = RowData(0)


class ActionParam(DataRow):
    _sign = b'ActionParam|eJzLywMAAUwA3Q=='
    sheet_name = 'ActionParam'
    _display = 'param'
    param: int_t = RowData(0)
    pvp_param: int_t = RowData(1)


class ActionProcStatus(DataRow):
    _sign = b'ActionProcStatus|eJzLAwAAbwBv'
    sheet_name = 'ActionProcStatus'
    _display = 'status'
    status: 'Status' = RowForeign(0, 'Status')


class ActionTimeline(DataRow):
    _sign = b'ActionTimeline|eJzLy0vLy8srzgOBtLw0EAIKAABrVAlC'
    sheet_name = 'ActionTimeline'
    _display = 'filename'
    type: int_t = RowData(0)
    priority: int_t = RowData(1)
    is_loop: bool_t = RowData(2)
    stance: int_t = RowData(3)
    slot: int_t = RowData(4)
    look_at_mode: int_t = RowData(5)
    filename: str_t = RowData(6)
    action_timeline_eid_mode: int_t = RowData(7)
    weapon_timeline: 'WeaponTimeline' = RowForeign(8, 'WeaponTimeline')
    load_type: int_t = RowData(9)
    start_attach: int_t = RowData(10)
    mount: int_t = RowData(11)
    ornament: bool_t = RowData(12)
    replace_group: int_t = RowData(13)
    is_motion_canceled_by_moving: bool_t = RowData(14)
    kill_upper: bool_t = RowData(15)
    cancel_emote: int_t = RowData(16)
    resident: bool_t = RowData(17)
    resident_pap: bool_t = RowData(18)
    pause: bool_t = RowData(19)
    random_start_frame: int_t = RowData(20)


class ActionTimeline(DataRow):
    _sign = b'ActionTimeline|eJzLy0vLy8srzgOBtLw0EErLAwBiEgjU'
    sheet_name = 'ActionTimeline'
    _display = 'filename'
    type: int_t = RowData(0)
    priority: int_t = RowData(1)
    is_loop: bool_t = RowData(2)
    stance: int_t = RowData(3)
    slot: int_t = RowData(4)
    look_at_mode: int_t = RowData(5)
    filename: str_t = RowData(6)
    action_timeline_eid_mode: int_t = RowData(7)
    weapon_timeline: 'WeaponTimeline' = RowForeign(8, 'WeaponTimeline')
    load_type: int_t = RowData(9)
    start_attach: int_t = RowData(10)
    mount: int_t = RowData(11)
    ornament: bool_t = RowData(12)
    replace_group: int_t = RowData(13)
    is_motion_canceled_by_moving: bool_t = RowData(14)
    kill_upper: bool_t = RowData(15)
    cancel_emote: int_t = RowData(16)
    resident: bool_t = RowData(17)
    resident_pap: bool_t = RowData(18)
    pause: bool_t = RowData(19)
    random_start_frame: int_t = RowData(20)


class ActionTimelineMove(DataRow):
    _sign = b'ActionTimelineMove|eJzLywOCNAAJBAKN'
    sheet_name = 'ActionTimelineMove'
    translate_type: int_t = RowData(0)
    translate_param: int_t = RowData(1)
    collision: int_t = RowData(2)
    rotate_type: int_t = RowData(3)
    rotate_param: int_t = RowData(4)
    stick_camera: bool_t = RowData(5)


class ActionTimelineReplace(DataRow):
    _sign = b'ActionTimelineReplace|eJzLywMAAUwA3Q=='
    sheet_name = 'ActionTimelineReplace'
    swimming: 'ActionTimeline' = RowForeign(0, 'ActionTimeline')
    diving: 'ActionTimeline' = RowForeign(1, 'ActionTimeline')


class ActionTransient(DataRow):
    _sign = b'ActionTransient|eJwrBgAAdAB0'
    sheet_name = 'ActionTransient'
    _display = 'text'
    text: str_t = RowData(0)


class ActivityFeedButtons(DataRow):
    _sign = b'ActivityFeedButtons|eJzLKwYCAAapAjs='
    sheet_name = 'ActivityFeedButtons'
    field_0: int_t = RowData(0)
    banner_url: str_t = RowData(1)
    description: str_t = RowData(2)
    language: str_t = RowData(3)
    picture_url: str_t = RowData(4)


class ActivityFeedCaptions(DataRow):
    _sign = b'ActivityFeedCaptions|eJwrLi4uBgAEggHN'
    sheet_name = 'ActivityFeedCaptions'
    ja: str_t = RowData(0)
    en: str_t = RowData(1)
    de: str_t = RowData(2)
    fr: str_t = RowData(3)


class ActivityFeedGroupCaptions(DataRow):
    _sign = b'ActivityFeedGroupCaptions|eJwrLi4uBgAEggHN'
    sheet_name = 'ActivityFeedGroupCaptions'
    ja: str_t = RowData(0)
    en: str_t = RowData(1)
    de: str_t = RowData(2)
    fr: str_t = RowData(3)


class ActivityFeedImages(DataRow):
    _sign = b'ActivityFeedImages|eJwrLgYCAAbCAkA='
    sheet_name = 'ActivityFeedImages'
    expansion_image: str_t = RowData(0)
    activity_feed_ja: str_t = RowData(1)
    activity_feed_en: str_t = RowData(2)
    activity_feed_de: str_t = RowData(3)
    activity_feed_fr: str_t = RowData(4)


class Addon(DataRow):
    _sign = b'Addon|eJwrBgAAdAB0'
    sheet_name = 'Addon'
    _display = 'text'
    text: str_t = RowData(0)


class AddonHudSize(DataRow):
    _sign = b'AddonHudSize|eJzLy8vLAwAEUAG5'
    sheet_name = 'AddonHudSize'
    x: int_t = RowData(0)
    y: int_t = RowData(1)
    w: int_t = RowData(2)
    h: int_t = RowData(3)


class AddonLayout(DataRow):
    _sign = b'AddonLayout|eJzLy8vLAwAEUAG5'
    sheet_name = 'AddonLayout'
    align: int_t = RowData(0)
    x: float_t = RowData(1)
    y: float_t = RowData(2)
    scale: int_t = RowData(3)


class AddonParam(DataRow):
    _sign = b'AddonParam|eJwrTgMAAU4A2g=='
    sheet_name = 'AddonParam'
    text_0: str_t = RowData(0)
    flag_1: bool_t = RowData(1)


class AddonTalkParam(DataRow):
    _sign = b'AddonTalkParam|eJzLywMBAAkMApU='
    sheet_name = 'AddonTalkParam'
    num_0: int_t = RowData(0)
    num_1: int_t = RowData(1)
    num_2: int_t = RowData(2)
    num_3: int_t = RowData(3)
    num_4: int_t = RowData(4)
    num_5: int_t = RowData(5)


class AddonTransient(DataRow):
    _sign = b'AddonTransient|eJwrBgAAdAB0'
    sheet_name = 'AddonTransient'
    text: str_t = RowData(0)


class AdvancedVibration(DataRow):
    _sign = b'AdvancedVibration|eJwrzisGQgAJSAKk'
    sheet_name = 'AdvancedVibration'
    vib_file: str_t = RowData(0)
    vib_file_index: int_t = RowData(1)
    snd_file1: str_t = RowData(2)
    snd_file1_index: int_t = RowData(3)
    snd_file2: str_t = RowData(4)
    snd_file2_index: int_t = RowData(5)


class Adventure(DataRow):
    _sign = b'Adventure|eJzLy4OC4uLivDQALWAGDA=='
    sheet_name = 'Adventure'
    _display = 'text_title_text'
    layout_id: 'Level' = RowForeign(0, 'Level')
    exp_param: int_t = RowData(1)
    clear_min_lv: int_t = RowData(2)
    clear_emote_cond: 'Emote' = RowForeign(3, 'Emote')
    clear_start_time_cond: int_t = RowData(4)
    clear_end_time_cond: int_t = RowData(5)
    area_name: 'PlaceName' = RowForeign(6, 'PlaceName')
    spot_icon: 'Icon' = IconRow(7)
    landscape_picture: 'Icon' = IconRow(8)
    text_title_text: str_t = RowData(9)
    text_hint_text: str_t = RowData(10)
    text_flavor_text: str_t = RowData(11)
    region_picture: 'Icon' = IconRow(12)
    is_show_region: bool_t = RowData(13)


class AdventureExPhase(DataRow):
    _sign = b'AdventureExPhase|eJzLywMCAAZ3Aic='
    sheet_name = 'AdventureExPhase'
    open_quest: 'Quest' = RowForeign(0, 'Quest')
    adventure_start: 'Adventure' = RowForeign(1, 'Adventure')
    adventure_end: 'Adventure' = RowForeign(2, 'Adventure')
    ex_disk_version: 'ExVersion' = RowForeign(3, 'ExVersion')
    complete_screen_image: int_t = RowData(4)


class AetherCurrent(DataRow):
    _sign = b'AetherCurrent|eJzLAwAAbwBv'
    sheet_name = 'AetherCurrent'
    _display = 'quest'
    quest: 'Quest' = RowForeign(0, 'Quest')


class AetherCurrentCompFlgSet(DataRow):
    _sign = b'AetherCurrentCompFlgSet|eJzLy0MFADqABuE='
    sheet_name = 'AetherCurrentCompFlgSet'
    territory: 'TerritoryType' = RowForeign(0, 'TerritoryType')
    aeter_current: List[int_t] = ListData(ir((1, 15, 1)), RowData)


class AetherialWheel(DataRow):
    _sign = b'AetherialWheel|eJzLy8vLAwAEUAG5'
    sheet_name = 'AetherialWheel'
    wheel_item_id: 'Item' = RowForeign(0, 'Item')
    wheel_energy_item_id: 'Item' = RowForeign(1, 'Item')
    grade: int_t = RowData(2)
    sublime_hour: int_t = RowData(3)


class Aetheryte(DataRow):
    _sign = b'Aetheryte|eJwrzivOQwJpxXlpYAYAgZYKUA=='
    sheet_name = 'Aetheryte'
    _display = 'telepo_name'
    text_sgl: str_t = RowData(0)
    text_sgg: int_t = RowData(1)
    text_plr: str_t = RowData(2)
    text_plg: int_t = RowData(3)
    text_vow: int_t = RowData(4)
    text_cnt: int_t = RowData(5)
    text_gen: int_t = RowData(6)
    text_def_: int_t = RowData(7)
    telepo_name: 'PlaceName' = RowForeign(8, 'PlaceName')
    transfer_name: 'PlaceName' = RowForeign(9, 'PlaceName')
    territory_type: 'TerritoryType' = RowForeign(10, 'TerritoryType')
    pop_range: List[int_t] = ListData(ir((11, 4, 1)), RowData)
    telepo: bool_t = RowData(15)
    script: str_t = RowData(16)
    town: int_t = RowData(17)
    is_bonus: bool_t = RowData(18)
    unlock_quest: 'Quest' = RowForeign(19, 'Quest')
    map: 'Map' = RowForeign(20, 'Map')
    cost_pos_x: int_t = RowData(21)
    cost_pos_y: int_t = RowData(22)
    sort_key: int_t = RowData(23)


class AetheryteSystemDefine(DataRow):
    _sign = b'AetheryteSystemDefine|eJwrzgMAAVYA4g=='
    sheet_name = 'AetheryteSystemDefine'
    _display = 'define_name'
    define_name: str_t = RowData(0)
    define_value: int_t = RowData(1)


class AetheryteTransient(DataRow):
    _sign = b'AetheryteTransient|eJxLAwAAZwBn'
    sheet_name = 'AetheryteTransient'
    is_outside: bool_t = RowData(0)


class AirshipExplorationLevel(DataRow):
    _sign = b'AirshipExplorationLevel|eJzLywMAAUwA3Q=='
    sheet_name = 'AirshipExplorationLevel'
    cost_limit: int_t = RowData(0)
    lv_up_exp: int_t = RowData(1)


class AirshipExplorationLog(DataRow):
    _sign = b'AirshipExplorationLog|eJwrBgAAdAB0'
    sheet_name = 'AirshipExplorationLog'
    _display = 'text'
    text: str_t = RowData(0)


class AirshipExplorationParamType(DataRow):
    _sign = b'AirshipExplorationParamType|eJwrBgAAdAB0'
    sheet_name = 'AirshipExplorationParamType'
    _display = 'text'
    text: str_t = RowData(0)


class AirshipExplorationPart(DataRow):
    _sign = b'AirshipExplorationPart|eJzLy4MBABesBE0='
    sheet_name = 'AirshipExplorationPart'
    category: int_t = RowData(0)
    airship_level: int_t = RowData(1)
    cost: int_t = RowData(2)
    exploration: int_t = RowData(3)
    carry: int_t = RowData(4)
    cruise: int_t = RowData(5)
    fuel: int_t = RowData(6)
    luck: int_t = RowData(7)
    pattern_id: int_t = RowData(8)
    repair_item_num: int_t = RowData(9)


class AirshipExplorationPoint(DataRow):
    _sign = b'AirshipExplorationPoint|eJwrLk7LQwAALVMGBw=='
    sheet_name = 'AirshipExplorationPoint'
    _display = 'text_name'
    text_name: str_t = RowData(0)
    text_abbreviation: str_t = RowData(1)
    for_content: bool_t = RowData(2)
    x: int_t = RowData(3)
    y: int_t = RowData(4)
    level: int_t = RowData(5)
    energy: int_t = RowData(6)
    time: int_t = RowData(7)
    fuel_consumption: int_t = RowData(8)
    condition_category: List[int_t] = ListData(ir((9, 2, 2)), RowData)
    condition_param: List[int_t] = ListData(ir((10, 2, 2)), RowData)
    reward_exp: int_t = RowData(13)


class AirshipSkyIsland(DataRow):
    _sign = b'AirshipSkyIsland|eJzLywMBAAkMApU='
    sheet_name = 'AirshipSkyIsland'
    level: int_t = RowData(0)
    point: int_t = RowData(1)
    condition_category: List[int_t] = ListData(ir((2, 2, 2)), RowData)
    condition_param: List[int_t] = ListData(ir((3, 2, 2)), RowData)


class AkatsukiNote(DataRow):
    _sign = b'AkatsukiNote|eJzLy4MCABNfA98='
    sheet_name = 'AkatsukiNote'
    sort: int_t = RowData(0)
    check_id: int_t = RowData(1)
    item_text_id: int_t = RowData(2)
    disclosure_value0: int_t = RowData(3)
    disclosure_value1: int_t = RowData(4)
    detail_title_text_id: int_t = RowData(5)
    detail_image: int_t = RowData(6)
    job_text_id: int_t = RowData(7)
    detail_main_text_id: int_t = RowData(8)


class AkatsukiNoteString(DataRow):
    _sign = b'AkatsukiNoteString|eJwrBgAAdAB0'
    sheet_name = 'AkatsukiNoteString'
    text: str_t = RowData(0)


class AnimaWeapon5(DataRow):
    _sign = b'AnimaWeapon5|eJzLy4MAAA+AA3E='
    sheet_name = 'AnimaWeapon5'
    base_item: 'Item' = RowForeign(0, 'Item')
    icon: int_t = RowData(1)
    strengthening_max: int_t = RowData(2)
    param: List[int_t] = ListData(ir((3, 5, 1)), RowData)


class AnimaWeapon5Param(DataRow):
    _sign = b'AnimaWeapon5Param|eJzLKwYAAVEA4g=='
    sheet_name = 'AnimaWeapon5Param'
    _display = 'base_param'
    base_param: 'BaseParam' = RowForeign(0, 'BaseParam')
    ui_name: str_t = RowData(1)


class AnimaWeapon5PatternGroup(DataRow):
    _sign = b'AnimaWeapon5PatternGroup|eJwrBgAAdAB0'
    sheet_name = 'AnimaWeapon5PatternGroup'
    _display = 'name'
    name: str_t = RowData(0)


class AnimaWeapon5SpiritTalk(DataRow):
    _sign = b'AnimaWeapon5SpiritTalk|eJzLAwAAbwBv'
    sheet_name = 'AnimaWeapon5SpiritTalk'
    _display = 'param'
    param: 'AnimaWeapon5SpiritTalkParam' = RowForeign(0, 'AnimaWeapon5SpiritTalkParam')


class AnimaWeapon5SpiritTalkParam(DataRow):
    _sign = b'AnimaWeapon5SpiritTalkParam|eJwrLgYAAVsA5w=='
    sheet_name = 'AnimaWeapon5SpiritTalkParam'
    _display = 'text_male'
    text_male: str_t = RowData(0)
    text_female: str_t = RowData(1)


class AnimaWeapon5SpiritTalkType(DataRow):
    _sign = b'AnimaWeapon5SpiritTalkType|eJzLAwAAbwBv'
    sheet_name = 'AnimaWeapon5SpiritTalkType'
    rate: int_t = RowData(0)


class AnimaWeapon5TradeItem(DataRow):
    _sign = b'AnimaWeapon5TradeItem|eJzLy8vLS8KBAKmAC6k='
    sheet_name = 'AnimaWeapon5TradeItem'
    pattern_group: int_t = RowData(0)
    output_item: 'Item' = RowForeign(1, 'Item')
    output_num: int_t = RowData(2)
    input_item: List[int_t] = ListData(ir((3, 8, 3)), RowData)
    is_input_hq: List[bool_t] = ListData(ir((4, 8, 3)), RowData)
    input_num: List[int_t] = ListData(ir((5, 8, 3)), RowData)
    ui_sort_key: 'AnimaWeapon5PatternGroup' = RowForeign(27, 'AnimaWeapon5PatternGroup')


class AnimaWeaponFUITalk(DataRow):
    _sign = b'AnimaWeaponFUITalk|eJzLAwAAbwBv'
    sheet_name = 'AnimaWeaponFUITalk'
    _display = 'param'
    param: 'AnimaWeaponFUITalkParam' = RowForeign(0, 'AnimaWeaponFUITalkParam')


class AnimaWeaponFUITalkParam(DataRow):
    _sign = b'AnimaWeaponFUITalkParam|eJwrLgYAAVsA5w=='
    sheet_name = 'AnimaWeaponFUITalkParam'
    _display = 'text_male'
    text_male: str_t = RowData(0)
    text_female: str_t = RowData(1)


class AnimaWeaponIcon(DataRow):
    _sign = b'AnimaWeaponIcon|eJzLywMCAAZ3Aic='
    sheet_name = 'AnimaWeaponIcon'
    icon4: 'Icon' = IconRow(0)
    icon5: 'Icon' = IconRow(1)
    icon6: 'Icon' = IconRow(2)
    icon7: 'Icon' = IconRow(3)
    icon8: 'Icon' = IconRow(4)


class AnimaWeaponItem(DataRow):
    _sign = b'AnimaWeaponItem|eJzLy0MGAC0sBgU='
    sheet_name = 'AnimaWeaponItem'
    item: List[int_t] = ListData(ir((0, 14, 1)), RowData)


class AnimationLOD(DataRow):
    _sign = b'AnimationLOD|eJzLy8tLggIAGrcEWw=='
    sheet_name = 'AnimationLOD'
    camera_distance: float_t = RowData(0)
    sample_interval: float_t = RowData(1)
    bone_lod: int_t = RowData(2)
    animation_enable: List[bool_t] = ListData(ir((3, 8, 1)), RowData)


class AozAction(DataRow):
    _sign = b'AozAction|eJzLywMAAUwA3Q=='
    sheet_name = 'AozAction'
    _display = 'learning_action'
    learning_action: 'Action' = RowForeign(0, 'Action')
    rarity: int_t = RowData(1)


class AozActionTransient(DataRow):
    _sign = b'AozActionTransient|eJzLyysuzgOCNCQAAFiPCEM='
    sheet_name = 'AozActionTransient'
    ui_priority: int_t = RowData(0)
    large_icon: 'Icon' = IconRow(1)
    text_effect: str_t = RowData(2)
    text_description: str_t = RowData(3)
    learning_source_type: int_t = RowData(4)
    place_name: int_t = RowData(5)
    target_job_quest: 'Quest' = RowForeign(6, 'Quest')
    prev_job_quest: 'Quest' = RowForeign(7, 'Quest')
    filter_flag__target_enemy: bool_t = RowData(8)
    filter_flag__target_friend: bool_t = RowData(9)
    filter_flag__status_slow: bool_t = RowData(10)
    filter_flag__status_stone: bool_t = RowData(11)
    filter_flag__status_palsy: bool_t = RowData(12)
    filter_flag__status_silence: bool_t = RowData(13)
    filter_flag__status_blind: bool_t = RowData(14)
    filter_flag__status_stun: bool_t = RowData(15)
    filter_flag__status_sleep: bool_t = RowData(16)
    filter_flag__status_bind: bool_t = RowData(17)
    filter_flag__status_heavy: bool_t = RowData(18)
    filter_flag__status_death: bool_t = RowData(19)


class AquariumFish(DataRow):
    _sign = b'AquariumFish|eJzLy8vLAwAEUAG5'
    sheet_name = 'AquariumFish'
    _display = 'item'
    water: 'AquariumWater' = RowForeign(0, 'AquariumWater')
    size: int_t = RowData(1)
    item: 'Item' = RowForeign(2, 'Item')
    kind: int_t = RowData(3)


class AquariumWater(DataRow):
    _sign = b'AquariumWater|eJzLKwYAAVEA4g=='
    sheet_name = 'AquariumWater'
    _display = 'text'
    kind: int_t = RowData(0)
    text: str_t = RowData(1)


class ArchiveItem(DataRow):
    _sign = b'ArchiveItem|eJzLy0sDAAKPAUM='
    sheet_name = 'ArchiveItem'
    item: int_t = RowData(0)
    item_num: int_t = RowData(1)
    hq: bool_t = RowData(2)


class ArrayEventHandler(DataRow):
    _sign = b'ArrayEventHandler|eJzLy0MFADqABuE='
    sheet_name = 'ArrayEventHandler'
    event_handler: List[int_t] = ListData(ir((0, 16, 1)), RowData)


class AttackType(DataRow):
    _sign = b'AttackType|eJwrBgAAdAB0'
    sheet_name = 'AttackType'
    _display = 'text'
    text: str_t = RowData(0)


class Attract(DataRow):
    _sign = b'Attract|eJzLy8tLywMABmcCHw=='
    sheet_name = 'Attract'
    distance: int_t = RowData(0)
    speed: int_t = RowData(1)
    offset: int_t = RowData(2)
    radius: bool_t = RowData(3)
    direction: int_t = RowData(4)


class Attributive(DataRow):
    _sign = b'Attributive|eJwrLiYSAACC/xJs'
    sheet_name = 'Attributive'
    text_0: str_t = RowData(0)
    text_1: str_t = RowData(1)
    text_2: str_t = RowData(2)
    text_3: str_t = RowData(3)
    text_4: str_t = RowData(4)
    text_5: str_t = RowData(5)
    text_6: str_t = RowData(6)
    text_7: str_t = RowData(7)
    text_8: str_t = RowData(8)
    text_9: str_t = RowData(9)
    text_10: str_t = RowData(10)
    text_11: str_t = RowData(11)
    text_12: str_t = RowData(12)
    text_13: str_t = RowData(13)
    text_14: str_t = RowData(14)
    text_15: str_t = RowData(15)
    text_16: str_t = RowData(16)
    text_17: str_t = RowData(17)
    text_18: str_t = RowData(18)
    text_19: str_t = RowData(19)
    text_20: str_t = RowData(20)
    text_21: str_t = RowData(21)
    text_22: str_t = RowData(22)
    text_23: str_t = RowData(23)
    text_24: str_t = RowData(24)
    text_25: str_t = RowData(25)
    text_26: str_t = RowData(26)
    text_27: str_t = RowData(27)
    text_28: str_t = RowData(28)
    text_29: str_t = RowData(29)
    text_30: str_t = RowData(30)
    text_31: str_t = RowData(31)
    text_32: str_t = RowData(32)
    text_33: str_t = RowData(33)
    text_34: str_t = RowData(34)
    text_35: str_t = RowData(35)
    text_36: str_t = RowData(36)
    text_37: str_t = RowData(37)
    text_38: str_t = RowData(38)
    text_39: str_t = RowData(39)
    text_40: str_t = RowData(40)


class BGM(DataRow):
    _sign = b'BGM|eJwrzktLS8vLAwAL0gLw'
    sheet_name = 'BGM'
    _display = 'path'
    path: str_t = RowData(0)
    priority: int_t = RowData(1)
    pass_end: bool_t = RowData(2)
    disable_restart: bool_t = RowData(3)
    disable_restart_time_out: bool_t = RowData(4)
    disable_restart_reset_time: float_t = RowData(5)
    special_mode: int_t = RowData(6)


class BGMFade(DataRow):
    _sign = b'BGMFade|eJzLy8sDAAKXAUs='
    sheet_name = 'BGMFade'
    scene_out: int_t = RowData(0)
    scene_in: int_t = RowData(1)
    fade_type: 'BGMFadeType' = RowForeign(2, 'BGMFadeType')


class BGMFadeType(DataRow):
    _sign = b'BGMFadeType|eJzLy8vLAwAEUAG5'
    sheet_name = 'BGMFadeType'
    fade_out_time: float_t = RowData(0)
    fade_in_time: float_t = RowData(1)
    fade_in_start_time: float_t = RowData(2)
    resume_fade_in_time: float_t = RowData(3)


class BGMScene(DataRow):
    _sign = b'BGMScene|eJxLSwMCAAX/Af8='
    sheet_name = 'BGMScene'
    ignore_battle: bool_t = RowData(0)
    force_auto_reset: bool_t = RowData(1)
    enable_pass_end: bool_t = RowData(2)
    resume: bool_t = RowData(3)
    enable_disable_restart: bool_t = RowData(4)


class BGMSituation(DataRow):
    _sign = b'BGMSituation|eJzLywMCAAZ3Aic='
    sheet_name = 'BGMSituation'
    daytime_id: 'BGM' = RowForeign(0, 'BGM')
    night_id: 'BGM' = RowForeign(1, 'BGM')
    battle_id: 'BGM' = RowForeign(2, 'BGM')
    daybreak_id: 'BGM' = RowForeign(3, 'BGM')
    twilight_id: 'BGM' = RowForeign(4, 'BGM')


class BGMSwitch(DataRow):
    _sign = b'BGMSwitch|eJzLy8vLAwAEUAG5'
    sheet_name = 'BGMSwitch'
    type: 'BGMSystemDefine' = RowForeign(0, 'BGMSystemDefine')
    param0: 'Quest' = RowForeign(1, 'Quest')
    param1: int_t = RowData(2)
    bgm: int_t = RowData(3)


class BGMSystemDefine(DataRow):
    _sign = b'BGMSystemDefine|eJzLAwAAbwBv'
    sheet_name = 'BGMSystemDefine'
    _display = 'value_float'
    value_float: float_t = RowData(0)


class BKJEObj(DataRow):
    _sign = b'BKJEObj|eJzLy8vLAwAEUAG5'
    sheet_name = 'BKJEObj'
    base_id: int_t = RowData(0)
    strategy_type: int_t = RowData(1)
    layout_id: int_t = RowData(2)
    work_index: int_t = RowData(3)


class BKJLivestock(DataRow):
    _sign = b'BKJLivestock|eJzLAwAAbwBv'
    sheet_name = 'BKJLivestock'
    b_npc_base_id: int_t = RowData(0)


class BKJPouch(DataRow):
    _sign = b'BKJPouch|eJzLywMAAUwA3Q=='
    sheet_name = 'BKJPouch'
    catalog_id: int_t = RowData(0)
    category: int_t = RowData(1)


class BKJSeed(DataRow):
    _sign = b'BKJSeed|eJzLAwAAbwBv'
    sheet_name = 'BKJSeed'
    shared_group: int_t = RowData(0)


class BKJShipment(DataRow):
    _sign = b'BKJShipment|eJzLywMAAUwA3Q=='
    sheet_name = 'BKJShipment'
    num_0: int_t = RowData(0)
    num_1: int_t = RowData(1)


class BKJSpecialtyGoods(DataRow):
    _sign = b'BKJSpecialtyGoods|eJzLAwAAbwBv'
    sheet_name = 'BKJSpecialtyGoods'
    shared_group_id: int_t = RowData(0)


class BNpcAnnounceIcon(DataRow):
    _sign = b'BNpcAnnounceIcon|eJzLAwAAbwBv'
    sheet_name = 'BNpcAnnounceIcon'
    _display = 'icon'
    icon: 'Icon' = IconRow(0)


class BNpcBase(DataRow):
    _sign = b'BNpcBase|eJzLy4OBNDABBEAKAGu8CU0='
    sheet_name = 'BNpcBase'
    normal_ai: 'Behavior' = RowForeign(0, 'Behavior')
    battalion: 'Battalion' = RowForeign(1, 'Battalion')
    link_race: 'LinkRace' = RowForeign(2, 'LinkRace')
    rank: int_t = RowData(3)
    scale: float_t = RowData(4)
    model: 'ModelChara' = RowForeign(5, 'ModelChara')
    customize: 'BNpcCustomize' = RowForeign(6, 'BNpcCustomize')
    equipment: 'NpcEquip' = RowForeign(7, 'NpcEquip')
    se_pack: int_t = RowData(8)
    special: int_t = RowData(9)
    combo_position_ignored: bool_t = RowData(10)
    event_handler: 'ArrayEventHandler' = RowForeign(11, 'ArrayEventHandler')
    move_ai: int_t = RowData(12)
    parts: 'BNpcParts' = RowForeign(13, 'BNpcParts')
    pop_vfx: int_t = RowData(14)
    is_display_level: bool_t = RowData(15)
    is_target_line: bool_t = RowData(16)
    target_ring: bool_t = RowData(17)
    disp_force: bool_t = RowData(18)
    announce_icon: int_t = RowData(19)
    element: int_t = RowData(20)
    bot_knowledge: int_t = RowData(21)


class BNpcBasePopVfx(DataRow):
    _sign = b'BNpcBasePopVfx|eJzLAwAAbwBv'
    sheet_name = 'BNpcBasePopVfx'
    vfx: int_t = RowData(0)


class BNpcCustomize(DataRow):
    _sign = b'BNpcCustomize|eJzLy8MFAJbsCy0='
    sheet_name = 'BNpcCustomize'
    customize: 'List[Tribe]' = ListData(ir((0, 26, 1)), RowForeign, 'Tribe')


class BNpcName(DataRow):
    _sign = b'BNpcName|eJwrzivOAwEAD8YDew=='
    sheet_name = 'BNpcName'
    _display = 'text_sgl'
    text_sgl: str_t = RowData(0)
    text_sgg: int_t = RowData(1)
    text_plr: str_t = RowData(2)
    text_plg: int_t = RowData(3)
    text_vow: int_t = RowData(4)
    text_cnt: int_t = RowData(5)
    text_gen: int_t = RowData(6)
    text_def_: int_t = RowData(7)


class BNpcParts(DataRow):
    _sign = b'BNpcParts|eJzLy0sCgjwIIIsJAI8ZGz0='
    sheet_name = 'BNpcParts'
    parts: 'List[BNpcBase]' = ListData(ir((0, 6, 11)), RowForeign, 'BNpcBase')
    model_attribute: List[int_t] = ListData(ir((1, 6, 11)), RowData)
    att_default: List[bool_t] = ListData(ir((2, 6, 11)), RowData)
    timeline: List[bool_t] = ListData(ir((3, 6, 11)), RowData)
    play_break_timeline: List[bool_t] = ListData(ir((4, 6, 11)), RowData)
    offset_y_chara: List[bool_t] = ListData(ir((5, 6, 11)), RowData)
    offset_x: List[float_t] = ListData(ir((6, 6, 11)), RowData)
    offset_y: List[float_t] = ListData(ir((7, 6, 11)), RowData)
    offset_z: List[float_t] = ListData(ir((8, 6, 11)), RowData)
    dir_offset: List[int_t] = ListData(ir((9, 6, 11)), RowData)
    radius: List[float_t] = ListData(ir((10, 6, 11)), RowData)


class BNpcState(DataRow):
    _sign = b'BNpcState|eJzLywOBJDDMy0sDADKbBkc='
    sheet_name = 'BNpcState'
    slot: int_t = RowData(0)
    over_ray: List[int_t] = ListData(ir((1, 2, 1)), RowData)
    model_state: int_t = RowData(3)
    idle: int_t = RowData(4)
    model_attribute: List[int_t] = ListData(ir((5, 3, 2)), RowData)
    attribute_flag: List[bool_t] = ListData(ir((6, 3, 2)), RowData)
    scale: float_t = RowData(11)
    model_scale: int_t = RowData(12)
    loop_timeline: int_t = RowData(13)
    loop_timeline_clear: bool_t = RowData(14)


class BacklightColor(DataRow):
    _sign = b'BacklightColor|eJzLAwAAbwBv'
    sheet_name = 'BacklightColor'
    _display = 'color'
    color: int_t = RowData(0)


class Ballista(DataRow):
    _sign = b'Ballista|eJzLy4MDABxnBLs='
    sheet_name = 'Ballista'
    b_npc: 'BNpcBase' = RowForeign(0, 'BNpcBase')
    near: int_t = RowData(1)
    far: int_t = RowData(2)
    angle: int_t = RowData(3)
    bullet: List[int_t] = ListData(ir((4, 3, 1)), RowData)
    action: 'List[Action]' = ListData(ir((7, 3, 1)), RowForeign, 'Action')
    timeline: 'Action' = RowForeign(10, 'Action')


class Balloon(DataRow):
    _sign = b'Balloon|eJxLKwYAAUEA2g=='
    sheet_name = 'Balloon'
    _display = 'text'
    slowly: bool_t = RowData(0)
    text: str_t = RowData(1)


class BannerBg(DataRow):
    _sign = b'BannerBg|eJzLy8vLKwYABnwCLA=='
    sheet_name = 'BannerBg'
    _display = 'text'
    icon: 'Icon' = IconRow(0)
    list_icon: 'Icon' = IconRow(1)
    banner_condition: 'BannerCondition' = RowForeign(2, 'BannerCondition')
    sort_id: int_t = RowData(3)
    text: str_t = RowData(4)


class BannerCondition(DataRow):
    _sign = b'BannerCondition|eJzLy0MGaQAzlwZr'
    sheet_name = 'BannerCondition'
    condition_type: int_t = RowData(0)
    condition_data: List[int_t] = ListData(ir((1, 6, 1)), RowData)
    obtain_type: int_t = RowData(7)
    obtain_arg: List[int_t] = ListData(ir((8, 3, 1)), RowData)
    obtain_unlock_type: int_t = RowData(11)
    obtain_unlock_data: 'Quest' = RowForeign(12, 'Quest')
    obtain_hint_type: int_t = RowData(13)
    hide_if_not_obtain: bool_t = RowData(14)


class BannerDecoration(DataRow):
    _sign = b'BannerDecoration|eJzLy8vLKwYABnwCLA=='
    sheet_name = 'BannerDecoration'
    _display = 'text'
    icon: 'Icon' = IconRow(0)
    list_icon: 'Icon' = IconRow(1)
    banner_condition: 'BannerCondition' = RowForeign(2, 'BannerCondition')
    sort_id: int_t = RowData(3)
    text: str_t = RowData(4)


class BannerDesignPreset(DataRow):
    _sign = b'BannerDesignPreset|eJzLy8vLKwYABnwCLA=='
    sheet_name = 'BannerDesignPreset'
    _display = 'text'
    bg: 'BannerBg' = RowForeign(0, 'BannerBg')
    frame: 'BannerFrame' = RowForeign(1, 'BannerFrame')
    decoration: 'BannerDecoration' = RowForeign(2, 'BannerDecoration')
    sort_id: int_t = RowData(3)
    text: str_t = RowData(4)


class BannerFacial(DataRow):
    _sign = b'BannerFacial|eJzLy8sDAAKXAUs='
    sheet_name = 'BannerFacial'
    emote: 'Emote' = RowForeign(0, 'Emote')
    banner_condition: 'BannerCondition' = RowForeign(1, 'BannerCondition')
    sort_id: int_t = RowData(2)


class BannerFrame(DataRow):
    _sign = b'BannerFrame|eJzLy8vLKwYABnwCLA=='
    sheet_name = 'BannerFrame'
    _display = 'text'
    icon: 'Icon' = IconRow(0)
    list_icon: 'Icon' = IconRow(1)
    banner_condition: 'BannerCondition' = RowForeign(2, 'BannerCondition')
    sort_id: int_t = RowData(3)
    text: str_t = RowData(4)


class BannerObtainHintType(DataRow):
    _sign = b'BannerObtainHintType|eJwrBgAAdAB0'
    sheet_name = 'BannerObtainHintType'
    text: str_t = RowData(0)


class BannerPreset(DataRow):
    _sign = b'BannerPreset|eJzLy8MFAJbsCy0='
    sheet_name = 'BannerPreset'
    cam_pos_x: float_t = RowData(0)
    cam_pos_y: float_t = RowData(1)
    cam_pos_z: float_t = RowData(2)
    cam_look_at_x: float_t = RowData(3)
    cam_look_at_y: float_t = RowData(4)
    cam_look_at_z: float_t = RowData(5)
    cam_roll: int_t = RowData(6)
    cam_zoom: int_t = RowData(7)
    timeline: int_t = RowData(8)
    timeline_frame: float_t = RowData(9)
    facial: int_t = RowData(10)
    face_yaw: float_t = RowData(11)
    face_pitch: float_t = RowData(12)
    eye_yaw: float_t = RowData(13)
    eye_pitch: float_t = RowData(14)
    design: int_t = RowData(15)
    light1__color_r: int_t = RowData(16)
    light1__color_g: int_t = RowData(17)
    light1__color_b: int_t = RowData(18)
    light1__scale: int_t = RowData(19)
    light1__dir_h: int_t = RowData(20)
    light1__dir_v: int_t = RowData(21)
    light2__color_r: int_t = RowData(22)
    light2__color_g: int_t = RowData(23)
    light2__color_b: int_t = RowData(24)
    light2__scale: int_t = RowData(25)


class BannerTimeline(DataRow):
    _sign = b'BannerTimeline|eJzLywODYgAPhQN2'
    sheet_name = 'BannerTimeline'
    timeline_type: int_t = RowData(0)
    timeline_data: int_t = RowData(1)
    class_job: 'ClassJobCategory' = RowForeign(2, 'ClassJobCategory')
    filter_type: int_t = RowData(3)
    banner_condition: 'BannerCondition' = RowForeign(4, 'BannerCondition')
    sort_id: int_t = RowData(5)
    list_icon: 'Icon' = IconRow(6)
    text: str_t = RowData(7)


class BaseParam(DataRow):
    _sign = b'BaseParam|eJzLKy7OIwKkAQBiCBEz'
    sheet_name = 'BaseParam'
    _display = 'text_name'
    packet_index: int_t = RowData(0)
    text_name: str_t = RowData(1)
    text_help: str_t = RowData(2)
    sort_id: int_t = RowData(3)
    item_param_rate: List[int_t] = ListData(ir((4, 22, 1)), RowData)
    role_rate: List[int_t] = ListData(ir((26, 13, 1)), RowData)
    inv_sign: bool_t = RowData(39)


class Battalion(DataRow):
    _sign = b'Battalion|eJxLSkIBAC3/Bb8='
    sheet_name = 'Battalion'
    table: List[bool_t] = ListData(ir((0, 15, 1)), RowData)


class BattleLeve(DataRow):
    _sign = b'BattleLeve|eJzLyxuSAABEk06j'
    sheet_name = 'BattleLeve'
    route_point_time_route_point_time: List[int_t] = ListData(ir((0, 8, 1)), RowData)
    entry_base_id: List[int_t] = ListData(ir((8, 8, 1)), RowData)
    entry_level: List[int_t] = ListData(ir((16, 8, 1)), RowData)
    entry_name_id: List[int_t] = ListData(ir((24, 8, 1)), RowData)
    entry_drop_event_item_id: List[int_t] = ListData(ir((32, 8, 1)), RowData)
    entry_drop_event_item_max: List[int_t] = ListData(ir((40, 8, 1)), RowData)
    entry_drop_event_item_rate: List[int_t] = ListData(ir((48, 8, 1)), RowData)
    entry_param: List[List[int_t]] = ListData(ir(((56, 6, 8), 8, 1)), ListData, RowData)
    entry_num_of_appearance: List[List[int_t]] = ListData(ir(((104, 8, 8), 8, 1)), ListData, RowData)
    todo_todo_sequence: List[int_t] = ListData(ir((168, 8, 1)), RowData)
    rule: 'BattleLeveRule' = RowForeign(176, 'BattleLeveRule')
    variation: int_t = RowData(177)
    objective: 'List[LeveString]' = ListData(ir((178, 3, 1)), RowForeign, 'LeveString')
    help: List[int_t] = ListData(ir((181, 2, 1)), RowData)


class BattleLeveRule(DataRow):
    _sign = b'BattleLeveRule|eJwrBgAAdAB0'
    sheet_name = 'BattleLeveRule'
    _display = 'script'
    script: str_t = RowData(0)


class BeastRankBonus(DataRow):
    _sign = b'BeastRankBonus|eJzLy0MDAEHPB08='
    sheet_name = 'BeastRankBonus'
    exp_rate: List[int_t] = ListData(ir((0, 8, 1)), RowData)
    item: 'Item' = RowForeign(8, 'Item')
    item_num_multiple: List[int_t] = ListData(ir((9, 8, 1)), RowData)


class BeastReputationRank(DataRow):
    _sign = b'BeastReputationRank|eJzLKy7OAwAEaQHD'
    sheet_name = 'BeastReputationRank'
    _display = 'text_text'
    max_reputation_value: int_t = RowData(0)
    text_text: str_t = RowData(1)
    text_text_ex1: str_t = RowData(2)
    color: 'UIColor' = RowForeign(3, 'UIColor')


class BeastTribe(DataRow):
    _sign = b'BeastTribe|eJxLy4OCYiAE0wBJUQfE'
    sheet_name = 'BeastTribe'
    _display = 'text_sgl'
    fix_exp: bool_t = RowData(0)
    fix_exp_base_level_limit: int_t = RowData(1)
    rank_bonus: 'BeastRankBonus' = RowForeign(2, 'BeastRankBonus')
    reputation_icon: 'Icon' = IconRow(3)
    reward_icon: 'Icon' = IconRow(4)
    last_rank: int_t = RowData(5)
    category: 'ExVersion' = RowForeign(6, 'ExVersion')
    currency: 'Item' = RowForeign(7, 'Item')
    sort_id: int_t = RowData(8)
    text_sgl: str_t = RowData(9)
    text_sgg: int_t = RowData(10)
    text_plr: str_t = RowData(11)
    text_plg: int_t = RowData(12)
    text_vow: int_t = RowData(13)
    text_cnt: int_t = RowData(14)
    text_gen: int_t = RowData(15)
    text_def_: int_t = RowData(16)
    text_reputation_value: str_t = RowData(17)


class Behavior(DataRow):
    _sign = b'Behavior|eJzLy0MDAEHPB08='
    sheet_name = 'Behavior'
    pack: int_t = RowData(0)
    caster: int_t = RowData(1)
    target: int_t = RowData(2)
    action: int_t = RowData(3)
    action_arg: 'Balloon' = RowForeign(4, 'Balloon')
    action_arg2: int_t = RowData(5)
    action_arg3: int_t = RowData(6)
    move_method: int_t = RowData(7)
    balloon: int_t = RowData(8)
    cond0__target: int_t = RowData(9)
    cond0__type: int_t = RowData(10)
    cont0__type_arg0: int_t = RowData(11)
    cont0__type_arg1: int_t = RowData(12)
    cond1__target: int_t = RowData(13)
    cond1__type: int_t = RowData(14)
    cont1__type_arg0: int_t = RowData(15)
    cont1__type_arg1: int_t = RowData(16)


class BehaviorMove(DataRow):
    _sign = b'BehaviorMove|eJxLy8tLAwAEKAGp'
    sheet_name = 'BehaviorMove'
    running: bool_t = RowData(0)
    fade_type: int_t = RowData(1)
    speed: float_t = RowData(2)
    warp_at_start: bool_t = RowData(3)


class BehaviorPath(DataRow):
    _sign = b'BehaviorPath|eJxLSwOCPAAIbAJt'
    sheet_name = 'BehaviorPath'
    is_walking: bool_t = RowData(0)
    is_fade_in: bool_t = RowData(1)
    is_fade_out: bool_t = RowData(2)
    is_turn_transition: bool_t = RowData(3)
    is_warp_to_begin: bool_t = RowData(4)
    speed: float_t = RowData(5)


class BenchmarkCutSceneTable(DataRow):
    _sign = b'BenchmarkCutSceneTable|eJwrzgOCtDwADCIDAA=='
    sheet_name = 'BenchmarkCutSceneTable'
    text_0: str_t = RowData(0)
    num_1: int_t = RowData(1)
    float_2: float_t = RowData(2)
    float_3: float_t = RowData(3)
    num_4: int_t = RowData(4)
    flag_5: bool_t = RowData(5)
    num_6: int_t = RowData(6)


class BenchmarkOverrideEquipment(DataRow):
    _sign = b'BenchmarkOverrideEquipment|eJzLy8MHAMfsDOU='
    sheet_name = 'BenchmarkOverrideEquipment'
    field_0: int_t = RowData(0)
    field_1: int_t = RowData(1)
    field_2: int_t = RowData(2)
    field_3: int_t = RowData(3)
    model_main_hand: int_t = RowData(4)
    dye_main_hand: 'Stain' = RowForeign(5, 'Stain')
    model_off_hand: int_t = RowData(6)
    dye_off_hand: 'Stain' = RowForeign(7, 'Stain')
    field_8: int_t = RowData(8)
    field_9: int_t = RowData(9)
    model_head: int_t = RowData(10)
    dye_head: 'Stain' = RowForeign(11, 'Stain')
    model_body: int_t = RowData(12)
    dye_body: 'Stain' = RowForeign(13, 'Stain')
    model_hands: int_t = RowData(14)
    dye_hands: 'Stain' = RowForeign(15, 'Stain')
    model_legs: int_t = RowData(16)
    dye_legs: 'Stain' = RowForeign(17, 'Stain')
    model_feet: int_t = RowData(18)
    dye_feet: 'Stain' = RowForeign(19, 'Stain')
    model_ears: int_t = RowData(20)
    dye_ears: 'Stain' = RowForeign(21, 'Stain')
    model_neck: int_t = RowData(22)
    dye_neck: 'Stain' = RowForeign(23, 'Stain')
    model_wrists: int_t = RowData(24)
    dye_wrists: 'Stain' = RowForeign(25, 'Stain')
    model_left_ring: int_t = RowData(26)
    dye_left_ring: 'Stain' = RowForeign(27, 'Stain')
    model_right_ring: int_t = RowData(28)
    dye_right_ring: 'Stain' = RowForeign(29, 'Stain')


class BgcArmyAction(DataRow):
    _sign = b'BgcArmyAction|eJzLK87LSwMABoMCJA=='
    sheet_name = 'BgcArmyAction'
    action: int_t = RowData(0)
    text: str_t = RowData(1)
    icon: int_t = RowData(2)
    ui_priority: int_t = RowData(3)
    indirection: bool_t = RowData(4)


class BgcArmyActionTransient(DataRow):
    _sign = b'BgcArmyActionTransient|eJwrBgAAdAB0'
    sheet_name = 'BgcArmyActionTransient'
    text: str_t = RowData(0)


class Booster(DataRow):
    _sign = b'Booster|eJzLy8vLAwAEUAG5'
    sheet_name = 'Booster'
    kind: int_t = RowData(0)
    catalog_id: int_t = RowData(1)
    check_level: int_t = RowData(2)
    event_picture: int_t = RowData(3)


class Buddy(DataRow):
    _sign = b'Buddy|eJzLy8vLKwYCAA+yA4U='
    sheet_name = 'Buddy'
    base: int_t = RowData(0)
    base_equip: 'List[Quest]' = ListData(ir((1, 3, 1)), RowForeign, 'Quest')
    action_se: List[str_t] = ListData(ir((4, 4, 1)), RowData)


class BuddyAction(DataRow):
    _sign = b'BuddyAction|eJwrLs4DAgAJQwKf'
    sheet_name = 'BuddyAction'
    _display = 'text_name'
    text_name: str_t = RowData(0)
    text_help: str_t = RowData(1)
    icon: 'Icon' = IconRow(2)
    status_icon: 'Icon' = IconRow(3)
    reward: int_t = RowData(4)
    ui_priority: int_t = RowData(5)


class BuddyEquip(DataRow):
    _sign = b'BuddyEquip|eJwrzivOAwEICQQAQpwHXg=='
    sheet_name = 'BuddyEquip'
    _display = 'text_ui_name'
    text_sgl: str_t = RowData(0)
    text_sgg: int_t = RowData(1)
    text_plr: str_t = RowData(2)
    text_plg: int_t = RowData(3)
    text_vow: int_t = RowData(4)
    text_cnt: int_t = RowData(5)
    text_gen: int_t = RowData(6)
    text_def_: int_t = RowData(7)
    text_ui_name: str_t = RowData(8)
    model: List[int_t] = ListData(ir((9, 3, 1)), RowData)
    grand_company: 'GrandCompany' = RowForeign(12, 'GrandCompany')
    icon: List[Icon] = ListData(ir((13, 3, 1)), IconRow)
    ui_priority: int_t = RowData(16)


class BuddyItem(DataRow):
    _sign = b'BuddyItem|eJzLS0tLywMABi8CDw=='
    sheet_name = 'BuddyItem'
    item: 'Item' = RowForeign(0, 'Item')
    use_training: bool_t = RowData(1)
    use_field: bool_t = RowData(2)
    use_snack: bool_t = RowData(3)
    status: int_t = RowData(4)


class BuddyRank(DataRow):
    _sign = b'BuddyRank|eJzLAwAAbwBv'
    sheet_name = 'BuddyRank'
    rank_up_exp: int_t = RowData(0)


class BuddySkill(DataRow):
    _sign = b'BuddySkill|eJzLS8vLywMABlcCHw=='
    sheet_name = 'BuddySkill'
    point: int_t = RowData(0)
    is_active: bool_t = RowData(1)
    line: List[int_t] = ListData(ir((2, 3, 1)), RowData)


class Cabinet(DataRow):
    _sign = b'Cabinet|eJzLy8sDAAKXAUs='
    sheet_name = 'Cabinet'
    _display = 'item'
    item: 'Item' = RowForeign(0, 'Item')
    priority: int_t = RowData(1)
    category: 'CabinetCategory' = RowForeign(2, 'CabinetCategory')


class CabinetCategory(DataRow):
    _sign = b'CabinetCategory|eJzLy8sDAAKXAUs='
    sheet_name = 'CabinetCategory'
    _display = 'text'
    ui_sort: int_t = RowData(0)
    icon: 'Icon' = IconRow(1)
    text: 'Addon' = RowForeign(2, 'Addon')


class Calendar(DataRow):
    _sign = b'Calendar|eJzLy6MMAAB+LRuB'
    sheet_name = 'Calendar'
    days_month: List[int_t] = ListData(ir((0, 32, 1)), RowData)
    days_day: List[int_t] = ListData(ir((32, 32, 1)), RowData)


class Carry(DataRow):
    _sign = b'Carry|eJzLy8vLAwAEUAG5'
    sheet_name = 'Carry'
    model: int_t = RowData(0)
    timeline: int_t = RowData(1)
    ex_hot_bar: int_t = RowData(2)
    motion: int_t = RowData(3)


class Channeling(DataRow):
    _sign = b'Channeling|eJwrzktLSwMABmACFA=='
    sheet_name = 'Channeling'
    file: str_t = RowData(0)
    limit_dist: int_t = RowData(1)
    control_chara_only: bool_t = RowData(2)
    vfx_high_priority: bool_t = RowData(3)
    clear_dead: bool_t = RowData(4)


class CharaCardBase(DataRow):
    _sign = b'CharaCardBase|eJzLy0tKysvLKwYADwEDXg=='
    sheet_name = 'CharaCardBase'
    _display = 'text'
    icon: 'Icon' = IconRow(0)
    text_color: int_t = RowData(1)
    layout: List[bool_t] = ListData(ir((2, 2, 1)), RowData)
    design_type: int_t = RowData(4)
    obtain_condition: 'BannerCondition' = RowForeign(5, 'BannerCondition')
    sort_id: int_t = RowData(6)
    text: str_t = RowData(7)


class CharaCardDecoration(DataRow):
    _sign = b'CharaCardDecoration|eJzLywOBYgAMFAMI'
    sheet_name = 'CharaCardDecoration'
    _display = 'text'
    type: int_t = RowData(0)
    sub_type: int_t = RowData(1)
    icon: 'Icon' = IconRow(2)
    design_type: int_t = RowData(3)
    obtain_condition: 'BannerCondition' = RowForeign(4, 'BannerCondition')
    sort_id: int_t = RowData(5)
    text: str_t = RowData(6)


class CharaCardDesignPreset(DataRow):
    _sign = b'CharaCardDesignPreset|eJzLy4OCYgAXsQRS'
    sheet_name = 'CharaCardDesignPreset'
    _display = 'text'
    base: 'CharaCardBase' = RowForeign(0, 'CharaCardBase')
    header: 'CharaCardHeader' = RowForeign(1, 'CharaCardHeader')
    footer: 'CharaCardHeader' = RowForeign(2, 'CharaCardHeader')
    decoration: 'List[CharaCardDecoration]' = ListData(ir((3, 5, 1)), RowForeign, 'CharaCardDecoration')
    sort_id: int_t = RowData(8)
    text: str_t = RowData(9)


class CharaCardDesignType(DataRow):
    _sign = b'CharaCardDesignType|eJxLSkpKgwAAFYgD8Q=='
    sheet_name = 'CharaCardDesignType'
    type: List[bool_t] = ListData(ir((0, 3, 1)), RowData)
    header: bool_t = RowData(3)
    footer: bool_t = RowData(4)
    bg: bool_t = RowData(5)
    base_pattern: bool_t = RowData(6)
    banner_frame: bool_t = RowData(7)
    frame: bool_t = RowData(8)
    sticker: bool_t = RowData(9)


class CharaCardHeader(DataRow):
    _sign = b'CharaCardHeader|eJzLy4OAYgATZAPk'
    sheet_name = 'CharaCardHeader'
    _display = 'text'
    header_icon: 'Icon' = IconRow(0)
    footer_icon: 'Icon' = IconRow(1)
    header_text_color: int_t = RowData(2)
    footer_text_color: int_t = RowData(3)
    move_collision_type: int_t = RowData(4)
    design_type: int_t = RowData(5)
    obtain_condition: int_t = RowData(6)
    sort_id: int_t = RowData(7)
    text: str_t = RowData(8)


class CharaCardPlayStyle(DataRow):
    _sign = b'CharaCardPlayStyle|eJzLyysGAAKcAVA='
    sheet_name = 'CharaCardPlayStyle'
    _display = 'text'
    icon: 'Icon' = IconRow(0)
    sort_id: int_t = RowData(1)
    text: str_t = RowData(2)


class CharaMakeClassEquip(DataRow):
    _sign = b'CharaMakeClassEquip|eJzLy4MAAA+AA3E='
    sheet_name = 'CharaMakeClassEquip'
    helmet: int_t = RowData(0)
    top: int_t = RowData(1)
    glove: int_t = RowData(2)
    down: int_t = RowData(3)
    shoes: int_t = RowData(4)
    weapon: int_t = RowData(5)
    sub_weapon: int_t = RowData(6)
    class_: 'ClassJob' = RowForeign(7, 'ClassJob')


class CharaMakeCustomize(DataRow):
    _sign = b'CharaMakeCustomize|eJzLy8tLy8vLAwAL7wL7'
    sheet_name = 'CharaMakeCustomize'
    _display = 'icon'
    graphic: int_t = RowData(0)
    icon: 'Icon' = IconRow(1)
    need_reward: int_t = RowData(2)
    hide: bool_t = RowData(3)
    lobby: 'Lobby' = RowForeign(4, 'Lobby')
    item: 'Item' = RowForeign(5, 'Item')
    face: int_t = RowData(6)


class CharaMakeName(DataRow):
    _sign = b'CharaMakeName|eJwrLiYJAAD69hUe'
    sheet_name = 'CharaMakeName'
    text_hu_m__m: str_t = RowData(0)
    text_hu_m__f: str_t = RowData(1)
    text_hu_m__l: str_t = RowData(2)
    text_hu_h__m: str_t = RowData(3)
    text_hu_h__f: str_t = RowData(4)
    text_hu_h__l: str_t = RowData(5)
    text_el__m: str_t = RowData(6)
    text_el__f: str_t = RowData(7)
    text_el_f__l: str_t = RowData(8)
    text_el_s__l: str_t = RowData(9)
    text_mq_s__m: str_t = RowData(10)
    text_mq_s__f: str_t = RowData(11)
    text_mq_s__ml: str_t = RowData(12)
    text_mq_s__fl: str_t = RowData(13)
    text_mq_m__m: str_t = RowData(14)
    text_mq_m__f: str_t = RowData(15)
    text_mq_m__l: str_t = RowData(16)
    text_la_p__mf: str_t = RowData(17)
    text_la_p__ml: str_t = RowData(18)
    text_la_p__mr: str_t = RowData(19)
    text_la_d__mn: str_t = RowData(20)
    text_la_d__mr: str_t = RowData(21)
    text_la_d__fn: str_t = RowData(22)
    text_la_d__fr: str_t = RowData(23)
    text_ro_z__mf: str_t = RowData(24)
    text_ro_z__ml: str_t = RowData(25)
    text_ro_z__ff: str_t = RowData(26)
    text_ro_z__fl: str_t = RowData(27)
    text_ro_r__f: str_t = RowData(28)
    text_ro_r__ml: str_t = RowData(29)
    text_ro_r__fl: str_t = RowData(30)
    text_au_r__mf: str_t = RowData(31)
    text_au_r__ff: str_t = RowData(32)
    text_au_r__l: str_t = RowData(33)
    text_au_x__mf: str_t = RowData(34)
    text_au_x__ff: str_t = RowData(35)
    text_au_x__l: str_t = RowData(36)
    text_hr_h__f: str_t = RowData(37)
    text_hr_h__l: str_t = RowData(38)
    text_hr_t__f: str_t = RowData(39)
    text_hr_t__l: str_t = RowData(40)
    text_vi__mf: str_t = RowData(41)
    text_vi_r__ml: str_t = RowData(42)
    text_vi_v__ml: str_t = RowData(43)
    text_vi__f: str_t = RowData(44)
    text_vi_r__l: str_t = RowData(45)
    text_vi_v__l: str_t = RowData(46)


class CharaMakeType(DataRow):
    _sign = b'CharaMakeType|eJztwSEBAAAAw6DG6y9vHwIoAAAA3gDWjKd8'
    sheet_name = 'CharaMakeType'
    race: 'Race' = RowForeign(0, 'Race')
    tribe: 'Tribe' = RowForeign(1, 'Tribe')
    gender: int_t = RowData(2)
    looks_menu: List[int_t] = ListData(ir((3, 28, 1)), RowData)
    looks_init_val: List[int_t] = ListData(ir((31, 28, 1)), RowData)
    looks_sub_menu_type: List[int_t] = ListData(ir((59, 28, 1)), RowData)
    looks_sub_menu_num: List[int_t] = ListData(ir((87, 28, 1)), RowData)
    looks_look_at: List[int_t] = ListData(ir((115, 28, 1)), RowData)
    looks_sub_menu_mask: List[int_t] = ListData(ir((143, 28, 1)), RowData)
    looks_customize: List[int_t] = ListData(ir((171, 28, 1)), RowData)
    looks_sub_menu_param: List[List[int_t]] = ListData(ir(((199, 100, 28), 28, 1)), ListData, RowData)
    looks_sub_menu_graphic: List[List[int_t]] = ListData(ir(((2999, 10, 28), 28, 1)), ListData, RowData)
    voice: List[int_t] = ListData(ir((3279, 12, 1)), RowData)
    face_option_option: List[List[int_t]] = ListData(ir(((3291, 7, 8), 8, 1)), ListData, RowData)
    equip_helmet: List[int_t] = ListData(ir((3347, 3, 1)), RowData)
    equip_top: List[int_t] = ListData(ir((3350, 3, 1)), RowData)
    equip_glove: List[int_t] = ListData(ir((3353, 3, 1)), RowData)
    equip_down: List[int_t] = ListData(ir((3356, 3, 1)), RowData)
    equip_shoes: List[int_t] = ListData(ir((3359, 3, 1)), RowData)
    equip_weapon: List[int_t] = ListData(ir((3362, 3, 1)), RowData)
    equip_sub_weapon: List[int_t] = ListData(ir((3365, 3, 1)), RowData)


class ChocoboRace(DataRow):
    _sign = b'ChocoboRace|eJzLywMAAUwA3Q=='
    sheet_name = 'ChocoboRace'
    rank: 'ChocoboRaceRank' = RowForeign(0, 'ChocoboRaceRank')
    territory: 'ChocoboRaceTerritory' = RowForeign(1, 'ChocoboRaceTerritory')


class ChocoboRaceAbility(DataRow):
    _sign = b'ChocoboRaceAbility|eJwrLs7LywMABqQCMQ=='
    sheet_name = 'ChocoboRaceAbility'
    _display = 'text_name'
    text_name: str_t = RowData(0)
    text_help: str_t = RowData(1)
    icon: 'Icon' = IconRow(2)
    type: 'ChocoboRaceAbilityType' = RowForeign(3, 'ChocoboRaceAbilityType')
    arg: int_t = RowData(4)


class ChocoboRaceAbilityType(DataRow):
    _sign = b'ChocoboRaceAbilityType|eJxLAwAAZwBn'
    sheet_name = 'ChocoboRaceAbilityType'
    _display = 'active'
    active: bool_t = RowData(0)


class ChocoboRaceCalculateParam(DataRow):
    _sign = b'ChocoboRaceCalculateParam|eJzLAwAAbwBv'
    sheet_name = 'ChocoboRaceCalculateParam'
    param: int_t = RowData(0)


class ChocoboRaceChallenge(DataRow):
    _sign = b'ChocoboRaceChallenge|eJwrzsvLAwAEZAG+'
    sheet_name = 'ChocoboRaceChallenge'
    text: str_t = RowData(0)
    race_id: int_t = RowData(1)
    reward_flag: int_t = RowData(2)
    min_rating: int_t = RowData(3)


class ChocoboRaceItem(DataRow):
    _sign = b'ChocoboRaceItem|eJwrLs4DAAKwAVU='
    sheet_name = 'ChocoboRaceItem'
    _display = 'text_name'
    text_name: str_t = RowData(0)
    text_help: str_t = RowData(1)
    icon: 'Icon' = IconRow(2)


class ChocoboRaceRank(DataRow):
    _sign = b'ChocoboRaceRank|eJzLywMCAAZ3Aic='
    sheet_name = 'ChocoboRaceRank'
    _display = 'text'
    rank_min: int_t = RowData(0)
    rank_max: int_t = RowData(1)
    text: 'GoldSaucerTextData' = RowForeign(2, 'GoldSaucerTextData')
    entry_fee: int_t = RowData(3)
    icon: 'Icon' = IconRow(4)


class ChocoboRaceRanking(DataRow):
    _sign = b'ChocoboRaceRanking|eJzLAwAAbwBv'
    sheet_name = 'ChocoboRaceRanking'
    goal_bgm: int_t = RowData(0)


class ChocoboRaceStatus(DataRow):
    _sign = b'ChocoboRaceStatus|eJzLywMAAUwA3Q=='
    sheet_name = 'ChocoboRaceStatus'
    _display = 'status'
    status: 'Status' = RowForeign(0, 'Status')
    loop_effect: int_t = RowData(1)


class ChocoboRaceTerritory(DataRow):
    _sign = b'ChocoboRaceTerritory|eJzLywMAAUwA3Q=='
    sheet_name = 'ChocoboRaceTerritory'
    _display = 'text'
    text: 'GoldSaucerTextData' = RowForeign(0, 'GoldSaucerTextData')
    icon: 'Icon' = IconRow(1)


class ChocoboRaceTutorial(DataRow):
    _sign = b'ChocoboRaceTutorial|eJzLy4MBABesBE0='
    sheet_name = 'ChocoboRaceTutorial'
    keyboard_npc_yell: List[int_t] = ListData(ir((0, 4, 1)), RowData)
    pad_npc_yell: List[int_t] = ListData(ir((4, 4, 1)), RowData)
    todo_message: int_t = RowData(8)
    todo_item: int_t = RowData(9)


class ChocoboRaceWeather(DataRow):
    _sign = b'ChocoboRaceWeather|eJzLywMAAUwA3Q=='
    sheet_name = 'ChocoboRaceWeather'
    weather: 'Weather' = RowForeign(0, 'Weather')
    type: 'Weather' = RowForeign(1, 'Weather')


class ChocoboTaxi(DataRow):
    _sign = b'ChocoboTaxi|eJzLy8vLSwMABm8CHw=='
    sheet_name = 'ChocoboTaxi'
    _display = 'terminus'
    terminus: 'ChocoboTaxiStand' = RowForeign(0, 'ChocoboTaxiStand')
    time_required: int_t = RowData(1)
    fare: int_t = RowData(2)
    speed: int_t = RowData(3)
    for_contents: bool_t = RowData(4)


class ChocoboTaxiStand(DataRow):
    _sign = b'ChocoboTaxiStand|eJzLy4OAYgATZAPk'
    sheet_name = 'ChocoboTaxiStand'
    _display = 'text'
    taxi: List[int_t] = ListData(ir((0, 8, 1)), RowData)
    text: str_t = RowData(8)


class CircleActivity(DataRow):
    _sign = b'CircleActivity|eJwrzssDAAKmAVA='
    sheet_name = 'CircleActivity'
    _display = 'text'
    text: str_t = RowData(0)
    icon: 'Icon' = IconRow(1)
    sort: int_t = RowData(2)


class ClassJob(DataRow):
    _sign = b'ClassJob|eJwrLi7OwwEwJdLSAOfsFDc='
    sheet_name = 'ClassJob'
    _display = 'text_name'
    text_name: str_t = RowData(0)
    text_abbreviation: str_t = RowData(1)
    text_name_female: str_t = RowData(2)
    kind: 'ClassJobCategory' = RowForeign(3, 'ClassJobCategory')
    work_index: int_t = RowData(4)
    battle_class_index: int_t = RowData(5)
    battle_class_with_job_index: int_t = RowData(6)
    job_index: int_t = RowData(7)
    non_combat_class_index: int_t = RowData(8)
    hp: int_t = RowData(9)
    mp: int_t = RowData(10)
    str: int_t = RowData(11)
    vit: int_t = RowData(12)
    dex: int_t = RowData(13)
    int: int_t = RowData(14)
    mnd: int_t = RowData(15)
    pie: int_t = RowData(16)
    element: List[int_t] = ListData(ir((17, 6, 1)), RowData)
    pvp_base_param_value: int_t = RowData(23)
    pvp_action_sort: int_t = RowData(24)
    pvp_initial_select_action_trait: int_t = RowData(25)
    main_class: 'ClassJob' = RowForeign(26, 'ClassJob')
    en_text: str_t = RowData(27)
    init_weapon: 'List[Item]' = ListData(ir((28, 2, 1)), RowForeign, 'Item')
    role: int_t = RowData(30)
    town: 'Town' = RowForeign(31, 'Town')
    monster_note: 'MonsterNote' = RowForeign(32, 'MonsterNote')
    party_buff: int_t = RowData(33)
    limit_break_action: 'List[Action]' = ListData(ir((34, 3, 1)), RowForeign, 'Action')
    ui_priority: int_t = RowData(37)
    job_stone: 'Item' = RowForeign(38, 'Item')
    job_acquire_quest: 'Quest' = RowForeign(39, 'Quest')
    relic_quest: 'Quest' = RowForeign(40, 'Quest')
    artifact_quest: 'Quest' = RowForeign(41, 'Quest')
    initial_level: int_t = RowData(42)
    recommend_equip_type: int_t = RowData(43)
    content_finder_matching_group: int_t = RowData(44)
    sp_job: bool_t = RowData(45)
    content_class_job_tutorial_flag: bool_t = RowData(46)


class ClassJobActionSort(DataRow):
    _sign = b'ClassJobActionSort|eJzLy8tLAwAESAGx'
    sheet_name = 'ClassJobActionSort'
    action: int_t = RowData(0)
    base_action: int_t = RowData(1)
    combo_id: int_t = RowData(2)
    kata_combo: bool_t = RowData(3)


class ClassJobCategory(DataRow):
    _sign = b'ClassJobCategory|eJwrTiIWAABcsRAm'
    sheet_name = 'ClassJobCategory'
    _display = 'text'
    text: str_t = RowData(0)
    class_job: List[bool_t] = ListData(ir((1, 41, 1)), RowData)


class ClassJobResident(DataRow):
    _sign = b'ClassJobResident|eJzLAwAAbwBv'
    sheet_name = 'ClassJobResident'
    action: int_t = RowData(0)


class CollectablesShop(DataRow):
    _sign = b'CollectablesShop|eJwrzkMGAC1yBgo='
    sheet_name = 'CollectablesShop'
    _display = 'text'
    text: str_t = RowData(0)
    disclosure_reward_or_quest: 'Quest' = RowForeign(1, 'Quest')
    type: int_t = RowData(2)
    item: List[int_t] = ListData(ir((3, 11, 1)), RowData)


class CollectablesShopItem(DataRow):
    _sign = b'CollectablesShopItem|eJzLy4MCABNfA98='
    sheet_name = 'CollectablesShopItem'
    _display = 'masterpiece_item'
    masterpiece_item: 'Item' = RowForeign(0, 'Item')
    item_group: 'CollectablesShopItemGroup' = RowForeign(1, 'CollectablesShopItemGroup')
    class_job_level: int_t = RowData(2)
    masterpiece_level: int_t = RowData(4)
    star_num: int_t = RowData(5)
    refine_step: int_t = RowData(6)
    refine_table: 'CollectablesShopRefine' = RowForeign(7, 'CollectablesShopRefine')
    reward_table: 'CollectablesShopRewardScrip' = RowForeign(8, 'CollectablesShopRewardScrip')


class CollectablesShopItem(DataRow):
    _sign = b'CollectablesShopItem|eJzLy4MAAA+AA3E='
    sheet_name = 'CollectablesShopItem'
    _display = 'masterpiece_item'
    masterpiece_item: 'Item' = RowForeign(0, 'Item')
    item_group: 'CollectablesShopItemGroup' = RowForeign(1, 'CollectablesShopItemGroup')
    class_job_level: int_t = RowData(2)
    masterpiece_level: int_t = RowData(3)
    star_num: int_t = RowData(4)
    refine_step: int_t = RowData(5)
    refine_table: 'CollectablesShopRefine' = RowForeign(6, 'CollectablesShopRefine')
    reward_table: 'CollectablesShopRewardScrip' = RowForeign(7, 'CollectablesShopRewardScrip')


class CollectablesShopItemGroup(DataRow):
    _sign = b'CollectablesShopItemGroup|eJwrBgAAdAB0'
    sheet_name = 'CollectablesShopItemGroup'
    _display = 'text'
    text: str_t = RowData(0)


class CollectablesShopRefine(DataRow):
    _sign = b'CollectablesShopRefine|eJzLy8sDAAKXAUs='
    sheet_name = 'CollectablesShopRefine'
    refine: List[int_t] = ListData(ir((0, 3, 1)), RowData)


class CollectablesShopRewardItem(DataRow):
    _sign = b'CollectablesShopRewardItem|eJzLS8sDAhABABdEBD0='
    sheet_name = 'CollectablesShopRewardItem'
    _display = 'item_a'
    item_a: 'Item' = RowForeign(0, 'Item')
    is_hq_a: bool_t = RowData(1)
    item_stack_a: List[int_t] = ListData(ir((2, 3, 1)), RowData)
    item_b: int_t = RowData(5)
    is_hq_b: bool_t = RowData(6)
    item_stack_b: List[int_t] = ListData(ir((7, 3, 1)), RowData)


class CollectablesShopRewardScrip(DataRow):
    _sign = b'CollectablesShopRewardScrip|eJzLywMDAAwPAwM='
    sheet_name = 'CollectablesShopRewardScrip'
    _display = 'currency'
    currency: int_t = RowData(0)
    currency_stack: List[int_t] = ListData(ir((1, 3, 1)), RowData)
    exp_rate: List[int_t] = ListData(ir((4, 3, 1)), RowData)


class CollisionIdPallet(DataRow):
    _sign = b'CollisionIdPallet|eJzLy8sDAAKXAUs='
    sheet_name = 'CollisionIdPallet'
    foot_vfx_run: int_t = RowData(0)
    foot_vfx_walk: int_t = RowData(1)
    shock_wave: int_t = RowData(2)


class ColorFilter(DataRow):
    _sign = b'ColorFilter|eJwrzsvLS8tDAAA6cAbe'
    sheet_name = 'ColorFilter'
    text: str_t = RowData(0)
    ui_sort_id: int_t = RowData(1)
    hue: float_t = RowData(2)
    saturation: float_t = RowData(3)
    photoshop_method: bool_t = RowData(4)
    brightness: float_t = RowData(5)
    contrast: float_t = RowData(6)
    monochrome: float_t = RowData(7)
    sepia: float_t = RowData(8)
    intensity: float_t = RowData(9)
    red: float_t = RowData(10)
    green: float_t = RowData(11)
    blue: float_t = RowData(12)
    negative: float_t = RowData(13)
    level_black: float_t = RowData(14)
    level_white: float_t = RowData(15)


class Colosseum(DataRow):
    _sign = b'Colosseum|eJzLSwMAAUQA1Q=='
    sheet_name = 'Colosseum'
    ex_rule: int_t = RowData(0)
    class_change: bool_t = RowData(1)


class ColosseumMatchRank(DataRow):
    _sign = b'ColosseumMatchRank|eJwrBgAAdAB0'
    sheet_name = 'ColosseumMatchRank'
    text: str_t = RowData(0)


class Companion(DataRow):
    _sign = b'Companion|eJwrzivOQwVpIAAkgSy4GAA8FRAf'
    sheet_name = 'Companion'
    _display = 'text_sgl'
    text_sgl: str_t = RowData(0)
    text_sgg: int_t = RowData(1)
    text_plr: str_t = RowData(2)
    text_plg: int_t = RowData(3)
    text_vow: int_t = RowData(4)
    text_cnt: int_t = RowData(5)
    text_gen: int_t = RowData(6)
    text_def_: int_t = RowData(7)
    model: 'ModelChara' = RowForeign(8, 'ModelChara')
    scale: int_t = RowData(9)
    inactive_idle: List[int_t] = ListData(ir((10, 2, 1)), RowData)
    inactive_battle: int_t = RowData(12)
    inactive_wandering: int_t = RowData(13)
    move_type: 'CompanionMove' = RowForeign(14, 'CompanionMove')
    special: int_t = RowData(15)
    wandering_wait: int_t = RowData(16)
    chat_group: int_t = RowData(17)
    creature: bool_t = RowData(18)
    doll: bool_t = RowData(19)
    stroke: bool_t = RowData(20)
    poke: bool_t = RowData(21)
    look_at: bool_t = RowData(22)
    enemy: int_t = RowData(23)
    battle: bool_t = RowData(24)
    roulette: bool_t = RowData(25)
    icon: 'Icon' = IconRow(26)
    priority: int_t = RowData(27)
    valid: bool_t = RowData(28)
    scale_lo_vm: int_t = RowData(29)
    cost: int_t = RowData(30)
    hp: int_t = RowData(31)
    special_skill: int_t = RowData(32)
    skill_angle: int_t = RowData(33)
    sp: int_t = RowData(34)
    skill_motion: int_t = RowData(35)
    skill_vfx: int_t = RowData(36)
    race: 'MinionRace' = RowForeign(37, 'MinionRace')


class CompanionMove(DataRow):
    _sign = b'CompanionMove|eJwrBgAAdAB0'
    sheet_name = 'CompanionMove'
    _display = 'text'
    text: str_t = RowData(0)


class CompanionTransient(DataRow):
    _sign = b'CompanionTransient|eJwrLgaCvLy8NBDIAwAtuAX2'
    sheet_name = 'CompanionTransient'
    text_help: str_t = RowData(0)
    text_expository: str_t = RowData(1)
    text_cry: str_t = RowData(2)
    text_skill_name: str_t = RowData(3)
    text_skill_help: str_t = RowData(4)
    attack: int_t = RowData(5)
    defense: int_t = RowData(6)
    speed: int_t = RowData(7)
    area_attack: bool_t = RowData(8)
    gate: bool_t = RowData(9)
    search: bool_t = RowData(10)
    shield: bool_t = RowData(11)
    stone: bool_t = RowData(12)
    skill_type: 'MinionSkillType' = RowForeign(13, 'MinionSkillType')


class CompanyAction(DataRow):
    _sign = b'CompanyAction|eJwrLs4DgjQADEgDBQ=='
    sheet_name = 'CompanyAction'
    _display = 'text_name'
    text_name: str_t = RowData(0)
    text_help: str_t = RowData(1)
    icon: 'Icon' = IconRow(2)
    need_rank: 'FCRank' = RowForeign(3, 'FCRank')
    price: int_t = RowData(4)
    ui_priority: int_t = RowData(5)
    buyable: bool_t = RowData(6)


class CompanyCraftDraft(DataRow):
    _sign = b'CompanyCraftDraft|eJwrzoMCABOMA+Q='
    sheet_name = 'CompanyCraftDraft'
    _display = 'text'
    text: str_t = RowData(0)
    category: 'CompanyCraftDraftCategory' = RowForeign(1, 'CompanyCraftDraftCategory')
    material_item: List[int_t] = ListData(ir((2, 3, 2)), RowData)
    material_item_num: List[int_t] = ListData(ir((3, 3, 2)), RowData)
    sort_id: int_t = RowData(8)


class CompanyCraftDraftCategory(DataRow):
    _sign = b'CompanyCraftDraftCategory|eJwrzoMDAByeBMA='
    sheet_name = 'CompanyCraftDraftCategory'
    _display = 'text'
    text: str_t = RowData(0)
    types: List[int_t] = ListData(ir((1, 10, 1)), RowData)


class CompanyCraftManufactoryState(DataRow):
    _sign = b'CompanyCraftManufactoryState|eJwrBgAAdAB0'
    sheet_name = 'CompanyCraftManufactoryState'
    _display = 'text'
    text: str_t = RowData(0)


class CompanyCraftPart(DataRow):
    _sign = b'CompanyCraftPart|eJzLywMBAAkMApU='
    sheet_name = 'CompanyCraftPart'
    pattern_id: int_t = RowData(0)
    type: 'CompanyCraftType' = RowForeign(1, 'CompanyCraftType')
    processes: List[int_t] = ListData(ir((2, 4, 1)), RowData)


class CompanyCraftProcess(DataRow):
    _sign = b'CompanyCraftProcess|eJzLyyMMAB5fD3k='
    sheet_name = 'CompanyCraftProcess'
    supply_item: List[int_t] = ListData(ir((0, 12, 3)), RowData)
    supply_unit: List[int_t] = ListData(ir((1, 12, 3)), RowData)
    number_of_supply: List[int_t] = ListData(ir((2, 12, 3)), RowData)


class CompanyCraftSequence(DataRow):
    _sign = b'CompanyCraftSequence|eJzLy0MGAC0sBgU='
    sheet_name = 'CompanyCraftSequence'
    _display = 'item'
    item: 'Item' = RowForeign(0, 'Item')
    category: int_t = RowData(1)
    draft_category: 'CompanyCraftDraftCategory' = RowForeign(2, 'CompanyCraftDraftCategory')
    type: 'CompanyCraftType' = RowForeign(3, 'CompanyCraftType')
    draft: 'CompanyCraftDraft' = RowForeign(4, 'CompanyCraftDraft')
    parts: List[int_t] = ListData(ir((5, 8, 1)), RowData)
    sort_id: int_t = RowData(13)


class CompanyCraftSupplyItem(DataRow):
    _sign = b'CompanyCraftSupplyItem|eJzLAwAAbwBv'
    sheet_name = 'CompanyCraftSupplyItem'
    _display = 'item'
    item: 'Item' = RowForeign(0, 'Item')


class CompanyCraftType(DataRow):
    _sign = b'CompanyCraftType|eJwrBgAAdAB0'
    sheet_name = 'CompanyCraftType'
    _display = 'text'
    text: str_t = RowData(0)


class CompanyLeve(DataRow):
    _sign = b'CompanyLeve|eJzLyxtqAAC/kkx9'
    sheet_name = 'CompanyLeve'
    route_point_time_route_point_time: List[int_t] = ListData(ir((0, 8, 1)), RowData)
    entry_base_id: List[int_t] = ListData(ir((8, 8, 1)), RowData)
    entry_level: List[int_t] = ListData(ir((16, 8, 1)), RowData)
    entry_name_id: List[int_t] = ListData(ir((24, 8, 1)), RowData)
    entry_drop_event_item_id: List[int_t] = ListData(ir((32, 8, 1)), RowData)
    entry_drop_event_item_max: List[int_t] = ListData(ir((40, 8, 1)), RowData)
    entry_drop_event_item_rate: List[int_t] = ListData(ir((48, 8, 1)), RowData)
    entry_param: List[List[int_t]] = ListData(ir(((56, 6, 8), 8, 1)), ListData, RowData)
    entry_num_of_appearance: List[List[int_t]] = ListData(ir(((104, 8, 8), 8, 1)), ListData, RowData)
    todo_todo_sequence: List[int_t] = ListData(ir((168, 8, 1)), RowData)
    rule: 'CompanyLeveRule' = RowForeign(176, 'CompanyLeveRule')
    variation: int_t = RowData(177)


class CompanyLeveRule(DataRow):
    _sign = b'CompanyLeveRule|eJwrzssDAAKmAVA='
    sheet_name = 'CompanyLeveRule'
    _display = 'script'
    script: str_t = RowData(0)
    objective: 'LeveString' = RowForeign(1, 'LeveString')
    help: 'LeveString' = RowForeign(2, 'LeveString')


class CompleteJournal(DataRow):
    _sign = b'CompleteJournal|eJzLywOC4jwcAADIaQzq'
    sheet_name = 'CompleteJournal'
    _display = 'text'
    id: int_t = RowData(0)
    level: int_t = RowData(1)
    level_offset: int_t = RowData(2)
    icon: 'Icon' = IconRow(3)
    separate: int_t = RowData(4)
    text: str_t = RowData(5)
    cut_scene: List[int_t] = ListData(ir((6, 24, 1)), RowData)


class CompleteJournalCategory(DataRow):
    _sign = b'CompleteJournalCategory|eJzLy8sDAAKXAUs='
    sheet_name = 'CompleteJournalCategory'
    begin: 'CompleteJournal' = RowForeign(0, 'CompleteJournal')
    end: 'CompleteJournal' = RowForeign(1, 'CompleteJournal')
    separate_type: int_t = RowData(2)


class Completion(DataRow):
    _sign = b'Completion|eJzLyysuLgYABpUCNg=='
    sheet_name = 'Completion'
    _display = 'text'
    group: int_t = RowData(0)
    key: int_t = RowData(1)
    lookup_table: str_t = RowData(2)
    text: str_t = RowData(3)
    group_title: str_t = RowData(4)


class Condition(DataRow):
    _sign = b'Condition|eJxLy8vLAwAEMAGx'
    sheet_name = 'Condition'
    sync: bool_t = RowData(0)
    permission: int_t = RowData(1)
    error_log: 'LogMessage' = RowForeign(2, 'LogMessage')
    priority: int_t = RowData(3)


class ConfigKey(DataRow):
    _sign = b'ConfigKey|eJwrzstLy8vLKwYAD4UDcw=='
    sheet_name = 'ConfigKey'
    label: str_t = RowData(0)
    param: int_t = RowData(1)
    platform: int_t = RowData(2)
    required: bool_t = RowData(3)
    category: int_t = RowData(4)
    sort: int_t = RowData(5)
    backlight_group: int_t = RowData(6)
    text: str_t = RowData(7)


class ContentAttributeRect(DataRow):
    _sign = b'ContentAttributeRect|eJzLyxtYAADcwzcB'
    sheet_name = 'ContentAttributeRect'
    param_type: List[int_t] = ListData(ir((0, 32, 1)), RowData)
    param_param: List[int_t] = ListData(ir((32, 32, 1)), RowData)
    param_layout_id: List[int_t] = ListData(ir((64, 32, 1)), RowData)
    param_kind: List[int_t] = ListData(ir((96, 32, 1)), RowData)


class ContentCloseCycle(DataRow):
    _sign = b'ContentCloseCycle|eJzLy8tLggMAJJMFHw=='
    sheet_name = 'ContentCloseCycle'
    base_time: int_t = RowData(0)
    check_time: int_t = RowData(1)
    open_flag_num: int_t = RowData(2)
    open_flag: List[bool_t] = ListData(ir((3, 10, 1)), RowData)


class ContentDirectorManagedSG(DataRow):
    _sign = b'ContentDirectorManagedSG|eJzLAwAAbwBv'
    sheet_name = 'ContentDirectorManagedSG'
    layout_id: int_t = RowData(0)


class ContentEffectiveTime(DataRow):
    _sign = b'ContentEffectiveTime|eJxLAwAAZwBn'
    sheet_name = 'ContentEffectiveTime'
    flag_0: bool_t = RowData(0)


class ContentEntry(DataRow):
    _sign = b'ContentEntry|eJwrBgAAdAB0'
    sheet_name = 'ContentEntry'
    text: str_t = RowData(0)


class ContentEventItem(DataRow):
    _sign = b'ContentEventItem|eJzLAwAAbwBv'
    sheet_name = 'ContentEventItem'
    event_item: int_t = RowData(0)


class ContentExAction(DataRow):
    _sign = b'ContentExAction|eJzLy8vLAwAEUAG5'
    sheet_name = 'ContentExAction'
    action_id: 'List[Action]' = ListData(ir((0, 2, 1)), RowForeign, 'Action')
    cost_count_max: List[int_t] = ListData(ir((2, 2, 1)), RowData)


class ContentFinderCondition(DataRow):
    _sign = b'ContentFinderCondition|eJwrzsvLS8tDBWlQkAcngKC4GC6dl0QsAAAwrCXg'
    sheet_name = 'ContentFinderCondition'
    _display = 'text_name'
    content_name: str_t = RowData(0)
    territory_type: 'TerritoryType' = RowForeign(1, 'TerritoryType')
    director_type: int_t = RowData(2)
    content_id: int_t = RowData(3)
    is_pvp: bool_t = RowData(4)
    ex_version: int_t = RowData(5)
    effective_time: int_t = RowData(6)
    close_cycle: int_t = RowData(7)
    accept_class_job_category: 'ClassJobCategory' = RowForeign(8, 'ClassJobCategory')
    member_type: 'ContentMemberType' = RowForeign(9, 'ContentMemberType')
    finder_party_condition: int_t = RowData(10)
    entry_party_member_num: int_t = RowData(11)
    open_type: int_t = RowData(12)
    open_param0: 'Quest' = RowForeign(13, 'Quest')
    ui_open_type: int_t = RowData(14)
    ui_open_param: int_t = RowData(15)
    level: int_t = RowData(16)
    level_max: int_t = RowData(17)
    item_level: int_t = RowData(18)
    item_level_max: int_t = RowData(19)
    force_sync: bool_t = RowData(20)
    small_party: bool_t = RowData(21)
    lift_restriction: bool_t = RowData(22)
    halfway: bool_t = RowData(23)
    enable_item_limit: bool_t = RowData(24)
    tourism: bool_t = RowData(25)
    rate_match: bool_t = RowData(26)
    rate_change: bool_t = RowData(27)
    loot_mode: int_t = RowData(28)
    accept_client_request: bool_t = RowData(29)
    entry_finder_ui: bool_t = RowData(30)
    entry_raid_finder_ui: bool_t = RowData(31)
    enable_finder_ui: bool_t = RowData(32)
    raid_finder_param_id: int_t = RowData(33)
    raid_finder_job_matching: bool_t = RowData(34)
    enable_party_member_entry: bool_t = RowData(35)
    enable_replay: bool_t = RowData(36)
    sorting_language: bool_t = RowData(37)
    only_home_world: bool_t = RowData(38)
    exclusive: bool_t = RowData(39)
    hide_notification: bool_t = RowData(40)
    text_name: str_t = RowData(41)
    text_short_name: str_t = RowData(42)
    ui_type: 'ContentType' = RowForeign(43, 'ContentType')
    ui_category: int_t = RowData(44)
    contact_list: int_t = RowData(45)
    sort_key: int_t = RowData(46)
    image: 'Icon' = IconRow(47)
    inlay: 'Icon' = IconRow(48)
    treasure_obtained_flag: int_t = RowData(49)
    dummy_expand_table: int_t = RowData(50)
    is_dkt: bool_t = RowData(51)
    penalty_type: int_t = RowData(52)
    random: List[bool_t] = ListData(ir((53, 41, 1)), RowData)


class ContentFinderConditionTransient(DataRow):
    _sign = b'ContentFinderConditionTransient|eJwrBgAAdAB0'
    sheet_name = 'ContentFinderConditionTransient'
    _display = 'text'
    text: str_t = RowData(0)


class ContentGauge(DataRow):
    _sign = b'ContentGauge|eJzLK85LK86DAAAhpwUr'
    sheet_name = 'ContentGauge'
    style: int_t = RowData(0)
    text: str_t = RowData(1)
    color_default: 'ContentGaugeColor' = RowForeign(2, 'ContentGaugeColor')
    type: bool_t = RowData(3)
    se: str_t = RowData(4)
    param: List[int_t] = ListData(ir((5, 2, 3)), RowData)
    op: List[int_t] = ListData(ir((6, 2, 3)), RowData)
    color: List[int_t] = ListData(ir((7, 2, 3)), RowData)
    time_limit: int_t = RowData(11)


class ContentGaugeColor(DataRow):
    _sign = b'ContentGaugeColor|eJzLy8sDAAKXAUs='
    sheet_name = 'ContentGaugeColor'
    gauge_color: int_t = RowData(0)
    text_color: List[int_t] = ListData(ir((1, 2, 1)), RowData)


class ContentMemberType(DataRow):
    _sign = b'ContentMemberType|eJxLy0tLy4ODNBAAAE+fB+s='
    sheet_name = 'ContentMemberType'
    alliance: bool_t = RowData(0)
    alliance_type: int_t = RowData(1)
    alliance_entry: bool_t = RowData(2)
    alliance_entry_only: bool_t = RowData(3)
    alliance_need_party_count: int_t = RowData(4)
    alliance_need_member_count: int_t = RowData(5)
    player_max: int_t = RowData(6)
    party_member_count: int_t = RowData(7)
    party_count: int_t = RowData(8)
    party_count_start: int_t = RowData(9)
    tank_count: int_t = RowData(10)
    healer_count: int_t = RowData(11)
    melee_count: int_t = RowData(12)
    ranged_count: int_t = RowData(13)
    differentiate_dps: bool_t = RowData(14)
    free_role: bool_t = RowData(15)
    instance_player_limit: bool_t = RowData(16)
    pvp_team_entry: bool_t = RowData(17)
    check_sp_job: bool_t = RowData(18)


class ContentNpcTalk(DataRow):
    _sign = b'ContentNpcTalk|eJzLy4MCABNfA98='
    sheet_name = 'ContentNpcTalk'
    type: int_t = RowData(0)
    talk: List[int_t] = ListData(ir((1, 8, 1)), RowData)


class ContentRandomSelect(DataRow):
    _sign = b'ContentRandomSelect|eJzLAwAAbwBv'
    sheet_name = 'ContentRandomSelect'
    _display = 'content_finder_condition'
    content_finder_condition: 'ContentFinderCondition' = RowForeign(0, 'ContentFinderCondition')


class ContentRewardCondition(DataRow):
    _sign = b'ContentRewardCondition|eJzLAwAAbwBv'
    sheet_name = 'ContentRewardCondition'
    condition_type: int_t = RowData(0)


class ContentRoulette(DataRow):
    _sign = b'ContentRoulette|eJwrLgaCvLy0tLy0PAwAFkoDAhATSAIAu7kTGA=='
    sheet_name = 'ContentRoulette'
    _display = 'text_name'
    text_name: str_t = RowData(0)
    text_short_name: str_t = RowData(1)
    text_uniq_name: str_t = RowData(2)
    text_description: str_t = RowData(3)
    text_contents: str_t = RowData(4)
    ex_version: int_t = RowData(5)
    effective_time: int_t = RowData(6)
    hide_notification: bool_t = RowData(7)
    enable_finder: bool_t = RowData(8)
    open_rule: 'ContentRouletteOpenRule' = RowForeign(9, 'ContentRouletteOpenRule')
    pvp: bool_t = RowData(10)
    level: int_t = RowData(11)
    level_max: int_t = RowData(12)
    item_level: int_t = RowData(13)
    item_level_max: int_t = RowData(14)
    image: 'Icon' = IconRow(15)
    role_bonus: 'ContentRouletteRoleBonus' = RowForeign(16, 'ContentRouletteRoleBonus')
    clear_reward_a: int_t = RowData(17)
    clear_reward_b: int_t = RowData(18)
    clear_reward_c: int_t = RowData(19)
    clear_reward_pvp_exp: int_t = RowData(20)
    clear_reward_wolf_mark: int_t = RowData(21)
    sortkey: int_t = RowData(23)
    accept_class_job_category: int_t = RowData(24)
    member_type: 'ContentMemberType' = RowForeign(25, 'ContentMemberType')
    finder_party_condition: int_t = RowData(26)
    entry_party_member_num: int_t = RowData(27)
    reward: int_t = RowData(28)
    accept_client_request: bool_t = RowData(29)
    ui_type: int_t = RowData(30)
    ui_category: int_t = RowData(31)
    timelimit: int_t = RowData(32)
    timelimit_max: int_t = RowData(33)
    enable_using_item: bool_t = RowData(34)
    halfway: bool_t = RowData(35)
    rate_match: bool_t = RowData(36)
    rate_change: bool_t = RowData(37)
    loot_mode: int_t = RowData(38)
    instance_content_reward: 'InstanceContent' = RowForeign(39, 'InstanceContent')
    net_cafe: bool_t = RowData(40)
    random_select: int_t = RowData(41)
    only_home_world: bool_t = RowData(42)
    is_dkt: bool_t = RowData(43)
    penalty_type: int_t = RowData(44)


class ContentRoulette(DataRow):
    _sign = b'ContentRoulette|eJwrLgaCvLy0tLy0PHQAFkkDAhATSAIAqGESqg=='
    sheet_name = 'ContentRoulette'
    _display = 'text_name'
    text_name: str_t = RowData(0)
    text_short_name: str_t = RowData(1)
    text_uniq_name: str_t = RowData(2)
    text_description: str_t = RowData(3)
    text_contents: str_t = RowData(4)
    ex_version: int_t = RowData(5)
    effective_time: int_t = RowData(6)
    hide_notification: bool_t = RowData(7)
    enable_finder: bool_t = RowData(8)
    open_rule: 'ContentRouletteOpenRule' = RowForeign(9, 'ContentRouletteOpenRule')
    pvp: bool_t = RowData(10)
    level: int_t = RowData(11)
    level_max: int_t = RowData(12)
    item_level: int_t = RowData(13)
    item_level_max: int_t = RowData(14)
    image: 'Icon' = IconRow(15)
    role_bonus: 'ContentRouletteRoleBonus' = RowForeign(16, 'ContentRouletteRoleBonus')
    clear_reward_a: int_t = RowData(17)
    clear_reward_b: int_t = RowData(18)
    clear_reward_c: int_t = RowData(19)
    clear_reward_pvp_exp: int_t = RowData(20)
    clear_reward_wolf_mark: int_t = RowData(21)
    sortkey: int_t = RowData(22)
    accept_class_job_category: int_t = RowData(23)
    member_type: 'ContentMemberType' = RowForeign(24, 'ContentMemberType')
    finder_party_condition: int_t = RowData(25)
    entry_party_member_num: int_t = RowData(26)
    reward: int_t = RowData(27)
    accept_client_request: bool_t = RowData(28)
    ui_type: int_t = RowData(29)
    ui_category: int_t = RowData(30)
    timelimit: int_t = RowData(31)
    timelimit_max: int_t = RowData(32)
    enable_using_item: bool_t = RowData(33)
    halfway: bool_t = RowData(34)
    rate_match: bool_t = RowData(35)
    rate_change: bool_t = RowData(36)
    loot_mode: int_t = RowData(37)
    instance_content_reward: 'InstanceContent' = RowForeign(38, 'InstanceContent')
    net_cafe: bool_t = RowData(39)
    random_select: int_t = RowData(40)
    only_home_world: bool_t = RowData(41)
    is_dkt: bool_t = RowData(42)
    penalty_type: int_t = RowData(43)


class ContentRouletteOpenRule(DataRow):
    _sign = b'ContentRouletteOpenRule|eJxLywMAATwA1Q=='
    sheet_name = 'ContentRouletteOpenRule'
    need_clear_all: bool_t = RowData(0)
    required_open_num: int_t = RowData(1)


class ContentRouletteRoleBonus(DataRow):
    _sign = b'ContentRouletteRoleBonus|eJzLy0MAACGQBSk='
    sheet_name = 'ContentRouletteRoleBonus'
    exp_rate: int_t = RowData(0)
    gil_rate: int_t = RowData(1)
    seals_rate: int_t = RowData(2)
    tomestone_a: int_t = RowData(3)
    tomestone_b: int_t = RowData(4)
    tomestone_c: int_t = RowData(5)
    item: 'List[Item]' = ListData(ir((6, 2, 3)), RowForeign, 'Item')
    item_count: List[int_t] = ListData(ir((7, 2, 3)), RowData)
    item_condition: List[int_t] = ListData(ir((8, 2, 3)), RowData)


class ContentTalk(DataRow):
    _sign = b'ContentTalk|eJzLKwYAAVEA4g=='
    sheet_name = 'ContentTalk'
    _display = 'text'
    param: 'ContentTalkParam' = RowForeign(0, 'ContentTalkParam')
    text: str_t = RowData(1)


class ContentTalkParam(DataRow):
    _sign = b'ContentTalkParam|eJxLywMBAAjcAo0='
    sheet_name = 'ContentTalkParam'
    look_at: bool_t = RowData(0)
    turn: int_t = RowData(1)
    gesture: 'ActionTimeline' = RowForeign(2, 'ActionTimeline')
    lip_sync: int_t = RowData(3)
    facial: int_t = RowData(4)
    shape: int_t = RowData(5)


class ContentTodo(DataRow):
    _sign = b'ContentTodo|eJzLy8vLSwMABm8CHw=='
    sheet_name = 'ContentTodo'
    type: int_t = RowData(0)
    text: int_t = RowData(1)
    param: int_t = RowData(2)
    progress: int_t = RowData(3)
    hide_flag: bool_t = RowData(4)


class ContentTourismConstruct(DataRow):
    _sign = b'ContentTourismConstruct|eJzLy0MGAC0sBgU='
    sheet_name = 'ContentTourismConstruct'
    type: int_t = RowData(0)
    param: List[int_t] = ListData(ir((1, 13, 1)), RowData)


class ContentType(DataRow):
    _sign = b'ContentType|eJwrzgMBAAkqApo='
    sheet_name = 'ContentType'
    _display = 'text'
    text: str_t = RowData(0)
    icon_large: 'Icon' = IconRow(1)
    icon_small: 'Icon' = IconRow(2)
    in_content_detail: int_t = RowData(3)
    priority: int_t = RowData(4)
    journal_separate: int_t = RowData(5)


class ContentUICategory(DataRow):
    _sign = b'ContentUICategory|eJwrBgAAdAB0'
    sheet_name = 'ContentUICategory'
    text: str_t = RowData(0)


class ContentsNote(DataRow):
    _sign = b'ContentsNote|eJzLy4OD4uI8AC1FBg8='
    sheet_name = 'ContentsNote'
    category: 'ContentsNoteCategory' = RowForeign(0, 'ContentsNoteCategory')
    icon: 'Icon' = IconRow(1)
    ui_priority: int_t = RowData(2)
    cond_arg: int_t = RowData(3)
    reward: List[int_t] = ListData(ir((4, 2, 2)), RowData)
    reward_arg: List[int_t] = ListData(ir((5, 2, 2)), RowData)
    open_level: int_t = RowData(8)
    open_how_to: 'HowTo' = RowForeign(9, 'HowTo')
    open_reward: int_t = RowData(10)
    text_name: str_t = RowData(11)
    text_help: str_t = RowData(12)
    exp_limit: int_t = RowData(13)


class ContentsNoteCategory(DataRow):
    _sign = b'ContentsNoteCategory|eJzLKwYAAVEA4g=='
    sheet_name = 'ContentsNoteCategory'
    ui_priority: int_t = RowData(0)
    text: str_t = RowData(1)


class ContentsNoteLevel(DataRow):
    _sign = b'ContentsNoteLevel|eJzLAwAAbwBv'
    sheet_name = 'ContentsNoteLevel'
    num_0: int_t = RowData(0)


class ContentsNoteRewardEurekaEXP(DataRow):
    _sign = b'ContentsNoteRewardEurekaEXP|eJzLAwAAbwBv'
    sheet_name = 'ContentsNoteRewardEurekaEXP'
    base_exp: int_t = RowData(0)


class ContentsTutorial(DataRow):
    _sign = b'ContentsTutorial|eJwrLs6DAgAYCwRX'
    sheet_name = 'ContentsTutorial'
    _display = 'title_title'
    title_title: str_t = RowData(0)
    title_sub_title: str_t = RowData(1)
    page: List[int_t] = ListData(ir((2, 8, 1)), RowData)


class ContentsTutorialPage(DataRow):
    _sign = b'ContentsTutorialPage|eJzLKwYAAVEA4g=='
    sheet_name = 'ContentsTutorialPage'
    icon: 'Icon' = IconRow(0)
    text: str_t = RowData(1)


class CraftAction(DataRow):
    _sign = b'CraftAction|eJwrLs6DgLQ8OAAAWrsImw=='
    sheet_name = 'CraftAction'
    _display = 'text_name'
    text_name: str_t = RowData(0)
    text_help: str_t = RowData(1)
    timeline: 'ActionTimeline' = RowForeign(2, 'ActionTimeline')
    sub_timeline: 'ActionTimeline' = RowForeign(3, 'ActionTimeline')
    icon: 'Icon' = IconRow(4)
    class_job: 'ClassJob' = RowForeign(5, 'ClassJob')
    use_class_job: 'ClassJobCategory' = RowForeign(6, 'ClassJobCategory')
    lv: int_t = RowData(7)
    reward: 'Quest' = RowForeign(8, 'Quest')
    meister: bool_t = RowData(9)
    cond_non_status: int_t = RowData(10)
    cost_cp: int_t = RowData(11)
    action: 'List[CraftAction]' = ListData(ir((12, 8, 1)), RowForeign, 'CraftAction')


class CraftLeve(DataRow):
    _sign = b'CraftLeve|eJzLy4MDABxnBLs='
    sheet_name = 'CraftLeve'
    _display = 'leve'
    leve: 'Leve' = RowForeign(0, 'Leve')
    talk: 'CraftLeveTalk' = RowForeign(1, 'CraftLeveTalk')
    additional_times: int_t = RowData(2)
    item: List[int_t] = ListData(ir((3, 4, 2)), RowData)
    item_num: List[int_t] = ListData(ir((4, 4, 2)), RowData)


class CraftLeveTalk(DataRow):
    _sign = b'CraftLeveTalk|eJxLSwOBPLygGAwAfTwR+w=='
    sheet_name = 'CraftLeveTalk'
    param_look_at: List[bool_t] = ListData(ir((0, 6, 1)), RowData)
    param_turn: List[int_t] = ListData(ir((6, 6, 1)), RowData)
    param_gesture: List[int_t] = ListData(ir((12, 6, 1)), RowData)
    param_lip_sync: List[int_t] = ListData(ir((18, 6, 1)), RowData)
    param_facial: List[int_t] = ListData(ir((24, 6, 1)), RowData)
    param_shape: List[int_t] = ListData(ir((30, 6, 1)), RowData)
    text: List[str_t] = ListData(ir((36, 6, 1)), RowData)


class CraftLevelDifference(DataRow):
    _sign = b'CraftLevelDifference|eJzLAwAAbwBv'
    sheet_name = 'CraftLevelDifference'
    level_difference: int_t = RowData(0)


class CraftType(DataRow):
    _sign = b'CraftType|eJzLyysGAAKcAVA='
    sheet_name = 'CraftType'
    _display = 'text'
    main_physical: int_t = RowData(0)
    sub_physical: int_t = RowData(1)
    text: str_t = RowData(2)


class Credit(DataRow):
    _sign = b'Credit|eJzLy4MDABxnBLs='
    sheet_name = 'Credit'
    type: int_t = RowData(0)
    cast: 'List[CreditCast]' = ListData(ir((1, 10, 1)), RowForeign, 'CreditCast')


class CreditBackImage(DataRow):
    _sign = b'CreditBackImage|eJzLy0tLS8vLAwALrwLr'
    sheet_name = 'CreditBackImage'
    start: int_t = RowData(0)
    end: int_t = RowData(1)
    transparent: bool_t = RowData(2)
    scale_on: bool_t = RowData(3)
    lang_layer: bool_t = RowData(4)
    image: 'Icon' = IconRow(5)
    effect: int_t = RowData(6)


class CreditCast(DataRow):
    _sign = b'CreditCast|eJwrBgAAdAB0'
    sheet_name = 'CreditCast'
    _display = 'text'
    text: str_t = RowData(0)


class CreditDataSet(DataRow):
    _sign = b'CreditDataSet|eJzLy8vLSwMABm8CHw=='
    sheet_name = 'CreditDataSet'
    credit_list: int_t = RowData(0)
    credit_list_ch: int_t = RowData(1)
    credit_list_ko: int_t = RowData(2)
    back_image: int_t = RowData(3)
    is_not_skip: bool_t = RowData(4)


class CreditFont(DataRow):
    _sign = b'CreditFont|eJzLy4MCABNfA98='
    sheet_name = 'CreditFont'
    font: int_t = RowData(0)
    size: int_t = RowData(1)
    color_r: int_t = RowData(2)
    color_g: int_t = RowData(3)
    color_b: int_t = RowData(4)
    edge_r: int_t = RowData(5)
    edge_g: int_t = RowData(6)
    edge_b: int_t = RowData(7)
    kerning: int_t = RowData(8)


class CreditList(DataRow):
    _sign = b'CreditList|eJzLywMBAAkMApU='
    sheet_name = 'CreditList'
    space: int_t = RowData(0)
    icon: 'Icon' = IconRow(1)
    font: 'CreditFont' = RowForeign(2, 'CreditFont')
    x: int_t = RowData(3)
    align: int_t = RowData(4)
    text: 'CreditListText' = RowForeign(5, 'CreditListText')


class CreditListText(DataRow):
    _sign = b'CreditListText|eJwrBgAAdAB0'
    sheet_name = 'CreditListText'
    _display = 'text'
    text: str_t = RowData(0)


class CreditVersion(DataRow):
    _sign = b'CreditVersion|eJzLAwAAbwBv'
    sheet_name = 'CreditVersion'
    play_credit: int_t = RowData(0)


class CurrencyScripConvert(DataRow):
    _sign = b'CurrencyScripConvert|eJxLy8vLAwAEMAGx'
    sheet_name = 'CurrencyScripConvert'
    visible: bool_t = RowData(0)
    from_currency: int_t = RowData(1)
    to_currency: int_t = RowData(2)
    rate: int_t = RowData(3)


class CustomTalk(DataRow):
    _sign = b'CustomTalk|eJzLyyvGD/LwgrTi4jQYAHEBcXUiQA=='
    sheet_name = 'CustomTalk'
    _display = 'script'
    announce_icon: 'Icon' = IconRow(0)
    map_icon: 'Icon' = IconRow(1)
    script: str_t = RowData(2)
    define_name: List[str_t] = ListData(ir((3, 30, 1)), RowData)
    define_value: List[int_t] = ListData(ir((33, 30, 1)), RowData)
    client_event: bool_t = RowData(63)
    text_name: str_t = RowData(64)
    text_tooltip: str_t = RowData(65)
    accept_callback: bool_t = RowData(66)
    condition_callback: bool_t = RowData(67)
    permission_callback: bool_t = RowData(68)
    targeting_possible_callback: bool_t = RowData(69)
    announce_callback: bool_t = RowData(70)
    listen_emote: bool_t = RowData(71)
    listen_enter_territory: bool_t = RowData(72)
    listen_housing: bool_t = RowData(73)
    listen_ui: bool_t = RowData(74)
    nest_handler: int_t = RowData(75)
    event_situation_icon: int_t = RowData(76)
    dynamic_icon: int_t = RowData(77)
    accept_world_travelling: bool_t = RowData(78)


class CustomTalkDefineClient(DataRow):
    _sign = b'CustomTalkDefineClient|eJwrzgMAAVYA4g=='
    sheet_name = 'CustomTalkDefineClient'
    name: str_t = RowData(0)
    value: int_t = RowData(1)


class CustomTalkNestHandlers(DataRow):
    _sign = b'CustomTalkNestHandlers|eJzLAwAAbwBv'
    sheet_name = 'CustomTalkNestHandlers'
    nest_handler: int_t = RowData(0)


class CustomTalkResident(DataRow):
    _sign = b'CustomTalkResident|eJzLAwAAbwBv'
    sheet_name = 'CustomTalkResident'
    client_derived_class: int_t = RowData(0)


class CutActionTimeline(DataRow):
    _sign = b'CutActionTimeline|eJwrzgMCAAaQAiw='
    sheet_name = 'CutActionTimeline'
    filename: str_t = RowData(0)
    load_type: int_t = RowData(1)
    motion_type: int_t = RowData(2)
    start_attach: int_t = RowData(3)
    weapon_timeline: int_t = RowData(4)


class CutSceneIncompQuest(DataRow):
    _sign = b'CutSceneIncompQuest|eJzLAwAAbwBv'
    sheet_name = 'CutSceneIncompQuest'
    _display = 'incomp_quest'
    incomp_quest: 'Quest' = RowForeign(0, 'Quest')


class CutScreenImage(DataRow):
    _sign = b'CutScreenImage|eJzLy8sDAAKXAUs='
    sheet_name = 'CutScreenImage'
    type: int_t = RowData(0)
    icon: int_t = RowData(1)
    jingle: int_t = RowData(2)


class Cutscene(DataRow):
    _sign = b'Cutscene|eJwrzstLywMBABNcA9w='
    sheet_name = 'Cutscene'
    _display = 'path'
    path: str_t = RowData(0)
    class_job: int_t = RowData(1)
    cutscene_type: int_t = RowData(2)
    sp_select: bool_t = RowData(3)
    branch_condition_quest: List[int_t] = ListData(ir((4, 4, 1)), RowData)
    incomp_quest: int_t = RowData(8)


class CutsceneActorSize(DataRow):
    _sign = b'CutsceneActorSize|eJzLywMBAAkMApU='
    sheet_name = 'CutsceneActorSize'
    race: int_t = RowData(0)
    tribe: int_t = RowData(1)
    customize_sex: int_t = RowData(2)
    pc_size: int_t = RowData(3)
    pc_size_extra: int_t = RowData(4)
    pc_size_sb: int_t = RowData(5)


class CutsceneEventMotion(DataRow):
    _sign = b'CutsceneEventMotion|eJzLy0MGAC0sBgU='
    sheet_name = 'CutsceneEventMotion'
    model_chara_type: int_t = RowData(0)
    skeleton_id: int_t = RowData(1)
    walk__loop__speed: float_t = RowData(2)
    run__loop__speed: float_t = RowData(3)
    slowwalk__loop__speed: float_t = RowData(4)
    slowrun__loop__speed: float_t = RowData(5)
    battlewalk__loop__speed: float_t = RowData(6)
    battlerun__loop__speed: float_t = RowData(7)
    dash__loop__speed: float_t = RowData(8)
    dash__loop2__speed: float_t = RowData(9)
    turn__cw90__frame: float_t = RowData(10)
    turn__ccw90__frame: float_t = RowData(11)
    turn__cw180__frame: float_t = RowData(12)
    turn__ccw180__frame: float_t = RowData(13)


class CutsceneMotion(DataRow):
    _sign = b'CutsceneMotion|eJzLy4MDABxnBLs='
    sheet_name = 'CutsceneMotion'
    walk__loop__speed: float_t = RowData(0)
    run__loop__speed: float_t = RowData(1)
    slowwalk__loop__speed: float_t = RowData(2)
    slowrun__loop__speed: float_t = RowData(3)
    battlewalk__loop__speed: float_t = RowData(4)
    battlerun__loop__speed: float_t = RowData(5)
    dash__loop__speed: float_t = RowData(6)
    turn__cw90__frame: int_t = RowData(7)
    turn__ccw90__frame: int_t = RowData(8)
    turn__cw180__frame: int_t = RowData(9)
    turn__ccw180__frame: int_t = RowData(10)


class CutsceneName(DataRow):
    _sign = b'CutsceneName|eJwrBgAAdAB0'
    sheet_name = 'CutsceneName'
    text: str_t = RowData(0)


class CutsceneWorkIndex(DataRow):
    _sign = b'CutsceneWorkIndex|eJzLAwAAbwBv'
    sheet_name = 'CutsceneWorkIndex'
    work_index: int_t = RowData(0)


class CycleTime(DataRow):
    _sign = b'CycleTime|eJzLywMAAUwA3Q=='
    sheet_name = 'CycleTime'
    first_cycle_offset: int_t = RowData(0)
    cycle: int_t = RowData(1)


class DailySupplyItem(DataRow):
    _sign = b'DailySupplyItem|eJzLy8MOAIEAClE='
    sheet_name = 'DailySupplyItem'
    item: List[int_t] = ListData(ir((0, 8, 3)), RowData)
    count: List[int_t] = ListData(ir((1, 8, 3)), RowData)
    level: List[int_t] = ListData(ir((2, 8, 3)), RowData)


class DawnContent(DataRow):
    _sign = b'DawnContent|eJzLS0tLy0MBAEgMB6U='
    sheet_name = 'DawnContent'
    _display = 'content'
    content: 'ContentFinderCondition' = RowForeign(0, 'ContentFinderCondition')
    under_construction: bool_t = RowData(1)
    grow_supported: bool_t = RowData(2)
    member_select: bool_t = RowData(3)
    exp: List[int_t] = ListData(ir((4, 2, 1)), RowData)
    enter_quest: int_t = RowData(6)
    enter_quest_sequence: int_t = RowData(7)
    announce_entrance_e_obj: List[int_t] = ListData(ir((8, 2, 1)), RowData)
    announce_e_npc: List[int_t] = ListData(ir((10, 8, 1)), RowData)


class DawnContentParticipable(DataRow):
    _sign = b'DawnContentParticipable|eJzLAwAAbwBv'
    sheet_name = 'DawnContentParticipable'
    quest_member: int_t = RowData(0)


class DawnGrowMember(DataRow):
    _sign = b'DawnGrowMember|eJzLywMDAAwPAwM='
    sheet_name = 'DawnGrowMember'
    icon: List[int_t] = ListData(ir((0, 3, 1)), RowData)
    icon_pt: List[int_t] = ListData(ir((3, 3, 1)), RowData)
    ui_param: 'DawnMemberUIParam' = RowForeign(6, 'DawnMemberUIParam')


class DawnMember(DataRow):
    _sign = b'DawnMember|eJzLywMAAUwA3Q=='
    sheet_name = 'DawnMember'
    class_job: int_t = RowData(0)
    fake_class_job: int_t = RowData(1)


class DawnMemberUIParam(DataRow):
    _sign = b'DawnMemberUIParam|eJwrLs4rBgAEeAHI'
    sheet_name = 'DawnMemberUIParam'
    _display = 'class_job_en_name'
    class_job_en_name: str_t = RowData(0)
    lang_param_name: str_t = RowData(1)
    lang_param_voice: int_t = RowData(2)
    lang_param_class_job_name: str_t = RowData(3)


class DawnQuestMember(DataRow):
    _sign = b'DawnQuestMember|eJzLywMBAAkMApU='
    sheet_name = 'DawnQuestMember'
    _display = 'e_npc_id'
    base: int_t = RowData(0)
    exclusive_group: int_t = RowData(1)
    e_npc_id: 'ENpcResident' = RowForeign(2, 'ENpcResident')
    icon: 'Icon' = IconRow(3)
    icon_pt: 'Icon' = IconRow(4)
    ui_param: 'DawnMemberUIParam' = RowForeign(5, 'DawnMemberUIParam')


class DeepDungeon(DataRow):
    _sign = b'DeepDungeon|eJzLy8MKivPSAJbzCyo='
    sheet_name = 'DeepDungeon'
    _display = 'text'
    weapon: 'DeepDungeonEquipment' = RowForeign(0, 'DeepDungeonEquipment')
    armor: 'DeepDungeonEquipment' = RowForeign(1, 'DeepDungeonEquipment')
    item: List[int_t] = ListData(ir((2, 16, 1)), RowData)
    magic_stone_type: int_t = RowData(18)
    magic_stone: List[int_t] = ListData(ir((19, 4, 1)), RowData)
    text: str_t = RowData(23)
    open_condition: 'ContentFinderCondition' = RowForeign(24, 'ContentFinderCondition')
    up_flag: bool_t = RowData(25)


class DeepDungeonBan(DataRow):
    _sign = b'DeepDungeonBan|eJzLy8sDAAKXAUs='
    sheet_name = 'DeepDungeonBan'
    _display = 'effect_ui'
    screen_image: 'ScreenImage' = RowForeign(0, 'ScreenImage')
    log_message: 'LogMessage' = RowForeign(1, 'LogMessage')
    effect_ui: 'DeepDungeonFloorEffectUI' = RowForeign(2, 'DeepDungeonFloorEffectUI')


class DeepDungeonDanger(DataRow):
    _sign = b'DeepDungeonDanger|eJzLy8sDAAKXAUs='
    sheet_name = 'DeepDungeonDanger'
    screen_image: 'ScreenImage' = RowForeign(0, 'ScreenImage')
    log_message: 'LogMessage' = RowForeign(1, 'LogMessage')
    effect_ui: 'DeepDungeonFloorEffectUI' = RowForeign(2, 'DeepDungeonFloorEffectUI')


class DeepDungeonDemiclone(DataRow):
    _sign = b'DeepDungeonDemiclone|eJzLK84rzgOB4mIAHNAEzw=='
    sheet_name = 'DeepDungeonDemiclone'
    icon: int_t = RowData(0)
    text_sgl: str_t = RowData(1)
    text_sgg: int_t = RowData(2)
    text_plr: str_t = RowData(3)
    text_plg: int_t = RowData(4)
    text_vow: int_t = RowData(5)
    text_cnt: int_t = RowData(6)
    text_gen: int_t = RowData(7)
    text_def_: int_t = RowData(8)
    text_name: str_t = RowData(9)
    text_help: str_t = RowData(10)


class DeepDungeonEquipment(DataRow):
    _sign = b'DeepDungeonEquipment|eJzLK84rzgOB4mIAHNAEzw=='
    sheet_name = 'DeepDungeonEquipment'
    _display = 'text_name'
    icon: 'Icon' = IconRow(0)
    text_sgl: str_t = RowData(1)
    text_sgg: int_t = RowData(2)
    text_plr: str_t = RowData(3)
    text_plg: int_t = RowData(4)
    text_vow: int_t = RowData(5)
    text_cnt: int_t = RowData(6)
    text_gen: int_t = RowData(7)
    text_def_: int_t = RowData(8)
    text_name: str_t = RowData(9)
    text_help: str_t = RowData(10)


class DeepDungeonFloorEffectUI(DataRow):
    _sign = b'DeepDungeonFloorEffectUI|eJzLKy4GAAKmAVU='
    sheet_name = 'DeepDungeonFloorEffectUI'
    _display = 'text_name'
    icon: 'Icon' = IconRow(0)
    text_name: str_t = RowData(1)
    text_help: str_t = RowData(2)


class DeepDungeonGrowData(DataRow):
    _sign = b'DeepDungeonGrowData|eJzLAwAAbwBv'
    sheet_name = 'DeepDungeonGrowData'
    limit_equip_level: int_t = RowData(0)


class DeepDungeonItem(DataRow):
    _sign = b'DeepDungeonItem|eJzLK84rzgOB4uI8ACINBT0='
    sheet_name = 'DeepDungeonItem'
    _display = 'text_name'
    icon: 'Icon' = IconRow(0)
    text_sgl: str_t = RowData(1)
    text_sgg: int_t = RowData(2)
    text_plr: str_t = RowData(3)
    text_plg: int_t = RowData(4)
    text_vow: int_t = RowData(5)
    text_cnt: int_t = RowData(6)
    text_gen: int_t = RowData(7)
    text_def_: int_t = RowData(8)
    text_name: str_t = RowData(9)
    text_help: str_t = RowData(10)
    action: 'Action' = RowForeign(11, 'Action')


class DeepDungeonLayer(DataRow):
    _sign = b'DeepDungeonLayer|eJzLywMDAAwPAwM='
    sheet_name = 'DeepDungeonLayer'
    deep_dungeon_id: 'DeepDungeon' = RowForeign(0, 'DeepDungeon')
    progress: int_t = RowData(1)
    map: 'List[DeepDungeonMap5X]' = ListData(ir((2, 2, 1)), RowForeign, 'DeepDungeonMap5X')
    large_room: 'DeepDungeonMap5X' = RowForeign(4, 'DeepDungeonMap5X')
    weapon: int_t = RowData(5)
    armor: int_t = RowData(6)


class DeepDungeonMagicStone(DataRow):
    _sign = b'DeepDungeonMagicStone|eJzLK84rzgOB4mIAHNAEzw=='
    sheet_name = 'DeepDungeonMagicStone'
    _display = 'text_name'
    icon: 'Icon' = IconRow(0)
    text_sgl: str_t = RowData(1)
    text_sgg: int_t = RowData(2)
    text_plr: str_t = RowData(3)
    text_plg: int_t = RowData(4)
    text_vow: int_t = RowData(5)
    text_cnt: int_t = RowData(6)
    text_gen: int_t = RowData(7)
    text_def_: int_t = RowData(8)
    text_name: str_t = RowData(9)
    text_help: str_t = RowData(10)


class DeepDungeonMap5X(DataRow):
    _sign = b'DeepDungeonMap5X|eJzLywMCAAZ3Aic='
    sheet_name = 'DeepDungeonMap5X'
    room: List[int_t] = ListData(ir((0, 5, 1)), RowData)


class DeepDungeonRoom(DataRow):
    _sign = b'DeepDungeonRoom|eJzLywMCAAZ3Aic='
    sheet_name = 'DeepDungeonRoom'
    shield_id: int_t = RowData(0)
    link: List[int_t] = ListData(ir((1, 4, 1)), RowData)


class DeepDungeonStatus(DataRow):
    _sign = b'DeepDungeonStatus|eJzLy8sDAAKXAUs='
    sheet_name = 'DeepDungeonStatus'
    screen_image: 'ScreenImage' = RowForeign(0, 'ScreenImage')
    log_message: 'LogMessage' = RowForeign(1, 'LogMessage')
    effect_ui: 'DeepDungeonFloorEffectUI' = RowForeign(2, 'DeepDungeonFloorEffectUI')


class DefaultTalk(DataRow):
    _sign = b'DefaultTalk|eJzLy0MDaWlpxcXFAHZVCdo='
    sheet_name = 'DefaultTalk'
    layout_id: int_t = RowData(0)
    camera_mode: int_t = RowData(1)
    param_turn: List[int_t] = ListData(ir((2, 3, 1)), RowData)
    param_gesture: List[int_t] = ListData(ir((5, 3, 1)), RowData)
    param_lip_sync: List[int_t] = ListData(ir((8, 3, 1)), RowData)
    param_facial: List[int_t] = ListData(ir((11, 3, 1)), RowData)
    param_shape: List[int_t] = ListData(ir((14, 3, 1)), RowData)
    param_is_auto_shake: List[bool_t] = ListData(ir((17, 3, 1)), RowData)
    text: List[str_t] = ListData(ir((20, 3, 1)), RowData)


class DefaultTalkLipSyncType(DataRow):
    _sign = b'DefaultTalkLipSyncType|eJzLAwAAbwBv'
    sheet_name = 'DefaultTalkLipSyncType'
    _display = 'action_time_line'
    action_time_line: 'ActionTimeline' = RowForeign(0, 'ActionTimeline')


class DeliveryQuest(DataRow):
    _sign = b'DeliveryQuest|eJzLAwAAbwBv'
    sheet_name = 'DeliveryQuest'
    _display = 'quest'
    quest: 'Quest' = RowForeign(0, 'Quest')


class Description(DataRow):
    _sign = b'Description|eJzLyysuLk7LAwAMOwMK'
    sheet_name = 'Description'
    _display = 'text_name'
    type: int_t = RowData(0)
    disclosure_reward_or_quest: 'Quest' = RowForeign(1, 'Quest')
    text_name: str_t = RowData(2)
    text_ui_name: str_t = RowData(3)
    text_ui_sub_name: str_t = RowData(4)
    system: bool_t = RowData(5)
    section: 'DescriptionSection' = RowForeign(6, 'DescriptionSection')


class DescriptionPage(DataRow):
    _sign = b'DescriptionPage|eJzLy8MFAJbsCy0='
    sheet_name = 'DescriptionPage'
    disclosure_type: int_t = RowData(0)
    disclosure_value0: 'Quest' = RowForeign(1, 'Quest')
    disclosure_value1: int_t = RowData(2)
    name_id: int_t = RowData(3)
    image: List[int_t] = ListData(ir((4, 11, 2)), RowData)
    text: List[int_t] = ListData(ir((5, 10, 2)), RowData)
    read_flag: int_t = RowData(25)


class DescriptionSection(DataRow):
    _sign = b'DescriptionSection|eJzLywMAAUwA3Q=='
    sheet_name = 'DescriptionSection'
    _display = 'name_id'
    name_id: 'DescriptionString' = RowForeign(0, 'DescriptionString')
    page_id: 'DescriptionPage' = RowForeign(1, 'DescriptionPage')


class DescriptionStandAlone(DataRow):
    _sign = b'DescriptionStandAlone|eJzLAwAAbwBv'
    sheet_name = 'DescriptionStandAlone'
    type: int_t = RowData(0)


class DescriptionStandAloneTransient(DataRow):
    _sign = b'DescriptionStandAloneTransient|eJzLKy4GAAKmAVU='
    sheet_name = 'DescriptionStandAloneTransient'
    section: int_t = RowData(0)
    text_ui_name: str_t = RowData(1)
    text_ui_sub_name: str_t = RowData(2)


class DescriptionString(DataRow):
    _sign = b'DescriptionString|eJwrBgAAdAB0'
    sheet_name = 'DescriptionString'
    _display = 'text'
    text: str_t = RowData(0)


class DirectorSystemDefine(DataRow):
    _sign = b'DirectorSystemDefine|eJwrzgMAAVYA4g=='
    sheet_name = 'DirectorSystemDefine'
    define_name: str_t = RowData(0)
    define_value: int_t = RowData(1)


class DirectorType(DataRow):
    _sign = b'DirectorType|eJxLS8tLyysGAAihAoI='
    sheet_name = 'DirectorType'
    solo: bool_t = RowData(0)
    attacked_content_only: bool_t = RowData(1)
    come_back_failed_message: int_t = RowData(2)
    home_point_override: bool_t = RowData(3)
    map_range_icon: int_t = RowData(4)
    debug_name: str_t = RowData(5)


class DisposalShop(DataRow):
    _sign = b'DisposalShop|eJwrzkMDaQBJ3ge6'
    sheet_name = 'DisposalShop'
    _display = 'text'
    text: str_t = RowData(0)
    filter_filter_type: List[int_t] = ListData(ir((1, 8, 1)), RowData)
    filter_param: List[int_t] = ListData(ir((9, 8, 1)), RowData)
    system: bool_t = RowData(17)


class DisposalShopFilterType(DataRow):
    _sign = b'DisposalShopFilterType|eJwrBgAAdAB0'
    sheet_name = 'DisposalShopFilterType'
    _display = 'text'
    text: str_t = RowData(0)


class DisposalShopItem(DataRow):
    _sign = b'DisposalShopItem|eJzLS8tLy8sDAAjMAoU='
    sheet_name = 'DisposalShopItem'
    _display = 'disposal_item_id'
    disposal_item_id: 'Item' = RowForeign(0, 'Item')
    disposal_item_is_hq: bool_t = RowData(1)
    exchange_item_id: 'Item' = RowForeign(2, 'Item')
    exchange_item_is_hq: bool_t = RowData(3)
    exchange_item_num: int_t = RowData(4)
    sort: int_t = RowData(5)


class DomaStoryProgress(DataRow):
    _sign = b'DomaStoryProgress|eJzLAwAAbwBv'
    sheet_name = 'DomaStoryProgress'
    next: int_t = RowData(0)


class DpsChallenge(DataRow):
    _sign = b'DpsChallenge|eJzLS8sDguJiAA9XA3M='
    sheet_name = 'DpsChallenge'
    _display = 'text_name'
    class_job_level: int_t = RowData(0)
    is_level_sync: bool_t = RowData(1)
    sync_item_level: int_t = RowData(2)
    location: 'PlaceName' = RowForeign(3, 'PlaceName')
    header: 'Icon' = IconRow(4)
    sort: int_t = RowData(5)
    text_name: str_t = RowData(6)
    text_description: str_t = RowData(7)


class DpsChallengeOfficer(DataRow):
    _sign = b'DpsChallengeOfficer|eJzLy8MFAJbsCy0='
    sheet_name = 'DpsChallengeOfficer'
    quest: 'Quest' = RowForeign(0, 'Quest')
    challenge_list_challenge: List[int_t] = ListData(ir((1, 25, 1)), RowData)


class DpsChallengeTransient(DataRow):
    _sign = b'DpsChallengeTransient|eJzLAwAAbwBv'
    sheet_name = 'DpsChallengeTransient'
    instance_content: 'InstanceContent' = RowForeign(0, 'InstanceContent')


class DynamicEvent(DataRow):
    _sign = b'DynamicEvent|eJzLy4OB4mIgAQAzzAZ9'
    sheet_name = 'DynamicEvent'
    _display = 'text_title'
    type: 'DynamicEventType' = RowForeign(0, 'DynamicEventType')
    enemy_type: 'DynamicEventEnemyType' = RowForeign(1, 'DynamicEventEnemyType')
    member_count: int_t = RowData(2)
    time: int_t = RowData(3)
    area_shared: int_t = RowData(4)
    warning_range: int_t = RowData(5)
    quest_id: 'Quest' = RowForeign(6, 'Quest')
    quest_sequence: int_t = RowData(7)
    single_battle: 'DynamicEventSingleBattle' = RowForeign(8, 'DynamicEventSingleBattle')
    generate_log: 'LogMessage' = RowForeign(9, 'LogMessage')
    text_title: str_t = RowData(10)
    text_description: str_t = RowData(11)
    marker_x: int_t = RowData(12)
    marker_y: int_t = RowData(13)
    marker_z: int_t = RowData(14)


class DynamicEventEnemyType(DataRow):
    _sign = b'DynamicEventEnemyType|eJwrBgAAdAB0'
    sheet_name = 'DynamicEventEnemyType'
    _display = 'text'
    text: str_t = RowData(0)


class DynamicEventManager(DataRow):
    _sign = b'DynamicEventManager|eJzLAwAAbwBv'
    sheet_name = 'DynamicEventManager'
    dynamic_event_set: int_t = RowData(0)


class DynamicEventSet(DataRow):
    _sign = b'DynamicEventSet|eJzLAwAAbwBv'
    sheet_name = 'DynamicEventSet'
    id: int_t = RowData(0)


class DynamicEventSingleBattle(DataRow):
    _sign = b'DynamicEventSingleBattle|eJzLyysGAAKcAVA='
    sheet_name = 'DynamicEventSingleBattle'
    name: 'BNpcName' = RowForeign(0, 'BNpcName')
    icon: 'Icon' = IconRow(1)
    text: str_t = RowData(2)


class DynamicEventType(DataRow):
    _sign = b'DynamicEventType|eJzLywMCAAZ3Aic='
    sheet_name = 'DynamicEventType'
    icon: 'Icon' = IconRow(0)
    map_icon: 'Icon' = IconRow(1)
    screen_image: List[int_t] = ListData(ir((2, 3, 1)), RowData)


class ENpcBase(DataRow):
    _sign = b'ENpcBase|eJzLS8ujBsBqClAQAKRgKLs='
    sheet_name = 'ENpcBase'
    idle_timeline: int_t = RowData(0)
    not_rewrite_height: bool_t = RowData(1)
    event_handler_event_handler: List[int_t] = ListData(ir((2, 32, 1)), RowData)
    scale: float_t = RowData(34)
    model: 'ModelChara' = RowForeign(35, 'ModelChara')
    customize: 'List[Tribe]' = ListData(ir((36, 26, 1)), RowForeign, 'Tribe')
    voice: int_t = RowData(62)
    equip_preset: 'NpcEquip' = RowForeign(63, 'NpcEquip')
    behavior: 'Behavior' = RowForeign(64, 'Behavior')
    weapon: int_t = RowData(65)
    weapon_stain: 'Stain' = RowForeign(66, 'Stain')
    sub_weapon: int_t = RowData(67)
    sub_weapon_stain: 'Stain' = RowForeign(68, 'Stain')
    equip: List[int_t] = ListData([69, 72, 74, 76, 78, 80, 82, 84, 86, 88], RowData)
    stain: 'List[Stain]' = ListData([70, 73, 75, 77, 79, 81, 83, 85, 87, 89], RowForeign, 'Stain')
    visor: bool_t = RowData(71)
    invisibility: int_t = RowData(90)
    default_balloon: 'Balloon' = RowForeign(91, 'Balloon')
    ignore_group_pose: bool_t = RowData(92)
    dress_up: int_t = RowData(93)
    bot_knowledge: int_t = RowData(94)


class ENpcDressUp(DataRow):
    _sign = b'ENpcDressUp|eJzLywMAAUwA3Q=='
    sheet_name = 'ENpcDressUp'
    dress_up_type: int_t = RowData(0)
    dress: 'ENpcDressUpDress' = RowForeign(1, 'ENpcDressUpDress')


class ENpcDressUpDress(DataRow):
    _sign = b'ENpcDressUpDress|eJzLSwOBPPIAACPkGg8='
    sheet_name = 'ENpcDressUpDress'
    threshold: int_t = RowData(0)
    change_invisibility: bool_t = RowData(1)
    change_customize: bool_t = RowData(2)
    change_equip_model: bool_t = RowData(3)
    change_chara_model: bool_t = RowData(4)
    reset_lively_hide: bool_t = RowData(5)
    invisibility: int_t = RowData(6)
    name: 'ENpcResident' = RowForeign(7, 'ENpcResident')
    model: int_t = RowData(8)
    idle_timeline: 'Behavior' = RowForeign(9, 'Behavior')
    behavior: int_t = RowData(10)
    customize: List[int_t] = ListData(ir((11, 26, 1)), RowData)
    weapon_model: int_t = RowData(37)
    weapon_stain: 'Stain' = RowForeign(38, 'Stain')
    sub_weapon_model: int_t = RowData(39)
    sub_weapon_stain: 'Stain' = RowForeign(40, 'Stain')
    equip: List[int_t] = ListData(ir((41, 10, 2)), RowData)
    stain: 'List[Stain]' = ListData(ir((42, 10, 2)), RowForeign, 'Stain')


class ENpcResident(DataRow):
    _sign = b'ENpcResident|eJwrzivOA4HivDQAHNIEwg=='
    sheet_name = 'ENpcResident'
    _display = 'text_sgl'
    text_sgl: str_t = RowData(0)
    text_sgg: int_t = RowData(1)
    text_plr: str_t = RowData(2)
    text_plg: int_t = RowData(3)
    text_vow: int_t = RowData(4)
    text_cnt: int_t = RowData(5)
    text_gen: int_t = RowData(6)
    text_def_: int_t = RowData(7)
    text_title: str_t = RowData(8)
    pop_type: int_t = RowData(9)
    important: bool_t = RowData(10)


class EObj(DataRow):
    _sign = b'EObj|eJxLSoKAPCBIS0vLA8I0AFNACAk='
    sheet_name = 'EObj'
    system_flag: List[bool_t] = ListData(ir((0, 8, 1)), RowData)
    pop_type: int_t = RowData(8)
    event_handler: int_t = RowData(9)
    invisibility: int_t = RowData(10)
    shared_group: 'ExportedSG' = RowForeign(11, 'ExportedSG')
    target: bool_t = RowData(12)
    director_control: bool_t = RowData(13)
    eye_collision: bool_t = RowData(14)
    event_high_addition: int_t = RowData(15)
    idle_camera_ignore: bool_t = RowData(16)
    bot_knowledge: int_t = RowData(17)
    quest_manual_shared_group_control: bool_t = RowData(18)
    newborn_shared_group_control: bool_t = RowData(19)


class EObjName(DataRow):
    _sign = b'EObjName|eJwrzivOAwEAD8YDew=='
    sheet_name = 'EObjName'
    _display = 'singular'
    singular: str_t = RowData(0)
    adjective: int_t = RowData(1)
    plural: str_t = RowData(2)
    possessive_pronoun: int_t = RowData(3)
    starts_with_vowel: int_t = RowData(4)
    field_5: int_t = RowData(5)
    pronoun: int_t = RowData(6)
    article: int_t = RowData(7)


class EmjAddon(DataRow):
    _sign = b'EmjAddon|eJwrBgAAdAB0'
    sheet_name = 'EmjAddon'
    _display = 'text'
    text: str_t = RowData(0)


class EmjCharaViewCamera(DataRow):
    _sign = b'EmjCharaViewCamera|eJzLywMBAAkMApU='
    sheet_name = 'EmjCharaViewCamera'
    x: float_t = RowData(0)
    y: float_t = RowData(1)
    scale: float_t = RowData(2)
    my_x: float_t = RowData(3)
    my_y: float_t = RowData(4)
    my_scale: float_t = RowData(5)


class EmjDani(DataRow):
    _sign = b'EmjDani|eJzLy8tLy4MCACFIBSE='
    sheet_name = 'EmjDani'
    icon: 'Icon' = IconRow(0)
    initial_dani_point: int_t = RowData(1)
    required_dani_point: int_t = RowData(2)
    has_demotion: bool_t = RowData(3)
    rank_point_normal1: int_t = RowData(4)
    rank_point_normal2: int_t = RowData(5)
    rank_point_normal3: int_t = RowData(6)
    rank_point_normal4: int_t = RowData(7)
    rank_point_hard1: int_t = RowData(8)
    rank_point_hard2: int_t = RowData(9)
    rank_point_hard3: int_t = RowData(10)
    rank_point_hard4: int_t = RowData(11)


class Emote(DataRow):
    _sign = b'Emote|eJwrzoOAtLQ0MAGiwAAAiSwKhA=='
    sheet_name = 'Emote'
    _display = 'text'
    text: str_t = RowData(0)
    timeline_id: int_t = RowData(1)
    timeline_id__begin: int_t = RowData(2)
    timeline_id__ground_sitting: int_t = RowData(3)
    timeline_id__chair_sitting: int_t = RowData(4)
    timeline_id__mounting: int_t = RowData(5)
    timeline_id__lying: int_t = RowData(6)
    timeline_id__adjust: int_t = RowData(7)
    enable_on_mount: bool_t = RowData(8)
    enable_on_swimming: bool_t = RowData(9)
    enable_on_diving: bool_t = RowData(10)
    category: 'EmoteCategory' = RowForeign(11, 'EmoteCategory')
    mode: 'EmoteMode' = RowForeign(12, 'EmoteMode')
    is_end_emote_mode: bool_t = RowData(13)
    is_rotate: bool_t = RowData(14)
    is_available_when_fishing: bool_t = RowData(15)
    is_drawn_sword: bool_t = RowData(16)
    is_drawn_sword_off: bool_t = RowData(17)
    ui__priority: int_t = RowData(18)
    text_command: 'TextCommand' = RowForeign(19, 'TextCommand')
    icon: 'Icon' = IconRow(20)
    log: 'LogMessage' = RowForeign(21, 'LogMessage')
    log_self: 'LogMessage' = RowForeign(22, 'LogMessage')
    reward: int_t = RowData(23)
    version: int_t = RowData(24)


class EmoteCategory(DataRow):
    _sign = b'EmoteCategory|eJwrBgAAdAB0'
    sheet_name = 'EmoteCategory'
    _display = 'name'
    name: str_t = RowData(0)


class EmoteMode(DataRow):
    _sign = b'EmoteMode|eJzLy0sDgrw0AA7oA0k='
    sheet_name = 'EmoteMode'
    start_emote: 'Emote' = RowForeign(0, 'Emote')
    end_emote: 'Emote' = RowForeign(1, 'Emote')
    end_on_emote: bool_t = RowData(2)
    end_on_rotate: bool_t = RowData(3)
    camera: bool_t = RowData(4)
    move: bool_t = RowData(5)
    condition_mode: int_t = RowData(6)
    group_pose_repeat: bool_t = RowData(7)


class EmoteTransient(DataRow):
    _sign = b'EmoteTransient|eJwrBgAAdAB0'
    sheet_name = 'EmoteTransient'
    text: str_t = RowData(0)


class EquipRaceCategory(DataRow):
    _sign = b'EquipRaceCategory|eJxLSoKAtDQAFSQD3Q=='
    sheet_name = 'EquipRaceCategory'
    condition_race: List[bool_t] = ListData(ir((0, 8, 1)), RowData)
    condition_male: bool_t = RowData(8)
    condition_female: bool_t = RowData(9)


class EquipSlotCategory(DataRow):
    _sign = b'EquipSlotCategory|eJzLy0MGAC0sBgU='
    sheet_name = 'EquipSlotCategory'
    permit: List[int_t] = ListData(ir((0, 14, 1)), RowData)


class Error(DataRow):
    _sign = b'Error|eJwrBgAAdAB0'
    sheet_name = 'Error'
    text_0: str_t = RowData(0)


class Eureka(DataRow):
    _sign = b'Eureka|eJzLy8vLSwMABm8CHw=='
    sheet_name = 'Eureka'
    level_max: int_t = RowData(0)
    aether_item: int_t = RowData(1)
    grow_buff: int_t = RowData(2)
    strengthen_buff: int_t = RowData(3)
    magicite_item: bool_t = RowData(4)


class EurekaAetherItem(DataRow):
    _sign = b'EurekaAetherItem|eJwrzivOA4FiABO0A+4='
    sheet_name = 'EurekaAetherItem'
    _display = 'singular'
    singular: str_t = RowData(0)
    adjective: int_t = RowData(1)
    plural: str_t = RowData(2)
    possessive_pronoun: int_t = RowData(3)
    starts_with_vowel: int_t = RowData(4)
    field_5: int_t = RowData(5)
    pronoun: int_t = RowData(6)
    article: int_t = RowData(7)
    name: str_t = RowData(8)


class EurekaAethernet(DataRow):
    _sign = b'EurekaAethernet|eJzLAwAAbwBv'
    sheet_name = 'EurekaAethernet'
    _display = 'location'
    location: 'PlaceName' = RowForeign(0, 'PlaceName')


class EurekaDungeonPortal(DataRow):
    _sign = b'EurekaDungeonPortal|eJzLAwAAbwBv'
    sheet_name = 'EurekaDungeonPortal'
    pop_range: int_t = RowData(0)


class EurekaGrowData(DataRow):
    _sign = b'EurekaGrowData|eJzLAwAAbwBv'
    sheet_name = 'EurekaGrowData'
    element_val_pc: int_t = RowData(0)


class EurekaLogosMixerProbability(DataRow):
    _sign = b'EurekaLogosMixerProbability|eJzLAwAAbwBv'
    sheet_name = 'EurekaLogosMixerProbability'
    probability: int_t = RowData(0)


class EurekaMagiaAction(DataRow):
    _sign = b'EurekaMagiaAction|eJzLywMAAUwA3Q=='
    sheet_name = 'EurekaMagiaAction'
    action: 'Action' = RowForeign(0, 'Action')
    count: int_t = RowData(1)


class EurekaMagiciteItem(DataRow):
    _sign = b'EurekaMagiciteItem|eJzLy8sDAAKXAUs='
    sheet_name = 'EurekaMagiciteItem'
    type: 'EurekaMagiciteItemType' = RowForeign(0, 'EurekaMagiciteItemType')
    class_job: 'ClassJobCategory' = RowForeign(1, 'ClassJobCategory')
    item: 'Item' = RowForeign(2, 'Item')


class EurekaMagiciteItemType(DataRow):
    _sign = b'EurekaMagiciteItemType|eJwrBgAAdAB0'
    sheet_name = 'EurekaMagiciteItemType'
    _display = 'text'
    text: str_t = RowData(0)


class EurekaSphereElementAdjust(DataRow):
    _sign = b'EurekaSphereElementAdjust|eJzLAwAAbwBv'
    sheet_name = 'EurekaSphereElementAdjust'
    _display = 'element_adjust'
    element_adjust: int_t = RowData(0)


class EurekaStoryProgress(DataRow):
    _sign = b'EurekaStoryProgress|eJzLAwAAbwBv'
    sheet_name = 'EurekaStoryProgress'
    next: int_t = RowData(0)


class EventAction(DataRow):
    _sign = b'EventAction|eJwrzgMBAAkqApo='
    sheet_name = 'EventAction'
    _display = 'text'
    text: str_t = RowData(0)
    icon: 'Icon' = IconRow(1)
    time: int_t = RowData(2)
    action_timeline__start: int_t = RowData(3)
    action_timeline__loop: int_t = RowData(4)
    action_timeline__end: int_t = RowData(5)


class EventCustomIconType(DataRow):
    _sign = b'EventCustomIconType|eJzLyyMZAAA6FRXr'
    sheet_name = 'EventCustomIconType'
    detail_announce: List[int_t] = ListData(ir((0, 10, 1)), RowData)
    detail_announce_lock: List[int_t] = ListData(ir((10, 10, 1)), RowData)
    detail_map: List[int_t] = ListData(ir((20, 10, 1)), RowData)
    detail_map_lock: List[int_t] = ListData(ir((30, 10, 1)), RowData)
    detail_todo: List[int_t] = ListData(ir((40, 10, 1)), RowData)
    num: int_t = RowData(50)


class EventIconPriority(DataRow):
    _sign = b'EventIconPriority|eJzLy8MAAFG3CCs='
    sheet_name = 'EventIconPriority'
    icon: List[int_t] = ListData(ir((0, 19, 1)), RowData)


class EventIconPriority(DataRow):
    _sign = b'EventIconPriority|eJzLy8MDALsHDHc='
    sheet_name = 'EventIconPriority'
    icon: List[int_t] = ListData(ir((0, 29, 1)), RowData)


class EventIconPriorityPair(DataRow):
    _sign = b'EventIconPriorityPair|eJzLAwAAbwBv'
    sheet_name = 'EventIconPriorityPair'
    map_icon: int_t = RowData(0)


class EventIconType(DataRow):
    _sign = b'EventIconType|eJzLywMCAAZ3Aic='
    sheet_name = 'EventIconType'
    announce: 'Icon' = IconRow(0)
    map: 'Icon' = IconRow(1)
    announce_lock: 'Icon' = IconRow(2)
    map_lock: 'Icon' = IconRow(3)
    num: int_t = RowData(4)


class EventItem(DataRow):
    _sign = b'EventItem|eJwrzivOA4E0CAUEAEoTB8Q='
    sheet_name = 'EventItem'
    _display = 'text_sgl'
    text_sgl: str_t = RowData(0)
    text_sgg: int_t = RowData(1)
    text_plr: str_t = RowData(2)
    text_plg: int_t = RowData(3)
    text_vow: int_t = RowData(4)
    text_cnt: int_t = RowData(5)
    text_gen: int_t = RowData(6)
    text_def_: int_t = RowData(7)
    text_help_dummy: bool_t = RowData(8)
    text_ui_name: str_t = RowData(9)
    icon: 'Icon' = IconRow(10)
    action: 'Action' = RowForeign(11, 'Action')
    stack_max: int_t = RowData(12)
    category: int_t = RowData(13)
    event_handler: 'Quest' = RowForeign(14, 'Quest')
    cast_time: int_t = RowData(15)
    cast_timeline: 'EventItemCastTimeline' = RowForeign(16, 'EventItemCastTimeline')
    timeline: int_t = RowData(17)


class EventItemCastTimeline(DataRow):
    _sign = b'EventItemCastTimeline|eJzLAwAAbwBv'
    sheet_name = 'EventItemCastTimeline'
    _display = 'timeline'
    timeline: 'ActionTimeline' = RowForeign(0, 'ActionTimeline')


class EventItemCategory(DataRow):
    _sign = b'EventItemCategory|eJwrzssDAAKmAVA='
    sheet_name = 'EventItemCategory'
    text: str_t = RowData(0)
    get_log_message: int_t = RowData(1)
    discard_log_message: int_t = RowData(2)


class EventItemHelp(DataRow):
    _sign = b'EventItemHelp|eJwrTgMAAU4A2g=='
    sheet_name = 'EventItemHelp'
    _display = 'text'
    text: str_t = RowData(0)
    system_flag: bool_t = RowData(1)


class EventItemTimeline(DataRow):
    _sign = b'EventItemTimeline|eJzLAwAAbwBv'
    sheet_name = 'EventItemTimeline'
    _display = 'timeline'
    timeline: 'ActionTimeline' = RowForeign(0, 'ActionTimeline')


class EventPathMove(DataRow):
    _sign = b'EventPathMove|eJzLy0vLg4DiYgAhTwUr'
    sheet_name = 'EventPathMove'
    quest: int_t = RowData(0)
    mount: int_t = RowData(1)
    is_fly: bool_t = RowData(2)
    motion_type: int_t = RowData(3)
    speed: int_t = RowData(4)
    path: List[int_t] = ListData(ir((5, 2, 1)), RowData)
    path_fade: int_t = RowData(7)
    invisible: List[int_t] = ListData(ir((8, 2, 1)), RowData)
    text_announce: str_t = RowData(10)
    text_selection_title: str_t = RowData(11)


class EventSituationIconTooltip(DataRow):
    _sign = b'EventSituationIconTooltip|eJwrTgMAAU4A2g=='
    sheet_name = 'EventSituationIconTooltip'
    text: str_t = RowData(0)
    system: bool_t = RowData(1)


class EventSystemDefine(DataRow):
    _sign = b'EventSystemDefine|eJwrzgMAAVYA4g=='
    sheet_name = 'EventSystemDefine'
    _display = 'define_name'
    define_name: str_t = RowData(0)
    define_value: int_t = RowData(1)


class EventVfx(DataRow):
    _sign = b'EventVfx|eJwrzivOy8sDAAk+Ap8='
    sheet_name = 'EventVfx'
    text: str_t = RowData(0)
    directory: int_t = RowData(1)
    file_name: str_t = RowData(2)
    ui_sort_id: int_t = RowData(3)
    ui_attribute: int_t = RowData(4)
    attribute: int_t = RowData(5)


class ExHotbarCrossbarIndexType(DataRow):
    _sign = b'ExHotbarCrossbarIndexType|eJzLy0MFADqABuE='
    sheet_name = 'ExHotbarCrossbarIndexType'
    index: List[int_t] = ListData(ir((0, 16, 1)), RowData)


class ExVersion(DataRow):
    _sign = b'ExVersion|eJwrzssDAAKmAVA='
    sheet_name = 'ExVersion'
    _display = 'text'
    text: str_t = RowData(0)
    quest_accept_screen_image: 'ScreenImage' = RowForeign(1, 'ScreenImage')
    quest_complete_screen_image: 'ScreenImage' = RowForeign(2, 'ScreenImage')


class ExportedGatheringPoint(DataRow):
    _sign = b'ExportedGatheringPoint|eJzLywMCAAZ3Aic='
    sheet_name = 'ExportedGatheringPoint'
    center_x: float_t = RowData(0)
    center_z: float_t = RowData(1)
    gathering_type: 'GatheringType' = RowForeign(2, 'GatheringType')
    gathering_point_type: int_t = RowData(3)
    radius: int_t = RowData(4)


class ExportedSG(DataRow):
    _sign = b'ExportedSG|eJwrBgAAdAB0'
    sheet_name = 'ExportedSG'
    _display = 'sg_file_path'
    sg_file_path: str_t = RowData(0)


class ExtraCommand(DataRow):
    _sign = b'ExtraCommand|eJwrLs7LAwAEcwHD'
    sheet_name = 'ExtraCommand'
    text_name: str_t = RowData(0)
    text_help: str_t = RowData(1)
    icon: int_t = RowData(2)
    sort_id: int_t = RowData(3)


class FCActivity(DataRow):
    _sign = b'FCActivity|eJwrzgMBAAkqApo='
    sheet_name = 'FCActivity'
    _display = 'text'
    text: str_t = RowData(0)
    self_kind: int_t = RowData(1)
    target_kind: int_t = RowData(2)
    num_param: int_t = RowData(3)
    category: 'FCActivityCategory' = RowForeign(4, 'FCActivityCategory')
    icon_type: int_t = RowData(5)


class FCActivityCategory(DataRow):
    _sign = b'FCActivityCategory|eJzLKwYAAVEA4g=='
    sheet_name = 'FCActivityCategory'
    _display = 'text'
    priority: int_t = RowData(0)
    text: str_t = RowData(1)


class FCAuthority(DataRow):
    _sign = b'FCAuthority|eJwrzssDAAKmAVA='
    sheet_name = 'FCAuthority'
    _display = 'text'
    text: str_t = RowData(0)
    category: 'FCAuthorityCategory' = RowForeign(1, 'FCAuthorityCategory')
    sort: int_t = RowData(2)


class FCAuthorityCategory(DataRow):
    _sign = b'FCAuthorityCategory|eJwrBgAAdAB0'
    sheet_name = 'FCAuthorityCategory'
    _display = 'text'
    text: str_t = RowData(0)


class FCChestName(DataRow):
    _sign = b'FCChestName|eJwrzgMAAVYA4g=='
    sheet_name = 'FCChestName'
    _display = 'name'
    name: str_t = RowData(0)
    field_1: int_t = RowData(1)


class FCCrestSymbol(DataRow):
    _sign = b'FCCrestSymbol|eJzLy8sDAAKXAUs='
    sheet_name = 'FCCrestSymbol'
    color_num: int_t = RowData(0)
    fc_right: int_t = RowData(1)
    sort_id: int_t = RowData(2)


class FCDefine(DataRow):
    _sign = b'FCDefine|eJzLAwAAbwBv'
    sheet_name = 'FCDefine'
    value: int_t = RowData(0)


class FCHierarchy(DataRow):
    _sign = b'FCHierarchy|eJwrBgAAdAB0'
    sheet_name = 'FCHierarchy'
    _display = 'text'
    text: str_t = RowData(0)


class FCProfile(DataRow):
    _sign = b'FCProfile|eJzLKwYAAVEA4g=='
    sheet_name = 'FCProfile'
    _display = 'text'
    priority: int_t = RowData(0)
    text: str_t = RowData(1)


class FCRank(DataRow):
    _sign = b'FCRank|eJzLy4MAAA+AA3E='
    sheet_name = 'FCRank'
    next_point: int_t = RowData(0)
    current_point: int_t = RowData(1)
    rights: List[int_t] = ListData(ir((2, 3, 1)), RowData)
    fc_action_active_num: int_t = RowData(5)
    fc_action_stock_num: int_t = RowData(6)
    fc_chest_box_num: int_t = RowData(7)


class FCReputation(DataRow):
    _sign = b'FCReputation|eJzLy8vLKwYABnwCLA=='
    sheet_name = 'FCReputation'
    _display = 'name'
    next_point: int_t = RowData(0)
    current_point: int_t = RowData(1)
    discount_rate: int_t = RowData(2)
    color: 'UIColor' = RowForeign(3, 'UIColor')
    name: str_t = RowData(4)


class FCRights(DataRow):
    _sign = b'FCRights|eJwrLs7LAwAEcwHD'
    sheet_name = 'FCRights'
    _display = 'rights_name_text'
    rights_name_text: str_t = RowData(0)
    rights_name_help: str_t = RowData(1)
    icon: 'Icon' = IconRow(2)
    sort_id: 'FCRank' = RowForeign(3, 'FCRank')


class FashionCheckThemeCategory(DataRow):
    _sign = b'FashionCheckThemeCategory|eJwrBgAAdAB0'
    sheet_name = 'FashionCheckThemeCategory'
    text: str_t = RowData(0)


class FashionCheckWeeklyTheme(DataRow):
    _sign = b'FashionCheckWeeklyTheme|eJwrBgAAdAB0'
    sheet_name = 'FashionCheckWeeklyTheme'
    text: str_t = RowData(0)


class Fate(DataRow):
    _sign = b'Fate|eJwrLgaBPCwgLQ2E07BJAQBpaBa9'
    sheet_name = 'Fate'
    _display = 'text_title_text'
    text_title_text: str_t = RowData(0)
    text_description_text: str_t = RowData(1)
    text_description_text2: str_t = RowData(2)
    text_todo_name1: str_t = RowData(3)
    text_todo_name2: str_t = RowData(4)
    text_todo_name3: str_t = RowData(5)
    mode: int_t = RowData(6)
    rule: int_t = RowData(7)
    rule_ex: 'FateRuleEx' = RowForeign(8, 'FateRuleEx')
    event_range: int_t = RowData(9)
    level: int_t = RowData(10)
    sync_lv: int_t = RowData(11)
    trade_item_id: 'EventItem' = RowForeign(12, 'EventItem')
    todo_value_type: List[int_t] = ListData(ir((13, 3, 1)), RowData)
    icon: 'Icon' = IconRow(16)
    icon_small: 'Icon' = IconRow(17)
    icon_small2: 'Icon' = IconRow(18)
    bgm: 'BGM' = RowForeign(19, 'BGM')
    guard_npc_layout_id: int_t = RowData(20)
    accept_screen_image: 'ScreenImage' = RowForeign(21, 'ScreenImage')
    complete_screen_image: 'ScreenImage' = RowForeign(22, 'ScreenImage')
    failed_screen_image: 'ScreenImage' = RowForeign(23, 'ScreenImage')
    map_visibility_type: int_t = RowData(24)
    map_visibility_value: 'Quest' = RowForeign(25, 'Quest')
    is_quest: bool_t = RowData(26)
    is_priority_draw: bool_t = RowData(27)
    action_status: 'Status' = RowForeign(28, 'Status')
    join_status: int_t = RowData(29)
    is_collection_infinite: bool_t = RowData(30)
    success_bgm_continue: bool_t = RowData(31)
    failure_bgm_continue: bool_t = RowData(32)
    resident: int_t = RowData(33)
    class_job_category: int_t = RowData(34)
    event_permission: int_t = RowData(35)
    text_param: 'List[ArrayEventHandler]' = ListData(ir((36, 2, 1)), RowForeign, 'ArrayEventHandler')
    quest: 'EventItem' = RowForeign(38, 'EventItem')
    local_progress: 'List[EventItem]' = ListData(ir((39, 6, 1)), RowForeign, 'EventItem')
    map_marker_icon_id: List[int_t] = ListData(ir((45, 8, 1)), RowData)


class FateEvent(DataRow):
    _sign = b'FateEvent|eJzLyyMOpEEBjF8MBQB5wRtp'
    sheet_name = 'FateEvent'
    param_turn: List[int_t] = ListData(ir((0, 8, 1)), RowData)
    param_gesture: List[int_t] = ListData(ir((8, 8, 1)), RowData)
    param_lip_sync: List[int_t] = ListData(ir((16, 8, 1)), RowData)
    param_facial: List[int_t] = ListData(ir((24, 8, 1)), RowData)
    param_shape: List[int_t] = ListData(ir((32, 8, 1)), RowData)
    param_is_auto_shake: List[bool_t] = ListData(ir((40, 8, 1)), RowData)
    param_widget_type: List[int_t] = ListData(ir((48, 8, 1)), RowData)
    text: List[str_t] = ListData(ir((56, 8, 1)), RowData)


class FateMode(DataRow):
    _sign = b'FateMode|eJzLywMCAAZ3Aic='
    sheet_name = 'FateMode'
    nearby_message: int_t = RowData(0)
    starter_announce_icon: 'Icon' = IconRow(1)
    starter_map_icon: 'Icon' = IconRow(2)
    trader_announce_icon: 'Icon' = IconRow(3)
    trader_map_icon: 'Icon' = IconRow(4)


class FateProgressUI(DataRow):
    _sign = b'FateProgressUI|eJzLywMBAAkMApU='
    sheet_name = 'FateProgressUI'
    territory: 'TerritoryType' = RowForeign(0, 'TerritoryType')
    achievement: 'Achievement' = RowForeign(1, 'Achievement')
    rank: List[int_t] = ListData(ir((2, 2, 1)), RowData)
    ui_location: int_t = RowData(4)
    ui_sort: int_t = RowData(5)


class FateRuleEx(DataRow):
    _sign = b'FateRuleEx|eJzLAwAAbwBv'
    sheet_name = 'FateRuleEx'
    type: int_t = RowData(0)


class FateShop(DataRow):
    _sign = b'FateShop|eJzLy4MBABesBE0='
    sheet_name = 'FateShop'
    shop: List[int_t] = ListData(ir((0, 2, 1)), RowData)
    talk: List[int_t] = ListData(ir((2, 8, 1)), RowData)


class FateTokenType(DataRow):
    _sign = b'FateTokenType|eJzLAwAAbwBv'
    sheet_name = 'FateTokenType'
    _display = 'item_id'
    item_id: 'Item' = RowForeign(0, 'Item')


class FccShop(DataRow):
    _sign = b'FccShop|eJwrzsMLANXaDVg='
    sheet_name = 'FccShop'
    _display = 'text'
    text: str_t = RowData(0)
    items_item: List[int_t] = ListData(ir((1, 10, 1)), RowData)
    items_fcc_price: List[int_t] = ListData(ir((11, 10, 1)), RowData)
    items_need_rank: List[int_t] = ListData(ir((21, 10, 1)), RowData)


class Festival(DataRow):
    _sign = b'Festival|eJwrzgMAAVYA4g=='
    sheet_name = 'Festival'
    _display = 'name'
    name: str_t = RowData(0)
    weather: int_t = RowData(1)


class FieldMarker(DataRow):
    _sign = b'FieldMarker|eJzLy8srBgAEVQG+'
    sheet_name = 'FieldMarker'
    _display = 'text'
    vfx: 'VFX' = RowForeign(0, 'VFX')
    icon: 'Icon' = IconRow(1)
    map_marker_icon: 'Icon' = IconRow(2)
    text: str_t = RowData(3)


class FishParameter(DataRow):
    _sign = b'FishParameter|eJwrzsvLS0vLA5NpeQAskgXi'
    sheet_name = 'FishParameter'
    _display = 'item_id'
    text: str_t = RowData(0)
    item_id: int_t = RowData(1)
    level: 'GatheringItemLevelConvertTable' = RowForeign(2, 'GatheringItemLevelConvertTable')
    level_star: int_t = RowData(3)
    is_mask_condition: bool_t = RowData(4)
    is_special_condition: bool_t = RowData(5)
    record_type: 'FishingRecordType' = RowForeign(6, 'FishingRecordType')
    territory: 'TerritoryType' = RowForeign(7, 'TerritoryType')
    typical_fishing_spot: int_t = RowData(8)
    folklore: 'GatheringSubCategory' = RowForeign(9, 'GatheringSubCategory')
    is_fish_print: bool_t = RowData(10)
    is_catch_time: bool_t = RowData(11)
    is_weather_condition: bool_t = RowData(12)
    guardian_achievement_count: int_t = RowData(13)


class FishParameter(DataRow):
    _sign = b'FishParameter|eJwrzsvLSwNjABeeBEI='
    sheet_name = 'FishParameter'
    _display = 'item_id'
    text: str_t = RowData(0)
    item_id: int_t = RowData(1)
    level: 'GatheringItemLevelConvertTable' = RowForeign(2, 'GatheringItemLevelConvertTable')
    level_star: int_t = RowData(3)
    is_mask_condition: bool_t = RowData(4)
    record_type: 'FishingRecordType' = RowForeign(5, 'FishingRecordType')
    typical_fishing_spot: int_t = RowData(6)
    folklore: 'GatheringSubCategory' = RowForeign(7, 'GatheringSubCategory')
    is_fish_print: bool_t = RowData(8)
    guardian_achievement_count: int_t = RowData(9)


class FishParameterReverse(DataRow):
    _sign = b'FishParameterReverse|eJxLAwAAZwBn'
    sheet_name = 'FishParameterReverse'
    masked: bool_t = RowData(0)


class FishingBaitParameter(DataRow):
    _sign = b'FishingBaitParameter|eJzLAwAAbwBv'
    sheet_name = 'FishingBaitParameter'
    item_id: int_t = RowData(0)


class FishingNoteInfo(DataRow):
    _sign = b'FishingNoteInfo|eJzLywMDAAwPAwM='
    sheet_name = 'FishingNoteInfo'


class FishingRecordType(DataRow):
    _sign = b'FishingRecordType|eJzLywMDAAwPAwM='
    sheet_name = 'FishingRecordType'
    _display = 'name_id'
    name_id: 'Addon' = RowForeign(0, 'Addon')
    rank: List[int_t] = ListData(ir((1, 5, 1)), RowData)
    type: int_t = RowData(6)


class FishingRecordTypeTransient(DataRow):
    _sign = b'FishingRecordTypeTransient|eJzLAwAAbwBv'
    sheet_name = 'FishingRecordTypeTransient'
    icon: 'Icon' = IconRow(0)


class FishingSpot(DataRow):
    _sign = b'FishingSpot|eJzLKy7OS8vDBACBQQpT'
    sheet_name = 'FishingSpot'
    _display = 'spot_name_id'
    level: int_t = RowData(0)
    text_reach_start: str_t = RowData(1)
    text_reach_end: str_t = RowData(2)
    category: int_t = RowData(3)
    rare: bool_t = RowData(4)
    territory_type: 'TerritoryType' = RowForeign(5, 'TerritoryType')
    notebook_region: 'PlaceName' = RowForeign(6, 'PlaceName')
    notebook_area: 'PlaceName' = RowForeign(7, 'PlaceName')
    maker_pos_x: int_t = RowData(8)
    maker_pos_y: int_t = RowData(9)
    maker_type: int_t = RowData(10)
    name_layout: int_t = RowData(11)
    target: List[int_t] = ListData(ir((12, 10, 1)), RowData)
    spot_name_id: 'PlaceName' = RowForeign(22, 'PlaceName')
    sort_key: int_t = RowData(23)


class FittingShop(DataRow):
    _sign = b'FittingShop|eJzLy8MPAOMADcE='
    sheet_name = 'FittingShop'
    contents_category: List[int_t] = ListData(ir((0, 32, 1)), RowData)


class FittingShopCategory(DataRow):
    _sign = b'FittingShopCategory|eJzLKwYAAVEA4g=='
    sheet_name = 'FittingShopCategory'
    display_id: int_t = RowData(0)
    text: str_t = RowData(1)


class FittingShopCategoryItem(DataRow):
    _sign = b'FittingShopCategoryItem|eJzLy8sDAAKXAUs='
    sheet_name = 'FittingShopCategoryItem'
    item_id: int_t = RowData(0)
    display_id: int_t = RowData(1)
    sort_id: int_t = RowData(2)


class FittingShopItemSet(DataRow):
    _sign = b'FittingShopItemSet|eJzLywOBYgAMFAMI'
    sheet_name = 'FittingShopItemSet'
    item_item_id: List[int_t] = ListData(ir((0, 6, 1)), RowData)
    text: str_t = RowData(6)


class Frontline(DataRow):
    _sign = b'Frontline|eJzLy8MOAIEAClE='
    sheet_name = 'Frontline'
    win_score: int_t = RowData(0)
    advantage_score: int_t = RowData(1)
    start_image_text: List[int_t] = ListData(ir((2, 3, 1)), RowData)
    win_image_text: List[int_t] = ListData(ir((5, 3, 1)), RowData)
    lose_image_text: List[int_t] = ListData(ir((8, 3, 1)), RowData)
    draw_image_text: int_t = RowData(11)
    bgm: List[int_t] = ListData(ir((12, 3, 1)), RowData)
    game_bgm: List[int_t] = ListData(ir((15, 3, 1)), RowData)
    game_advantage_bgm: List[int_t] = ListData(ir((18, 3, 1)), RowData)
    landing_point: List[int_t] = ListData(ir((21, 3, 1)), RowData)


class Frontline(DataRow):
    _sign = b'Frontline|eJzLy8MKAHavCeM='
    sheet_name = 'Frontline'
    advantage_score: int_t = RowData(0)
    start_image_text: List[int_t] = ListData(ir((1, 3, 1)), RowData)
    win_image_text: List[int_t] = ListData(ir((4, 3, 1)), RowData)
    lose_image_text: List[int_t] = ListData(ir((7, 3, 1)), RowData)
    draw_image_text: int_t = RowData(10)
    bgm: List[int_t] = ListData(ir((11, 3, 1)), RowData)
    game_bgm: List[int_t] = ListData(ir((14, 3, 1)), RowData)
    game_advantage_bgm: List[int_t] = ListData(ir((17, 3, 1)), RowData)
    landing_point: List[int_t] = ListData(ir((20, 3, 1)), RowData)


class Frontline01(DataRow):
    _sign = b'Frontline01|eJzLyxseAAC/b1Xx'
    sheet_name = 'Frontline01'
    base_params_base_event_range_id: List[int_t] = ListData(ir((0, 8, 1)), RowData)
    base_params_base_name: List[int_t] = ListData(ir((8, 8, 1)), RowData)
    base_params_base_map_marker: List[int_t] = ListData(ir((16, 8, 1)), RowData)
    shared_group_sg_layout_id: List[int_t] = ListData(ir((24, 48, 1)), RowData)
    shared_group_sg_idle_index: List[int_t] = ListData(ir((72, 48, 1)), RowData)
    shared_group_sg_change_index: List[int_t] = ListData(ir((120, 48, 1)), RowData)
    shared_group_visibilities_sg_visibilities_layout_id: List[int_t] = ListData(ir((168, 16, 1)), RowData)
    shared_group_visibilities_sg_visibilities_timeline: List[int_t] = ListData(ir((184, 16, 1)), RowData)


class Frontline02(DataRow):
    _sign = b'Frontline02|eJzLy8MHAMfsDOU='
    sheet_name = 'Frontline02'
    num_0: int_t = RowData(0)
    num_1: int_t = RowData(1)
    num_2: int_t = RowData(2)
    num_3: int_t = RowData(3)
    num_4: int_t = RowData(4)
    num_5: int_t = RowData(5)
    num_6: int_t = RowData(6)
    num_7: int_t = RowData(7)
    num_8: int_t = RowData(8)
    num_9: int_t = RowData(9)
    num_10: int_t = RowData(10)
    num_11: int_t = RowData(11)
    num_12: int_t = RowData(12)
    num_13: int_t = RowData(13)
    num_14: int_t = RowData(14)
    num_15: int_t = RowData(15)
    num_16: int_t = RowData(16)
    num_17: int_t = RowData(17)
    num_18: int_t = RowData(18)
    num_19: int_t = RowData(19)
    num_20: int_t = RowData(20)
    num_21: int_t = RowData(21)
    num_22: int_t = RowData(22)
    num_23: int_t = RowData(23)
    num_24: int_t = RowData(24)
    num_25: int_t = RowData(25)
    num_26: int_t = RowData(26)
    num_27: int_t = RowData(27)
    num_28: int_t = RowData(28)
    num_29: int_t = RowData(29)


class Frontline03(DataRow):
    _sign = b'Frontline03|eJzLy8MCAGNXCQc='
    sheet_name = 'Frontline03'
    access_point_ranks_point: List[int_t] = ListData(ir((0, 3, 1)), RowData)
    access_point_ranks_interval_time: List[int_t] = ListData(ir((3, 3, 1)), RowData)
    access_point_ranks_limit_point: List[int_t] = ListData(ir((6, 3, 1)), RowData)
    access_point_ranks_icon: List[List[int_t]] = ListData(ir(((9, 4, 3), 3, 1)), ListData, RowData)


class Frontline04(DataRow):
    _sign = b'Frontline04|eJzLyxsFKAAAy3F1Tw=='
    sheet_name = 'Frontline04'
    node_base_event_range_id: 'List[Level]' = ListData(ir((0, 3, 1)), RowForeign, 'Level')
    node_base_name: List[int_t] = ListData(ir((3, 3, 1)), RowData)
    node_base_map_marker: List[int_t] = ListData(ir((6, 3, 1)), RowData)
    shared_group_sg_layout_id: List[int_t] = ListData(ir((9, 48, 1)), RowData)
    shared_group_sg_idle_index: List[int_t] = ListData(ir((57, 48, 1)), RowData)
    shared_group_sg_change_index: List[int_t] = ListData(ir((105, 48, 1)), RowData)
    break_object_type: List[int_t] = ListData(ir((153, 24, 1)), RowData)
    break_object_layout_id: List[int_t] = ListData(ir((177, 24, 1)), RowData)
    break_object_collision: List[int_t] = ListData(ir((201, 24, 1)), RowData)
    break_object_bnpc: List[int_t] = ListData(ir((225, 24, 1)), RowData)
    break_object_name_id: List[int_t] = ListData(ir((249, 24, 1)), RowData)


class FurnitureCatalogCategory(DataRow):
    _sign = b'FurnitureCatalogCategory|eJwrzssDAAKmAVA='
    sheet_name = 'FurnitureCatalogCategory'
    _display = 'text'
    text: str_t = RowData(0)
    housing_item_type: int_t = RowData(1)
    sort: int_t = RowData(2)


class FurnitureCatalogItemList(DataRow):
    _sign = b'FurnitureCatalogItemList|eJzLy8sDAAKXAUs='
    sheet_name = 'FurnitureCatalogItemList'
    _display = 'item'
    category: 'FurnitureCatalogCategory' = RowForeign(0, 'FurnitureCatalogCategory')
    item: 'Item' = RowForeign(1, 'Item')
    version: int_t = RowData(2)


class GCRankGridaniaFemaleText(DataRow):
    _sign = b'GCRankGridaniaFemaleText|eJwrzivOA4HiYgAYFQRh'
    sheet_name = 'GCRankGridaniaFemaleText'
    _display = 'singular'
    singular: str_t = RowData(0)
    adjective: int_t = RowData(1)
    plural: str_t = RowData(2)
    possessive_pronoun: int_t = RowData(3)
    starts_with_vowel: int_t = RowData(4)
    field_5: int_t = RowData(5)
    pronoun: int_t = RowData(6)
    article: int_t = RowData(7)
    name_rank: str_t = RowData(8)
    field_9: str_t = RowData(9)


class GCRankGridaniaMaleText(DataRow):
    _sign = b'GCRankGridaniaMaleText|eJwrzivOA4HiYgAYFQRh'
    sheet_name = 'GCRankGridaniaMaleText'
    _display = 'singular'
    singular: str_t = RowData(0)
    adjective: int_t = RowData(1)
    plural: str_t = RowData(2)
    possessive_pronoun: int_t = RowData(3)
    starts_with_vowel: int_t = RowData(4)
    field_5: int_t = RowData(5)
    pronoun: int_t = RowData(6)
    article: int_t = RowData(7)
    name_rank: str_t = RowData(8)
    field_9: str_t = RowData(9)


class GCRankLimsaFemaleText(DataRow):
    _sign = b'GCRankLimsaFemaleText|eJwrzivOA4HiYgAYFQRh'
    sheet_name = 'GCRankLimsaFemaleText'
    _display = 'singular'
    singular: str_t = RowData(0)
    adjective: int_t = RowData(1)
    plural: str_t = RowData(2)
    possessive_pronoun: int_t = RowData(3)
    starts_with_vowel: int_t = RowData(4)
    field_5: int_t = RowData(5)
    pronoun: int_t = RowData(6)
    article: int_t = RowData(7)
    name_rank: str_t = RowData(8)
    field_9: str_t = RowData(9)


class GCRankLimsaMaleText(DataRow):
    _sign = b'GCRankLimsaMaleText|eJwrzivOA4HiYgAYFQRh'
    sheet_name = 'GCRankLimsaMaleText'
    _display = 'singular'
    singular: str_t = RowData(0)
    adjective: int_t = RowData(1)
    plural: str_t = RowData(2)
    possessive_pronoun: int_t = RowData(3)
    starts_with_vowel: int_t = RowData(4)
    field_5: int_t = RowData(5)
    pronoun: int_t = RowData(6)
    article: int_t = RowData(7)
    name_rank: str_t = RowData(8)
    field_9: str_t = RowData(9)


class GCRankUldahFemaleText(DataRow):
    _sign = b'GCRankUldahFemaleText|eJwrzivOA4HiYgAYFQRh'
    sheet_name = 'GCRankUldahFemaleText'
    _display = 'singular'
    singular: str_t = RowData(0)
    adjective: int_t = RowData(1)
    plural: str_t = RowData(2)
    possessive_pronoun: int_t = RowData(3)
    starts_with_vowel: int_t = RowData(4)
    field_5: int_t = RowData(5)
    pronoun: int_t = RowData(6)
    article: int_t = RowData(7)
    name_rank: str_t = RowData(8)
    field_9: str_t = RowData(9)


class GCRankUldahMaleText(DataRow):
    _sign = b'GCRankUldahMaleText|eJwrzivOA4HiYgAYFQRh'
    sheet_name = 'GCRankUldahMaleText'
    _display = 'singular'
    singular: str_t = RowData(0)
    adjective: int_t = RowData(1)
    plural: str_t = RowData(2)
    possessive_pronoun: int_t = RowData(3)
    starts_with_vowel: int_t = RowData(4)
    field_5: int_t = RowData(5)
    pronoun: int_t = RowData(6)
    article: int_t = RowData(7)
    name_rank: str_t = RowData(8)
    field_9: str_t = RowData(9)


class GCScripShopCategory(DataRow):
    _sign = b'GCScripShopCategory|eJzLy8sDAAKXAUs='
    sheet_name = 'GCScripShopCategory'
    grand_company: 'GrandCompany' = RowForeign(0, 'GrandCompany')
    rank_category: int_t = RowData(1)
    gc_shop_item_category: int_t = RowData(2)


class GCScripShopItem(DataRow):
    _sign = b'GCScripShopItem|eJzLy8vLAwAEUAG5'
    sheet_name = 'GCScripShopItem'
    _display = 'item_id'
    item_id: 'Item' = RowForeign(0, 'Item')
    valid_rank: 'GrandCompanyRank' = RowForeign(1, 'GrandCompanyRank')
    scrip: int_t = RowData(2)
    sort: int_t = RowData(3)


class GCShop(DataRow):
    _sign = b'GCShop|eJzLAwAAbwBv'
    sheet_name = 'GCShop'
    grand_company: 'GrandCompany' = RowForeign(0, 'GrandCompany')


class GCShopItemCategory(DataRow):
    _sign = b'GCShopItemCategory|eJwrBgAAdAB0'
    sheet_name = 'GCShopItemCategory'
    _display = 'text'
    text: str_t = RowData(0)


class GCSupplyDefine(DataRow):
    _sign = b'GCSupplyDefine|eJzLAwAAbwBv'
    sheet_name = 'GCSupplyDefine'
    value: int_t = RowData(0)


class GCSupplyDuty(DataRow):
    _sign = b'GCSupplyDuty|eJzLy6MUAAC2eRxd'
    sheet_name = 'GCSupplyDuty'
    wood_worker_item_wdk: List[int_t] = ListData(ir((0, 3, 2)), RowData)
    wood_worker_stack_wdk: List[int_t] = ListData(ir((1, 3, 2)), RowData)
    culinarian_item_cul: List[int_t] = ListData(ir((6, 3, 2)), RowData)
    culinarian_stack_cul: List[int_t] = ListData(ir((7, 3, 2)), RowData)
    alchemist_item_alc: List[int_t] = ListData(ir((12, 3, 2)), RowData)
    alchemist_stack_alc: List[int_t] = ListData(ir((13, 3, 2)), RowData)
    armourer_item_arm: List[int_t] = ListData(ir((18, 3, 2)), RowData)
    armourer_stack_arm: List[int_t] = ListData(ir((19, 3, 2)), RowData)
    tanner_item_tan: List[int_t] = ListData(ir((24, 3, 2)), RowData)
    tanner_stack_tan: List[int_t] = ListData(ir((25, 3, 2)), RowData)
    gold_smith_item_gld: List[int_t] = ListData(ir((30, 3, 2)), RowData)
    gold_smith_stack_gld: List[int_t] = ListData(ir((31, 3, 2)), RowData)
    weaver_item_wvr: List[int_t] = ListData(ir((36, 3, 2)), RowData)
    weaver_stack_wvr: List[int_t] = ListData(ir((37, 3, 2)), RowData)
    black_smith_item_bsm: List[int_t] = ListData(ir((42, 3, 2)), RowData)
    black_smith_stack_bsm: List[int_t] = ListData(ir((43, 3, 2)), RowData)
    miner_item_min: List[int_t] = ListData(ir((48, 3, 2)), RowData)
    miner_stack_min: List[int_t] = ListData(ir((49, 3, 2)), RowData)
    harvester_item_hrv: List[int_t] = ListData(ir((54, 3, 2)), RowData)
    harvester_stack_hrv: List[int_t] = ListData(ir((55, 3, 2)), RowData)
    fisherman_item_fsh: List[int_t] = ListData(ir((60, 3, 2)), RowData)
    fisherman_stack_fsh: List[int_t] = ListData(ir((61, 3, 2)), RowData)


class GCSupplyDutyReward(DataRow):
    _sign = b'GCSupplyDutyReward|eJzLywMCAAZ3Aic='
    sheet_name = 'GCSupplyDutyReward'
    exp_of_munition: int_t = RowData(0)
    exp_of_supplies: int_t = RowData(1)
    seals_of_booty: int_t = RowData(2)
    seals_of_munition: int_t = RowData(3)
    seals_of_supplies: int_t = RowData(4)


class GFATE(DataRow):
    _sign = b'GFATE|eJzLyyMKpJEIAEjJI+M='
    sheet_name = 'GFATE'
    type: int_t = RowData(0)
    position_type: int_t = RowData(1)
    bgm: int_t = RowData(2)
    screen_image_text: List[int_t] = ListData(ir((3, 3, 1)), RowData)
    resident: int_t = RowData(6)
    announce_icons_layout_id: List[int_t] = ListData(ir((7, 16, 1)), RowData)
    announce_icons_icon: List[int_t] = ListData(ir((23, 16, 1)), RowData)
    announce_icons_is_pre_join: List[bool_t] = ListData(ir((39, 16, 1)), RowData)
    announce_icons_is_joined: List[bool_t] = ListData(ir((55, 16, 1)), RowData)
    announce_icons_is_finish: List[bool_t] = ListData(ir((71, 16, 1)), RowData)


class GFateClimbing(DataRow):
    _sign = b'GFateClimbing|eJzLKwYAAVEA4g=='
    sheet_name = 'GFateClimbing'
    goal_action_timeline: int_t = RowData(0)
    text: str_t = RowData(1)


class GFateClimbing2(DataRow):
    _sign = b'GFateClimbing2|eJzLAwAAbwBv'
    sheet_name = 'GFateClimbing2'
    content_entry: 'ContentEntry' = RowForeign(0, 'ContentEntry')


class GFateClimbing2Content(DataRow):
    _sign = b'GFateClimbing2Content|eJzLAwAAbwBv'
    sheet_name = 'GFateClimbing2Content'
    start_message: 'PublicContentTextData' = RowForeign(0, 'PublicContentTextData')


class GFateClimbing2TotemType(DataRow):
    _sign = b'GFateClimbing2TotemType|eJzLAwAAbwBv'
    sheet_name = 'GFateClimbing2TotemType'
    todo_text: 'PublicContentTextData' = RowForeign(0, 'PublicContentTextData')


class GFateDance(DataRow):
    _sign = b'GFateDance|eJzLywMAAUwA3Q=='
    sheet_name = 'GFateDance'
    num_of_motion: int_t = RowData(0)
    num_of_dance: int_t = RowData(1)


class GFateHiddenObject(DataRow):
    _sign = b'GFateHiddenObject|eJzLAwAAbwBv'
    sheet_name = 'GFateHiddenObject'
    transformation: int_t = RowData(0)


class GFateRideShooting(DataRow):
    _sign = b'GFateRideShooting|eJzLAwAAbwBv'
    sheet_name = 'GFateRideShooting'
    content_entry: 'ContentEntry' = RowForeign(0, 'ContentEntry')


class GFateRoulette(DataRow):
    _sign = b'GFateRoulette|eJzLAwAAbwBv'
    sheet_name = 'GFateRoulette'
    lottery_number: int_t = RowData(0)


class GFateStelth(DataRow):
    _sign = b'GFateStelth|eJzLKwYAAVEA4g=='
    sheet_name = 'GFateStelth'
    num_of_items: int_t = RowData(0)
    text: str_t = RowData(1)


class GameRewardObtainType(DataRow):
    _sign = b'GameRewardObtainType|eJzLywMAAUwA3Q=='
    sheet_name = 'GameRewardObtainType'
    icon: int_t = RowData(0)
    obtain_format: int_t = RowData(1)


class GardeningSeed(DataRow):
    _sign = b'GardeningSeed|eJzLy8tLS8sDAAjkAoU='
    sheet_name = 'GardeningSeed'
    _display = 'crop'
    crop: 'Item' = RowForeign(0, 'Item')
    model_id: int_t = RowData(1)
    harvest_icon: 'Icon' = IconRow(2)
    se: bool_t = RowData(3)
    plant_pot_exclusive: bool_t = RowData(4)
    flower: int_t = RowData(5)


class GathererCrafterTool(DataRow):
    _sign = b'GathererCrafterTool|eJzLywMAAUwA3Q=='
    sheet_name = 'GathererCrafterTool'
    effect_type: int_t = RowData(0)
    effect_value: int_t = RowData(1)


class GathererReductionReward(DataRow):
    _sign = b'GathererReductionReward|eJzLSwMAAUQA1Q=='
    sheet_name = 'GathererReductionReward'
    refine: int_t = RowData(0)
    is_lowest_item_rate: bool_t = RowData(1)


class GatheringCondition(DataRow):
    _sign = b'GatheringCondition|eJwrBgAAdAB0'
    sheet_name = 'GatheringCondition'
    _display = 'text'
    text: str_t = RowData(0)


class GatheringExp(DataRow):
    _sign = b'GatheringExp|eJzLAwAAbwBv'
    sheet_name = 'GatheringExp'
    exp: int_t = RowData(0)


class GatheringItem(DataRow):
    _sign = b'GatheringItem|eJzLy0vLA6E8ABMHA88='
    sheet_name = 'GatheringItem'
    _display = 'item_id'
    item_id: int_t = RowData(0)
    level: 'GatheringItemLevelConvertTable' = RowForeign(1, 'GatheringItemLevelConvertTable')
    is_notebook: bool_t = RowData(2)
    need_insight: 'Quest' = RowForeign(3, 'Quest')
    need_complete_quest: int_t = RowData(4)
    is_hidden_for_notebook: bool_t = RowData(5)
    mutated_gathering_item: int_t = RowData(6)
    collectables_refine_type: int_t = RowData(7)
    collectables_refine: int_t = RowData(8)


class GatheringItemLevelConvertTable(DataRow):
    _sign = b'GatheringItemLevelConvertTable|eJzLywMAAUwA3Q=='
    sheet_name = 'GatheringItemLevelConvertTable'
    ui_level: int_t = RowData(0)
    difficulty: int_t = RowData(1)


class GatheringItemPoint(DataRow):
    _sign = b'GatheringItemPoint|eJzLAwAAbwBv'
    sheet_name = 'GatheringItemPoint'
    _display = 'gathering_point_id'
    gathering_point_id: 'GatheringPoint' = RowForeign(0, 'GatheringPoint')


class GatheringLeve(DataRow):
    _sign = b'GatheringLeve|eJzLy0MHaQBRrwgj'
    sheet_name = 'GatheringLeve'
    route: List[int_t] = ListData(ir((0, 4, 1)), RowData)
    item: 'List[EventItem]' = ListData(ir((4, 4, 2)), RowForeign, 'EventItem')
    item_num: List[int_t] = ListData(ir((5, 4, 2)), RowData)
    num: int_t = RowData(12)
    rule: 'GatheringLeveRule' = RowForeign(13, 'GatheringLeveRule')
    variation: int_t = RowData(14)
    objective: List[int_t] = ListData(ir((15, 2, 1)), RowData)
    b_npc_entry: 'GatheringLeveBNpcEntry' = RowForeign(17, 'GatheringLeveBNpcEntry')
    use_sub_arm: bool_t = RowData(18)


class GatheringLeveBNpcEntry(DataRow):
    _sign = b'GatheringLeveBNpcEntry|eJzLy0MAACGQBSk='
    sheet_name = 'GatheringLeveBNpcEntry'
    num_0: int_t = RowData(0)
    num_1: int_t = RowData(1)
    num_2: int_t = RowData(2)
    num_3: int_t = RowData(3)
    num_4: int_t = RowData(4)
    num_5: int_t = RowData(5)
    num_6: int_t = RowData(6)
    num_7: int_t = RowData(7)
    num_8: int_t = RowData(8)
    num_9: int_t = RowData(9)
    num_10: int_t = RowData(10)
    num_11: int_t = RowData(11)


class GatheringLeveRoute(DataRow):
    _sign = b'GatheringLeveRoute|eJzLy8MOAIEAClE='
    sheet_name = 'GatheringLeveRoute'
    point: List[int_t] = ListData(ir((0, 12, 2)), RowData)
    b_npc_pop_range: List[int_t] = ListData(ir((1, 12, 2)), RowData)


class GatheringLeveRule(DataRow):
    _sign = b'GatheringLeveRule|eJwrBgAAdAB0'
    sheet_name = 'GatheringLeveRule'
    _display = 'script'
    script: str_t = RowData(0)


class GatheringNotebookItem(DataRow):
    _sign = b'GatheringNotebookItem|eJzLAwAAbwBv'
    sheet_name = 'GatheringNotebookItem'
    gathering_item_id: int_t = RowData(0)


class GatheringNotebookList(DataRow):
    _sign = b'GatheringNotebookList|eJzLy6MDAACmLytn'
    sheet_name = 'GatheringNotebookList'
    item_num: int_t = RowData(0)
    item_id: List[int_t] = ListData(ir((1, 100, 1)), RowData)


class GatheringPoint(DataRow):
    _sign = b'GatheringPoint|eJzLy4MCABNfA98='
    sheet_name = 'GatheringPoint'
    type: int_t = RowData(0)
    kind: int_t = RowData(1)
    base_id: 'GatheringPointBase' = RowForeign(2, 'GatheringPointBase')
    count: int_t = RowData(3)
    bonus: List[int_t] = ListData(ir((4, 2, 1)), RowData)
    area_id: 'TerritoryType' = RowForeign(6, 'TerritoryType')
    place_name_id: 'PlaceName' = RowForeign(7, 'PlaceName')
    sub_category: 'GatheringSubCategory' = RowForeign(8, 'GatheringSubCategory')


class GatheringPointBase(DataRow):
    _sign = b'GatheringPointBase|eJzLy4MBABesBE0='
    sheet_name = 'GatheringPointBase'
    type: 'GatheringType' = RowForeign(0, 'GatheringType')
    lv: int_t = RowData(1)
    gathering_item_id: List[int_t] = ListData(ir((2, 8, 1)), RowData)


class GatheringPointBonus(DataRow):
    _sign = b'GatheringPointBonus|eJzLywOBtDwAD3ADaQ=='
    sheet_name = 'GatheringPointBonus'
    bonus_cond: 'GatheringCondition' = RowForeign(0, 'GatheringCondition')
    bonus_cond_val: int_t = RowData(1)
    bonus_cond_val_max: int_t = RowData(2)
    bonus_type: 'GatheringPointBonusType' = RowForeign(3, 'GatheringPointBonusType')
    bonus_point: int_t = RowData(4)
    bonus_point_max: int_t = RowData(5)
    reverse_condition: bool_t = RowData(6)
    need_complete_quest: int_t = RowData(7)


class GatheringPointBonusType(DataRow):
    _sign = b'GatheringPointBonusType|eJwrBgAAdAB0'
    sheet_name = 'GatheringPointBonusType'
    _display = 'text'
    text: str_t = RowData(0)


class GatheringPointName(DataRow):
    _sign = b'GatheringPointName|eJwrzivOAwEAD8YDew=='
    sheet_name = 'GatheringPointName'
    _display = 'text_sgl'
    text_sgl: str_t = RowData(0)
    text_sgg: int_t = RowData(1)
    text_plr: str_t = RowData(2)
    text_plg: int_t = RowData(3)
    text_vow: int_t = RowData(4)
    text_cnt: int_t = RowData(5)
    text_gen: int_t = RowData(6)
    text_def_: int_t = RowData(7)


class GatheringPointTransient(DataRow):
    _sign = b'GatheringPointTransient|eJzLy8sDAAKXAUs='
    sheet_name = 'GatheringPointTransient'
    ephemeral_start_time: int_t = RowData(0)
    ephemeral_end_time: int_t = RowData(1)
    rare_pop_time_table_id: 'GatheringRarePopTimeTable' = RowForeign(2, 'GatheringRarePopTimeTable')


class GatheringRarePopTimeTable(DataRow):
    _sign = b'GatheringRarePopTimeTable|eJzLywMBAAkMApU='
    sheet_name = 'GatheringRarePopTimeTable'
    start_time: List[int_t] = ListData(ir((0, 3, 2)), RowData)
    pop_life: List[int_t] = ListData(ir((1, 3, 2)), RowData)


class GatheringSubCategory(DataRow):
    _sign = b'GatheringSubCategory|eJzLywOC4jwADBkDCA=='
    sheet_name = 'GatheringSubCategory'
    _display = 'text'
    type: 'GatheringType' = RowForeign(0, 'GatheringType')
    class_: 'ClassJob' = RowForeign(1, 'ClassJob')
    work_index: 'Quest' = RowForeign(2, 'Quest')
    division: int_t = RowData(3)
    item: 'Item' = RowForeign(4, 'Item')
    text: str_t = RowData(5)
    appearance_rule: int_t = RowData(6)


class GatheringType(DataRow):
    _sign = b'GatheringType|eJwrzssDAAKmAVA='
    sheet_name = 'GatheringType'
    _display = 'text'
    text: str_t = RowData(0)
    map_icon: 'Icon' = IconRow(1)
    rare_map_icon: 'Icon' = IconRow(2)


class GcArmyCandidateCategory(DataRow):
    _sign = b'GcArmyCandidateCategory|eJwrBgAAdAB0'
    sheet_name = 'GcArmyCandidateCategory'
    text: str_t = RowData(0)


class GcArmyCapture(DataRow):
    _sign = b'GcArmyCapture|eJzLy4MAAA+AA3E='
    sheet_name = 'GcArmyCapture'
    content: int_t = RowData(0)
    level: int_t = RowData(1)
    level_max: int_t = RowData(2)
    item_level: int_t = RowData(3)
    item_level_max: int_t = RowData(4)
    open_condition_capture: int_t = RowData(5)
    company_seal: int_t = RowData(6)
    member_exp: int_t = RowData(7)


class GcArmyCaptureTactics(DataRow):
    _sign = b'GcArmyCaptureTactics|eJzLywMBAAkMApU='
    sheet_name = 'GcArmyCaptureTactics'
    _display = 'buff_status'
    buff_status: 'Status' = RowForeign(0, 'Status')
    buff_status_effect_hp: int_t = RowData(1)
    buff_status_effect_attack: int_t = RowData(2)
    buff_status_effec_defense: int_t = RowData(3)
    name_id: 'Addon' = RowForeign(4, 'Addon')
    icon_id: 'Icon' = IconRow(5)


class GcArmyEquipPreset(DataRow):
    _sign = b'GcArmyEquipPreset|eJzLywMDAAwPAwM='
    sheet_name = 'GcArmyEquipPreset'
    main_weapon: 'Item' = RowForeign(0, 'Item')
    sub_weapon: 'Item' = RowForeign(1, 'Item')
    equip: 'List[Item]' = ListData(ir((2, 5, 1)), RowForeign, 'Item')


class GcArmyExpedition(DataRow):
    _sign = b'GcArmyExpedition|eJzLy4OA4uI8sgAAgFgbiw=='
    sheet_name = 'GcArmyExpedition'
    _display = 'name'
    need_progress: int_t = RowData(0)
    disable_progress: int_t = RowData(1)
    min_member_level: int_t = RowData(2)
    company_seal: int_t = RowData(3)
    exp: int_t = RowData(4)
    success_rate: int_t = RowData(5)
    sort_id: int_t = RowData(6)
    type: 'GcArmyExpeditionType' = RowForeign(7, 'GcArmyExpeditionType')
    name: str_t = RowData(8)
    detail: str_t = RowData(9)
    variation_reward_item: List[int_t] = ListData(ir((10, 6, 1)), RowData)
    variation_reward_item_num: List[int_t] = ListData(ir((16, 6, 1)), RowData)
    variation_team_physical: List[int_t] = ListData(ir((22, 6, 1)), RowData)
    variation_team_physical_bonus: List[int_t] = ListData(ir((28, 6, 1)), RowData)
    variation_team_mental: List[int_t] = ListData(ir((34, 6, 1)), RowData)
    variation_team_mental_bonus: List[int_t] = ListData(ir((40, 6, 1)), RowData)
    variation_team_tactical: List[int_t] = ListData(ir((46, 6, 1)), RowData)
    variation_team_tactical_bonus: List[int_t] = ListData(ir((52, 6, 1)), RowData)
    variation_bonus_complete_bonus: List[int_t] = ListData(ir((58, 6, 1)), RowData)


class GcArmyExpeditionMemberBonus(DataRow):
    _sign = b'GcArmyExpeditionMemberBonus|eJzLywMAAUwA3Q=='
    sheet_name = 'GcArmyExpeditionMemberBonus'
    race: 'Race' = RowForeign(0, 'Race')
    class_job: 'ClassJob' = RowForeign(1, 'ClassJob')


class GcArmyExpeditionTrait(DataRow):
    _sign = b'GcArmyExpeditionTrait|eJzLy4OBYgAcbATA'
    sheet_name = 'GcArmyExpeditionTrait'
    rarity_effect: List[int_t] = ListData(ir((0, 5, 2)), RowData)
    rarity_rate: List[int_t] = ListData(ir((1, 5, 2)), RowData)
    text: str_t = RowData(10)


class GcArmyExpeditionTraitCond(DataRow):
    _sign = b'GcArmyExpeditionTraitCond|eJwrBgAAdAB0'
    sheet_name = 'GcArmyExpeditionTraitCond'
    text: str_t = RowData(0)


class GcArmyExpeditionType(DataRow):
    _sign = b'GcArmyExpeditionType|eJwrBgAAdAB0'
    sheet_name = 'GcArmyExpeditionType'
    _display = 'text'
    text: str_t = RowData(0)


class GcArmyMember(DataRow):
    _sign = b'GcArmyMember|eJzLywMAAUwA3Q=='
    sheet_name = 'GcArmyMember'
    special_equip: int_t = RowData(0)
    home: int_t = RowData(1)


class GcArmyMemberGrow(DataRow):
    _sign = b'GcArmyMemberGrow|eJzLyxuJAAACSWm1'
    sheet_name = 'GcArmyMemberGrow'
    class_job: 'ClassJob' = RowForeign(0, 'ClassJob')
    class_change_item: 'Item' = RowForeign(1, 'Item')
    param_equip_preset: List[int_t] = ListData(ir((2, 61, 1)), RowData)
    param_physical: List[int_t] = ListData(ir((63, 61, 1)), RowData)
    param_mental: List[int_t] = ListData(ir((124, 61, 1)), RowData)
    param_tactical: List[int_t] = ListData(ir((185, 61, 1)), RowData)


class GcArmyMemberGrowExp(DataRow):
    _sign = b'GcArmyMemberGrowExp|eJzLAwAAbwBv'
    sheet_name = 'GcArmyMemberGrowExp'
    next_exp: int_t = RowData(0)


class GcArmyProgress(DataRow):
    _sign = b'GcArmyProgress|eJzLy8sDAAKXAUs='
    sheet_name = 'GcArmyProgress'
    progress: int_t = RowData(0)
    army_rank: int_t = RowData(1)
    team_power_sum_max: int_t = RowData(2)


class GcArmyTraining(DataRow):
    _sign = b'GcArmyTraining|eJzLy8vLKy4GAAkbAp8='
    sheet_name = 'GcArmyTraining'
    _display = 'text'
    team_physical_up: int_t = RowData(0)
    team_mental_up: int_t = RowData(1)
    team_tactical_up: int_t = RowData(2)
    exp: int_t = RowData(3)
    text: str_t = RowData(4)
    effect_text: str_t = RowData(5)


class GeneralAction(DataRow):
    _sign = b'GeneralAction|eJwrLs4DgzQAE6wD4Q=='
    sheet_name = 'GeneralAction'
    _display = 'text_name'
    text_name: str_t = RowData(0)
    text_help: str_t = RowData(1)
    type: int_t = RowData(2)
    action: 'Action' = RowForeign(3, 'Action')
    reward: int_t = RowData(4)
    recast: int_t = RowData(5)
    ui_priority: int_t = RowData(6)
    icon: 'Icon' = IconRow(7)
    ui_control: bool_t = RowData(8)


class GilShop(DataRow):
    _sign = b'GilShop|eJwrzgOCtDwADCIDAA=='
    sheet_name = 'GilShop'
    _display = 'text'
    text: str_t = RowData(0)
    map_icon: 'Icon' = IconRow(1)
    disclosure_reward_or_quest: 'Quest' = RowForeign(2, 'Quest')
    qualified_talk: 'DefaultTalk' = RowForeign(3, 'DefaultTalk')
    unqualified_talk: 'DefaultTalk' = RowForeign(4, 'DefaultTalk')
    system: bool_t = RowData(5)
    festival: int_t = RowData(6)


class GilShopInfo(DataRow):
    _sign = b'GilShopInfo|eJzLAwAAbwBv'
    sheet_name = 'GilShopInfo'
    handlig: int_t = RowData(0)


class GilShopItem(DataRow):
    _sign = b'GilShopItem|eJzLS8uDAAATHwPX'
    sheet_name = 'GilShopItem'
    _display = 'item_id'
    item_id: 'Item' = RowForeign(0, 'Item')
    is_hq: bool_t = RowData(1)
    stain_id: int_t = RowData(2)
    quest: List[int_t] = ListData(ir((3, 2, 1)), RowData)
    achievement: 'Achievement' = RowForeign(5, 'Achievement')
    mask_type: int_t = RowData(6)
    sort: int_t = RowData(7)
    added_version: int_t = RowData(8)


class GimmickAccessor(DataRow):
    _sign = b'GimmickAccessor|eJzLywODtLQ0ABd8BDU='
    sheet_name = 'GimmickAccessor'
    type: int_t = RowData(0)
    param: List[int_t] = ListData(ir((1, 6, 1)), RowData)
    carry: bool_t = RowData(7)
    transformation: bool_t = RowData(8)
    client_visibility: bool_t = RowData(9)


class GimmickBill(DataRow):
    _sign = b'GimmickBill|eJwrBgAAdAB0'
    sheet_name = 'GimmickBill'
    text: str_t = RowData(0)


class GimmickJump(DataRow):
    _sign = b'GimmickJump|eJzLy8vLS0sDAAj0AoU='
    sheet_name = 'GimmickJump'
    fall_damage: int_t = RowData(0)
    height: int_t = RowData(1)
    loop_motion: 'ActionTimeline' = RowForeign(2, 'ActionTimeline')
    end_motion: 'ActionTimeline' = RowForeign(3, 'ActionTimeline')
    start_client: bool_t = RowData(4)
    over_write: bool_t = RowData(5)


class GimmickRect(DataRow):
    _sign = b'GimmickRect|eJzLy4MDABxnBLs='
    sheet_name = 'GimmickRect'
    layout_id: int_t = RowData(0)
    trigger_in: int_t = RowData(1)
    in_param: List[int_t] = ListData(ir((2, 4, 1)), RowData)
    trigger_out: int_t = RowData(6)
    out_param: List[int_t] = ListData(ir((7, 4, 1)), RowData)


class GimmickTalk(DataRow):
    _sign = b'GimmickTalk|eJzLSysGAAKMAUg='
    sheet_name = 'GimmickTalk'
    type: int_t = RowData(0)
    talker: bool_t = RowData(1)
    text: str_t = RowData(2)


class GimmickYesNo(DataRow):
    _sign = b'GimmickYesNo|eJwrLi4GAAK1AVo='
    sheet_name = 'GimmickYesNo'
    text_text1: str_t = RowData(0)
    text_text2: str_t = RowData(1)
    text_text3: str_t = RowData(2)


class GoldSaucerArcadeMachine(DataRow):
    _sign = b'GoldSaucerArcadeMachine|eJzLyyMKFAMBAJboEo8='
    sheet_name = 'GoldSaucerArcadeMachine'
    type: int_t = RowData(0)
    time: int_t = RowData(1)
    action_time: int_t = RowData(2)
    play_num: int_t = RowData(3)
    play_fee: int_t = RowData(4)
    ui_type: int_t = RowData(5)
    timeup_icon: 'Icon' = IconRow(6)
    offset_x: int_t = RowData(7)
    offset_y: int_t = RowData(8)
    offset_z: int_t = RowData(9)
    idle_motion: int_t = RowData(10)
    result_ui_wait_time: int_t = RowData(11)
    result_ui_offset_x: int_t = RowData(12)
    result_ui_offset_y: int_t = RowData(13)
    result_ui_offset_z: int_t = RowData(14)
    results_gauge: List[List[int_t]] = ListData(ir(((15, 2, 4), 4, 1)), ListData, RowData)
    results_score: List[int_t] = ListData(ir((23, 4, 1)), RowData)
    results_player_motion: List[int_t] = ListData(ir((27, 4, 1)), RowData)
    results_sg_timeline: List[int_t] = ListData(ir((31, 4, 1)), RowData)
    results_icon: List[Icon] = ListData(ir((35, 4, 1)), IconRow)
    text_title: str_t = RowData(39)
    text_description: str_t = RowData(40)
    text_description2: str_t = RowData(41)
    text_todo: str_t = RowData(42)


class GoldSaucerContent(DataRow):
    _sign = b'GoldSaucerContent|eJzLy8vLAwAEUAG5'
    sheet_name = 'GoldSaucerContent'
    director_type: int_t = RowData(0)
    time: int_t = RowData(1)
    territory_type: int_t = RowData(2)
    content_finder_condition: int_t = RowData(3)


class GoldSaucerTalk(DataRow):
    _sign = b'GoldSaucerTalk|eJzLy0vLywNjKChGAACuWgww'
    sheet_name = 'GoldSaucerTalk'
    type: int_t = RowData(0)
    shape: int_t = RowData(1)
    next_page: bool_t = RowData(2)
    next: int_t = RowData(3)
    turn: int_t = RowData(4)
    gesture: int_t = RowData(5)
    is_default_yes: bool_t = RowData(6)
    select_talk: List[int_t] = ListData(ir((7, 10, 1)), RowData)
    text: List[str_t] = ListData(ir((17, 11, 1)), RowData)


class GoldSaucerTextData(DataRow):
    _sign = b'GoldSaucerTextData|eJwrBgAAdAB0'
    sheet_name = 'GoldSaucerTextData'
    _display = 'text'
    text: str_t = RowData(0)


class GrandCompany(DataRow):
    _sign = b'GrandCompany|eJwrzivOA4HiPAAYEARc'
    sheet_name = 'GrandCompany'
    _display = 'text_sgl'
    text_sgl: str_t = RowData(0)
    text_sgg: int_t = RowData(1)
    text_plr: str_t = RowData(2)
    text_plg: int_t = RowData(3)
    text_vow: int_t = RowData(4)
    text_cnt: int_t = RowData(5)
    text_gen: int_t = RowData(6)
    text_def_: int_t = RowData(7)
    text_swt: str_t = RowData(8)
    monster_note: int_t = RowData(9)


class GrandCompanyRank(DataRow):
    _sign = b'GrandCompanyRank|eJzLy4MDABxnBLs='
    sheet_name = 'GrandCompanyRank'
    rank_category: int_t = RowData(0)
    linear_rank: int_t = RowData(1)
    cs_max: int_t = RowData(2)
    next_cs: int_t = RowData(3)
    icon_of_limsa: 'Icon' = IconRow(4)
    icon_of_gridania: 'Icon' = IconRow(5)
    icon_of_uldah: 'Icon' = IconRow(6)
    rank_up_quest_of_limsa: 'Quest' = RowForeign(7, 'Quest')
    rank_up_quest_of_gridania: 'Quest' = RowForeign(8, 'Quest')
    rank_up_quest_of_uldah: 'Quest' = RowForeign(9, 'Quest')
    rank_of_monster_note_condition: int_t = RowData(10)


class GroupPoseCharaStatus(DataRow):
    _sign = b'GroupPoseCharaStatus|eJzLAwAAbwBv'
    sheet_name = 'GroupPoseCharaStatus'
    status: int_t = RowData(0)


class GroupPoseCharacterShowPreset(DataRow):
    _sign = b'GroupPoseCharacterShowPreset|eJxLS0MGACnkBZU='
    sheet_name = 'GroupPoseCharacterShowPreset'
    self: bool_t = RowData(0)
    my_minion: bool_t = RowData(1)
    g_pose_pc: bool_t = RowData(2)
    g_pose_buddy: bool_t = RowData(3)
    g_pose_pet: bool_t = RowData(4)
    g_pose_minion: bool_t = RowData(5)
    g_pose_npc: bool_t = RowData(6)
    other_pc: bool_t = RowData(7)
    other_buddy: bool_t = RowData(8)
    other_pet: bool_t = RowData(9)
    other_minion: bool_t = RowData(10)
    other_npc: bool_t = RowData(11)
    enemy: bool_t = RowData(12)
    object: bool_t = RowData(13)


class GroupPoseFrame(DataRow):
    _sign = b'GroupPoseFrame|eJzLyyvOA4JiAA+jA3s='
    sheet_name = 'GroupPoseFrame'
    _display = 'name'
    frame_type: int_t = RowData(0)
    image: 'Icon' = IconRow(1)
    uld: str_t = RowData(2)
    vfx: int_t = RowData(3)
    fill_color: int_t = RowData(4)
    sort_id: int_t = RowData(5)
    festival: int_t = RowData(6)
    name: str_t = RowData(7)


class GroupPoseStamp(DataRow):
    _sign = b'GroupPoseStamp|eJzLywODtLS0YgAcJASo'
    sheet_name = 'GroupPoseStamp'
    _display = 'name'
    icon: 'Icon' = IconRow(0)
    type: int_t = RowData(1)
    category: 'GroupPoseStampCategory' = RowForeign(2, 'GroupPoseStampCategory')
    sort_id: int_t = RowData(3)
    condition_type: int_t = RowData(4)
    condition_data: int_t = RowData(5)
    festival: int_t = RowData(6)
    is_icon_shared_all_languages: bool_t = RowData(7)
    allow_horizontal_flip: bool_t = RowData(8)
    allow_vertical_flip: bool_t = RowData(9)
    name: str_t = RowData(10)


class GroupPoseStampCategory(DataRow):
    _sign = b'GroupPoseStampCategory|eJzLKwYAAVEA4g=='
    sheet_name = 'GroupPoseStampCategory'
    _display = 'name'
    sort_id: int_t = RowData(0)
    name: str_t = RowData(1)


class GroupPoseStampFontColor(DataRow):
    _sign = b'GroupPoseStampFontColor|eJzLy8srBgAEVQG+'
    sheet_name = 'GroupPoseStampFontColor'
    font_color: int_t = RowData(0)
    edge_color: int_t = RowData(1)
    sort_id: int_t = RowData(2)
    name: str_t = RowData(3)


class GuardianDeity(DataRow):
    _sign = b'GuardianDeity|eJwrLs4DAAKwAVU='
    sheet_name = 'GuardianDeity'
    _display = 'text_name'
    text_name: str_t = RowData(0)
    text_help: str_t = RowData(1)
    icon: 'Icon' = IconRow(2)


class Guide(DataRow):
    _sign = b'Guide|eJzLywMAAUwA3Q=='
    sheet_name = 'Guide'
    title: 'GuideTitle' = RowForeign(0, 'GuideTitle')
    page: 'GuidePage' = RowForeign(1, 'GuidePage')


class GuidePage(DataRow):
    _sign = b'GuidePage|eJzLywMAAUwA3Q=='
    sheet_name = 'GuidePage'
    element_type: int_t = RowData(0)
    element_content: int_t = RowData(1)


class GuidePageString(DataRow):
    _sign = b'GuidePageString|eJwrBgAAdAB0'
    sheet_name = 'GuidePageString'
    _display = 'text'
    text: str_t = RowData(0)


class GuideTitle(DataRow):
    _sign = b'GuideTitle|eJwrLgYAAVsA5w=='
    sheet_name = 'GuideTitle'
    _display = 'text_title'
    text_title: str_t = RowData(0)
    text_sub_title: str_t = RowData(1)


class GuildOrder(DataRow):
    _sign = b'GuildOrder|eJzLKwaCPDhISgIAQs0HSw=='
    sheet_name = 'GuildOrder'
    officer_base: 'ENpcResident' = RowForeign(0, 'ENpcResident')
    text_operation_text: str_t = RowData(1)
    text_order_text: List[str_t] = ListData(ir((2, 2, 1)), RowData)
    text_summary_text: str_t = RowData(4)
    reward_exp: List[int_t] = ListData(ir((5, 2, 1)), RowData)
    reward_gil: List[int_t] = ListData(ir((7, 2, 1)), RowData)
    reward_seal: List[int_t] = ListData(ir((9, 2, 1)), RowData)
    reward_item: List[int_t] = ListData(ir((11, 2, 1)), RowData)
    reward_stack: List[int_t] = ListData(ir((13, 2, 1)), RowData)
    reward_hq: List[bool_t] = ListData(ir((15, 2, 1)), RowData)


class GuildOrderGuide(DataRow):
    _sign = b'GuildOrderGuide|eJzLywMBAAkMApU='
    sheet_name = 'GuildOrderGuide'
    talk: List[int_t] = ListData(ir((0, 6, 1)), RowData)


class GuildOrderOfficer(DataRow):
    _sign = b'GuildOrderOfficer|eJzLywMBAAkMApU='
    sheet_name = 'GuildOrderOfficer'
    talk: List[int_t] = ListData(ir((0, 6, 1)), RowData)


class GuildleveAssignment(DataRow):
    _sign = b'GuildleveAssignment|eJwrzgOCNBDIAwAb/gSY'
    sheet_name = 'GuildleveAssignment'
    text: str_t = RowData(0)
    type: int_t = RowData(1)
    talk: 'GuildleveAssignmentTalk' = RowForeign(2, 'GuildleveAssignmentTalk')
    unlock_quest: int_t = RowData(3)
    decide_quest: int_t = RowData(4)
    have_maelstrom_leve: bool_t = RowData(5)
    have_twin_adder_leve: bool_t = RowData(6)
    have_immortal_leve: bool_t = RowData(7)
    have_multi_ticket_leve: bool_t = RowData(8)
    hide_battle_leve: bool_t = RowData(9)
    need_grand_company_rank: int_t = RowData(10)


class GuildleveAssignmentCategory(DataRow):
    _sign = b'GuildleveAssignmentCategory|eJzLy4MAAA+AA3E='
    sheet_name = 'GuildleveAssignmentCategory'
    filter: List[int_t] = ListData(ir((0, 8, 1)), RowData)


class GuildleveAssignmentTalk(DataRow):
    _sign = b'GuildleveAssignmentTalk|eJxLSwOCPFygGAoAOa8QVQ=='
    sheet_name = 'GuildleveAssignmentTalk'
    param_look_at: List[bool_t] = ListData(ir((0, 5, 1)), RowData)
    param_turn: List[int_t] = ListData(ir((5, 5, 1)), RowData)
    param_gesture: List[int_t] = ListData(ir((10, 5, 1)), RowData)
    param_lip_sync: List[int_t] = ListData(ir((15, 5, 1)), RowData)
    param_facial: List[int_t] = ListData(ir((20, 5, 1)), RowData)
    param_shape: List[int_t] = ListData(ir((25, 5, 1)), RowData)
    text: List[str_t] = ListData(ir((30, 8, 1)), RowData)


class GuildleveEvaluation(DataRow):
    _sign = b'GuildleveEvaluation|eJwrBgAAdAB0'
    sheet_name = 'GuildleveEvaluation'
    text: str_t = RowData(0)


class HWDAnnounce(DataRow):
    _sign = b'HWDAnnounce|eJwrzsvLAwAEZAG+'
    sheet_name = 'HWDAnnounce'
    text: str_t = RowData(0)
    announcer: 'ENpcResident' = RowForeign(1, 'ENpcResident')
    delay_time: int_t = RowData(2)
    show_time: int_t = RowData(3)


class HWDCrafterSupply(DataRow):
    _sign = b'HWDCrafterSupply|eJzLyxsFlAEAT2WKXQ=='
    sheet_name = 'HWDCrafterSupply'
    duty_item: List[int_t] = ListData(ir((0, 23, 1)), RowData)
    duty_lv: List[int_t] = ListData(ir((23, 23, 1)), RowData)
    duty_max_level_for_getting_stamp: List[int_t] = ListData(ir((46, 23, 1)), RowData)
    duty_stars: List[int_t] = ListData(ir((69, 23, 1)), RowData)
    duty_refine: List[List[int_t]] = ListData(ir(((92, 3, 23), 23, 1)), ListData, RowData)
    duty_reward: List[List[int_t]] = ListData(ir(((161, 3, 23), 23, 1)), ListData, RowData)
    duty_reward_old: List[List[int_t]] = ListData(ir(((230, 3, 23), 23, 1)), ListData, RowData)
    duty_term: List[int_t] = ListData(ir((299, 23, 1)), RowData)


class HWDCrafterSupplyReward(DataRow):
    _sign = b'HWDCrafterSupplyReward|eJzLy8sDAAKXAUs='
    sheet_name = 'HWDCrafterSupplyReward'
    currency: int_t = RowData(0)
    exp: int_t = RowData(1)
    ranking_point: int_t = RowData(2)


class HWDCrafterSupplyTerm(DataRow):
    _sign = b'HWDCrafterSupplyTerm|eJwrBgAAdAB0'
    sheet_name = 'HWDCrafterSupplyTerm'
    _display = 'text'
    text: str_t = RowData(0)


class HWDDevLayerControl(DataRow):
    _sign = b'HWDDevLayerControl|eJzLywMAAUwA3Q=='
    sheet_name = 'HWDDevLayerControl'
    phase: int_t = RowData(0)
    festival_phase: int_t = RowData(1)


class HWDDevLevelUI(DataRow):
    _sign = b'HWDDevLevelUI|eJzLywMAAUwA3Q=='
    sheet_name = 'HWDDevLevelUI'
    info_board_rank: int_t = RowData(0)
    info_board_topix: int_t = RowData(1)


class HWDDevLevelWebText(DataRow):
    _sign = b'HWDDevLevelWebText|eJwrLgYAAVsA5w=='
    sheet_name = 'HWDDevLevelWebText'
    text: str_t = RowData(0)
    info_text: str_t = RowData(1)


class HWDDevLively(DataRow):
    _sign = b'HWDDevLively|eJzLy8sDAAKXAUs='
    sheet_name = 'HWDDevLively'
    _display = 'e_npc_id'
    e_npc_id: 'ENpcBase' = RowForeign(0, 'ENpcBase')
    idle_timeline: int_t = RowData(1)
    behavior_pack_id: int_t = RowData(2)


class HWDDevProgress(DataRow):
    _sign = b'HWDDevProgress|eJxLAwAAZwBn'
    sheet_name = 'HWDDevProgress'
    _display = 'can_go_next'
    can_go_next: bool_t = RowData(0)


class HWDGathereInspectTerm(DataRow):
    _sign = b'HWDGathereInspectTerm|eJwrBgAAdAB0'
    sheet_name = 'HWDGathereInspectTerm'
    _display = 'text'
    text: str_t = RowData(0)


class HWDGathererInspection(DataRow):
    _sign = b'HWDGathererInspection|eJzLyxsFo4AIAAAtLu2f'
    sheet_name = 'HWDGathererInspection'
    duty_remove_gathering_item: List[int_t] = ListData(ir((0, 79, 1)), RowData)
    duty_remove_fishing_item: List[int_t] = ListData(ir((79, 79, 1)), RowData)
    duty_unit: List[int_t] = ListData(ir((158, 79, 1)), RowData)
    duty_reward_item: List[int_t] = ListData(ir((237, 79, 1)), RowData)
    duty_reward_others: List[int_t] = ListData(ir((316, 79, 1)), RowData)
    duty_reward_others_old: List[int_t] = ListData(ir((395, 79, 1)), RowData)
    duty_term: List[int_t] = ListData(ir((474, 79, 1)), RowData)


class HWDGathererInspectionReward(DataRow):
    _sign = b'HWDGathererInspectionReward|eJzLywMAAUwA3Q=='
    sheet_name = 'HWDGathererInspectionReward'
    _display = 'currency'
    currency: int_t = RowData(0)
    ranking_point: int_t = RowData(1)


class HWDInfoBoardArticle(DataRow):
    _sign = b'HWDInfoBoardArticle|eJzLy8tLKwYABmwCJA=='
    sheet_name = 'HWDInfoBoardArticle'
    _display = 'title'
    type: 'HWDInfoBoardArticleType' = RowForeign(0, 'HWDInfoBoardArticleType')
    new: int_t = RowData(1)
    number: int_t = RowData(2)
    is_info_progress: bool_t = RowData(3)
    title: str_t = RowData(4)


class HWDInfoBoardArticleTransient(DataRow):
    _sign = b'HWDInfoBoardArticleTransient|eJzLKy4GAAKmAVU='
    sheet_name = 'HWDInfoBoardArticleTransient'
    _display = 'title_text_body'
    icon: 'Icon' = IconRow(0)
    title_text_body: str_t = RowData(1)
    title_name: str_t = RowData(2)


class HWDInfoBoardArticleType(DataRow):
    _sign = b'HWDInfoBoardArticleType|eJwrBgAAdAB0'
    sheet_name = 'HWDInfoBoardArticleType'
    _display = 'name'
    name: str_t = RowData(0)


class HWDInfoBoardBackNumber(DataRow):
    _sign = b'HWDInfoBoardBackNumber|eJzLyysGAAKcAVA='
    sheet_name = 'HWDInfoBoardBackNumber'
    begin: int_t = RowData(0)
    end: int_t = RowData(1)
    title: str_t = RowData(2)


class HWDLevelChangeDeception(DataRow):
    _sign = b'HWDLevelChangeDeception|eJzLAwAAbwBv'
    sheet_name = 'HWDLevelChangeDeception'
    _display = 'screen_image'
    screen_image: 'ScreenImage' = RowForeign(0, 'ScreenImage')


class HWDSharedGroup(DataRow):
    _sign = b'HWDSharedGroup|eJzLywMAAUwA3Q=='
    sheet_name = 'HWDSharedGroup'
    layout_id: int_t = RowData(0)
    control: 'HWDSharedGroupControlParam' = RowForeign(1, 'HWDSharedGroupControlParam')


class HWDSharedGroupControlParam(DataRow):
    _sign = b'HWDSharedGroupControlParam|eJzLywMAAUwA3Q=='
    sheet_name = 'HWDSharedGroupControlParam'
    development_level: int_t = RowData(0)
    timeline: int_t = RowData(1)


class HairMakeType(DataRow):
    _sign = b'HairMakeType|eJzLyxsFo2AUjALqAgDv0t3g'
    sheet_name = 'HairMakeType'
    race: 'Race' = RowForeign(0, 'Race')
    tribe: 'Tribe' = RowForeign(1, 'Tribe')
    gender: int_t = RowData(2)
    looks_menu: List[int_t] = ListData(ir((3, 9, 1)), RowData)
    looks_init_val: List[int_t] = ListData(ir((12, 9, 1)), RowData)
    looks_sub_menu_type: List[int_t] = ListData(ir((21, 9, 1)), RowData)
    looks_sub_menu_num: List[int_t] = ListData(ir((30, 9, 1)), RowData)
    looks_look_at: List[int_t] = ListData(ir((39, 9, 1)), RowData)
    looks_sub_menu_mask: List[int_t] = ListData(ir((48, 9, 1)), RowData)
    looks_customize: List[int_t] = ListData(ir((57, 9, 1)), RowData)
    looks_sub_menu_param: List[List[int_t]] = ListData(ir(((66, 100, 9), 9, 1)), ListData, RowData)
    looks_sub_menu_graphic: List[List[int_t]] = ListData(ir(((966, 10, 9), 9, 1)), ListData, RowData)
    face_option_option: List[List[int_t]] = ListData(ir(((1056, 7, 8), 8, 1)), ListData, RowData)


class HouseRetainerPose(DataRow):
    _sign = b'HouseRetainerPose|eJzLAwAAbwBv'
    sheet_name = 'HouseRetainerPose'
    _display = 'timeline'
    timeline: 'ActionTimeline' = RowForeign(0, 'ActionTimeline')


class HousingAethernet(DataRow):
    _sign = b'HousingAethernet|eJzLy8vLAwAEUAG5'
    sheet_name = 'HousingAethernet'
    pop_range: 'Level' = RowForeign(0, 'Level')
    territory_type: 'TerritoryType' = RowForeign(1, 'TerritoryType')
    transfer_name: 'PlaceName' = RowForeign(2, 'PlaceName')
    sort_key: int_t = RowData(3)


class HousingAppeal(DataRow):
    _sign = b'HousingAppeal|eJwrzssDAAKmAVA='
    sheet_name = 'HousingAppeal'
    _display = 'text'
    text: str_t = RowData(0)
    icon: 'Icon' = IconRow(1)
    sort: int_t = RowData(2)


class HousingEmploymentNpcList(DataRow):
    _sign = b'HousingEmploymentNpcList|eJzLy8sDAAKXAUs='
    sheet_name = 'HousingEmploymentNpcList'
    race_choices: 'HousingEmploymentNpcRace' = RowForeign(0, 'HousingEmploymentNpcRace')
    npc_id: List[int_t] = ListData(ir((1, 2, 1)), RowData)


class HousingEmploymentNpcRace(DataRow):
    _sign = b'HousingEmploymentNpcRace|eJwrBgAAdAB0'
    sheet_name = 'HousingEmploymentNpcRace'
    _display = 'text'
    text: str_t = RowData(0)


class HousingExterior(DataRow):
    _sign = b'HousingExterior|eJzLy8vLKwYABnwCLA=='
    sheet_name = 'HousingExterior'
    id: int_t = RowData(0)
    category: int_t = RowData(1)
    region: 'PlaceName' = RowForeign(2, 'PlaceName')
    size: int_t = RowData(3)
    path: str_t = RowData(4)


class HousingFurniture(DataRow):
    _sign = b'HousingFurniture|eJzLy4OAtDQwAQAzHwZT'
    sheet_name = 'HousingFurniture'
    _display = 'item'
    id: int_t = RowData(0)
    category: int_t = RowData(1)
    use_type: int_t = RowData(2)
    param: int_t = RowData(3)
    layout_limit: int_t = RowData(4)
    pile_limit: int_t = RowData(5)
    event_handler: 'CustomTalk' = RowForeign(6, 'CustomTalk')
    item: 'Item' = RowForeign(7, 'Item')
    disposable: bool_t = RowData(8)
    has_crest: 'HousingPlacement' = RowForeign(9, 'HousingPlacement')
    place_text: int_t = RowData(10)
    unplace_text: int_t = RowData(11)
    unplace_lumber_text: int_t = RowData(12)
    is_sitting_access: bool_t = RowData(13)
    is_anyone_access: bool_t = RowData(14)


class HousingInterior(DataRow):
    _sign = b'HousingInterior|eJzLy8srBgAEVQG+'
    sheet_name = 'HousingInterior'
    id: int_t = RowData(0)
    category: int_t = RowData(1)
    material: int_t = RowData(2)
    path: str_t = RowData(3)


class HousingLandSet(DataRow):
    _sign = b'HousingLandSet|eJzLyxsFxAMA0SCBxQ=='
    sheet_name = 'HousingLandSet'
    lands_size: List[int_t] = ListData(ir((0, 60, 1)), RowData)
    lands_land_range: List[int_t] = ListData(ir((60, 60, 1)), RowData)
    lands_signboard_e_obj: List[int_t] = ListData(ir((120, 60, 1)), RowData)
    lands_exit_pop_range: List[int_t] = ListData(ir((180, 60, 1)), RowData)
    lands_init_price: List[int_t] = ListData(ir((240, 60, 1)), RowData)
    mansion_map_range: List[int_t] = ListData(ir((300, 2, 1)), RowData)


class HousingMapMarkerInfo(DataRow):
    _sign = b'HousingMapMarkerInfo|eJzLywMCAAZ3Aic='
    sheet_name = 'HousingMapMarkerInfo'
    trans_x: float_t = RowData(0)
    trans_y: float_t = RowData(1)
    trans_z: float_t = RowData(2)
    range_on_map: float_t = RowData(3)
    map: 'Map' = RowForeign(4, 'Map')


class HousingMateAuthority(DataRow):
    _sign = b'HousingMateAuthority|eJwrBgAAdAB0'
    sheet_name = 'HousingMateAuthority'
    text: str_t = RowData(0)


class HousingMerchantPose(DataRow):
    _sign = b'HousingMerchantPose|eJzLKwYAAVEA4g=='
    sheet_name = 'HousingMerchantPose'
    _display = 'text'
    timeline: 'ActionTimeline' = RowForeign(0, 'ActionTimeline')
    text: str_t = RowData(1)


class HousingPileLimit(DataRow):
    _sign = b'HousingPileLimit|eJzLy8tLAgEADswDNQ=='
    sheet_name = 'HousingPileLimit'
    width: int_t = RowData(0)
    depth: int_t = RowData(1)
    height: int_t = RowData(2)
    object: List[bool_t] = ListData(ir((3, 5, 1)), RowData)


class HousingPlacement(DataRow):
    _sign = b'HousingPlacement|eJwrBgAAdAB0'
    sheet_name = 'HousingPlacement'
    _display = 'text'
    text: str_t = RowData(0)


class HousingPreset(DataRow):
    _sign = b'HousingPreset|eJwrzivOwwYAgeYKWw=='
    sheet_name = 'HousingPreset'
    name_sgl: str_t = RowData(0)
    name_sgg: int_t = RowData(1)
    name_plr: str_t = RowData(2)
    name_plg: int_t = RowData(3)
    name_vow: int_t = RowData(4)
    name_cnt: int_t = RowData(5)
    name_gen: int_t = RowData(6)
    name_def_: int_t = RowData(7)
    region: 'PlaceName' = RowForeign(8, 'PlaceName')
    size: int_t = RowData(9)
    roof: 'Item' = RowForeign(10, 'Item')
    wall: 'Item' = RowForeign(11, 'Item')
    window: 'Item' = RowForeign(12, 'Item')
    door: 'Item' = RowForeign(13, 'Item')
    interior: 'List[Item]' = ListData(ir((14, 10, 1)), RowForeign, 'Item')


class HousingTrainingDoll(DataRow):
    _sign = b'HousingTrainingDoll|eJzLAwAAbwBv'
    sheet_name = 'HousingTrainingDoll'
    b_npc_base: int_t = RowData(0)


class HousingUnitedExterior(DataRow):
    _sign = b'HousingUnitedExterior|eJzLy4MCABNfA98='
    sheet_name = 'HousingUnitedExterior'
    size: int_t = RowData(0)
    part: List[int_t] = ListData(ir((1, 8, 1)), RowData)


class HousingUnplacement(DataRow):
    _sign = b'HousingUnplacement|eJwrBgAAdAB0'
    sheet_name = 'HousingUnplacement'
    text: str_t = RowData(0)


class HousingYardObject(DataRow):
    _sign = b'HousingYardObject|eJzLywODtLQ0MAkAMt8GSw=='
    sheet_name = 'HousingYardObject'
    _display = 'item'
    id: int_t = RowData(0)
    category: int_t = RowData(1)
    use_type: int_t = RowData(2)
    param: int_t = RowData(3)
    layout_limit: int_t = RowData(4)
    event_handler: 'CustomTalk' = RowForeign(5, 'CustomTalk')
    item: 'Item' = RowForeign(6, 'Item')
    disposable: bool_t = RowData(7)
    is_quest_used: bool_t = RowData(8)
    is_auto_lumber: bool_t = RowData(9)
    place_text: int_t = RowData(10)
    unplace_text: int_t = RowData(11)
    unplace_lumber_text: int_t = RowData(12)
    is_anyone_access: bool_t = RowData(13)


class HousingYardObject(DataRow):
    _sign = b'HousingYardObject|eJzLywODtLQ0EAkALJQF5Q=='
    sheet_name = 'HousingYardObject'
    _display = 'item'
    id: int_t = RowData(0)
    category: int_t = RowData(1)
    use_type: int_t = RowData(2)
    param: int_t = RowData(3)
    layout_limit: int_t = RowData(4)
    event_handler: 'CustomTalk' = RowForeign(5, 'CustomTalk')
    item: 'Item' = RowForeign(6, 'Item')
    disposable: bool_t = RowData(7)
    is_quest_used: bool_t = RowData(8)
    is_auto_lumber: bool_t = RowData(9)
    place_text: int_t = RowData(10)
    unplace_text: int_t = RowData(11)
    unplace_lumber_text: int_t = RowData(12)
    is_anyone_access: bool_t = RowData(13)


class HowTo(DataRow):
    _sign = b'HowTo|eJwrTstDAgAtCgYC'
    sheet_name = 'HowTo'
    _display = 'text'
    text: str_t = RowData(0)
    announce: bool_t = RowData(1)
    page: List[int_t] = ListData(ir((2, 5, 1)), RowData)
    page_pad: List[int_t] = ListData(ir((7, 5, 1)), RowData)
    category: 'HowToCategory' = RowForeign(12, 'HowToCategory')
    sort_id: int_t = RowData(13)


class HowToCategory(DataRow):
    _sign = b'HowToCategory|eJwrBgAAdAB0'
    sheet_name = 'HowToCategory'
    _display = 'text'
    text: str_t = RowData(0)


class HowToPage(DataRow):
    _sign = b'HowToPage|eJzLy8vLKy4uBgAMLQMS'
    sheet_name = 'HowToPage'
    _display = 'icon'
    type: int_t = RowData(0)
    icon_kind: int_t = RowData(1)
    icon: 'Icon' = IconRow(2)
    text_kind: int_t = RowData(3)
    text: List[str_t] = ListData(ir((4, 3, 1)), RowData)


class Hud(DataRow):
    _sign = b'Hud|eJwrLi4GAAK1AVo='
    sheet_name = 'Hud'
    text_0: str_t = RowData(0)
    text_1: str_t = RowData(1)
    text_2: str_t = RowData(2)


class HudTransient(DataRow):
    _sign = b'HudTransient|eJzLy8vLAwAEUAG5'
    sheet_name = 'HudTransient'
    category: int_t = RowData(0)
    setting_type: int_t = RowData(1)
    size: int_t = RowData(2)
    simple_size: int_t = RowData(3)


class HugeCraftworksNpc(DataRow):
    _sign = b'HugeCraftworksNpc|eJzLy0MGaWCQRzRIAgNcIsUAPaUnPA=='
    sheet_name = 'HugeCraftworksNpc'
    _display = 'leader'
    leader: 'ENpcResident' = RowForeign(0, 'ENpcResident')
    target_class_job_category: 'ClassJobCategory' = RowForeign(1, 'ClassJobCategory')
    supply_delivery_item: List[int_t] = ListData(ir((2, 6, 1)), RowData)
    supply_delivery_item_count: List[int_t] = ListData(ir((8, 6, 1)), RowData)
    supply_is_hq: List[bool_t] = ListData(ir((14, 6, 1)), RowData)
    supply_reward_currency: List[int_t] = ListData(ir((20, 6, 1)), RowData)
    supply_reward_currency_count: List[int_t] = ListData(ir((26, 6, 1)), RowData)
    supply_reward_currency_count_hq_rate: List[int_t] = ListData(ir((32, 6, 1)), RowData)
    supply_reward_gil: List[int_t] = ListData(ir((38, 6, 1)), RowData)
    supply_reward_gil_hq_rate: List[int_t] = ListData(ir((44, 6, 1)), RowData)
    supply_reward_exp_rate: List[int_t] = ListData(ir((50, 6, 1)), RowData)
    rank_up_reward_rank_up_reward_item: List[List[int_t]] = ListData(ir(((56, 2, 18), 6, 1)), ListData, RowData)
    rank_up_reward_is_hq: List[List[bool_t]] = ListData(ir(((62, 2, 18), 6, 1)), ListData, RowData)
    rank_up_reward_rank_up_reward_item_count: List[List[int_t]] = ListData(ir(((68, 2, 18), 6, 1)), ListData, RowData)
    text: str_t = RowData(92)


class HugeCraftworksRank(DataRow):
    _sign = b'HugeCraftworksRank|eJzLy8sDAAKXAUs='
    sheet_name = 'HugeCraftworksRank'
    need_level: int_t = RowData(0)
    reward_exp: int_t = RowData(1)
    reward_hq_exp_rate: int_t = RowData(2)


class IKDContentBonus(DataRow):
    _sign = b'IKDContentBonus|eJwrLs7LywMABqQCMQ=='
    sheet_name = 'IKDContentBonus'
    _display = 'text_name'
    text_name: str_t = RowData(0)
    text_help: str_t = RowData(1)
    rate: int_t = RowData(2)
    icon: 'Icon' = IconRow(3)
    sort_key: int_t = RowData(4)


class IKDFishParam(DataRow):
    _sign = b'IKDFishParam|eJzLy8sDAAKXAUs='
    sheet_name = 'IKDFishParam'
    _display = 'fish_parameter_id'
    fish_parameter_id: 'FishParameter' = RowForeign(0, 'FishParameter')
    bonus: 'IKDContentBonus' = RowForeign(1, 'IKDContentBonus')
    player_bonus: int_t = RowData(2)


class IKDPlayerMissionCondition(DataRow):
    _sign = b'IKDPlayerMissionCondition|eJzLKwYAAVEA4g=='
    sheet_name = 'IKDPlayerMissionCondition'
    fish_num: int_t = RowData(0)
    text: str_t = RowData(1)


class IKDRoute(DataRow):
    _sign = b'IKDRoute|eJzLy4ODYgAhlQUu'
    sheet_name = 'IKDRoute'
    _display = 'text'
    spot: List[int_t] = ListData(ir((0, 3, 2)), RowData)
    time: List[int_t] = ListData(ir((1, 3, 2)), RowData)
    map_icon: List[Icon] = ListData(ir((6, 2, 1)), IconRow)
    map_condition: int_t = RowData(8)
    content_finder_condition: 'ContentFinderCondition' = RowForeign(9, 'ContentFinderCondition')
    route_open_quest: int_t = RowData(10)
    text: str_t = RowData(11)


class IKDRoute(DataRow):
    _sign = b'IKDRoute|eJzLy4OAYgATZAPk'
    sheet_name = 'IKDRoute'
    _display = 'text'
    spot: List[int_t] = ListData(ir((0, 3, 2)), RowData)
    time: List[int_t] = ListData(ir((1, 3, 2)), RowData)
    map_icon: 'Icon' = IconRow(6)
    content_finder_condition: 'TerritoryType' = RowForeign(7, 'TerritoryType')
    text: str_t = RowData(8)


class IKDRouteTable(DataRow):
    _sign = b'IKDRouteTable|eJzLywMAAUwA3Q=='
    sheet_name = 'IKDRouteTable'
    _display = 'route'
    route: 'List[IKDRoute]' = ListData(ir((0, 2, 1)), RowForeign, 'IKDRoute')


class IKDRouteTable(DataRow):
    _sign = b'IKDRouteTable|eJzLAwAAbwBv'
    sheet_name = 'IKDRouteTable'
    _display = 'route'
    route: 'IKDRoute' = RowForeign(0, 'IKDRoute')


class IKDSpot(DataRow):
    _sign = b'IKDSpot|eJzLy8sDAAKXAUs='
    sheet_name = 'IKDSpot'
    _display = 'fishing_spot'
    fishing_spot: 'FishingSpot' = RowForeign(0, 'FishingSpot')
    fever_fishing_spot: 'FishingSpot' = RowForeign(1, 'FishingSpot')
    place_name: 'PlaceName' = RowForeign(2, 'PlaceName')


class IKDTimeDefine(DataRow):
    _sign = b'IKDTimeDefine|eJzLAwAAbwBv'
    sheet_name = 'IKDTimeDefine'
    icon: int_t = RowData(0)


class IconLanguage(DataRow):
    _sign = b'IconLanguage|eJxLSoIBABUYA9U='
    sheet_name = 'IconLanguage'
    field_0: bool_t = RowData(0)
    field_1: bool_t = RowData(1)
    field_2: bool_t = RowData(2)
    field_3: bool_t = RowData(3)
    field_4: bool_t = RowData(4)
    field_5: bool_t = RowData(5)
    field_6: bool_t = RowData(6)
    field_7: bool_t = RowData(7)
    field_8: bool_t = RowData(8)
    field_9: bool_t = RowData(9)


class InclusionShop(DataRow):
    _sign = b'InclusionShop|eJzLyyvOwwsA8coONA=='
    sheet_name = 'InclusionShop'
    requirement: int_t = RowData(0)
    welcom: int_t = RowData(1)
    name: str_t = RowData(2)
    contents_shop_category: List[int_t] = ListData(ir((3, 30, 1)), RowData)


class InclusionShopCategory(DataRow):
    _sign = b'InclusionShopCategory|eJwrzssDAAKmAVA='
    sheet_name = 'InclusionShopCategory'
    _display = 'name'
    name: str_t = RowData(0)
    class_job_category: 'ClassJobCategory' = RowForeign(1, 'ClassJobCategory')
    series: 'InclusionShopSeries' = RowForeign(2, 'InclusionShopSeries')


class InclusionShopSeries(DataRow):
    _sign = b'InclusionShopSeries|eJzLAwAAbwBv'
    sheet_name = 'InclusionShopSeries'
    _display = 'shop'
    shop: 'SpecialShop' = RowForeign(0, 'SpecialShop')


class InclusionShopWelcom(DataRow):
    _sign = b'InclusionShopWelcom|eJzLy8sDAAKXAUs='
    sheet_name = 'InclusionShopWelcom'
    design: int_t = RowData(0)
    text_title: int_t = RowData(1)
    text_body: int_t = RowData(2)


class InclusionShopWelcomText(DataRow):
    _sign = b'InclusionShopWelcomText|eJwrBgAAdAB0'
    sheet_name = 'InclusionShopWelcomText'
    text: str_t = RowData(0)


class IndividualWeather(DataRow):
    _sign = b'IndividualWeather|eJzLy8MNAK6QDAk='
    sheet_name = 'IndividualWeather'
    param_weather: List[int_t] = ListData(ir((0, 7, 1)), RowData)
    param_condition_type: List[int_t] = ListData(ir((7, 7, 1)), RowData)
    param_param: List[List[int_t]] = ListData(ir(((14, 2, 7), 7, 1)), ListData, RowData)


class InstanceContent(DataRow):
    _sign = b'InstanceContent|eJzLy8tLywMDKEUESEOjAOvNHRE='
    sheet_name = 'InstanceContent'
    type: 'InstanceContentType' = RowForeign(0, 'InstanceContentType')
    reward_type: int_t = RowData(1)
    time: int_t = RowData(2)
    name: bool_t = RowData(3)
    music: 'BGM' = RowForeign(4, 'BGM')
    clear_music: 'BGM' = RowForeign(5, 'BGM')
    start_cutscene: 'Cutscene' = RowForeign(6, 'Cutscene')
    entrance_rect: int_t = RowData(7)
    content_finder_condition: int_t = RowData(8)
    colosseum: 'Colosseum' = RowForeign(9, 'Colosseum')
    disable_complete_text: bool_t = RowData(10)
    boss_message: 'List[InstanceContentTextData]' = ListData(ir((11, 2, 1)), RowForeign, 'InstanceContentTextData')
    boss_name: 'BNpcBase' = RowForeign(13, 'BNpcBase')
    content_text_start: 'InstanceContentTextData' = RowForeign(14, 'InstanceContentTextData')
    content_text_end: 'InstanceContentTextData' = RowForeign(15, 'InstanceContentTextData')
    sortkey: int_t = RowData(16)
    reward_beginner_bonus_gil: int_t = RowData(17)
    reward_beginner_bonus_exp: int_t = RowData(18)
    reward_beginner_bonus_a: int_t = RowData(19)
    reward_beginner_bonus_b: int_t = RowData(20)
    reward_clear_exp: int_t = RowData(21)
    reward_clear_bonus_exp: int_t = RowData(22)
    reward_clear_a: int_t = RowData(23)
    reward_clear_b: int_t = RowData(24)
    reward_clear_c: int_t = RowData(25)
    reward_middle_exp: List[int_t] = ListData(ir((26, 5, 1)), RowData)
    reward_middle_a: List[int_t] = ListData(ir((31, 5, 1)), RowData)
    reward_middle_b: List[int_t] = ListData(ir((36, 5, 1)), RowData)
    reward_middle_c: List[int_t] = ListData(ir((41, 5, 1)), RowData)
    reward_total_exp: int_t = RowData(46)
    reward_total_gil: int_t = RowData(47)
    reward_clear_item: 'InstanceContentRewardItem' = RowForeign(48, 'InstanceContentRewardItem')
    reward_random_bonus_rate: int_t = RowData(49)
    reward_index: int_t = RowData(50)
    instance_buff: 'InstanceContentBuff' = RowForeign(51, 'InstanceContentBuff')
    force_buff: bool_t = RowData(52)
    open_flag_index: 'InstanceContent' = RowForeign(53, 'InstanceContent')
    raid_progress: int_t = RowData(54)
    ui_category: int_t = RowData(55)
    qte: int_t = RowData(56)
    content_gauge: int_t = RowData(57)
    content_attribute_rect: int_t = RowData(58)
    link_dead_kill: bool_t = RowData(59)
    data_index: int_t = RowData(60)
    shared_group: int_t = RowData(61)
    todo: int_t = RowData(62)
    faith_content_buff: int_t = RowData(63)
    tourism_construct: int_t = RowData(64)
    common_content_flag: int_t = RowData(65)
    battle_shared_group_action_clip: bool_t = RowData(66)
    event_item: int_t = RowData(67)


class InstanceContentBuff(DataRow):
    _sign = b'InstanceContentBuff|eJzLywMAAUwA3Q=='
    sheet_name = 'InstanceContentBuff'
    param_base: int_t = RowData(0)
    param_add: int_t = RowData(1)


class InstanceContentCSBonus(DataRow):
    _sign = b'InstanceContentCSBonus|eJzLywMCAAZ3Aic='
    sheet_name = 'InstanceContentCSBonus'
    content_id: 'InstanceContent' = RowForeign(0, 'InstanceContent')
    item: 'Item' = RowForeign(1, 'Item')
    count: List[int_t] = ListData(ir((2, 3, 1)), RowData)


class InstanceContentGuide(DataRow):
    _sign = b'InstanceContentGuide|eJzLywMAAUwA3Q=='
    sheet_name = 'InstanceContentGuide'
    instance_content: 'InstanceContent' = RowForeign(0, 'InstanceContent')
    event_range: int_t = RowData(1)


class InstanceContentQICData(DataRow):
    _sign = b'InstanceContentQICData|eJzLSwMAAUQA1Q=='
    sheet_name = 'InstanceContentQICData'
    clear_wait: int_t = RowData(0)
    hide_remain_time_flag: bool_t = RowData(1)


class InstanceContentRewardItem(DataRow):
    _sign = b'InstanceContentRewardItem|eJzLywMAAUwA3Q=='
    sheet_name = 'InstanceContentRewardItem'
    obtained_flag: List[int_t] = ListData(ir((0, 2, 1)), RowData)


class InstanceContentTextData(DataRow):
    _sign = b'InstanceContentTextData|eJwrBgAAdAB0'
    sheet_name = 'InstanceContentTextData'
    _display = 'text'
    text: str_t = RowData(0)


class InstanceContentType(DataRow):
    _sign = b'InstanceContentType|eJxLy0vLSwMBABJnA6c='
    sheet_name = 'InstanceContentType'
    save_flag: bool_t = RowData(0)
    open_flag: int_t = RowData(1)
    dead_flag: bool_t = RowData(2)
    start_log: int_t = RowData(3)
    vote_kick: bool_t = RowData(4)
    vote_give_up: bool_t = RowData(5)
    mip: bool_t = RowData(6)
    content_portrait: bool_t = RowData(7)
    disable_portrait_open: bool_t = RowData(8)


class InstanceContentType(DataRow):
    _sign = b'InstanceContentType|eJxLy0vLSwMCAA7AA0E='
    sheet_name = 'InstanceContentType'
    save_flag: bool_t = RowData(0)
    open_flag: int_t = RowData(1)
    dead_flag: bool_t = RowData(2)
    start_log: int_t = RowData(3)
    vote_kick: bool_t = RowData(4)
    vote_give_up: bool_t = RowData(5)
    mip: bool_t = RowData(6)
    content_portrait: bool_t = RowData(7)


class Item(DataRow):
    _sign = b'Item|eJwrzivOA4FiCAUBaUAAJuH8PBIBUEcaAPwOJs8='
    sheet_name = 'Item'
    _display = 'text_ui_name'
    text_sgl: str_t = RowData(0)
    text_sgg: int_t = RowData(1)
    text_plr: str_t = RowData(2)
    text_plg: int_t = RowData(3)
    text_vow: int_t = RowData(4)
    text_cnt: int_t = RowData(5)
    text_gen: int_t = RowData(6)
    text_def_: int_t = RowData(7)
    text_help: str_t = RowData(8)
    text_ui_name: str_t = RowData(9)
    icon: 'Icon' = IconRow(10)
    level: 'ItemLevel' = RowForeign(11, 'ItemLevel')
    rarity: int_t = RowData(12)
    category: int_t = RowData(13)
    category_arg: int_t = RowData(14)
    ui_category: 'ItemUICategory' = RowForeign(15, 'ItemUICategory')
    search_category: 'ItemSearchCategory' = RowForeign(16, 'ItemSearchCategory')
    slot: 'EquipSlotCategory' = RowForeign(17, 'EquipSlotCategory')
    sort_category: 'ItemSortCategory' = RowForeign(18, 'ItemSortCategory')
    sort_id: int_t = RowData(19)
    stack_max: int_t = RowData(20)
    only_one: bool_t = RowData(21)
    disable_passed_others: bool_t = RowData(22)
    disable_abandon: bool_t = RowData(23)
    lot: bool_t = RowData(24)
    price: int_t = RowData(25)
    sell_price: int_t = RowData(26)
    hq: bool_t = RowData(27)
    stain: bool_t = RowData(28)
    crest: bool_t = RowData(29)
    action: 'ItemAction' = RowForeign(30, 'ItemAction')
    cast_time: int_t = RowData(31)
    recast_time: int_t = RowData(32)
    repair: 'ClassJob' = RowForeign(33, 'ClassJob')
    repair_item: 'ItemRepairResource' = RowForeign(34, 'ItemRepairResource')
    mirage_item: 'Item' = RowForeign(35, 'Item')
    desynthesis: int_t = RowData(36)
    masterpiece: bool_t = RowData(37)
    force_craft_masterpiece: bool_t = RowData(38)
    gatherer_reduction: int_t = RowData(39)
    equip_item_equip_level: int_t = RowData(40)
    equip_item_equip_pvp_rank: int_t = RowData(41)
    equip_item_cond_race: int_t = RowData(42)
    equip_item_cond_class_job: 'ClassJobCategory' = RowForeign(43, 'ClassJobCategory')
    equip_item_cond_grand_company: 'GrandCompany' = RowForeign(44, 'GrandCompany')
    equip_item_series: 'ItemSeries' = RowForeign(45, 'ItemSeries')
    equip_item_role: int_t = RowData(46)
    equip_item_model_id: int_t = RowData(47)
    equip_item_sub_model_id: int_t = RowData(48)
    equip_item_class_: 'ClassJob' = RowForeign(49, 'ClassJob')
    equip_item_attack_type: int_t = RowData(50)
    equip_item_damage: int_t = RowData(51)
    equip_item_magic_damage: int_t = RowData(52)
    equip_item_attack_interval: int_t = RowData(53)
    equip_item_attack_range: int_t = RowData(54)
    equip_item_shield_rate: int_t = RowData(55)
    equip_item_shield_block_rate: int_t = RowData(56)
    equip_item_defense: int_t = RowData(57)
    equip_item_magic_defense: int_t = RowData(58)
    equip_item_bonus_type: List[int_t] = ListData(ir((59, 6, 2)), RowData)
    equip_item_bonus_value: List[int_t] = ListData(ir((60, 6, 2)), RowData)
    equip_item_special_bonus: 'ItemSpecialBonus' = RowForeign(71, 'ItemSpecialBonus')
    equip_item_special_bonus_arg: int_t = RowData(72)
    equip_item_special_bonus_type: List[int_t] = ListData(ir((73, 6, 2)), RowData)
    equip_item_special_bonus_value: List[int_t] = ListData(ir((74, 6, 2)), RowData)
    equip_item_materialize_type: int_t = RowData(85)
    equip_item_materia_socket: int_t = RowData(86)
    equip_item_materia_prohibition: bool_t = RowData(87)
    equip_item_materia_effect_only_in_pvp: bool_t = RowData(88)
    equip_item_item_level_sync_type: int_t = RowData(89)
    equip_item_prism_convert: bool_t = RowData(90)


class ItemAction(DataRow):
    _sign = b'ItemAction|eJzLS0tLy8MEAHS3Ccs='
    sheet_name = 'ItemAction'
    cond_lv: int_t = RowData(0)
    cond_battle: bool_t = RowData(1)
    cond_pvp: bool_t = RowData(2)
    cond_pvp_only: bool_t = RowData(3)
    action: int_t = RowData(4)
    calcu0_arg: List[int_t] = ListData(ir((5, 3, 1)), RowData)
    calcu1_arg: List[int_t] = ListData(ir((8, 3, 1)), RowData)
    calcu2_arg: List[int_t] = ListData(ir((11, 3, 1)), RowData)
    hq_calcu0_arg: List[int_t] = ListData(ir((14, 3, 1)), RowData)
    hq_calcu1_arg: List[int_t] = ListData(ir((17, 3, 1)), RowData)
    hq_calcu2_arg: List[int_t] = ListData(ir((20, 3, 1)), RowData)


class ItemActionTelepo(DataRow):
    _sign = b'ItemActionTelepo|eJzLywMAAUwA3Q=='
    sheet_name = 'ItemActionTelepo'
    _display = 'use_cond_arg'
    use_cond_arg: int_t = RowData(0)
    error_log_message: 'LogMessage' = RowForeign(1, 'LogMessage')


class ItemBarterCheck(DataRow):
    _sign = b'ItemBarterCheck|eJzLy8sDAAKXAUs='
    sheet_name = 'ItemBarterCheck'
    item_barter_check_type: 'AddonTransient' = RowForeign(0, 'AddonTransient')
    message: int_t = RowData(1)
    sub_message: 'Addon' = RowForeign(2, 'Addon')


class ItemFood(DataRow):
    _sign = b'ItemFood|eJzLy0vKAwEkEgBQKwgH'
    sheet_name = 'ItemFood'
    exp: int_t = RowData(0)
    param: List[int_t] = ListData(ir((1, 3, 6)), RowData)
    rate: List[bool_t] = ListData(ir((2, 3, 6)), RowData)
    value: List[int_t] = ListData(ir((3, 3, 6)), RowData)
    limit: List[int_t] = ListData(ir((4, 3, 6)), RowData)
    value_hq: List[int_t] = ListData(ir((5, 3, 6)), RowData)
    limit_hq: List[int_t] = ListData(ir((6, 3, 6)), RowData)


class ItemLevel(DataRow):
    _sign = b'ItemLevel|eJzLy6MWAACo6B/N'
    sheet_name = 'ItemLevel'
    base_param: List[int_t] = ListData(ir((0, 74, 1)), RowData)


class ItemOnceHqMasterpiece(DataRow):
    _sign = b'ItemOnceHqMasterpiece|eJxLSwMAATQAzQ=='
    sheet_name = 'ItemOnceHqMasterpiece'
    hq: bool_t = RowData(0)
    masterpiece: bool_t = RowData(1)


class ItemRepairPrice(DataRow):
    _sign = b'ItemRepairPrice|eJzLAwAAbwBv'
    sheet_name = 'ItemRepairPrice'
    price: int_t = RowData(0)


class ItemRepairResource(DataRow):
    _sign = b'ItemRepairResource|eJzLAwAAbwBv'
    sheet_name = 'ItemRepairResource'
    item: 'Item' = RowForeign(0, 'Item')


class ItemRetainerLevelUp(DataRow):
    _sign = b'ItemRetainerLevelUp|eJzLywMAAUwA3Q=='
    sheet_name = 'ItemRetainerLevelUp'
    item: int_t = RowData(0)
    level: int_t = RowData(1)


class ItemSearchCategory(DataRow):
    _sign = b'ItemSearchCategory|eJwrzgOCNAAJIgKS'
    sheet_name = 'ItemSearchCategory'
    _display = 'text'
    text: str_t = RowData(0)
    icon: 'Icon' = IconRow(1)
    block: int_t = RowData(2)
    display_order: int_t = RowData(3)
    class_level: 'ClassJob' = RowForeign(4, 'ClassJob')
    is_enable_acquire: bool_t = RowData(5)


class ItemSeries(DataRow):
    _sign = b'ItemSeries|eJwrBgAAdAB0'
    sheet_name = 'ItemSeries'
    _display = 'text'
    text: str_t = RowData(0)


class ItemSortCategory(DataRow):
    _sign = b'ItemSortCategory|eJzLAwAAbwBv'
    sheet_name = 'ItemSortCategory'
    _display = 'sort_id'
    sort_id: int_t = RowData(0)


class ItemSpecialBonus(DataRow):
    _sign = b'ItemSpecialBonus|eJwrBgAAdAB0'
    sheet_name = 'ItemSpecialBonus'
    _display = 'text'
    text: str_t = RowData(0)


class ItemStainCondition(DataRow):
    _sign = b'ItemStainCondition|eJzLAwAAbwBv'
    sheet_name = 'ItemStainCondition'
    quest: int_t = RowData(0)


class ItemUICategory(DataRow):
    _sign = b'ItemUICategory|eJwrzsvLAwAEZAG+'
    sheet_name = 'ItemUICategory'
    _display = 'text'
    text: str_t = RowData(0)
    icon: 'Icon' = IconRow(1)
    priority: int_t = RowData(2)
    kind: int_t = RowData(3)


class JigsawScore(DataRow):
    _sign = b'JigsawScore|eJzLy8vLAwAEUAG5'
    sheet_name = 'JigsawScore'
    score: int_t = RowData(0)
    combo: int_t = RowData(1)
    bridge: int_t = RowData(2)
    stand: int_t = RowData(3)


class JigsawTimeBonus(DataRow):
    _sign = b'JigsawTimeBonus|eJzLy8MGAGzMCXU='
    sheet_name = 'JigsawTimeBonus'
    time: List[int_t] = ListData(ir((0, 11, 1)), RowData)
    bonus: List[int_t] = ListData(ir((11, 11, 1)), RowData)


class Jingle(DataRow):
    _sign = b'Jingle|eJwrBgAAdAB0'
    sheet_name = 'Jingle'
    _display = 'path'
    path: str_t = RowData(0)


class JobHudManual(DataRow):
    _sign = b'JobHudManual|eJzLywMBAAkMApU='
    sheet_name = 'JobHudManual'
    _display = 'condition_value'
    hud: int_t = RowData(0)
    condition_type: List[int_t] = ListData(ir((1, 2, 2)), RowData)
    condition_value: 'List[Action]' = ListData(ir((2, 2, 2)), RowForeign, 'Action')
    guide: 'Guide' = RowForeign(5, 'Guide')


class JobHudManualPriority(DataRow):
    _sign = b'JobHudManualPriority|eJzLywMCAAZ3Aic='
    sheet_name = 'JobHudManualPriority'
    manual: List[int_t] = ListData(ir((0, 5, 1)), RowData)


class JournalCategory(DataRow):
    _sign = b'JournalCategory|eJwrzgMCAAaQAiw='
    sheet_name = 'JournalCategory'
    _display = 'text'
    text: str_t = RowData(0)
    separate_type: int_t = RowData(1)
    data_type: int_t = RowData(2)
    section: 'JournalSection' = RowForeign(3, 'JournalSection')
    show_condition: int_t = RowData(4)


class JournalGenre(DataRow):
    _sign = b'JournalGenre|eJzLy0srBgAERQG2'
    sheet_name = 'JournalGenre'
    _display = 'text'
    icon: 'Icon' = IconRow(0)
    category: 'JournalCategory' = RowForeign(1, 'JournalCategory')
    ui_map_marker_height_enable: bool_t = RowData(2)
    text: str_t = RowData(3)


class JournalSection(DataRow):
    _sign = b'JournalSection|eJwrTksDAAKOAUA='
    sheet_name = 'JournalSection'
    _display = 'text'
    text: str_t = RowData(0)
    enable_journal: bool_t = RowData(1)
    enable_replay: bool_t = RowData(2)


class Knockback(DataRow):
    _sign = b'Knockback|eJzLy0vLy8tLAwAL3wLz'
    sheet_name = 'Knockback'
    distance: int_t = RowData(0)
    speed: int_t = RowData(1)
    motion: bool_t = RowData(2)
    near_distance: int_t = RowData(3)
    direction: int_t = RowData(4)
    direction_arg: int_t = RowData(5)
    cancel_move: bool_t = RowData(6)


class LFGExtensionContent(DataRow):
    _sign = b'LFGExtensionContent|eJzLy8sDAAKXAUs='
    sheet_name = 'LFGExtensionContent'
    category: int_t = RowData(0)
    content_finder_condition: int_t = RowData(1)
    sort: int_t = RowData(2)


class LegacyQuest(DataRow):
    _sign = b'LegacyQuest|eJzLKy7OywMABpoCMQ=='
    sheet_name = 'LegacyQuest'
    legacy_quest_id: int_t = RowData(0)
    text_name: str_t = RowData(1)
    text_journal: str_t = RowData(2)
    sort_key: int_t = RowData(3)
    genre: int_t = RowData(4)


class Leve(DataRow):
    _sign = b'Leve|eJwrLs5DAmkoFIQFAAAKDo8='
    sheet_name = 'Leve'
    _display = 'text_name'
    text_name: str_t = RowData(0)
    text_objective: str_t = RowData(1)
    client: 'LeveClient' = RowForeign(2, 'LeveClient')
    guildleve_assignment_type: 'LeveAssignmentType' = RowForeign(3, 'LeveAssignmentType')
    assignment_type: int_t = RowData(4)
    town: 'Town' = RowForeign(5, 'Town')
    class_level: int_t = RowData(6)
    time_limit: int_t = RowData(7)
    ticket_num: int_t = RowData(8)
    evaluation: int_t = RowData(9)
    location: 'PlaceName' = RowForeign(10, 'PlaceName')
    finish_location: 'PlaceName' = RowForeign(11, 'PlaceName')
    fishing_spot_data: int_t = RowData(12)
    spearfishing_spot_data: int_t = RowData(13)
    special: bool_t = RowData(14)
    class_job: 'ClassJobCategory' = RowForeign(15, 'ClassJobCategory')
    genre: 'JournalGenre' = RowForeign(16, 'JournalGenre')
    region: int_t = RowData(17)
    area: 'PlaceName' = RowForeign(18, 'PlaceName')
    plate_region_icon: 'Icon' = IconRow(19)
    game_data: int_t = RowData(20)
    difficulty: bool_t = RowData(21)
    difficulty_max: int_t = RowData(22)
    reward_exp_rate: float_t = RowData(23)
    reward_static_exp: int_t = RowData(24)
    reward_gil: int_t = RowData(25)
    reward_item: 'LeveRewardItem' = RowForeign(26, 'LeveRewardItem')
    plate_design_vfx: 'LeveVfx' = RowForeign(27, 'LeveVfx')
    plate_frame_vfx: 'LeveVfx' = RowForeign(28, 'LeveVfx')
    todo_listener: 'Level' = RowForeign(29, 'Level')
    header: 'Icon' = IconRow(30)
    cancellable: bool_t = RowData(31)
    start_marker: 'Level' = RowForeign(32, 'Level')
    bgm: 'BGM' = RowForeign(33, 'BGM')


class LeveAssignmentType(DataRow):
    _sign = b'LeveAssignmentType|eJxLyysGAAKEAUg='
    sheet_name = 'LeveAssignmentType'
    _display = 'text'
    faction: bool_t = RowData(0)
    icon: 'Icon' = IconRow(1)
    text: str_t = RowData(2)


class LeveClient(DataRow):
    _sign = b'LeveClient|eJwrBgAAdAB0'
    sheet_name = 'LeveClient'
    _display = 'text'
    text: str_t = RowData(0)


class LeveRewardItem(DataRow):
    _sign = b'LeveRewardItem|eJzLy0MFADqABuE='
    sheet_name = 'LeveRewardItem'
    item_group: List[int_t] = ListData(ir((0, 8, 2)), RowData)
    item_group_rate: List[int_t] = ListData(ir((1, 8, 2)), RowData)


class LeveRewardItemGroup(DataRow):
    _sign = b'LeveRewardItemGroup|eJzLy0vKw4EAnQsLLw=='
    sheet_name = 'LeveRewardItemGroup'
    item: List[int_t] = ListData(ir((0, 9, 3)), RowData)
    stack: List[int_t] = ListData(ir((1, 9, 3)), RowData)
    hq: List[bool_t] = ListData(ir((2, 9, 3)), RowData)


class LeveString(DataRow):
    _sign = b'LeveString|eJwrBgAAdAB0'
    sheet_name = 'LeveString'
    _display = 'text'
    text: str_t = RowData(0)


class LeveSystemDefine(DataRow):
    _sign = b'LeveSystemDefine|eJwrzgMAAVYA4g=='
    sheet_name = 'LeveSystemDefine'
    define_name: str_t = RowData(0)
    define_value: int_t = RowData(1)


class LeveVfx(DataRow):
    _sign = b'LeveVfx|eJwrzgMAAVYA4g=='
    sheet_name = 'LeveVfx'
    _display = 'icon'
    path: str_t = RowData(0)
    icon: 'Icon' = IconRow(1)


class Level(DataRow):
    _sign = b'Level|eJzLy4MBABesBE0='
    sheet_name = 'Level'
    trans_x: float_t = RowData(0)
    trans_y: float_t = RowData(1)
    trans_z: float_t = RowData(2)
    rot_y: float_t = RowData(3)
    range_on_map: float_t = RowData(4)
    e_asset_type: int_t = RowData(5)
    base_id: int_t = RowData(6)
    map: 'Map' = RowForeign(7, 'Map')
    event_handler: int_t = RowData(8)
    territory_type: 'TerritoryType' = RowForeign(9, 'TerritoryType')


class LinkRace(DataRow):
    _sign = b'LinkRace|eJxLSkpKAgAD2AGJ'
    sheet_name = 'LinkRace'
    link: List[bool_t] = ListData(ir((0, 4, 1)), RowData)


class LoadingImage(DataRow):
    _sign = b'LoadingImage|eJwrBgAAdAB0'
    sheet_name = 'LoadingImage'
    path: str_t = RowData(0)


class LoadingTips(DataRow):
    _sign = b'LoadingTips|eJzLy0sDAAKPAUM='
    sheet_name = 'LoadingTips'
    condition_type: int_t = RowData(0)
    condition_arg: int_t = RowData(1)
    lang_enable: bool_t = RowData(2)


class LoadingTipsSub(DataRow):
    _sign = b'LoadingTipsSub|eJwrBgAAdAB0'
    sheet_name = 'LoadingTipsSub'
    text: str_t = RowData(0)


class Lobby(DataRow):
    _sign = b'Lobby|eJzLy8srLi4GAAkqAqQ='
    sheet_name = 'Lobby'
    _display = 'text_text'
    type: int_t = RowData(0)
    param: int_t = RowData(1)
    link: int_t = RowData(2)
    text_text: str_t = RowData(3)
    text_sub: str_t = RowData(4)
    text_help: str_t = RowData(5)


class Lockon(DataRow):
    _sign = b'Lockon|eJwrTgMAAU4A2g=='
    sheet_name = 'Lockon'
    file: str_t = RowData(0)
    control_chara_only: bool_t = RowData(1)


class LogFilter(DataRow):
    _sign = b'LogFilter|eJzLywOB4mIAD48Dew=='
    sheet_name = 'LogFilter'
    _display = 'text_name'
    log_kind: int_t = RowData(0)
    caster: int_t = RowData(1)
    target: int_t = RowData(2)
    category: int_t = RowData(3)
    display_order: int_t = RowData(4)
    preset: int_t = RowData(5)
    text_name: str_t = RowData(6)
    text_help: str_t = RowData(7)


class LogKind(DataRow):
    _sign = b'LogKind|eJzLK04DAAKZAUg='
    sheet_name = 'LogKind'
    diff__height: int_t = RowData(0)
    text: str_t = RowData(1)
    notice: bool_t = RowData(2)


class LogMessage(DataRow):
    _sign = b'LogMessage|eJzLy8tLKwYABmwCJA=='
    sheet_name = 'LogMessage'
    _display = 'text'
    type: int_t = RowData(0)
    addon: int_t = RowData(1)
    filter: int_t = RowData(2)
    item__drop: bool_t = RowData(3)
    text: str_t = RowData(4)


class LootModeType(DataRow):
    _sign = b'LootModeType|eJxLAwAAZwBn'
    sheet_name = 'LootModeType'
    is_ui_select: bool_t = RowData(0)


class LotteryExchangeShop(DataRow):
    _sign = b'LotteryExchangeShop|eJwrzhtgUAzEaQAynDmX'
    sheet_name = 'LotteryExchangeShop'
    text: str_t = RowData(0)
    items_need_item: List[int_t] = ListData(ir((1, 32, 1)), RowData)
    items_need_stack: List[int_t] = ListData(ir((33, 32, 1)), RowData)
    items_compare_value: List[int_t] = ListData(ir((65, 32, 1)), RowData)
    items_sort: List[int_t] = ListData(ir((97, 32, 1)), RowData)
    script: str_t = RowData(129)
    not_enough_log_message: int_t = RowData(130)
    item_full_log_message: int_t = RowData(131)
    discrepancy_log_message: int_t = RowData(132)
    system: bool_t = RowData(133)


class MJIAnimals(DataRow):
    _sign = b'MJIAnimals|eJzLywMDAAwPAwM='
    sheet_name = 'MJIAnimals'
    b_npc: 'BNpcBase' = RowForeign(0, 'BNpcBase')
    size: int_t = RowData(1)
    type: int_t = RowData(2)
    genus: int_t = RowData(3)
    main_product: int_t = RowData(4)
    sub_product: int_t = RowData(5)
    icon_ui: 'Icon' = IconRow(6)


class MJIBuilding(DataRow):
    _sign = b'MJIBuilding|eJzLy8MPAOMADcE='
    sheet_name = 'MJIBuilding'
    need_rank: int_t = RowData(0)
    shared_group: 'ExportedSG' = RowForeign(1, 'ExportedSG')
    lively: int_t = RowData(2)
    alt_lively: int_t = RowData(3)
    construction_shared_group: 'List[ExportedSG]' = ListData(ir((4, 4, 2)), RowForeign, 'ExportedSG')
    construction_lively: List[int_t] = ListData(ir((5, 4, 2)), RowData)
    construction_grow_time: List[int_t] = ListData(ir((12, 4, 1)), RowData)
    grow_time: int_t = RowData(16)
    shortening_grow_time: int_t = RowData(17)
    shortening_need_rank: int_t = RowData(18)
    material: List[int_t] = ListData(ir((19, 5, 1)), RowData)
    material_num: List[int_t] = ListData(ir((24, 5, 1)), RowData)
    name_id: 'MJIText' = RowForeign(29, 'MJIText')
    help_id: int_t = RowData(30)
    icon: 'Icon' = IconRow(31)


class MJIBuildingPlace(DataRow):
    _sign = b'MJIBuildingPlace|eJzLywMBAAkMApU='
    sheet_name = 'MJIBuildingPlace'
    place: int_t = RowData(0)
    signboard_e_obj: 'EObjName' = RowForeign(1, 'EObjName')
    signboard_shared_group: 'ExportedSG' = RowForeign(2, 'ExportedSG')
    need_development: int_t = RowData(3)
    pos_x: int_t = RowData(4)
    pos_z: int_t = RowData(5)


class MJICraftworksObject(DataRow):
    _sign = b'MJICraftworksObject|eJzLy0MBADOfBnM='
    sheet_name = 'MJICraftworksObject'
    _display = 'craft_item_id'
    craft_item_id: 'Item' = RowForeign(0, 'Item')
    theme: List[int_t] = ListData(ir((1, 3, 1)), RowData)
    material_item_id: List[int_t] = ListData(ir((4, 4, 2)), RowData)
    material_num: List[int_t] = ListData(ir((5, 4, 2)), RowData)
    open_rank: int_t = RowData(12)
    required_time: int_t = RowData(13)
    trade_value: int_t = RowData(14)


class MJICraftworksObjectTheme(DataRow):
    _sign = b'MJICraftworksObjectTheme|eJwrBgAAdAB0'
    sheet_name = 'MJICraftworksObjectTheme'
    _display = 'text'
    text: str_t = RowData(0)


class MJICraftworksPopularity(DataRow):
    _sign = b'MJICraftworksPopularity|eJzLy6MKAABKyx6D'
    sheet_name = 'MJICraftworksPopularity'
    item: List[int_t] = ListData(ir((0, 71, 1)), RowData)


class MJICraftworksPopularity(DataRow):
    _sign = b'MJICraftworksPopularity|eJzLy6MyAACTmiLP'
    sheet_name = 'MJICraftworksPopularity'
    item: List[int_t] = ListData(ir((0, 81, 1)), RowData)


class MJICraftworksPopularityType(DataRow):
    _sign = b'MJICraftworksPopularityType|eJzLAwAAbwBv'
    sheet_name = 'MJICraftworksPopularityType'
    _display = 'ratio'
    ratio: int_t = RowData(0)


class MJICraftworksRankRatio(DataRow):
    _sign = b'MJICraftworksRankRatio|eJzLAwAAbwBv'
    sheet_name = 'MJICraftworksRankRatio'
    ratio: int_t = RowData(0)


class MJICraftworksSupplyDefine(DataRow):
    _sign = b'MJICraftworksSupplyDefine|eJzLywMAAUwA3Q=='
    sheet_name = 'MJICraftworksSupplyDefine'
    supply: int_t = RowData(0)
    ratio: int_t = RowData(1)


class MJICraftworksTension(DataRow):
    _sign = b'MJICraftworksTension|eJzLAwAAbwBv'
    sheet_name = 'MJICraftworksTension'
    tension_max: int_t = RowData(0)


class MJICropSeed(DataRow):
    _sign = b'MJICropSeed|eJzLy8sDAAKXAUs='
    sheet_name = 'MJICropSeed'
    _display = 'crop'
    crop: 'Item' = RowForeign(0, 'Item')
    shared_group: 'ExportedSG' = RowForeign(1, 'ExportedSG')
    name_e_obj: 'EObjName' = RowForeign(2, 'EObjName')


class MJIDisposalShopItem(DataRow):
    _sign = b'MJIDisposalShopItem|eJzLywMCAAZ3Aic='
    sheet_name = 'MJIDisposalShopItem'
    disposal_item: int_t = RowData(0)
    exchange_item: int_t = RowData(1)
    exchange_rate: int_t = RowData(2)
    ui_category: 'MJIDisposalShopUICategory' = RowForeign(3, 'MJIDisposalShopUICategory')
    sort: int_t = RowData(4)


class MJIDisposalShopUICategory(DataRow):
    _sign = b'MJIDisposalShopUICategory|eJwrBgAAdAB0'
    sheet_name = 'MJIDisposalShopUICategory'
    _display = 'text'
    text: str_t = RowData(0)


class MJIFarmPastureRank(DataRow):
    _sign = b'MJIFarmPastureRank|eJzLyyMNAAD5jxSh'
    sheet_name = 'MJIFarmPastureRank'
    rank_param_undeveloped_exproted_sg: List[int_t] = ListData(ir((0, 4, 1)), RowData)
    rank_param_undeveloped_collision_exproted_g: List[int_t] = ListData(ir((4, 4, 1)), RowData)
    rank_param_developed_exproted_sg: List[int_t] = ListData(ir((8, 4, 1)), RowData)
    rank_param_complete_next_develop_exproted_sg: List[int_t] = ListData(ir((12, 4, 1)), RowData)
    rank_param_lively: List[int_t] = ListData(ir((16, 4, 1)), RowData)
    rank_param_next_develop_lively: List[int_t] = ListData(ir((20, 4, 1)), RowData)
    rank_param_complete_next_develop_lively: List[int_t] = ListData(ir((24, 4, 1)), RowData)
    rank_param_layout_id: List[int_t] = ListData(ir((28, 4, 1)), RowData)
    rank_param_need_island_gil: List[int_t] = ListData(ir((32, 4, 1)), RowData)
    rank_param_capacity: List[int_t] = ListData(ir((36, 4, 1)), RowData)
    rank_param_name_id: List[int_t] = ListData(ir((40, 4, 1)), RowData)
    rank_param_help_id: List[int_t] = ListData(ir((44, 4, 1)), RowData)


class MJIFunction(DataRow):
    _sign = b'MJIFunction|eJzLywMCAAZ3Aic='
    sheet_name = 'MJIFunction'
    open_condition_progress: int_t = RowData(0)
    open_condition_rank: int_t = RowData(1)
    open_condition_village_development: int_t = RowData(2)
    open_condition_farm_level: int_t = RowData(3)
    open_condition_pasture_level: int_t = RowData(4)


class MJIGardenscaping(DataRow):
    _sign = b'MJIGardenscaping|eJzLy4MCABNfA98='
    sheet_name = 'MJIGardenscaping'


class MJIGathering(DataRow):
    _sign = b'MJIGathering|eJzLAwAAbwBv'
    sheet_name = 'MJIGathering'
    _display = 'mji_gathering_object_info'
    mji_gathering_object_info: 'MJIGatheringObject' = RowForeign(0, 'MJIGatheringObject')


class MJIGatheringItem(DataRow):
    _sign = b'MJIGatheringItem|eJzLywMDAAwPAwM='
    sheet_name = 'MJIGatheringItem'
    _display = 'catalog_id'
    catalog_id: 'Item' = RowForeign(0, 'Item')
    sort: int_t = RowData(1)
    marker_tool: int_t = RowData(2)
    marker_x: int_t = RowData(3)
    marker_z: int_t = RowData(4)
    marker_radius: int_t = RowData(5)


class MJIGatheringItem(DataRow):
    _sign = b'MJIGatheringItem|eJzLywMBAAkMApU='
    sheet_name = 'MJIGatheringItem'
    _display = 'catalog_id'
    catalog_id: 'Item' = RowForeign(0, 'Item')
    sort: int_t = RowData(1)
    marker_tool: int_t = RowData(2)
    marker_x: int_t = RowData(3)
    marker_z: int_t = RowData(4)
    marker_radius: int_t = RowData(5)


class MJIGatheringObject(DataRow):
    _sign = b'MJIGatheringObject|eJzLywMCAAZ3Aic='
    sheet_name = 'MJIGatheringObject'
    _display = 'name_e_obj'
    shared_group: 'ExportedSG' = RowForeign(0, 'ExportedSG')
    map_icon: 'Icon' = IconRow(1)
    icon_flag: int_t = RowData(2)
    name_e_obj: 'EObjName' = RowForeign(3, 'EObjName')


class MJIGatheringObject(DataRow):
    _sign = b'MJIGatheringObject|eJzLy8vLAwAEUAG5'
    sheet_name = 'MJIGatheringObject'
    _display = 'name_e_obj'
    shared_group: 'ExportedSG' = RowForeign(0, 'ExportedSG')
    map_icon: 'Icon' = IconRow(1)
    icon_flag: int_t = RowData(2)
    name_e_obj: 'EObjName' = RowForeign(3, 'EObjName')


class MJIGatheringTool(DataRow):
    _sign = b'MJIGatheringTool|eJzLAwAAbwBv'
    sheet_name = 'MJIGatheringTool'
    tool: int_t = RowData(0)


class MJIHudMode(DataRow):
    _sign = b'MJIHudMode|eJwrLs7LAwAEcwHD'
    sheet_name = 'MJIHudMode'
    _display = 'text_name'
    text_name: str_t = RowData(0)
    text_header_name: str_t = RowData(1)
    icon: 'Icon' = IconRow(2)
    open_function: int_t = RowData(3)


class MJIItemCategory(DataRow):
    _sign = b'MJIItemCategory|eJwrLgYAAVsA5w=='
    sheet_name = 'MJIItemCategory'
    _display = 'text_name'
    text_name: str_t = RowData(0)
    text_name_plr: str_t = RowData(1)


class MJIItemPouch(DataRow):
    _sign = b'MJIItemPouch|eJzLy8vLAwAEUAG5'
    sheet_name = 'MJIItemPouch'
    _display = 'catalog_id'
    catalog_id: 'Item' = RowForeign(0, 'Item')
    category_id: 'MJIItemCategory' = RowForeign(1, 'MJIItemCategory')
    category_detail: 'MJICropSeed' = RowForeign(2, 'MJICropSeed')
    sort: int_t = RowData(3)


class MJIKeyItem(DataRow):
    _sign = b'MJIKeyItem|eJzLywMAAUwA3Q=='
    sheet_name = 'MJIKeyItem'
    _display = 'item'
    item: 'Item' = RowForeign(0, 'Item')
    sort: int_t = RowData(1)


class MJILandmark(DataRow):
    _sign = b'MJILandmark|eJzLy8MLANU/DVM='
    sheet_name = 'MJILandmark'
    need_development: int_t = RowData(0)
    need_rank: int_t = RowData(1)
    reward: int_t = RowData(2)
    shared_group: 'ExportedSG' = RowForeign(3, 'ExportedSG')
    lively: int_t = RowData(4)
    construction_shared_group: 'List[ExportedSG]' = ListData(ir((5, 4, 2)), RowForeign, 'ExportedSG')
    construction_lively: List[int_t] = ListData(ir((6, 4, 2)), RowData)
    construction_grow_time: List[int_t] = ListData(ir((13, 4, 1)), RowData)
    grow_time: int_t = RowData(17)
    material: List[int_t] = ListData(ir((18, 5, 1)), RowData)
    material_num: List[int_t] = ListData(ir((23, 5, 1)), RowData)
    name_id: 'MJIText' = RowForeign(28, 'MJIText')
    help_id: int_t = RowData(29)
    icon: 'Icon' = IconRow(30)


class MJILandmarkPlace(DataRow):
    _sign = b'MJILandmarkPlace|eJzLywMBAAkMApU='
    sheet_name = 'MJILandmarkPlace'
    place: int_t = RowData(0)
    signboard_e_obj: 'EObjName' = RowForeign(1, 'EObjName')
    signboard_shared_group: 'ExportedSG' = RowForeign(2, 'ExportedSG')
    need_development: int_t = RowData(3)
    pos_x: int_t = RowData(4)
    pos_z: int_t = RowData(5)


class MJILivelyActor(DataRow):
    _sign = b'MJILivelyActor|eJzLywMBAAkMApU='
    sheet_name = 'MJILivelyActor'
    base_id: 'ENpcResident' = RowForeign(0, 'ENpcResident')
    behavior: 'Behavior' = RowForeign(1, 'Behavior')
    trans_x: float_t = RowData(2)
    trans_y: float_t = RowData(3)
    trans_z: float_t = RowData(4)
    rot_y: float_t = RowData(5)


class MJIMinionPopAreas(DataRow):
    _sign = b'MJIMinionPopAreas|eJzLy8vLSwMABm8CHw=='
    sheet_name = 'MJIMinionPopAreas'
    requirement: int_t = RowData(0)
    marker_pos_x: int_t = RowData(1)
    marker_pos_z: int_t = RowData(2)
    area_name: int_t = RowData(3)


class MJIMinionPopAreas(DataRow):
    _sign = b'MJIMinionPopAreas|eJzLy8vLAwAEUAG5'
    sheet_name = 'MJIMinionPopAreas'
    requirement: int_t = RowData(0)
    marker_pos_x: int_t = RowData(1)
    marker_pos_z: int_t = RowData(2)
    area_name: int_t = RowData(3)


class MJIName(DataRow):
    _sign = b'MJIName|eJwrzivOAwEAD8YDew=='
    sheet_name = 'MJIName'


class MJIProgress(DataRow):
    _sign = b'MJIProgress|eJwrLi7OwwQAbgcJhA=='
    sheet_name = 'MJIProgress'
    text_development_goal: str_t = RowData(0)
    text_directive: str_t = RowData(1)
    text_arrival_message: str_t = RowData(2)
    need_item: List[int_t] = ListData(ir((3, 5, 3)), RowData)
    need_item_num: List[int_t] = ListData(ir((4, 5, 3)), RowData)
    gathering_item: List[int_t] = ListData(ir((5, 5, 3)), RowData)
    hud_mode: int_t = RowData(18)
    map_marker_pos_x: int_t = RowData(19)
    map_marker_pos_z: int_t = RowData(20)
    map_marker_range: int_t = RowData(21)


class MJIRank(DataRow):
    _sign = b'MJIRank|eJzLywMCAAZ3Aic='
    sheet_name = 'MJIRank'
    exp: int_t = RowData(0)
    function: int_t = RowData(1)
    log_message: List[int_t] = ListData(ir((2, 3, 1)), RowData)


class MJIRecipe(DataRow):
    _sign = b'MJIRecipe|eJzLy0MBADOfBnM='
    sheet_name = 'MJIRecipe'
    _display = 'key_item'
    first_craft_message: 'LogMessage' = RowForeign(0, 'LogMessage')
    key_item: 'MJIKeyItem' = RowForeign(1, 'MJIKeyItem')
    craft_item_id: 'MJIItemPouch' = RowForeign(2, 'MJIItemPouch')
    craft_num: int_t = RowData(3)
    material_item_id: List[int_t] = ListData(ir((4, 5, 2)), RowData)
    material_num: List[int_t] = ListData(ir((5, 5, 2)), RowData)
    sort_prio: int_t = RowData(14)


class MJIRecipeMaterial(DataRow):
    _sign = b'MJIRecipeMaterial|eJzLywMAAUwA3Q=='
    sheet_name = 'MJIRecipeMaterial'
    _display = 'item_pouch_id'
    item_pouch_id: 'MJIItemPouch' = RowForeign(0, 'MJIItemPouch')
    category_id: int_t = RowData(1)


class MJIStockyardManagementArea(DataRow):
    _sign = b'MJIStockyardManagementArea|eJzLy8sDAAKXAUs='
    sheet_name = 'MJIStockyardManagementArea'
    _display = 'name'
    rare_item: 'MJIItemPouch' = RowForeign(0, 'MJIItemPouch')
    lottery_table: int_t = RowData(1)
    name: 'MJIText' = RowForeign(2, 'MJIText')


class MJIStockyardManagementTable(DataRow):
    _sign = b'MJIStockyardManagementTable|eJzLAwAAbwBv'
    sheet_name = 'MJIStockyardManagementTable'
    _display = 'lottery_item'
    lottery_item: 'MJIItemPouch' = RowForeign(0, 'MJIItemPouch')


class MJIText(DataRow):
    _sign = b'MJIText|eJwrBgAAdAB0'
    sheet_name = 'MJIText'
    _display = 'text'
    text: str_t = RowData(0)


class MJIVillageAppearanceSG(DataRow):
    _sign = b'MJIVillageAppearanceSG|eJzLywMBAAkMApU='
    sheet_name = 'MJIVillageAppearanceSG'
    shared_group_appearance_sg: List[int_t] = ListData(ir((0, 3, 1)), RowData)
    shared_group_name_id: List[int_t] = ListData(ir((3, 3, 1)), RowData)


class MJIVillageAppearanceSG(DataRow):
    _sign = b'MJIVillageAppearanceSG|eJzLy4MAAA+AA3E='
    sheet_name = 'MJIVillageAppearanceSG'
    shared_group_appearance_sg: List[int_t] = ListData(ir((0, 4, 1)), RowData)
    shared_group_name_id: List[int_t] = ListData(ir((4, 4, 1)), RowData)


class MJIVillageAppearanceUI(DataRow):
    _sign = b'MJIVillageAppearanceUI|eJzLy8sDAAKXAUs='
    sheet_name = 'MJIVillageAppearanceUI'
    icon: 'Icon' = IconRow(0)
    name_id: int_t = RowData(1)
    define_id: int_t = RowData(2)


class MJIVillageDevelopment(DataRow):
    _sign = b'MJIVillageDevelopment|eJzLy0MBADOfBnM='
    sheet_name = 'MJIVillageDevelopment'
    e_npc: 'ENpcResident' = RowForeign(0, 'ENpcResident')
    need_rank: int_t = RowData(1)
    need_key_item: int_t = RowData(2)
    ooen_road_sg: int_t = RowData(3)
    ooen_road_lyaout_id: int_t = RowData(4)
    open_plaza_sg: int_t = RowData(5)
    open_plaza_layout_id: int_t = RowData(6)
    open_slope_sg: int_t = RowData(7)
    open_slope_layout_id: int_t = RowData(8)
    open_collision_sg: 'Behavior' = RowForeign(9, 'Behavior')
    open_collision_layout_id: int_t = RowData(10)
    open_obstacle_sg: 'Behavior' = RowForeign(11, 'Behavior')
    open_obstacle_layout_id: int_t = RowData(12)


class MJIVillageDevelopment(DataRow):
    _sign = b'MJIVillageDevelopment|eJzLy0MCACcnBZc='
    sheet_name = 'MJIVillageDevelopment'
    e_npc: 'ENpcResident' = RowForeign(0, 'ENpcResident')
    need_rank: int_t = RowData(1)
    need_key_item: int_t = RowData(2)
    ooen_road_sg: int_t = RowData(3)
    ooen_road_lyaout_id: int_t = RowData(4)
    open_plaza_sg: int_t = RowData(5)
    open_plaza_layout_id: int_t = RowData(6)
    open_slope_sg: int_t = RowData(7)
    open_slope_layout_id: int_t = RowData(8)
    open_collision_sg: 'Behavior' = RowForeign(9, 'Behavior')
    open_collision_layout_id: int_t = RowData(10)
    open_obstacle_sg: 'Behavior' = RowForeign(11, 'Behavior')
    open_obstacle_layout_id: int_t = RowData(12)


class MYCTemporaryItem(DataRow):
    _sign = b'MYCTemporaryItem|eJzLywMBAAkMApU='
    sheet_name = 'MYCTemporaryItem'
    _display = 'action'
    ui_category: 'MYCTemporaryItemUICategory' = RowForeign(0, 'MYCTemporaryItemUICategory')
    type: int_t = RowData(1)
    action: 'Action' = RowForeign(2, 'Action')
    count: int_t = RowData(3)
    size: int_t = RowData(4)
    sort_id: int_t = RowData(5)


class MYCTemporaryItemUICategory(DataRow):
    _sign = b'MYCTemporaryItemUICategory|eJwrLgYAAVsA5w=='
    sheet_name = 'MYCTemporaryItemUICategory'
    _display = 'name_name'
    name_name: str_t = RowData(0)
    name_des_name: str_t = RowData(1)


class MYCWarResultNotebook(DataRow):
    _sign = b'MYCWarResultNotebook|eJzLy4OA4uJiAByFBMo='
    sheet_name = 'MYCWarResultNotebook'
    _display = 'name_description_name'
    sort_id: int_t = RowData(0)
    section: int_t = RowData(1)
    link: int_t = RowData(2)
    unlock_quest: 'Quest' = RowForeign(3, 'Quest')
    extra_info_quest: int_t = RowData(4)
    thumbnail_icon: 'Icon' = IconRow(5)
    portrait_icon: 'Icon' = IconRow(6)
    rarity: int_t = RowData(7)
    furigana: str_t = RowData(8)
    name_description_name: str_t = RowData(9)
    name_description_description: str_t = RowData(10)


class MacroIcon(DataRow):
    _sign = b'MacroIcon|eJzLywMAAUwA3Q=='
    sheet_name = 'MacroIcon'
    _display = 'icon'
    icon: 'Icon' = IconRow(0)


class MacroIcon(DataRow):
    _sign = b'MacroIcon|eJzLAwAAbwBv'
    sheet_name = 'MacroIcon'
    _display = 'icon'
    icon: 'Icon' = IconRow(0)


class MacroIconRedirectOld(DataRow):
    _sign = b'MacroIconRedirectOld|eJzLywMAAUwA3Q=='
    sheet_name = 'MacroIconRedirectOld'
    old_icon_number: 'Icon' = IconRow(0)
    icon: 'Icon' = IconRow(1)


class MainCommand(DataRow):
    _sign = b'MainCommand|eJzLywOC4mIADB4DDQ=='
    sheet_name = 'MainCommand'
    _display = 'text_name'
    icon: 'Icon' = IconRow(0)
    action_menu: int_t = RowData(1)
    category: 'MainCommandCategory' = RowForeign(2, 'MainCommandCategory')
    sort_id: int_t = RowData(3)
    aggregation_order: int_t = RowData(4)
    text_name: str_t = RowData(5)
    text_help: str_t = RowData(6)


class MainCommandCategory(DataRow):
    _sign = b'MainCommandCategory|eJzLKwYAAVEA4g=='
    sheet_name = 'MainCommandCategory'
    _display = 'text'
    icon: int_t = RowData(0)
    text: str_t = RowData(1)


class MandervilleWeaponEnhance(DataRow):
    _sign = b'MandervilleWeaponEnhance|eJzLy0MFADqABuE='
    sheet_name = 'MandervilleWeaponEnhance'
    type: int_t = RowData(0)


class Maneuvers(DataRow):
    _sign = b'Maneuvers|eJzLy8vLAwAEUAG5'
    sheet_name = 'Maneuvers'
    start_range: List[int_t] = ListData(ir((0, 2, 1)), RowData)
    result_camera_transform: List[int_t] = ListData(ir((2, 2, 1)), RowData)


class ManeuversArmor(DataRow):
    _sign = b'ManeuversArmor|eJzLy8vLS8sDgeJiACFfBSs='
    sheet_name = 'ManeuversArmor'
    boarding_energy: int_t = RowData(0)
    armor_name: List[int_t] = ListData(ir((1, 2, 1)), RowData)
    boarding_limit: int_t = RowData(3)
    final_armor: bool_t = RowData(4)
    icon: int_t = RowData(5)
    image: List[int_t] = ListData(ir((6, 2, 1)), RowData)
    map_icon: List[int_t] = ListData(ir((8, 2, 1)), RowData)
    text_name: str_t = RowData(10)
    text_help: str_t = RowData(11)


class Map(DataRow):
    _sign = b'Map|eJzLywOB4jwYSEtLywMAWk4Ihg=='
    sheet_name = 'Map'
    _display = 'name_ui'
    show_condition: 'MapCondition' = RowForeign(0, 'MapCondition')
    priority_category_ui: int_t = RowData(1)
    priority_ui: int_t = RowData(2)
    priority_floor_ui: int_t = RowData(3)
    map_type: int_t = RowData(4)
    marker: int_t = RowData(5)
    path: str_t = RowData(6)
    scale: int_t = RowData(7)
    offset_x: int_t = RowData(8)
    offset_y: int_t = RowData(9)
    category_name_ui: 'PlaceName' = RowForeign(10, 'PlaceName')
    name_ui: 'PlaceName' = RowForeign(11, 'PlaceName')
    floor_name_ui: 'PlaceName' = RowForeign(12, 'PlaceName')
    discovery_index: int_t = RowData(13)
    discovery_flag: int_t = RowData(14)
    territory_type: 'TerritoryType' = RowForeign(15, 'TerritoryType')
    is_uint16_discovery: bool_t = RowData(16)
    is_event: bool_t = RowData(17)
    is_use_exclusive: bool_t = RowData(18)
    map_replace: int_t = RowData(19)


class MapCondition(DataRow):
    _sign = b'MapCondition|eJzLy8sDAAKXAUs='
    sheet_name = 'MapCondition'
    _display = 'quest'
    content: int_t = RowData(0)
    quest: 'Quest' = RowForeign(1, 'Quest')
    quest_sequence: int_t = RowData(2)


class MapExclusive(DataRow):
    _sign = b'MapExclusive|eJzLywMAAUwA3Q=='
    sheet_name = 'MapExclusive'
    exclusive_group: int_t = RowData(0)
    map: int_t = RowData(1)


class MapMarker(DataRow):
    _sign = b'MapMarker|eJzLy4MDABxnBLs='
    sheet_name = 'MapMarker'
    pos_x: int_t = RowData(0)
    pos_y: int_t = RowData(1)
    icon: 'Icon' = IconRow(2)
    name: 'PlaceName' = RowForeign(3, 'PlaceName')
    layout: int_t = RowData(4)
    region: 'MapMarkerRegion' = RowForeign(5, 'MapMarkerRegion')
    text_type: int_t = RowData(6)
    event_type: int_t = RowData(7)
    event_arg: int_t = RowData(8)
    event_sub_arg: int_t = RowData(9)
    open_flag: int_t = RowData(10)


class MapMarkerRegion(DataRow):
    _sign = b'MapMarkerRegion|eJzLy4ODNAAhiAUh'
    sheet_name = 'MapMarkerRegion'
    _display = 'col1_x'
    picture_scale: int_t = RowData(0)
    col1_x: int_t = RowData(1)
    col1_y: int_t = RowData(2)
    col1_w: int_t = RowData(3)
    col1_h: int_t = RowData(4)
    col2_x: int_t = RowData(5)
    col2_y: int_t = RowData(6)
    col2_w: int_t = RowData(7)
    col2_h: int_t = RowData(8)
    name_x: int_t = RowData(9)
    name_y: int_t = RowData(10)
    link: bool_t = RowData(11)


class MapReplace(DataRow):
    _sign = b'MapReplace|eJzLy8vLAwAEUAG5'
    sheet_name = 'MapReplace'
    quest: int_t = RowData(0)
    quest_sequence: int_t = RowData(1)
    replaced_map: int_t = RowData(2)
    replaced_territory_type: int_t = RowData(3)


class MapSymbol(DataRow):
    _sign = b'MapSymbol|eJzLy0sDAAKPAUM='
    sheet_name = 'MapSymbol'
    icon: 'Icon' = IconRow(0)
    name: 'PlaceName' = RowForeign(1, 'PlaceName')
    display_navi: bool_t = RowData(2)


class MapTransientPvPMap(DataRow):
    _sign = b'MapTransientPvPMap|eJzLywMAAUwA3Q=='
    sheet_name = 'MapTransientPvPMap'
    pvp_map_icon: int_t = RowData(0)
    pvp_map_scale: int_t = RowData(1)


class MapType(DataRow):
    _sign = b'MapType|eJzLAwAAbwBv'
    sheet_name = 'MapType'
    world_map: int_t = RowData(0)


class Marker(DataRow):
    _sign = b'Marker|eJzLyysGAAKcAVA='
    sheet_name = 'Marker'
    icon: 'Icon' = IconRow(0)
    text: str_t = RowData(2)


class Marker(DataRow):
    _sign = b'Marker|eJzLKwYAAVEA4g=='
    sheet_name = 'Marker'
    icon: 'Icon' = IconRow(0)
    text: str_t = RowData(1)


class MateAuthorityCategory(DataRow):
    _sign = b'MateAuthorityCategory|eJwrBgAAdAB0'
    sheet_name = 'MateAuthorityCategory'
    text_0: str_t = RowData(0)


class Materia(DataRow):
    _sign = b'Materia|eJzLy8MCAGNXCQc='
    sheet_name = 'Materia'
    item: List[int_t] = ListData(ir((0, 10, 1)), RowData)
    param: 'BaseParam' = RowForeign(10, 'BaseParam')
    param_value: List[int_t] = ListData(ir((11, 10, 1)), RowData)


class Materia(DataRow):
    _sign = b'Materia|eJzLyyMAAPEvDi8='
    sheet_name = 'Materia'
    item: List[int_t] = ListData(ir((0, 16, 1)), RowData)
    param: 'BaseParam' = RowForeign(16, 'BaseParam')
    param_value: List[int_t] = ListData(ir((17, 16, 1)), RowData)


class MateriaGrade(DataRow):
    _sign = b'MateriaGrade|eJzLy4MBABesBE0='
    sheet_name = 'MateriaGrade'
    retrive_rate: int_t = RowData(0)
    attach_price: int_t = RowData(1)
    attach_rate: List[int_t] = ListData(ir((2, 4, 1)), RowData)
    attach_hq_rate: List[int_t] = ListData(ir((6, 4, 1)), RowData)


class MateriaJoinRate(DataRow):
    _sign = b'MateriaJoinRate|eJzLy4MAAA+AA3E='
    sheet_name = 'MateriaJoinRate'
    field_0: float_t = RowData(0)
    field_1: float_t = RowData(1)
    field_2: float_t = RowData(2)
    field_3: float_t = RowData(3)
    field_4: float_t = RowData(4)
    field_5: float_t = RowData(5)
    field_6: float_t = RowData(6)
    field_7: float_t = RowData(7)


class MateriaJoinRateGatherCraft(DataRow):
    _sign = b'MateriaJoinRateGatherCraft|eJzLy4MAAA+AA3E='
    sheet_name = 'MateriaJoinRateGatherCraft'
    field_0: float_t = RowData(0)
    field_1: float_t = RowData(1)
    field_2: float_t = RowData(2)
    field_3: float_t = RowData(3)
    field_4: float_t = RowData(4)
    field_5: float_t = RowData(5)
    field_6: float_t = RowData(6)
    field_7: float_t = RowData(7)


class MateriaParam(DataRow):
    _sign = b'MateriaParam|eJzLy0tLQgYANcwGPQ=='
    sheet_name = 'MateriaParam'
    param: int_t = RowData(0)
    sort_id: int_t = RowData(1)
    disp_all: bool_t = RowData(2)
    item_role: List[bool_t] = ListData(ir((3, 13, 1)), RowData)


class MateriaTomestoneRate(DataRow):
    _sign = b'MateriaTomestoneRate|eJzLAwAAbwBv'
    sheet_name = 'MateriaTomestoneRate'
    _display = 'rate'
    rate: int_t = RowData(0)


class McGuffin(DataRow):
    _sign = b'McGuffin|eJzLAwAAbwBv'
    sheet_name = 'McGuffin'
    ui_data: int_t = RowData(0)


class McGuffinUIData(DataRow):
    _sign = b'McGuffinUIData|eJzLyysGAAKcAVA='
    sheet_name = 'McGuffinUIData'
    ui_sort: int_t = RowData(0)
    icon: int_t = RowData(1)
    name: str_t = RowData(2)


class MiniGameRA(DataRow):
    _sign = b'MiniGameRA|eJzLywOCtDQgSstDAABqjAlN'
    sheet_name = 'MiniGameRA'
    life_type: int_t = RowData(0)
    inlay_icon: 'Icon' = IconRow(1)
    result_icon: 'Icon' = IconRow(2)
    bgm: 'BGM' = RowForeign(3, 'BGM')
    bgm_change_type: int_t = RowData(4)
    enable_life: bool_t = RowData(5)
    max_life: int_t = RowData(7)
    show_status: bool_t = RowData(8)
    show_score: bool_t = RowData(9)
    show_combo: bool_t = RowData(10)
    great_score_rate: int_t = RowData(11)
    result_time: int_t = RowData(12)
    combo_bonus: int_t = RowData(13)
    score: List[int_t] = ListData(ir((14, 4, 1)), RowData)
    threshold: List[int_t] = ListData(ir((18, 4, 1)), RowData)


class MiniGameRA(DataRow):
    _sign = b'MiniGameRA|eJzLywOCtLy0tLQ8BAAAYZ8I5w=='
    sheet_name = 'MiniGameRA'
    life_type: int_t = RowData(0)
    inlay_icon: 'Icon' = IconRow(1)
    result_icon: 'Icon' = IconRow(2)
    bgm: 'BGM' = RowForeign(3, 'BGM')
    bgm_change_type: int_t = RowData(4)
    enable_life: bool_t = RowData(5)
    max_life: int_t = RowData(6)
    show_status: bool_t = RowData(7)
    show_score: bool_t = RowData(8)
    show_combo: bool_t = RowData(9)
    great_score_rate: int_t = RowData(10)
    result_time: int_t = RowData(11)
    combo_bonus: int_t = RowData(12)
    score: List[int_t] = ListData(ir((13, 4, 1)), RowData)
    threshold: List[int_t] = ListData(ir((17, 4, 1)), RowData)


class MiniGameRANotes(DataRow):
    _sign = b'MiniGameRANotes|eJzLywMDAAwPAwM='
    sheet_name = 'MiniGameRANotes'
    time: int_t = RowData(0)
    speed: int_t = RowData(1)
    pos_x: int_t = RowData(2)
    pos_y: int_t = RowData(3)
    type: int_t = RowData(4)
    type_param: List[int_t] = ListData(ir((5, 2, 1)), RowData)


class MiniGameTurnBreakAction(DataRow):
    _sign = b'MiniGameTurnBreakAction|eJzLy4OA4mIAF7sEVw=='
    sheet_name = 'MiniGameTurnBreakAction'
    param: List[int_t] = ListData(ir((0, 2, 1)), RowData)
    sp_cost: int_t = RowData(2)
    recast_turn: int_t = RowData(3)
    range_width: int_t = RowData(4)
    range_height: int_t = RowData(5)
    image: int_t = RowData(6)
    score: int_t = RowData(7)
    text_name: str_t = RowData(8)
    text_help: str_t = RowData(9)


class MiniGameTurnBreakConst(DataRow):
    _sign = b'MiniGameTurnBreakConst|eJzLAwAAbwBv'
    sheet_name = 'MiniGameTurnBreakConst'
    value: int_t = RowData(0)


class MiniGameTurnBreakEnemy(DataRow):
    _sign = b'MiniGameTurnBreakEnemy|eJzLy8vLS8uDgDQoyEMFAAkODsM='
    sheet_name = 'MiniGameTurnBreakEnemy'


class MiniGameTurnBreakPop(DataRow):
    _sign = b'MiniGameTurnBreakPop|eJzLy8vLAwAEUAG5'
    sheet_name = 'MiniGameTurnBreakPop'


class MiniGameTurnBreakPopOffset(DataRow):
    _sign = b'MiniGameTurnBreakPopOffset|eJzLy4MAAA+AA3E='
    sheet_name = 'MiniGameTurnBreakPopOffset'


class MiniGameTurnBreakStage(DataRow):
    _sign = b'MiniGameTurnBreakStage|eJzLy4MBABesBE0='
    sheet_name = 'MiniGameTurnBreakStage'


class MiniGameTurnBreakStatus(DataRow):
    _sign = b'MiniGameTurnBreakStatus|eJzLy0vLKy4GAAj7Apc='
    sheet_name = 'MiniGameTurnBreakStatus'


class MinionRace(DataRow):
    _sign = b'MinionRace|eJwrBgAAdAB0'
    sheet_name = 'MinionRace'
    _display = 'text'
    text: str_t = RowData(0)


class MinionRules(DataRow):
    _sign = b'MinionRules|eJwrLgYAAVsA5w=='
    sheet_name = 'MinionRules'
    _display = 'rule'
    rule: str_t = RowData(0)
    description: str_t = RowData(1)


class MinionSkillType(DataRow):
    _sign = b'MinionSkillType|eJwrBgAAdAB0'
    sheet_name = 'MinionSkillType'
    _display = 'text'
    text: str_t = RowData(0)


class MinionStage(DataRow):
    _sign = b'MinionStage|eJwrTssDAAKWAUg='
    sheet_name = 'MinionStage'
    text: str_t = RowData(0)
    boss: bool_t = RowData(1)
    bgm: int_t = RowData(2)


class MobHuntOrder(DataRow):
    _sign = b'MobHuntOrder|eJzLywMCAAZ3Aic='
    sheet_name = 'MobHuntOrder'
    target: 'MobHuntTarget' = RowForeign(0, 'MobHuntTarget')
    needed_kills: int_t = RowData(1)
    rank: int_t = RowData(2)
    star_rank: int_t = RowData(3)
    reward: 'MobHuntReward' = RowForeign(4, 'MobHuntReward')


class MobHuntOrderType(DataRow):
    _sign = b'MobHuntOrderType|eJzLywMCAAZ3Aic='
    sheet_name = 'MobHuntOrderType'
    order_cycle: int_t = RowData(0)
    quest: 'Quest' = RowForeign(1, 'Quest')
    event_item: 'EventItem' = RowForeign(2, 'EventItem')
    order_begin: 'MobHuntOrder' = RowForeign(3, 'MobHuntOrder')
    order_number: int_t = RowData(4)


class MobHuntReward(DataRow):
    _sign = b'MobHuntReward|eJzLy8vLAwAEUAG5'
    sheet_name = 'MobHuntReward'
    exp: int_t = RowData(0)
    gil: int_t = RowData(1)
    seal_type: 'ExVersion' = RowForeign(2, 'ExVersion')
    seal_value: int_t = RowData(3)


class MobHuntRewardCap(DataRow):
    _sign = b'MobHuntRewardCap|eJzLAwAAbwBv'
    sheet_name = 'MobHuntRewardCap'
    exp: int_t = RowData(0)


class MobHuntTarget(DataRow):
    _sign = b'MobHuntTarget|eJzLywMCAAZ3Aic='
    sheet_name = 'MobHuntTarget'
    _display = 'monster'
    monster: 'BNpcName' = RowForeign(0, 'BNpcName')
    fate: 'Fate' = RowForeign(1, 'Fate')
    icon: 'Icon' = IconRow(2)
    zone_name: 'Map' = RowForeign(3, 'Map')
    area_name: 'PlaceName' = RowForeign(4, 'PlaceName')


class ModelAttribute(DataRow):
    _sign = b'ModelAttribute|eJwrBgAAdAB0'
    sheet_name = 'ModelAttribute'
    name: str_t = RowData(0)


class ModelChara(DataRow):
    _sign = b'ModelChara|eJzLywOBtDQQBoI8ICMPAFgYCFk='
    sheet_name = 'ModelChara'
    model_type: int_t = RowData(0)
    skeleton_id: int_t = RowData(1)
    pattern_id: int_t = RowData(2)
    ime_chan_id: int_t = RowData(3)
    se_pack: int_t = RowData(4)
    pap_variation: int_t = RowData(5)
    no_shadow: bool_t = RowData(6)
    nameplate_in_offset_range: bool_t = RowData(7)
    nameplate_camera_offset: int_t = RowData(8)
    nameplate_y_offset: int_t = RowData(9)
    dead_clear_action_timeline: bool_t = RowData(10)
    force_visible: bool_t = RowData(11)
    larger_than_radius: bool_t = RowData(12)
    vfx_decal: bool_t = RowData(13)
    disable_selected_edge: bool_t = RowData(14)
    alpha: int_t = RowData(15)
    disable_look_at: bool_t = RowData(16)
    add_damage_weight_rate: int_t = RowData(17)
    radius: float_t = RowData(18)
    offset_y: float_t = RowData(19)


class ModelScale(DataRow):
    _sign = b'ModelScale|eJzLAwAAbwBv'
    sheet_name = 'ModelScale'
    scale: float_t = RowData(0)


class ModelSkeleton(DataRow):
    _sign = b'ModelSkeleton|eJzLy0MBaXkAQb8HRw=='
    sheet_name = 'ModelSkeleton'
    radius: float_t = RowData(0)
    vfx_scale: float_t = RowData(1)
    foot_scale: float_t = RowData(2)
    walk_speed: int_t = RowData(3)
    run_speed: int_t = RowData(4)
    walk_motion_min: int_t = RowData(5)
    walk_motion_max: int_t = RowData(6)
    run_motion_min: int_t = RowData(7)
    run_motion_max: int_t = RowData(8)
    float_height: List[int_t] = ListData(ir((9, 2, 1)), RowData)
    float_down: float_t = RowData(11)
    float_up: float_t = RowData(12)
    diving_float_height: int_t = RowData(13)
    motion_blend_type: int_t = RowData(14)
    loop_fly_se: bool_t = RowData(15)
    auto_attack_type: int_t = RowData(16)


class ModelState(DataRow):
    _sign = b'ModelState|eJzLywMAAUwA3Q=='
    sheet_name = 'ModelState'
    _display = 'timeline'
    type: int_t = RowData(0)
    timeline: 'ActionTimeline' = RowForeign(1, 'ActionTimeline')


class MonsterNote(DataRow):
    _sign = b'MonsterNote|eJzLy4OCYgAXsQRS'
    sheet_name = 'MonsterNote'
    _display = 'text'
    target: List[int_t] = ListData(ir((0, 4, 1)), RowData)
    needed_kills: List[int_t] = ListData(ir((4, 4, 1)), RowData)
    reward_exp: int_t = RowData(8)
    text: str_t = RowData(9)


class MonsterNoteTarget(DataRow):
    _sign = b'MonsterNoteTarget|eJzLy4MCABNfA98='
    sheet_name = 'MonsterNoteTarget'
    _display = 'monster'
    monster: 'BNpcName' = RowForeign(0, 'BNpcName')
    icon: 'Icon' = IconRow(1)
    town: 'Town' = RowForeign(2, 'Town')
    zone_name: List[int_t] = ListData(ir((3, 3, 2)), RowData)
    area_name: List[int_t] = ListData(ir((4, 3, 2)), RowData)


class MotionTimeline(DataRow):
    _sign = b'MotionTimeline|eJwrzktLSwMABmACFA=='
    sheet_name = 'MotionTimeline'
    filename: str_t = RowData(0)
    blend_group: int_t = RowData(1)
    is_loop: bool_t = RowData(2)
    is_blink_enable: bool_t = RowData(3)
    is_lip_enable: bool_t = RowData(4)


class MotionTimelineAdvanceBlend(DataRow):
    _sign = b'MotionTimelineAdvanceBlend|eJwrLgYAAVsA5w=='
    sheet_name = 'MotionTimelineAdvanceBlend'
    motion_timeline_name: str_t = RowData(0)
    next_motion_timeline_name: str_t = RowData(1)


class MotionTimelineBlendTable(DataRow):
    _sign = b'MotionTimelineBlendTable|eJzLywMBAAkMApU='
    sheet_name = 'MotionTimelineBlendTable'
    dest_blend_group: int_t = RowData(0)
    src_blend_group: int_t = RowData(1)
    blend_frame__pc: int_t = RowData(2)
    blend_frame__type_a: int_t = RowData(3)
    blend_frame__type_b: int_t = RowData(4)
    blend_frame__type_c: int_t = RowData(5)


class Mount(DataRow):
    _sign = b'Mount|eJwrzivOQwXFxUCRtDQUsTQQAFEA5bYUBA=='
    sheet_name = 'Mount'
    _display = 'text_sgl'
    text_sgl: str_t = RowData(0)
    text_sgg: int_t = RowData(1)
    text_plr: str_t = RowData(2)
    text_plg: int_t = RowData(3)
    text_vow: int_t = RowData(4)
    text_cnt: int_t = RowData(5)
    text_gen: int_t = RowData(6)
    text_def_: int_t = RowData(7)
    model: 'ModelChara' = RowForeign(8, 'ModelChara')
    control: int_t = RowData(9)
    flying_condition: 'MountFlyingCondition' = RowForeign(10, 'MountFlyingCondition')
    fly_motion_pitch_limit: int_t = RowData(11)
    glide_front: int_t = RowData(12)
    glide_front_diving: int_t = RowData(13)
    fly_effect: int_t = RowData(14)
    glide_effect: int_t = RowData(15)
    customize: 'MountCustomize' = RowForeign(16, 'MountCustomize')
    bgm: 'BGM' = RowForeign(17, 'BGM')
    call_se: str_t = RowData(18)
    call_false_se: str_t = RowData(19)
    exit_se: str_t = RowData(20)
    exit_move_dist: int_t = RowData(21)
    exit_move_speed: int_t = RowData(22)
    hide_parts: bool_t = RowData(23)
    is_emote: bool_t = RowData(24)
    equip_head: int_t = RowData(25)
    equip_body: int_t = RowData(26)
    equip_leg: int_t = RowData(27)
    equip_foot: int_t = RowData(28)
    save_index: int_t = RowData(29)
    icon: 'Icon' = IconRow(30)
    ui_priority: int_t = RowData(31)
    radius_rate: int_t = RowData(32)
    base_motion_speed__run: int_t = RowData(33)
    base_motion_speed__walk: int_t = RowData(34)
    diving_motion_speed: int_t = RowData(35)
    link_num: int_t = RowData(36)
    action: 'MountAction' = RowForeign(37, 'MountAction')
    is_float: bool_t = RowData(38)
    ex_hotbar_enable_config: bool_t = RowData(39)
    is_display_ep: bool_t = RowData(40)
    is_auto_gt: bool_t = RowData(41)
    not_move_can_turn: bool_t = RowData(42)
    strife_angle: int_t = RowData(43)
    strife_angle_flying_or_diving: int_t = RowData(44)
    disable_dismount_button: bool_t = RowData(45)
    hide_head_equip: bool_t = RowData(46)


class MountAction(DataRow):
    _sign = b'MountAction|eJzLywMBAAkMApU='
    sheet_name = 'MountAction'
    action: List[int_t] = ListData(ir((0, 6, 1)), RowData)


class MountCustomize(DataRow):
    _sign = b'MountCustomize|eJxLyyMCAAAtHg/f'
    sheet_name = 'MountCustomize'
    height_scale: bool_t = RowData(0)
    scale: List[int_t] = ListData(ir((1, 18, 1)), RowData)
    camera_scale_y: List[int_t] = ListData(ir((19, 18, 1)), RowData)


class MountFlyingCondition(DataRow):
    _sign = b'MountFlyingCondition|eJzLAwAAbwBv'
    sheet_name = 'MountFlyingCondition'
    _display = 'quest'
    quest: 'Quest' = RowForeign(0, 'Quest')


class MountSpeed(DataRow):
    _sign = b'MountSpeed|eJzLy8sDAAKXAUs='
    sheet_name = 'MountSpeed'
    _display = 'condition'
    condition: 'List[Quest]' = ListData(ir((0, 2, 1)), RowForeign, 'Quest')
    sort_key: int_t = RowData(2)


class MountTransient(DataRow):
    _sign = b'MountTransient|eJwrLi4GAAK1AVo='
    sheet_name = 'MountTransient'
    text_help: str_t = RowData(0)
    text_expository: str_t = RowData(1)
    text_cry: str_t = RowData(2)


class MoveControl(DataRow):
    _sign = b'MoveControl|eJzLy4MBABesBE0='
    sheet_name = 'MoveControl'
    accel: List[float_t] = ListData(ir((0, 2, 1)), RowData)
    speed: List[float_t] = ListData(ir((2, 2, 1)), RowData)
    speed_lr: List[float_t] = ListData(ir((4, 2, 1)), RowData)
    speed_back: float_t = RowData(6)
    rotate_accel: List[int_t] = ListData(ir((7, 2, 1)), RowData)
    battle_speed: int_t = RowData(9)


class MoveTimeline(DataRow):
    _sign = b'MoveTimeline|eJzLy4MBABesBE0='
    sheet_name = 'MoveTimeline'
    _display = 'idle'
    idle: 'ActionTimeline' = RowForeign(0, 'ActionTimeline')
    move_front: 'ActionTimeline' = RowForeign(1, 'ActionTimeline')
    move_back: 'ActionTimeline' = RowForeign(2, 'ActionTimeline')
    move_left: 'ActionTimeline' = RowForeign(3, 'ActionTimeline')
    move_right: 'ActionTimeline' = RowForeign(4, 'ActionTimeline')
    move_up: 'ActionTimeline' = RowForeign(5, 'ActionTimeline')
    move_down: 'ActionTimeline' = RowForeign(6, 'ActionTimeline')
    turn_left: 'ActionTimeline' = RowForeign(7, 'ActionTimeline')
    turn_right: 'ActionTimeline' = RowForeign(8, 'ActionTimeline')
    idle_to_move_front: 'ActionTimeline' = RowForeign(9, 'ActionTimeline')


class MoveVfx(DataRow):
    _sign = b'MoveVfx|eJzLywMAAUwA3Q=='
    sheet_name = 'MoveVfx'
    _display = 'flying'
    flying: 'VFX' = RowForeign(0, 'VFX')
    diving: 'VFX' = RowForeign(1, 'VFX')


class MovieStaffList(DataRow):
    _sign = b'MovieStaffList|eJzLy8vLAwAEUAG5'
    sheet_name = 'MovieStaffList'
    icon: 'Icon' = IconRow(0)
    fade_in: float_t = RowData(1)
    fade_out: float_t = RowData(2)
    fade_type: int_t = RowData(3)


class MovieSubtitle(DataRow):
    _sign = b'MovieSubtitle|eJzLywMAAUwA3Q=='
    sheet_name = 'MovieSubtitle'
    time_start_time: float_t = RowData(0)
    time_end_time: float_t = RowData(1)


class MovieSubtitle500(DataRow):
    _sign = b'MovieSubtitle500|eJzLywMAAUwA3Q=='
    sheet_name = 'MovieSubtitle500'
    start_time: float_t = RowData(0)
    end_time: float_t = RowData(1)


class MovieSubtitleVoyage(DataRow):
    _sign = b'MovieSubtitleVoyage|eJzLywMAAUwA3Q=='
    sheet_name = 'MovieSubtitleVoyage'
    start_time: float_t = RowData(0)
    end_time: float_t = RowData(1)


class MultipleHelp(DataRow):
    _sign = b'MultipleHelp|eJzLKy4GAAKmAVU='
    sheet_name = 'MultipleHelp'
    page: int_t = RowData(0)
    text_title: str_t = RowData(1)
    text_subtitle: str_t = RowData(2)


class MultipleHelpPage(DataRow):
    _sign = b'MultipleHelpPage|eJzLAwAAbwBv'
    sheet_name = 'MultipleHelpPage'
    text: int_t = RowData(0)


class MultipleHelpString(DataRow):
    _sign = b'MultipleHelpString|eJwrLgYAAVsA5w=='
    sheet_name = 'MultipleHelpString'
    text_title: str_t = RowData(0)
    text_body: str_t = RowData(1)


class NotebookDivision(DataRow):
    _sign = b'NotebookDivision|eJwrzgOBtCQoAAAx8gYQ'
    sheet_name = 'NotebookDivision'
    _display = 'text'
    text: str_t = RowData(0)
    notebook_division_category: 'NotebookDivisionCategory' = RowForeign(1, 'NotebookDivisionCategory')
    craft_opening_level: int_t = RowData(2)
    gathering_opening_level: int_t = RowData(3)
    need_complete_quest: 'Quest' = RowForeign(4, 'Quest')
    special_recipe_sort_in_category: int_t = RowData(5)
    is_special_recipe: bool_t = RowData(6)
    can_use_craft: List[bool_t] = ListData(ir((7, 8, 1)), RowData)


class NotebookDivisionCategory(DataRow):
    _sign = b'NotebookDivisionCategory|eJwrzgMAAVYA4g=='
    sheet_name = 'NotebookDivisionCategory'
    _display = 'text'
    text: str_t = RowData(0)
    sort: int_t = RowData(1)


class NotebookList(DataRow):
    _sign = b'NotebookList|eJzLywMAAUwA3Q=='
    sheet_name = 'NotebookList'
    num_0: int_t = RowData(0)
    num_1: int_t = RowData(1)


class NotoriousMonster(DataRow):
    _sign = b'NotoriousMonster|eJzLy8vLAwAEUAG5'
    sheet_name = 'NotoriousMonster'
    base_id: 'BNpcBase' = RowForeign(0, 'BNpcBase')
    rank: int_t = RowData(1)
    name_id: 'BNpcName' = RowForeign(2, 'BNpcName')
    resident: int_t = RowData(3)


class NotoriousMonsterTerritory(DataRow):
    _sign = b'NotoriousMonsterTerritory|eJzLy4MBABesBE0='
    sheet_name = 'NotoriousMonsterTerritory'
    nm_labels_nm_label: List[int_t] = ListData(ir((0, 10, 1)), RowData)


class NpcEquip(DataRow):
    _sign = b'NpcEquip|eJzLywOBtDwMAACLJwq3'
    sheet_name = 'NpcEquip'
    weapon_model: int_t = RowData(0)
    weapon_stain: 'Stain' = RowForeign(1, 'Stain')
    sub_weapon_model: int_t = RowData(2)
    sub_weapon_stain: 'Stain' = RowForeign(3, 'Stain')
    equip: List[int_t] = ListData([4, 7, 9, 11, 13, 15, 17, 19, 21, 23], RowData)
    stain: 'List[Stain]' = ListData([5, 8, 10, 12, 14, 16, 18, 20, 22, 24], RowForeign, 'Stain')
    visor: bool_t = RowData(6)


class NpcYell(DataRow):
    _sign = b'NpcYell|eJzLS0tLy8sD4WIAG0wEmA=='
    sheet_name = 'NpcYell'
    _display = 'npc_text'
    name_id: int_t = RowData(0)
    is_no_name: bool_t = RowData(1)
    is_name_addon_text: bool_t = RowData(2)
    event_target_say: bool_t = RowData(3)
    output_type: int_t = RowData(4)
    balloon_time: float_t = RowData(5)
    is_balloon_timely_disable: bool_t = RowData(6)
    is_balloon_immediately: bool_t = RowData(7)
    battle_talk_time: int_t = RowData(8)
    element_id: int_t = RowData(9)
    npc_text: str_t = RowData(10)


class Omen(DataRow):
    _sign = b'Omen|eJwrLs5LS8sDAAkbAo8='
    sheet_name = 'Omen'
    _display = 'path'
    path: str_t = RowData(0)
    path_ally: str_t = RowData(1)
    type: int_t = RowData(2)
    restrict_y_scale: bool_t = RowData(3)
    large_scale: bool_t = RowData(4)
    max_y_scale: int_t = RowData(5)


class Omikuji(DataRow):
    _sign = b'Omikuji|eJzLywOC4mIADB4DDQ=='
    sheet_name = 'Omikuji'
    guidance1: int_t = RowData(0)
    guidance2: int_t = RowData(1)
    guidance3: int_t = RowData(2)
    guidance4: int_t = RowData(3)
    guidance5: int_t = RowData(4)
    text_title: str_t = RowData(5)
    text_subtitle: str_t = RowData(6)


class OmikujiGuidance(DataRow):
    _sign = b'OmikujiGuidance|eJxLKy4GAAKOAU0='
    sheet_name = 'OmikujiGuidance'
    lottery: bool_t = RowData(0)
    text_text_header: str_t = RowData(1)
    text_text_main: str_t = RowData(2)


class OnlineStatus(DataRow):
    _sign = b'OnlineStatus|eJxLS0vLy8srBgALhALw'
    sheet_name = 'OnlineStatus'
    _display = 'list_order'
    high_prio: bool_t = RowData(0)
    list: bool_t = RowData(1)
    hide_content: bool_t = RowData(2)
    list_order: int_t = RowData(3)
    icon: 'Icon' = IconRow(4)


class OnlineStatus(DataRow):
    _sign = b'OnlineStatus|eJxLS8srzgMABjkCHA=='
    sheet_name = 'OnlineStatus'
    _display = 'text'
    list: bool_t = RowData(0)
    hide_content: bool_t = RowData(1)
    list_order: int_t = RowData(2)
    text: str_t = RowData(3)
    icon: 'Icon' = IconRow(4)


class OpenContent(DataRow):
    _sign = b'OpenContent|eJzLy8MPAOMADcE='
    sheet_name = 'OpenContent'
    field_0: int_t = RowData(0)
    field_1: int_t = RowData(1)
    field_2: int_t = RowData(2)
    field_3: int_t = RowData(3)
    field_4: int_t = RowData(4)
    field_5: int_t = RowData(5)
    field_6: int_t = RowData(6)
    field_7: int_t = RowData(7)
    field_8: int_t = RowData(8)
    field_9: int_t = RowData(9)
    field_10: int_t = RowData(10)
    field_11: int_t = RowData(11)
    field_12: int_t = RowData(12)
    field_13: int_t = RowData(13)
    field_14: int_t = RowData(14)
    field_15: int_t = RowData(15)
    field_16: int_t = RowData(16)
    field_17: int_t = RowData(17)
    field_18: int_t = RowData(18)
    field_19: int_t = RowData(19)
    field_20: int_t = RowData(20)
    field_21: int_t = RowData(21)
    field_22: int_t = RowData(22)
    field_23: int_t = RowData(23)
    field_24: int_t = RowData(24)
    field_25: int_t = RowData(25)
    field_26: int_t = RowData(26)
    field_27: int_t = RowData(27)
    field_28: int_t = RowData(28)
    field_29: int_t = RowData(29)
    field_30: int_t = RowData(30)
    field_31: int_t = RowData(31)


class OpenContentCandidateName(DataRow):
    _sign = b'OpenContentCandidateName|eJwrBgAAdAB0'
    sheet_name = 'OpenContentCandidateName'
    _display = 'text'
    text: str_t = RowData(0)


class OpenLuaUI(DataRow):
    _sign = b'OpenLuaUI|eJwrBgAAdAB0'
    sheet_name = 'OpenLuaUI'
    lua_define: str_t = RowData(0)


class Opening(DataRow):
    _sign = b'Opening|eJwrzismEuQRCQDntSQK'
    sheet_name = 'Opening'
    _display = 'script'
    script: str_t = RowData(0)
    quest: 'Quest' = RowForeign(1, 'Quest')
    define_name: List[str_t] = ListData(ir((2, 40, 1)), RowData)
    define_value: List[int_t] = ListData(ir((42, 40, 1)), RowData)


class OpeningSystemDefine(DataRow):
    _sign = b'OpeningSystemDefine|eJwrzgMAAVYA4g=='
    sheet_name = 'OpeningSystemDefine'
    define_name: str_t = RowData(0)
    define_value: int_t = RowData(1)


class Orchestrion(DataRow):
    _sign = b'Orchestrion|eJwrLgYAAVsA5w=='
    sheet_name = 'Orchestrion'
    title_text: str_t = RowData(0)
    title_hint_text: str_t = RowData(1)


class OrchestrionCategory(DataRow):
    _sign = b'OrchestrionCategory|eJwrzsvLSwMABogCJA=='
    sheet_name = 'OrchestrionCategory'
    _display = 'text'
    text: str_t = RowData(0)
    variable: int_t = RowData(1)
    icon: 'Icon' = IconRow(2)
    sort: int_t = RowData(3)
    is_list_wide: bool_t = RowData(4)


class OrchestrionPath(DataRow):
    _sign = b'OrchestrionPath|eJwrBgAAdAB0'
    sheet_name = 'OrchestrionPath'
    path: str_t = RowData(0)


class OrchestrionUiparam(DataRow):
    _sign = b'OrchestrionUiparam|eJzLywMAAUwA3Q=='
    sheet_name = 'OrchestrionUiparam'
    category: 'OrchestrionCategory' = RowForeign(0, 'OrchestrionCategory')
    track_no: int_t = RowData(1)


class Ornament(DataRow):
    _sign = b'Ornament|eJzLy4OAYiAEAQA6xgbr'
    sheet_name = 'Ornament'
    _display = 'text_sgl'
    model: int_t = RowData(0)
    customize_group: int_t = RowData(1)
    special: int_t = RowData(2)
    pose_emote_stance: int_t = RowData(3)
    action: int_t = RowData(4)
    save_index: int_t = RowData(5)
    icon: 'Icon' = IconRow(6)
    ui_priority: int_t = RowData(7)
    text_sgl: str_t = RowData(8)
    text_sgg: int_t = RowData(9)
    text_plr: str_t = RowData(10)
    text_plg: int_t = RowData(11)
    text_vow: int_t = RowData(12)
    text_cnt: int_t = RowData(13)
    text_gen: int_t = RowData(14)
    text_def_: int_t = RowData(15)


class OrnamentAction(DataRow):
    _sign = b'OrnamentAction|eJzLywMBAAkMApU='
    sheet_name = 'OrnamentAction'
    action: List[int_t] = ListData(ir((0, 6, 1)), RowData)


class OrnamentCustomize(DataRow):
    _sign = b'OrnamentCustomize|eJzLywMDAAwPAwM='
    sheet_name = 'OrnamentCustomize'
    scale: int_t = RowData(0)
    translation: List[int_t] = ListData(ir((1, 3, 1)), RowData)
    rotation: List[int_t] = ListData(ir((4, 3, 1)), RowData)


class OrnamentCustomizeGroup(DataRow):
    _sign = b'OrnamentCustomizeGroup|eJzLy8MAAFG3CCs='
    sheet_name = 'OrnamentCustomizeGroup'
    attach_e_id: int_t = RowData(0)
    customize: List[int_t] = ListData(ir((1, 18, 1)), RowData)


class OrnamentTransient(DataRow):
    _sign = b'OrnamentTransient|eJwrBgAAdAB0'
    sheet_name = 'OrnamentTransient'
    text: str_t = RowData(0)


class ParamGrow(DataRow):
    _sign = b'ParamGrow|eJzLy0MBADOfBnM='
    sheet_name = 'ParamGrow'
    next_exp: int_t = RowData(0)
    apply_action: int_t = RowData(1)
    apply_action_battle: int_t = RowData(2)
    base_exp: int_t = RowData(3)
    mp: int_t = RowData(4)
    param_base: int_t = RowData(5)
    param_base_rating: int_t = RowData(6)
    event_exp_rate: int_t = RowData(7)
    repair_exp: int_t = RowData(8)
    monster_note_exp: int_t = RowData(9)
    monster_note_seals: int_t = RowData(10)
    sync_item_level: int_t = RowData(11)
    proper_dungeon: int_t = RowData(12)
    proper_guild_order: int_t = RowData(13)
    refine_item_level: int_t = RowData(14)


class PartyContent(DataRow):
    _sign = b'PartyContent|eJzLy0vLIwQAHU8PcQ=='
    sheet_name = 'PartyContent'
    _display = 'content_finder_condition'
    type: int_t = RowData(0)
    time: int_t = RowData(1)
    name: bool_t = RowData(2)
    text_start: 'PartyContentTextData' = RowForeign(3, 'PartyContentTextData')
    text_end: 'PartyContentTextData' = RowForeign(4, 'PartyContentTextData')
    entrance_shield: List[int_t] = ListData(ir((5, 9, 1)), RowData)
    entrance_exit: List[int_t] = ListData(ir((14, 9, 1)), RowData)
    entrance_exit_obj: List[int_t] = ListData(ir((23, 9, 1)), RowData)
    data_index: int_t = RowData(32)
    content_finder_condition: 'ContentFinderCondition' = RowForeign(33, 'ContentFinderCondition')
    image: 'Icon' = IconRow(34)
    sortkey: int_t = RowData(35)


class PartyContentCutscene(DataRow):
    _sign = b'PartyContentCutscene|eJzLywMAAUwA3Q=='
    sheet_name = 'PartyContentCutscene'
    cutscene_id: 'List[Cutscene]' = ListData(ir((0, 2, 1)), RowForeign, 'Cutscene')


class PartyContentTextData(DataRow):
    _sign = b'PartyContentTextData|eJwrBgAAdAB0'
    sheet_name = 'PartyContentTextData'
    _display = 'text'
    text: str_t = RowData(0)


class PartyContentTransient(DataRow):
    _sign = b'PartyContentTransient|eJwrBgAAdAB0'
    sheet_name = 'PartyContentTransient'
    text_0: str_t = RowData(0)


class PatchMark(DataRow):
    _sign = b'PatchMark|eJzLy4MAAA+AA3E='
    sheet_name = 'PatchMark'
    category: int_t = RowData(0)
    sub_category_type: int_t = RowData(1)
    sub_category: int_t = RowData(2)
    conditon: int_t = RowData(3)
    condition_value: int_t = RowData(4)
    mark_id: int_t = RowData(5)
    group_no: int_t = RowData(6)
    version: int_t = RowData(7)


class Perform(DataRow):
    _sign = b'Perform|eJwrTsuDgGIgBgAnHAWZ'
    sheet_name = 'Perform'
    _display = 'sound'
    sound: str_t = RowData(0)
    loop_flag: bool_t = RowData(1)
    model: int_t = RowData(2)
    start_timeline: 'ActionTimeline' = RowForeign(3, 'ActionTimeline')
    end_timeline: 'ActionTimeline' = RowForeign(4, 'ActionTimeline')
    idle_timeline: 'ActionTimeline' = RowForeign(5, 'ActionTimeline')
    timeline_timeline: 'List[ActionTimeline]' = ListData(ir((6, 2, 1)), RowForeign, 'ActionTimeline')
    reward: 'ActionTimeline' = RowForeign(8, 'ActionTimeline')
    text: str_t = RowData(9)
    icon: int_t = RowData(10)
    ui_priority: 'PerformTransient' = RowForeign(11, 'PerformTransient')
    group_id: int_t = RowData(12)


class PerformGroup(DataRow):
    _sign = b'PerformGroup|eJzLywMCAAZ3Aic='
    sheet_name = 'PerformGroup'
    perform: List[int_t] = ListData(ir((0, 5, 1)), RowData)


class PerformGuideScore(DataRow):
    _sign = b'PerformGuideScore|eJwrzisGAAKrAVU='
    sheet_name = 'PerformGuideScore'
    path: str_t = RowData(0)
    sort_priority: int_t = RowData(1)
    text: str_t = RowData(2)


class PerformTransient(DataRow):
    _sign = b'PerformTransient|eJwrBgAAdAB0'
    sheet_name = 'PerformTransient'
    _display = 'text'
    text: str_t = RowData(0)


class Permission(DataRow):
    _sign = b'Permission|eJxLSqIPAAArCCfR'
    sheet_name = 'Permission'
    flag: List[bool_t] = ListData(ir((0, 104, 1)), RowData)


class Pet(DataRow):
    _sign = b'Pet|eJwrzgOBtLS0PDgAAFD2CBg='
    sheet_name = 'Pet'
    _display = 'text'
    text: str_t = RowData(0)
    use_action: List[int_t] = ListData(ir((1, 5, 1)), RowData)
    is_turret: bool_t = RowData(6)
    is_use_pet_action: bool_t = RowData(7)
    is_disp_ex_hotbar: bool_t = RowData(8)
    config_scale: List[int_t] = ListData(ir((9, 3, 1)), RowData)
    mirage_slot: int_t = RowData(12)
    mirage: List[int_t] = ListData(ir((13, 6, 1)), RowData)


class PetAction(DataRow):
    _sign = b'PetAction|eJwrLs7Ly0tLSwMAD5sDYw=='
    sheet_name = 'PetAction'
    _display = 'text_name'
    text_name: str_t = RowData(0)
    text_help: str_t = RowData(1)
    icon: 'Icon' = IconRow(2)
    action: 'Action' = RowForeign(3, 'Action')
    pet: 'Pet' = RowForeign(4, 'Pet')
    disable_order: bool_t = RowData(5)
    show_on_ui: bool_t = RowData(6)
    aa_log: bool_t = RowData(7)


class PetMirage(DataRow):
    _sign = b'PetMirage|eJzLyyvOowAAAGPdGxg='
    sheet_name = 'PetMirage'
    _display = 'text'
    scale: float_t = RowData(0)
    model_chara_id: int_t = RowData(1)
    text: str_t = RowData(2)
    replace_timeline_target_action: List[int_t] = ListData(ir((3, 15, 1)), RowData)
    replace_timeline_cast_timeline: List[int_t] = ListData(ir((18, 15, 1)), RowData)
    replace_timeline_timeline: List[int_t] = ListData(ir((33, 15, 1)), RowData)
    replace_timeline_hit_timeline: List[int_t] = ListData(ir((48, 15, 1)), RowData)


class PhysicsGroup(DataRow):
    _sign = b'PhysicsGroup|eJzLy0OANAgJAFF3CBs='
    sheet_name = 'PhysicsGroup'
    simulation_time: List[float_t] = ListData(ir((0, 6, 1)), RowData)
    ps3_simulation_time: List[float_t] = ListData(ir((6, 6, 1)), RowData)
    reset_by_look_at: bool_t = RowData(12)
    root_following_game: float_t = RowData(13)
    root_following_cut_scene: float_t = RowData(14)
    config_switch: List[int_t] = ListData(ir((15, 3, 1)), RowData)
    force_attract_by_physics_off: bool_t = RowData(18)


class PhysicsOffGroup(DataRow):
    _sign = b'PhysicsOffGroup|eJzLywMAAUwA3Q=='
    sheet_name = 'PhysicsOffGroup'
    group0: int_t = RowData(0)
    group1: int_t = RowData(1)


class PhysicsWind(DataRow):
    _sign = b'PhysicsWind|eJzLywMBAAkMApU='
    sheet_name = 'PhysicsWind'
    threshold: float_t = RowData(0)
    amplitude: float_t = RowData(1)
    amplitude_frequency: float_t = RowData(2)
    power_min: float_t = RowData(3)
    power_max: float_t = RowData(4)
    power_frequency: float_t = RowData(5)


class Picture(DataRow):
    _sign = b'Picture|eJzLywMAAUwA3Q=='
    sheet_name = 'Picture'
    icon: 'Icon' = IconRow(0)
    category: int_t = RowData(1)


class PlaceName(DataRow):
    _sign = b'PlaceName|eJwrzivOAwEQCQAiEgU4'
    sheet_name = 'PlaceName'
    _display = 'text_sgl'
    text_sgl: str_t = RowData(0)
    text_sgg: int_t = RowData(1)
    text_plr: str_t = RowData(2)
    text_plg: int_t = RowData(3)
    text_vow: int_t = RowData(4)
    text_cnt: int_t = RowData(5)
    text_gen: int_t = RowData(6)
    text_def_: int_t = RowData(7)
    text_swt: str_t = RowData(8)
    location_title: int_t = RowData(9)
    priority: int_t = RowData(10)
    show_condition: int_t = RowData(11)


class PlantPotFlowerSeed(DataRow):
    _sign = b'PlantPotFlowerSeed|eJzLy4MCABNfA98='
    sheet_name = 'PlantPotFlowerSeed'
    harvest_icons: List[int_t] = ListData(ir((0, 9, 1)), RowData)


class PlayerSearchLocation(DataRow):
    _sign = b'PlayerSearchLocation|eJzLKwYAAVEA4g=='
    sheet_name = 'PlayerSearchLocation'
    sort_id: int_t = RowData(0)
    name: str_t = RowData(1)


class PlayerSearchSubLocation(DataRow):
    _sign = b'PlayerSearchSubLocation|eJzLy8srLi4GAAkqAqQ='
    sheet_name = 'PlayerSearchSubLocation'
    sort_id: int_t = RowData(0)
    place_name_id: int_t = RowData(1)
    location_name: int_t = RowData(2)
    sub_location_name_name: str_t = RowData(3)
    sub_location_name_global_command: str_t = RowData(4)
    sub_location_name_local_command: str_t = RowData(5)


class PreHandler(DataRow):
    _sign = b'PreHandler|eJwrzoMAAA+oA3Y='
    sheet_name = 'PreHandler'
    _display = 'event_handler'
    text: str_t = RowData(0)
    announce_icon: 'Icon' = IconRow(1)
    event_handler: int_t = RowData(2)
    disclosure_reward_or_quest: 'Quest' = RowForeign(3, 'Quest')
    qualified_talk: 'DefaultTalk' = RowForeign(4, 'DefaultTalk')
    unqualified_talk: 'DefaultTalk' = RowForeign(5, 'DefaultTalk')
    movement: int_t = RowData(6)
    event_situation_icon: int_t = RowData(7)


class PreHandlerMovement(DataRow):
    _sign = b'PreHandlerMovement|eJzLywMAAUwA3Q=='
    sheet_name = 'PreHandlerMovement'
    turn_type: int_t = RowData(0)
    action_timeline: int_t = RowData(1)


class PresetCamera(DataRow):
    _sign = b'PresetCamera|eJzLy0MHAEmMB70='
    sheet_name = 'PresetCamera'
    eid: int_t = RowData(0)
    pos_x: float_t = RowData(1)
    pos_y: float_t = RowData(2)
    pos_z: float_t = RowData(3)
    elezene: float_t = RowData(4)
    lalafell: float_t = RowData(5)
    migote: float_t = RowData(6)
    roegadyn: float_t = RowData(7)
    aura: float_t = RowData(8)
    hrothgar: float_t = RowData(9)
    viera: float_t = RowData(10)
    hyuran__f: float_t = RowData(11)
    elezene__f: float_t = RowData(12)
    lalafell__f: float_t = RowData(13)
    migote__f: float_t = RowData(14)
    roegadyn__f: float_t = RowData(15)
    aura__f: float_t = RowData(16)
    viera__f: float_t = RowData(17)


class PresetCameraAdjust(DataRow):
    _sign = b'PresetCameraAdjust|eJzLy0MBADOfBnM='
    sheet_name = 'PresetCameraAdjust'
    hyuran__m: float_t = RowData(0)
    hyuran__f: float_t = RowData(1)
    elezene__m: float_t = RowData(2)
    elezene__f: float_t = RowData(3)
    lalafell__m: float_t = RowData(4)
    lalafell__f: float_t = RowData(5)
    migote__m: float_t = RowData(6)
    migote__f: float_t = RowData(7)
    roegadyn__m: float_t = RowData(8)
    roegadyn__f: float_t = RowData(9)
    aura__m: float_t = RowData(10)
    aura__f: float_t = RowData(11)
    hrothgar__m: float_t = RowData(12)
    viera__m: float_t = RowData(13)
    viera__f: float_t = RowData(14)


class PreviewableItems(DataRow):
    _sign = b'PreviewableItems|eJzLAwAAbwBv'
    sheet_name = 'PreviewableItems'
    picture: int_t = RowData(0)


class PublicContent(DataRow):
    _sign = b'PublicContent|eJzLy8srzkMGAEIVB1Q='
    sheet_name = 'PublicContent'
    _display = 'text'
    type: int_t = RowData(0)
    time: int_t = RowData(1)
    todo_icon: 'Icon' = IconRow(2)
    text: str_t = RowData(3)
    content_text_start: 'PublicContentTextData' = RowForeign(4, 'PublicContentTextData')
    content_text_end: 'PublicContentTextData' = RowForeign(5, 'PublicContentTextData')
    enter_cutscene: 'PublicContentCutscene' = RowForeign(6, 'PublicContentCutscene')
    exit_rect: int_t = RowData(7)
    return_pos: int_t = RowData(8)
    content_finder_condition: 'ContentFinderCondition' = RowForeign(9, 'ContentFinderCondition')
    data_index: int_t = RowData(10)
    content_attribute_rect: int_t = RowData(11)
    shared_group: int_t = RowData(12)
    content_open_flag: int_t = RowData(13)
    common_content_flag: int_t = RowData(14)
    clear_music: int_t = RowData(15)
    clear_cutscene: 'PublicContentCutscene' = RowForeign(16, 'PublicContentCutscene')


class PublicContentCutscene(DataRow):
    _sign = b'PublicContentCutscene|eJzLywMAAUwA3Q=='
    sheet_name = 'PublicContentCutscene'
    cutscene_id: 'List[Cutscene]' = ListData(ir((0, 2, 1)), RowForeign, 'Cutscene')


class PublicContentTextData(DataRow):
    _sign = b'PublicContentTextData|eJwrBgAAdAB0'
    sheet_name = 'PublicContentTextData'
    _display = 'text'
    text: str_t = RowData(0)


class PublicContentType(DataRow):
    _sign = b'PublicContentType|eJzLAwAAbwBv'
    sheet_name = 'PublicContentType'
    open_flag: int_t = RowData(0)


class PvPAction(DataRow):
    _sign = b'PvPAction|eJzLywOCpKSkPAAS8wO7'
    sheet_name = 'PvPAction'
    _display = 'action'
    action: 'Action' = RowForeign(0, 'Action')
    skill_point: int_t = RowData(1)
    trait: List[int_t] = ListData(ir((2, 3, 1)), RowData)
    grand_company: List[bool_t] = ListData(ir((5, 3, 1)), RowData)
    rank: int_t = RowData(8)


class PvPActionSort(DataRow):
    _sign = b'PvPActionSort|eJzLy0tLywMABk8CFw=='
    sheet_name = 'PvPActionSort'
    id_type: int_t = RowData(0)
    id: int_t = RowData(1)
    is_init_hotbar: bool_t = RowData(2)
    is_hotbar: bool_t = RowData(3)
    q_chat_icon: int_t = RowData(4)


class PvPBaseParamValue(DataRow):
    _sign = b'PvPBaseParamValue|eJzLy8sDAAKXAUs='
    sheet_name = 'PvPBaseParamValue'
    value: List[int_t] = ListData(ir((0, 3, 1)), RowData)


class PvPInitialSelectActionTrait(DataRow):
    _sign = b'PvPInitialSelectActionTrait|eJzLywMCAAZ3Aic='
    sheet_name = 'PvPInitialSelectActionTrait'
    action: List[int_t] = ListData(ir((0, 2, 1)), RowData)
    trait: List[int_t] = ListData(ir((2, 3, 1)), RowData)


class PvPRank(DataRow):
    _sign = b'PvPRank|eJzLAwAAbwBv'
    sheet_name = 'PvPRank'
    point: int_t = RowData(0)


class PvPRankTransient(DataRow):
    _sign = b'PvPRankTransient|eJwrLgYBAAl1ArM='
    sheet_name = 'PvPRankTransient'
    text_pvp_title_male: List[str_t] = ListData(ir((0, 3, 1)), RowData)
    text_pvp_title_female: List[str_t] = ListData(ir((3, 3, 1)), RowData)


class PvPSelectTrait(DataRow):
    _sign = b'PvPSelectTrait|eJwrzssDAAKmAVA='
    sheet_name = 'PvPSelectTrait'
    text: str_t = RowData(0)
    icon: 'Icon' = IconRow(1)
    param: int_t = RowData(2)


class PvPSelectTraitTransient(DataRow):
    _sign = b'PvPSelectTraitTransient|eJwrBgAAdAB0'
    sheet_name = 'PvPSelectTraitTransient'
    text: str_t = RowData(0)


class PvPSeries(DataRow):
    _sign = b'PvPSeries|eJzLyxvkAADlakUv'
    sheet_name = 'PvPSeries'
    max_reward_level: int_t = RowData(0)
    series_reward_item: List[List[int_t]] = ListData(ir(((1, 2, 32), 32, 1)), ListData, RowData)
    series_reward_item_num: List[List[int_t]] = ListData(ir(((65, 2, 32), 32, 1)), ListData, RowData)
    series_reward_achievement: List[int_t] = ListData(ir((129, 32, 1)), RowData)


class PvPSeriesLevel(DataRow):
    _sign = b'PvPSeriesLevel|eJzLAwAAbwBv'
    sheet_name = 'PvPSeriesLevel'
    next_exp: int_t = RowData(0)


class PvPTrait(DataRow):
    _sign = b'PvPTrait|eJzLy8sDAAKXAUs='
    sheet_name = 'PvPTrait'
    trait: 'List[Trait]' = ListData(ir((0, 3, 1)), RowForeign, 'Trait')


class QTE(DataRow):
    _sign = b'QTE|eJzLywOB4uLiNCAoLgYAM5YGbA=='
    sheet_name = 'QTE'
    type: int_t = RowData(0)
    limit_time: int_t = RowData(1)
    param: List[int_t] = ListData(ir((2, 3, 1)), RowData)
    start_se: int_t = RowData(5)
    ready_se: str_t = RowData(6)
    success_se: str_t = RowData(7)
    failure_se: str_t = RowData(8)
    server: bool_t = RowData(9)
    invincible: bool_t = RowData(10)
    camera: bool_t = RowData(11)
    start_screen_image: bool_t = RowData(12)
    text_action: str_t = RowData(13)
    text_flavor: str_t = RowData(14)


class Quest(DataRow):
    _sign = b'Quest|eJwrLs4jDNJgJBAVkwyIsGAUjAIkkDYKRjQY6PQ3FEASBGAXx6EHHLJpaQATKn8z'
    sheet_name = 'Quest'
    _display = 'text'
    text: str_t = RowData(0)
    script: str_t = RowData(1)
    need_ex_version: 'ExVersion' = RowForeign(2, 'ExVersion')
    class_job: 'ClassJobCategory' = RowForeign(3, 'ClassJobCategory')
    class_level: int_t = RowData(4)
    quest_level_offset: int_t = RowData(5)
    class_job2: 'ClassJobCategory' = RowForeign(6, 'ClassJobCategory')
    class_level2: int_t = RowData(7)
    prev_quest_operator: int_t = RowData(8)
    prev_quest: 'List[Quest]' = ListData([9, 11, 12], RowForeign, 'Quest')
    prev_quest_sequence: int_t = RowData(10)
    exclude_quest_operator: int_t = RowData(13)
    exclude_quest: List[int_t] = ListData(ir((14, 2, 1)), RowData)
    acquired_reward: int_t = RowData(16)
    start_town: int_t = RowData(17)
    first_class_operator: int_t = RowData(18)
    first_class: 'ClassJob' = RowForeign(19, 'ClassJob')
    grand_company: 'GrandCompany' = RowForeign(20, 'GrandCompany')
    grand_company_rank: 'GrandCompanyRank' = RowForeign(21, 'GrandCompanyRank')
    instance_content_operator: int_t = RowData(22)
    instance_content: List[int_t] = ListData(ir((23, 3, 1)), RowData)
    festival: 'Festival' = RowForeign(26, 'Festival')
    festival_phase_begin: int_t = RowData(27)
    festival_phase_end: int_t = RowData(28)
    time_begin: int_t = RowData(29)
    time_end: int_t = RowData(30)
    beast_tribe: 'BeastTribe' = RowForeign(31, 'BeastTribe')
    beast_reputation_rank: 'BeastReputationRank' = RowForeign(32, 'BeastReputationRank')
    beast_reputation_value: int_t = RowData(33)
    satisfaction_npc: 'SatisfactionNpc' = RowForeign(34, 'SatisfactionNpc')
    satisfaction_rank: int_t = RowData(35)
    mount: 'Mount' = RowForeign(36, 'Mount')
    house: bool_t = RowData(37)
    delivery_level: 'DeliveryQuest' = RowForeign(38, 'DeliveryQuest')
    client: int_t = RowData(39)
    client_layout: 'Level' = RowForeign(40, 'Level')
    client_behavior: 'Behavior' = RowForeign(41, 'Behavior')
    finish: int_t = RowData(42)
    repeatable: bool_t = RowData(43)
    repeat_cycle: int_t = RowData(44)
    repeat_flag: 'QuestRepeatFlag' = RowForeign(45, 'QuestRepeatFlag')
    introduction: bool_t = RowData(46)
    progress_condition: int_t = RowData(47)
    class_job_supply: 'QuestClassJobSupply' = RowForeign(48, 'QuestClassJobSupply')
    define_name: List[str_t] = ListData(ir((49, 50, 1)), RowData)
    define_value: List[int_t] = ListData(ir((99, 50, 1)), RowData)
    event_listener_sequence: List[int_t] = ListData(ir((149, 64, 1)), RowData)
    event_listener_todo: List[int_t] = ListData(ir((213, 64, 1)), RowData)
    event_listener_listener: List[int_t] = ListData(ir((277, 64, 1)), RowData)
    event_listener_event: List[int_t] = ListData(ir((341, 64, 1)), RowData)
    event_listener_condition_type: List[int_t] = ListData(ir((405, 64, 1)), RowData)
    event_listener_condition_value: List[int_t] = ListData(ir((469, 64, 1)), RowData)
    event_listener_condition_operator: List[int_t] = ListData(ir((533, 64, 1)), RowData)
    event_listener_behavior: List[int_t] = ListData(ir((597, 64, 1)), RowData)
    event_listener_accept_callback: List[bool_t] = ListData(ir((661, 64, 1)), RowData)
    event_listener_announce_callback: List[bool_t] = ListData(ir((725, 64, 1)), RowData)
    event_listener_qualified_callback: List[bool_t] = ListData(ir((789, 64, 1)), RowData)
    event_listener_targeting_possible_callback: List[bool_t] = ListData(ir((853, 64, 1)), RowData)
    event_listener_item_callback: List[bool_t] = ListData(ir((917, 64, 1)), RowData)
    event_listener_movable_flag: List[bool_t] = ListData(ir((981, 64, 1)), RowData)
    event_listener_condition_callback: List[bool_t] = ListData(ir((1045, 64, 1)), RowData)
    event_listener_visible_callback: List[bool_t] = ListData(ir((1109, 64, 1)), RowData)
    quest_todo_todo_sequence: List[int_t] = ListData(ir((1173, 24, 1)), RowData)
    quest_todo_countable_num: List[int_t] = ListData(ir((1197, 24, 1)), RowData)
    quest_todo_marker: List[List[int_t]] = ListData(ir(((1221, 8, 24), 24, 1)), ListData, RowData)
    quest_todo_todo_show_index: List[int_t] = ListData(ir((1413, 24, 1)), RowData)
    exp_base_level_limit: int_t = RowData(1437)
    exp_class: 'ClassJob' = RowForeign(1438, 'ClassJob')
    hide_reward: 'QuestRewardOther' = RowForeign(1439, 'QuestRewardOther')
    reward_exp_bonus: int_t = RowData(1440)
    reward_gil: int_t = RowData(1441)
    reward_company_point_type: 'Item' = RowForeign(1442, 'Item')
    reward_company_point_num: int_t = RowData(1443)
    reward_crystal_type: List[int_t] = ListData(ir((1444, 3, 1)), RowData)
    reward_crystal_num: List[int_t] = ListData(ir((1447, 3, 1)), RowData)
    reward_item_array_type: int_t = RowData(1450)
    reward_item: List[int_t] = ListData(ir((1451, 7, 1)), RowData)
    reward_item_num: List[int_t] = ListData(ir((1458, 7, 1)), RowData)
    reward_item_hq: List[bool_t] = ListData(ir((1465, 7, 1)), RowData)
    reward_item_stain_id: List[int_t] = ListData(ir((1472, 7, 1)), RowData)
    reward_optional_item: List[int_t] = ListData(ir((1479, 5, 1)), RowData)
    reward_optional_item_num: List[int_t] = ListData(ir((1484, 5, 1)), RowData)
    reward_optional_item_hq: List[bool_t] = ListData(ir((1489, 5, 1)), RowData)
    reward_optional_item_stain_id: List[int_t] = ListData(ir((1494, 5, 1)), RowData)
    reward_emote: 'Emote' = RowForeign(1499, 'Emote')
    reward_action: 'Action' = RowForeign(1500, 'Action')
    reward_general_action: List[int_t] = ListData(ir((1501, 2, 1)), RowData)
    reward_trait: int_t = RowData(1503)
    reward_other: 'QuestRewardOther' = RowForeign(1504, 'QuestRewardOther')
    reward_system: List[int_t] = ListData(ir((1505, 2, 1)), RowData)
    reward_instance_content: 'InstanceContent' = RowForeign(1507, 'InstanceContent')
    reward_allagan_tomestone_condition: int_t = RowData(1508)
    reward_allagan_tomestone_type: int_t = RowData(1509)
    reward_allagan_tomestone_num: int_t = RowData(1510)
    reward_beast_reputation_value_num: int_t = RowData(1511)
    area: 'PlaceName' = RowForeign(1512, 'PlaceName')
    genre: 'JournalGenre' = RowForeign(1513, 'JournalGenre')
    journal_type: int_t = RowData(1514)
    header: 'Icon' = IconRow(1515)
    inlay: 'Icon' = IconRow(1516)
    cancellable: bool_t = RowData(1517)
    hide_offer_icon: bool_t = RowData(1518)
    icon_type: 'EventIconType' = RowForeign(1519, 'EventIconType')
    quality: int_t = RowData(1520)
    sort: int_t = RowData(1521)
    zombie: bool_t = RowData(1522)


class Quest(DataRow):
    _sign = b'Quest|eJwrLs4jDNJgJBAVkwyIsGAUjAIkkDYKRjQY6PQ3FEASBGAXx6EHHLJpAJPofs0='
    sheet_name = 'Quest'
    _display = 'text'
    text: str_t = RowData(0)
    script: str_t = RowData(1)
    need_ex_version: 'ExVersion' = RowForeign(2, 'ExVersion')
    class_job: 'ClassJobCategory' = RowForeign(3, 'ClassJobCategory')
    class_level: int_t = RowData(4)
    quest_level_offset: int_t = RowData(5)
    class_job2: 'ClassJobCategory' = RowForeign(6, 'ClassJobCategory')
    class_level2: int_t = RowData(7)
    prev_quest_operator: int_t = RowData(8)
    prev_quest: 'List[Quest]' = ListData([9, 11, 12], RowForeign, 'Quest')
    prev_quest_sequence: int_t = RowData(10)
    exclude_quest_operator: int_t = RowData(13)
    exclude_quest: List[int_t] = ListData(ir((14, 2, 1)), RowData)
    acquired_reward: int_t = RowData(16)
    start_town: int_t = RowData(17)
    first_class_operator: int_t = RowData(18)
    first_class: 'ClassJob' = RowForeign(19, 'ClassJob')
    grand_company: 'GrandCompany' = RowForeign(20, 'GrandCompany')
    grand_company_rank: 'GrandCompanyRank' = RowForeign(21, 'GrandCompanyRank')
    instance_content_operator: int_t = RowData(22)
    instance_content: List[int_t] = ListData(ir((23, 3, 1)), RowData)
    festival: 'Festival' = RowForeign(26, 'Festival')
    festival_phase_begin: int_t = RowData(27)
    festival_phase_end: int_t = RowData(28)
    time_begin: int_t = RowData(29)
    time_end: int_t = RowData(30)
    beast_tribe: 'BeastTribe' = RowForeign(31, 'BeastTribe')
    beast_reputation_rank: 'BeastReputationRank' = RowForeign(32, 'BeastReputationRank')
    beast_reputation_value: int_t = RowData(33)
    satisfaction_npc: 'SatisfactionNpc' = RowForeign(34, 'SatisfactionNpc')
    satisfaction_rank: int_t = RowData(35)
    mount: 'Mount' = RowForeign(36, 'Mount')
    house: bool_t = RowData(37)
    delivery_level: 'DeliveryQuest' = RowForeign(38, 'DeliveryQuest')
    client: int_t = RowData(39)
    client_layout: 'Level' = RowForeign(40, 'Level')
    client_behavior: 'Behavior' = RowForeign(41, 'Behavior')
    finish: int_t = RowData(42)
    repeatable: bool_t = RowData(43)
    repeat_cycle: int_t = RowData(44)
    repeat_flag: 'QuestRepeatFlag' = RowForeign(45, 'QuestRepeatFlag')
    introduction: bool_t = RowData(46)
    progress_condition: int_t = RowData(47)
    class_job_supply: 'QuestClassJobSupply' = RowForeign(48, 'QuestClassJobSupply')
    define_name: List[str_t] = ListData(ir((49, 50, 1)), RowData)
    define_value: List[int_t] = ListData(ir((99, 50, 1)), RowData)
    event_listener_sequence: List[int_t] = ListData(ir((149, 64, 1)), RowData)
    event_listener_todo: List[int_t] = ListData(ir((213, 64, 1)), RowData)
    event_listener_listener: List[int_t] = ListData(ir((277, 64, 1)), RowData)
    event_listener_event: List[int_t] = ListData(ir((341, 64, 1)), RowData)
    event_listener_condition_type: List[int_t] = ListData(ir((405, 64, 1)), RowData)
    event_listener_condition_value: List[int_t] = ListData(ir((469, 64, 1)), RowData)
    event_listener_condition_operator: List[int_t] = ListData(ir((533, 64, 1)), RowData)
    event_listener_behavior: List[int_t] = ListData(ir((597, 64, 1)), RowData)
    event_listener_accept_callback: List[bool_t] = ListData(ir((661, 64, 1)), RowData)
    event_listener_announce_callback: List[bool_t] = ListData(ir((725, 64, 1)), RowData)
    event_listener_qualified_callback: List[bool_t] = ListData(ir((789, 64, 1)), RowData)
    event_listener_targeting_possible_callback: List[bool_t] = ListData(ir((853, 64, 1)), RowData)
    event_listener_item_callback: List[bool_t] = ListData(ir((917, 64, 1)), RowData)
    event_listener_movable_flag: List[bool_t] = ListData(ir((981, 64, 1)), RowData)
    event_listener_condition_callback: List[bool_t] = ListData(ir((1045, 64, 1)), RowData)
    event_listener_visible_callback: List[bool_t] = ListData(ir((1109, 64, 1)), RowData)
    quest_todo_todo_sequence: List[int_t] = ListData(ir((1173, 24, 1)), RowData)
    quest_todo_countable_num: List[int_t] = ListData(ir((1197, 24, 1)), RowData)
    quest_todo_marker: List[List[int_t]] = ListData(ir(((1221, 8, 24), 24, 1)), ListData, RowData)
    quest_todo_todo_show_index: List[int_t] = ListData(ir((1413, 24, 1)), RowData)
    exp_base_level_limit: int_t = RowData(1437)
    exp_class: 'ClassJob' = RowForeign(1438, 'ClassJob')
    hide_reward: 'QuestRewardOther' = RowForeign(1439, 'QuestRewardOther')
    reward_exp_bonus: int_t = RowData(1440)
    reward_gil: int_t = RowData(1441)
    reward_company_point_type: 'Item' = RowForeign(1442, 'Item')
    reward_company_point_num: int_t = RowData(1443)
    reward_crystal_type: List[int_t] = ListData(ir((1444, 3, 1)), RowData)
    reward_crystal_num: List[int_t] = ListData(ir((1447, 3, 1)), RowData)
    reward_item_array_type: int_t = RowData(1450)
    reward_item: List[int_t] = ListData(ir((1451, 7, 1)), RowData)
    reward_item_num: List[int_t] = ListData(ir((1458, 7, 1)), RowData)
    reward_item_hq: List[bool_t] = ListData(ir((1465, 7, 1)), RowData)
    reward_item_stain_id: List[int_t] = ListData(ir((1472, 7, 1)), RowData)
    reward_optional_item: List[int_t] = ListData(ir((1479, 5, 1)), RowData)
    reward_optional_item_num: List[int_t] = ListData(ir((1484, 5, 1)), RowData)
    reward_optional_item_hq: List[bool_t] = ListData(ir((1489, 5, 1)), RowData)
    reward_optional_item_stain_id: List[int_t] = ListData(ir((1494, 5, 1)), RowData)
    reward_emote: 'Emote' = RowForeign(1499, 'Emote')
    reward_action: 'Action' = RowForeign(1500, 'Action')
    reward_general_action: List[int_t] = ListData(ir((1501, 2, 1)), RowData)
    reward_trait: int_t = RowData(1503)
    reward_other: 'QuestRewardOther' = RowForeign(1504, 'QuestRewardOther')
    reward_system: List[int_t] = ListData(ir((1505, 2, 1)), RowData)
    reward_instance_content: 'InstanceContent' = RowForeign(1507, 'InstanceContent')
    reward_allagan_tomestone_condition: int_t = RowData(1508)
    reward_allagan_tomestone_type: int_t = RowData(1509)
    reward_allagan_tomestone_num: int_t = RowData(1510)
    reward_beast_reputation_value_num: int_t = RowData(1511)
    area: 'PlaceName' = RowForeign(1512, 'PlaceName')
    genre: 'JournalGenre' = RowForeign(1513, 'JournalGenre')
    journal_type: int_t = RowData(1514)
    header: 'Icon' = IconRow(1515)
    inlay: 'Icon' = IconRow(1516)
    cancellable: bool_t = RowData(1517)
    hide_offer_icon: bool_t = RowData(1518)
    icon_type: 'EventIconType' = RowForeign(1519, 'EventIconType')
    quality: int_t = RowData(1520)
    sort: int_t = RowData(1521)
    zombie: bool_t = RowData(1522)


class QuestAcceptAdditionCondition(DataRow):
    _sign = b'QuestAcceptAdditionCondition|eJzLy8tLAwAESAGx'
    sheet_name = 'QuestAcceptAdditionCondition'
    addition_condition: 'List[Quest]' = ListData(ir((0, 3, 1)), RowForeign, 'Quest')
    is_qualification_prev_quest: bool_t = RowData(3)


class QuestBattle(DataRow):
    _sign = b'QuestBattle|eJzLy8vLKx4mIG+YAADwZ7GB'
    sheet_name = 'QuestBattle'
    quest: int_t = RowData(0)
    sub_no: int_t = RowData(1)
    limit_time: int_t = RowData(2)
    sync_level: int_t = RowData(3)
    define_define_name: List[str_t] = ListData(ir((4, 200, 1)), RowData)
    define_define_value: List[int_t] = ListData(ir((204, 200, 1)), RowData)


class QuestBattleResident(DataRow):
    _sign = b'QuestBattleResident|eJzLAwAAbwBv'
    sheet_name = 'QuestBattleResident'
    content_finder_condition: int_t = RowData(0)


class QuestBattleSystemDefine(DataRow):
    _sign = b'QuestBattleSystemDefine|eJwrzgMAAVYA4g=='
    sheet_name = 'QuestBattleSystemDefine'
    define_name: str_t = RowData(0)
    define_value: int_t = RowData(1)


class QuestChapter(DataRow):
    _sign = b'QuestChapter|eJzLywMAAUwA3Q=='
    sheet_name = 'QuestChapter'
    _display = 'quest'
    quest: 'Quest' = RowForeign(0, 'Quest')
    chapter: 'QuestRedoChapter' = RowForeign(1, 'QuestRedoChapter')


class QuestClassJobReward(DataRow):
    _sign = b'QuestClassJobReward|eJzLy0MDSVAAAIoPCl8='
    sheet_name = 'QuestClassJobReward'
    class_job_category: 'ClassJobCategory' = RowForeign(0, 'ClassJobCategory')
    item: List[int_t] = ListData(ir((1, 4, 1)), RowData)
    item_num: List[int_t] = ListData(ir((5, 4, 1)), RowData)
    remove_item: List[int_t] = ListData(ir((9, 4, 1)), RowData)
    remove_item_num: List[int_t] = ListData(ir((13, 4, 1)), RowData)
    remove_item_need_equip: List[bool_t] = ListData(ir((17, 4, 1)), RowData)
    remove_item_need_accept: List[bool_t] = ListData(ir((21, 4, 1)), RowData)


class QuestClassJobSupply(DataRow):
    _sign = b'QuestClassJobSupply|eJzLywOCNAAJBAKN'
    sheet_name = 'QuestClassJobSupply'
    class_job_category: 'ClassJobCategory' = RowForeign(0, 'ClassJobCategory')
    sequence: int_t = RowData(1)
    supply_target: 'ENpcResident' = RowForeign(2, 'ENpcResident')
    supply_item: 'Item' = RowForeign(3, 'Item')
    supply_item_num: int_t = RowData(4)
    is_hq: bool_t = RowData(5)


class QuestCustomTodo(DataRow):
    _sign = b'QuestCustomTodo|eJzLywMAAUwA3Q=='
    sheet_name = 'QuestCustomTodo'
    work_index: int_t = RowData(0)
    value_max: int_t = RowData(1)


class QuestDefineClient(DataRow):
    _sign = b'QuestDefineClient|eJwrzgMAAVYA4g=='
    sheet_name = 'QuestDefineClient'
    name: str_t = RowData(0)
    value: int_t = RowData(1)


class QuestDerivedClass(DataRow):
    _sign = b'QuestDerivedClass|eJzLAwAAbwBv'
    sheet_name = 'QuestDerivedClass'
    _display = 'client_derived_class'
    client_derived_class: 'ClassJob' = RowForeign(0, 'ClassJob')


class QuestEffect(DataRow):
    _sign = b'QuestEffect|eJzLy4MBABesBE0='
    sheet_name = 'QuestEffect'
    details_effect_type: List[int_t] = ListData(ir((0, 4, 1)), RowData)
    details_effect_id: List[int_t] = ListData(ir((4, 4, 1)), RowData)
    warning_range_log: int_t = RowData(8)
    out_of_range_log: int_t = RowData(9)


class QuestEffectDefine(DataRow):
    _sign = b'QuestEffectDefine|eJzLAwAAbwBv'
    sheet_name = 'QuestEffectDefine'
    _display = 'quest_effect'
    quest_effect: 'QuestEffect' = RowForeign(0, 'QuestEffect')


class QuestEffectType(DataRow):
    _sign = b'QuestEffectType|eJzLAwAAbwBv'
    sheet_name = 'QuestEffectType'
    num_0: int_t = RowData(0)


class QuestEquipModel(DataRow):
    _sign = b'QuestEquipModel|eJzLywMAAUwA3Q=='
    sheet_name = 'QuestEquipModel'
    slot: int_t = RowData(0)
    model_id: int_t = RowData(1)


class QuestEventAreaEntranceInfo(DataRow):
    _sign = b'QuestEventAreaEntranceInfo|eJzLy8sDAAKXAUs='
    sheet_name = 'QuestEventAreaEntranceInfo'


class QuestHideReward(DataRow):
    _sign = b'QuestHideReward|eJxLAwAAZwBn'
    sheet_name = 'QuestHideReward'
    dummy: bool_t = RowData(0)


class QuestLinkMarker(DataRow):
    _sign = b'QuestLinkMarker|eJzLy8vLSwMABm8CHw=='
    sheet_name = 'QuestLinkMarker'
    map: int_t = RowData(0)
    target_layout: int_t = RowData(1)
    link_map: int_t = RowData(2)
    is_public: bool_t = RowData(4)


class QuestLinkMarker(DataRow):
    _sign = b'QuestLinkMarker|eJzLy8tLAwAESAGx'
    sheet_name = 'QuestLinkMarker'
    map: int_t = RowData(0)
    target_layout: int_t = RowData(1)
    link_map: int_t = RowData(2)
    is_public: bool_t = RowData(3)


class QuestLinkMarkerIcon(DataRow):
    _sign = b'QuestLinkMarkerIcon|eJzLAwAAbwBv'
    sheet_name = 'QuestLinkMarkerIcon'


class QuestLinkMarkerSet(DataRow):
    _sign = b'QuestLinkMarkerSet|eJzLy8vLS0sDAAj0AoU='
    sheet_name = 'QuestLinkMarkerSet'
    link_marker: int_t = RowData(0)
    quest: int_t = RowData(1)
    sequence_begin: int_t = RowData(2)
    sequence_end: int_t = RowData(3)


class QuestLinkMarkerSet(DataRow):
    _sign = b'QuestLinkMarkerSet|eJzLywMCAAZ3Aic='
    sheet_name = 'QuestLinkMarkerSet'
    link_marker: int_t = RowData(0)
    quest: int_t = RowData(1)
    sequence_begin: int_t = RowData(2)
    sequence_end: int_t = RowData(3)
    offer_target_layout: int_t = RowData(4)


class QuestRecomplete(DataRow):
    _sign = b'QuestRecomplete|eJzLAwAAbwBv'
    sheet_name = 'QuestRecomplete'
    work_index: int_t = RowData(0)


class QuestRedo(DataRow):
    _sign = b'QuestRedo|eJzLy6McAADwfR05'
    sheet_name = 'QuestRedo'
    quest_condition: 'List[Quest]' = ListData(ir((0, 2, 1)), RowForeign, 'Quest')
    next_redo: int_t = RowData(2)
    chapter: 'QuestRedoChapter' = RowForeign(3, 'QuestRedoChapter')
    redo_detail_quest: List[int_t] = ListData(ir((4, 32, 1)), RowData)
    redo_detail_route: List[int_t] = ListData(ir((36, 32, 1)), RowData)


class QuestRedoChapter(DataRow):
    _sign = b'QuestRedoChapter|eJzLy8sDAAKXAUs='
    sheet_name = 'QuestRedoChapter'
    category: int_t = RowData(0)
    order_in_category: int_t = RowData(1)
    incomp_chapter: int_t = RowData(2)


class QuestRedoChapterUI(DataRow):
    _sign = b'QuestRedoChapterUI|eJzLy4OA4uJiAByFBMo='
    sheet_name = 'QuestRedoChapterUI'
    _display = 'disclosure_reward_or_quest'
    disclosure_reward_or_quest: 'Quest' = RowForeign(0, 'Quest')
    disclosure_reward_or_quest2: int_t = RowData(1)
    tab_category: 'QuestRedoChapterUITab' = RowForeign(2, 'QuestRedoChapterUITab')
    group_category: 'QuestRedoChapterUICategory' = RowForeign(3, 'QuestRedoChapterUICategory')
    priority: int_t = RowData(4)
    icon_small: 'Icon' = IconRow(5)
    icon_large: 'Icon' = IconRow(6)
    icon_large_bg: 'Icon' = IconRow(7)
    text_title: str_t = RowData(8)
    text_title_short: str_t = RowData(9)
    text_detail: str_t = RowData(10)


class QuestRedoChapterUICategory(DataRow):
    _sign = b'QuestRedoChapterUICategory|eJzLKwYAAVEA4g=='
    sheet_name = 'QuestRedoChapterUICategory'
    _display = 'text'
    priority: int_t = RowData(0)
    text: str_t = RowData(1)


class QuestRedoChapterUITab(DataRow):
    _sign = b'QuestRedoChapterUITab|eJzLy8srBgAEVQG+'
    sheet_name = 'QuestRedoChapterUITab'
    _display = 'text'
    prio: int_t = RowData(0)
    icon: 'Icon' = IconRow(1)
    icon_selected: 'Icon' = IconRow(2)
    text: str_t = RowData(3)


class QuestRedoIncompChapter(DataRow):
    _sign = b'QuestRedoIncompChapter|eJzLAwAAbwBv'
    sheet_name = 'QuestRedoIncompChapter'
    _display = 'incomp_chapter'
    incomp_chapter: 'QuestRedoChapter' = RowForeign(0, 'QuestRedoChapter')


class QuestRepeatFlag(DataRow):
    _sign = b'QuestRepeatFlag|eJzLAwAAbwBv'
    sheet_name = 'QuestRepeatFlag'
    _display = 'quest'
    quest: int_t = RowData(0)


class QuestRewardOther(DataRow):
    _sign = b'QuestRewardOther|eJzLKwYAAVEA4g=='
    sheet_name = 'QuestRewardOther'
    _display = 'name'
    icon: 'Icon' = IconRow(0)
    name: str_t = RowData(1)


class QuestSelectTitle(DataRow):
    _sign = b'QuestSelectTitle|eJzLAwAAbwBv'
    sheet_name = 'QuestSelectTitle'
    addon_text: int_t = RowData(0)


class QuestSetDefine(DataRow):
    _sign = b'QuestSetDefine|eJzLAwAAbwBv'
    sheet_name = 'QuestSetDefine'
    value: int_t = RowData(0)


class QuestStatusParam(DataRow):
    _sign = b'QuestStatusParam|eJzLy8sDAAKXAUs='
    sheet_name = 'QuestStatusParam'
    status: int_t = RowData(0)
    system_type: int_t = RowData(1)
    system_arg: int_t = RowData(2)


class QuestSystemDefine(DataRow):
    _sign = b'QuestSystemDefine|eJwrzgMAAVYA4g=='
    sheet_name = 'QuestSystemDefine'
    define_name: str_t = RowData(0)
    define_value: int_t = RowData(1)


class QuickChat(DataRow):
    _sign = b'QuickChat|eJwrzgMCAAaQAiw='
    sheet_name = 'QuickChat'
    text: str_t = RowData(0)
    icon: 'Icon' = IconRow(1)
    addon: 'Addon' = RowForeign(2, 'Addon')
    sort_id: 'QuickChatTransient' = RowForeign(3, 'QuickChatTransient')
    valid_index: int_t = RowData(4)


class QuickChatTransient(DataRow):
    _sign = b'QuickChatTransient|eJwrBgAAdAB0'
    sheet_name = 'QuickChatTransient'
    _display = 'text'
    text: str_t = RowData(0)


class RPParameter(DataRow):
    _sign = b'RPParameter|eJzLy8sDAAKXAUs='
    sheet_name = 'RPParameter'
    _display = 'name_id'
    name_id: 'BNpcName' = RowForeign(0, 'BNpcName')
    class_job: 'ClassJob' = RowForeign(1, 'ClassJob')
    sex: int_t = RowData(2)


class Race(DataRow):
    _sign = b'Race|eJwrLs6DAwAiAwUz'
    sheet_name = 'Race'
    _display = 'text_name_female'
    text_name: str_t = RowData(0)
    text_name_female: str_t = RowData(1)
    body: 'List[Item]' = ListData(ir((2, 2, 4)), RowForeign, 'Item')
    hand: 'List[Item]' = ListData(ir((3, 2, 4)), RowForeign, 'Item')
    leg: 'List[Item]' = ListData(ir((4, 2, 4)), RowForeign, 'Item')
    foot: 'List[Item]' = ListData(ir((5, 2, 4)), RowForeign, 'Item')
    size: int_t = RowData(10)
    need_ex_version: 'ExVersion' = RowForeign(11, 'ExVersion')


class RacingChocoboGrade(DataRow):
    _sign = b'RacingChocoboGrade|eJzLAwAAbwBv'
    sheet_name = 'RacingChocoboGrade'
    cross_gil: int_t = RowData(0)


class RacingChocoboItem(DataRow):
    _sign = b'RacingChocoboItem|eJzLy8vLAwAEUAG5'
    sheet_name = 'RacingChocoboItem'
    _display = 'item'
    item: 'Item' = RowForeign(0, 'Item')
    type: int_t = RowData(1)
    arg: List[int_t] = ListData(ir((2, 2, 1)), RowData)


class RacingChocoboName(DataRow):
    _sign = b'RacingChocoboName|eJwrBgAAdAB0'
    sheet_name = 'RacingChocoboName'
    _display = 'text'
    text: str_t = RowData(0)


class RacingChocoboNameCategory(DataRow):
    _sign = b'RacingChocoboNameCategory|eJzLKwYAAVEA4g=='
    sheet_name = 'RacingChocoboNameCategory'
    _display = 'text'
    sort_id: int_t = RowData(0)
    text: str_t = RowData(1)


class RacingChocoboNameInfo(DataRow):
    _sign = b'RacingChocoboNameInfo|eJzLSwKCvLw8AA54A0E='
    sheet_name = 'RacingChocoboNameInfo'
    category: 'RacingChocoboNameCategory' = RowForeign(0, 'RacingChocoboNameCategory')
    filter: List[bool_t] = ListData(ir((1, 4, 1)), RowData)
    sort_id: List[int_t] = ListData(ir((5, 3, 1)), RowData)


class RacingChocoboParam(DataRow):
    _sign = b'RacingChocoboParam|eJwrBgAAdAB0'
    sheet_name = 'RacingChocoboParam'
    _display = 'name'
    name: str_t = RowData(0)


class RaidFinderParam(DataRow):
    _sign = b'RaidFinderParam|eJxLAwAAZwBn'
    sheet_name = 'RaidFinderParam'
    healer_matching_group_check: bool_t = RowData(0)


class ReactionEventObject(DataRow):
    _sign = b'ReactionEventObject|eJzLywMAAUwA3Q=='
    sheet_name = 'ReactionEventObject'
    object_info: int_t = RowData(0)
    layout_id: int_t = RowData(1)


class ReactionEventObjectInfo(DataRow):
    _sign = b'ReactionEventObjectInfo|eJzLAwAAbwBv'
    sheet_name = 'ReactionEventObjectInfo'
    base_id: int_t = RowData(0)


class RecastNavimesh(DataRow):
    _sign = b'RecastNavimesh|eJwrzoOANDBCByChNAANzQ7w'
    sheet_name = 'RecastNavimesh'
    field_0: str_t = RowData(0)
    tile_size: float_t = RowData(1)
    cell_size: float_t = RowData(2)
    cell_height: float_t = RowData(3)
    agent_height: float_t = RowData(4)
    agent_radius: float_t = RowData(5)
    agent_max_climb: float_t = RowData(6)
    agent_max_slope: float_t = RowData(7)
    field_8: bool_t = RowData(8)
    region_min_size: float_t = RowData(9)
    region_merged_size: float_t = RowData(10)
    field_11: bool_t = RowData(11)
    max_edge_length: float_t = RowData(12)
    max_edge_error: float_t = RowData(13)
    verts_per_poly: float_t = RowData(14)
    detail_mesh_sample_distance: float_t = RowData(15)
    detail_mesh_max_sample_error: float_t = RowData(16)
    field_17: float_t = RowData(17)
    field_18: float_t = RowData(18)
    field_19: float_t = RowData(19)
    field_20: float_t = RowData(20)
    field_21: float_t = RowData(21)
    field_22: float_t = RowData(22)
    field_23: float_t = RowData(23)
    field_24: float_t = RowData(24)
    field_25: float_t = RowData(25)
    field_26: float_t = RowData(26)
    field_27: float_t = RowData(27)
    field_28: float_t = RowData(28)
    field_29: float_t = RowData(29)
    field_30: bool_t = RowData(30)
    field_31: float_t = RowData(31)
    field_32: float_t = RowData(32)
    field_33: float_t = RowData(33)
    field_34: bool_t = RowData(34)


class Recipe(DataRow):
    _sign = b'Recipe|eJzLy8MF0pDZaWkgAsgCAPe/FHE='
    sheet_name = 'Recipe'
    _display = 'craft_item_id'
    number: int_t = RowData(0)
    craft_type: 'CraftType' = RowForeign(1, 'CraftType')
    level: 'RecipeLevelTable' = RowForeign(2, 'RecipeLevelTable')
    craft_item_id: 'Item' = RowForeign(3, 'Item')
    craft_num: int_t = RowData(4)
    material_item_id: List[int_t] = ListData(ir((5, 8, 2)), RowData)
    material_num: List[int_t] = ListData(ir((6, 8, 2)), RowData)
    crystal_type: List[int_t] = ListData(ir((21, 2, 2)), RowData)
    crystal_num: List[int_t] = ListData(ir((22, 2, 2)), RowData)
    category: 'RecipeNotebookList' = RowForeign(25, 'RecipeNotebookList')
    sub: bool_t = RowData(26)
    initial_quality_limit_rate: int_t = RowData(27)
    work_rate: int_t = RowData(28)
    quality_rate: int_t = RowData(29)
    material_point_rate: int_t = RowData(30)
    min_quality_for_nq: int_t = RowData(31)
    need_craftmanship: int_t = RowData(32)
    need_control: int_t = RowData(33)
    need_auto_craftmanship: int_t = RowData(34)
    need_auto_control: int_t = RowData(35)
    need_secret_recipe_book: 'SecretRecipeBook' = RowForeign(36, 'SecretRecipeBook')
    need_complete_quest: 'Quest' = RowForeign(37, 'Quest')
    can_auto_craft: bool_t = RowData(38)
    can_hq: bool_t = RowData(39)
    can_add_exp: bool_t = RowData(40)
    need_status: 'Status' = RowForeign(41, 'Status')
    need_equip_item: 'Item' = RowForeign(42, 'Item')
    meister: bool_t = RowData(43)
    high_difficulty: bool_t = RowData(44)
    collectables_refine_type: int_t = RowData(45)
    collectables_refine: int_t = RowData(46)
    added_version: int_t = RowData(47)


class RecipeLevelTable(DataRow):
    _sign = b'RecipeLevelTable|eJzLy0MAACGQBSk='
    sheet_name = 'RecipeLevelTable'
    ui_level: int_t = RowData(0)
    difficulty: int_t = RowData(1)
    productivity: int_t = RowData(2)
    technique: int_t = RowData(3)
    work_max: int_t = RowData(4)
    quality_max: int_t = RowData(5)
    progress_difficulty_rate: int_t = RowData(6)
    quality_difficulty_rate: int_t = RowData(7)
    below_level_progress_rate: int_t = RowData(8)
    below_level_quality_rate: int_t = RowData(9)
    material_point: int_t = RowData(10)
    recipe_material_state_pattern: int_t = RowData(11)


class RecipeLookup(DataRow):
    _sign = b'RecipeLookup|eJzLy4MAAA+AA3E='
    sheet_name = 'RecipeLookup'
    craft: 'List[Recipe]' = ListData(ir((0, 8, 1)), RowForeign, 'Recipe')


class RecipeNotebookList(DataRow):
    _sign = b'RecipeNotebookList|eJzLyxvkAADlakUv'
    sheet_name = 'RecipeNotebookList'
    recipe_num: int_t = RowData(0)
    recipe_id: List[int_t] = ListData(ir((1, 160, 1)), RowData)


class RecommendContents(DataRow):
    _sign = b'RecommendContents|eJzLy8vLAwAEUAG5'
    sheet_name = 'RecommendContents'
    _display = 'layout_id'
    layout_id: 'Level' = RowForeign(0, 'Level')
    class_job: 'ClassJob' = RowForeign(1, 'ClassJob')
    lv_min: int_t = RowData(2)
    lv_max: int_t = RowData(3)


class Relic(DataRow):
    _sign = b'Relic|eJzLy0MFADqABuE='
    sheet_name = 'Relic'
    _display = 'exchange_item'
    item: 'Item' = RowForeign(0, 'Item')
    exchange_item: 'Item' = RowForeign(1, 'Item')
    icon: 'Icon' = IconRow(2)
    materia: 'List[Materia]' = ListData([3, 7, 11, 14], RowForeign, 'Materia')
    main_note: 'List[RelicNote]' = ListData(ir((4, 3, 1)), RowForeign, 'RelicNote')
    sub_note: 'List[RelicNote]' = ListData(ir((8, 3, 1)), RowForeign, 'RelicNote')
    selection_a_note: 'List[RelicNote]' = ListData(ir((12, 2, 1)), RowForeign, 'RelicNote')
    selection_b_note: 'RelicNote' = RowForeign(15, 'RelicNote')


class Relic3(DataRow):
    _sign = b'Relic3|eJzLywMBAAkMApU='
    sheet_name = 'Relic3'
    _display = 'exchange_item'
    base_item: 'Item' = RowForeign(0, 'Item')
    synthetic_item: 'Item' = RowForeign(1, 'Item')
    strengthening_max: int_t = RowData(2)
    exchange_item: 'Item' = RowForeign(3, 'Item')
    icon: 'Icon' = IconRow(4)
    type: int_t = RowData(5)


class Relic3Materia(DataRow):
    _sign = b'Relic3Materia|eJzLy4MCABNfA98='
    sheet_name = 'Relic3Materia'
    materia: int_t = RowData(0)
    materia_type: List[int_t] = ListData(ir((1, 5, 1)), RowData)
    rate_pattern: List[int_t] = ListData(ir((6, 3, 1)), RowData)


class Relic3Rate(DataRow):
    _sign = b'Relic3Rate|eJzLy4MCABNfA98='
    sheet_name = 'Relic3Rate'
    pattern: List[int_t] = ListData(ir((0, 9, 1)), RowData)


class Relic3RatePattern(DataRow):
    _sign = b'Relic3RatePattern|eJzLy8sDAAKXAUs='
    sheet_name = 'Relic3RatePattern'
    rank_up_num: List[int_t] = ListData(ir((0, 3, 1)), RowData)


class Relic6Magicite(DataRow):
    _sign = b'Relic6Magicite|eJwrLs7LAwAEcwHD'
    sheet_name = 'Relic6Magicite'
    text_0: str_t = RowData(0)
    text_1: str_t = RowData(1)
    num_2: int_t = RowData(2)
    num_3: int_t = RowData(3)


class RelicItem(DataRow):
    _sign = b'RelicItem|eJzLy0MDAEHPB08='
    sheet_name = 'RelicItem'
    type: int_t = RowData(0)
    items_catalog_id: 'List[Item]' = ListData(ir((1, 16, 1)), RowForeign, 'Item')


class RelicMateria(DataRow):
    _sign = b'RelicMateria|eJzLAwAAbwBv'
    sheet_name = 'RelicMateria'
    grade_max: int_t = RowData(0)


class RelicNote(DataRow):
    _sign = b'RelicNote|eJzLyyMEAP/MDp0='
    sheet_name = 'RelicNote'
    event_item: 'EventItem' = RowForeign(0, 'EventItem')
    target: List[int_t] = ListData(ir((1, 10, 2)), RowData)
    needed_kills: List[int_t] = ListData(ir((2, 10, 2)), RowData)
    boss: List[int_t] = ListData(ir((21, 4, 1)), RowData)
    fate: List[int_t] = ListData(ir((25, 3, 2)), RowData)
    fate_territory_type: List[int_t] = ListData(ir((26, 3, 2)), RowData)
    guild_leve: List[int_t] = ListData(ir((31, 3, 1)), RowData)


class RelicNoteCategory(DataRow):
    _sign = b'RelicNoteCategory|eJzLKwYAAVEA4g=='
    sheet_name = 'RelicNoteCategory'
    _display = 'text'
    ui_priority: int_t = RowData(0)
    text: str_t = RowData(1)


class Resident(DataRow):
    _sign = b'Resident|eJzLywMCAAZ3Aic='
    sheet_name = 'Resident'
    type: int_t = RowData(0)
    value: int_t = RowData(1)
    model: 'NpcYell' = RowForeign(2, 'NpcYell')
    customize: int_t = RowData(3)
    resident_motion_type: 'ResidentMotionType' = RowForeign(4, 'ResidentMotionType')


class ResidentMotionType(DataRow):
    _sign = b'ResidentMotionType|eJwrLoYAABA0A5k='
    sheet_name = 'ResidentMotionType'
    motion: List[str_t] = ListData(ir((0, 8, 1)), RowData)


class ResistanceWeaponAdjust(DataRow):
    _sign = b'ResistanceWeaponAdjust|eJzLy4MAAA+AA3E='
    sheet_name = 'ResistanceWeaponAdjust'
    param_total: int_t = RowData(0)
    sub_param_max: int_t = RowData(1)
    sub_param: List[int_t] = ListData(ir((2, 4, 1)), RowData)
    inlay_icon: 'Icon' = IconRow(6)
    ui_progress: int_t = RowData(7)


class RetainerFortuneRewardRange(DataRow):
    _sign = b'RetainerFortuneRewardRange|eJzLAwAAbwBv'
    sheet_name = 'RetainerFortuneRewardRange'
    next_exp_multiple: int_t = RowData(0)


class RetainerTask(DataRow):
    _sign = b'RetainerTask|eJxLy0MGACy8Bf0='
    sheet_name = 'RetainerTask'
    is_random: bool_t = RowData(0)
    category: 'ClassJobCategory' = RowForeign(1, 'ClassJobCategory')
    level: int_t = RowData(2)
    sort_key: int_t = RowData(3)
    number_hq_req_param: 'RetainerTaskParameter' = RowForeign(4, 'RetainerTaskParameter')
    tip_cost: int_t = RowData(5)
    time: int_t = RowData(6)
    exp: int_t = RowData(7)
    cond_item_lv: int_t = RowData(8)
    cond_param_a: int_t = RowData(9)
    cond_param_b: int_t = RowData(10)
    param_a: int_t = RowData(11)
    param_b: int_t = RowData(12)
    task_num: int_t = RowData(13)


class RetainerTaskLvRange(DataRow):
    _sign = b'RetainerTaskLvRange|eJzLywMAAUwA3Q=='
    sheet_name = 'RetainerTaskLvRange'
    min_lv: int_t = RowData(0)
    max_lv: int_t = RowData(1)


class RetainerTaskNormal(DataRow):
    _sign = b'RetainerTaskNormal|eJzLy4MAAA+AA3E='
    sheet_name = 'RetainerTaskNormal'
    _display = 'item'
    item: 'Item' = RowForeign(0, 'Item')
    stack: List[int_t] = ListData(ir((1, 5, 1)), RowData)
    gathering_item: 'GatheringItem' = RowForeign(6, 'GatheringItem')
    fish_parameter_or_spearfishing_item: int_t = RowData(7)


class RetainerTaskParameter(DataRow):
    _sign = b'RetainerTaskParameter|eJzLy0MAACGQBSk='
    sheet_name = 'RetainerTaskParameter'
    battle_stack: List[int_t] = ListData(ir((0, 4, 1)), RowData)
    gathering_stack: List[int_t] = ListData(ir((4, 4, 1)), RowData)
    fishing_stack: List[int_t] = ListData(ir((8, 4, 1)), RowData)


class RetainerTaskParameterLvDiff(DataRow):
    _sign = b'RetainerTaskParameterLvDiff|eJzLywMAAUwA3Q=='
    sheet_name = 'RetainerTaskParameterLvDiff'
    time_correction_normal: int_t = RowData(0)
    time_correction_random: int_t = RowData(1)


class RetainerTaskRandom(DataRow):
    _sign = b'RetainerTaskRandom|eJwrzgMAAVYA4g=='
    sheet_name = 'RetainerTaskRandom'
    _display = 'text'
    text: str_t = RowData(0)
    sort_id: int_t = RowData(1)


class RideShooting(DataRow):
    _sign = b'RideShooting|eJzLyxsIAADJ8TK1'
    sheet_name = 'RideShooting'
    scheduler: 'GFateRideShooting' = RowForeign(0, 'GFateRideShooting')
    player_offset_y: int_t = RowData(1)
    shoot_offset_y: int_t = RowData(2)
    shot_vfx: int_t = RowData(3)
    shot_speed: int_t = RowData(4)
    shoot_guide_text: 'RideShootingTextData' = RowForeign(5, 'RideShootingTextData')
    lively_layout: List[int_t] = ListData(ir((6, 8, 1)), RowData)
    lively_pop_range: List[int_t] = ListData(ir((14, 8, 1)), RowData)
    lively_actor: List[List[int_t]] = ListData(ir(((22, 6, 16), 8, 1)), ListData, RowData)
    lively_actor_pop_rate: List[List[int_t]] = ListData(ir(((30, 6, 16), 8, 1)), ListData, RowData)


class RideShootingScheduler(DataRow):
    _sign = b'RideShootingScheduler|eJzLywMCAAZ3Aic='
    sheet_name = 'RideShootingScheduler'
    event: int_t = RowData(0)
    param: List[int_t] = ListData(ir((1, 4, 1)), RowData)


class RideShootingTarget(DataRow):
    _sign = b'RideShootingTarget|eJzLywMBAAkMApU='
    sheet_name = 'RideShootingTarget'
    type: int_t = RowData(0)
    move_type: int_t = RowData(1)
    move_param: List[int_t] = ListData(ir((2, 3, 1)), RowData)
    life_time: int_t = RowData(5)


class RideShootingTargetScheduler(DataRow):
    _sign = b'RideShootingTargetScheduler|eJzLy4MAAA+AA3E='
    sheet_name = 'RideShootingTargetScheduler'
    event: int_t = RowData(0)
    param: List[int_t] = ListData(ir((1, 2, 1)), RowData)
    target_group: int_t = RowData(3)
    target: List[int_t] = ListData(ir((4, 4, 1)), RowData)


class RideShootingTargetType(DataRow):
    _sign = b'RideShootingTargetType|eJzLywMBAAkMApU='
    sheet_name = 'RideShootingTargetType'
    e_obj: 'EObj' = RowForeign(0, 'EObj')
    score: int_t = RowData(1)
    collision_offset_x: int_t = RowData(2)
    collision_offset_y: int_t = RowData(3)
    collision_offset_z: int_t = RowData(4)
    collision_radius: int_t = RowData(5)


class RideShootingTextData(DataRow):
    _sign = b'RideShootingTextData|eJwrBgAAdAB0'
    sheet_name = 'RideShootingTextData'
    _display = 'text'
    text: str_t = RowData(0)


class Role(DataRow):
    _sign = b'Role|eJzLAwAAbwBv'
    sheet_name = 'Role'
    type: int_t = RowData(0)


class SE(DataRow):
    _sign = b'SE|eJwrBgAAdAB0'
    sheet_name = 'SE'
    path: str_t = RowData(0)


class SEBattle(DataRow):
    _sign = b'SEBattle|eJwrBgAAdAB0'
    sheet_name = 'SEBattle'
    path: str_t = RowData(0)


class SatisfactionArbitration(DataRow):
    _sign = b'SatisfactionArbitration|eJzLy8vLAwAEUAG5'
    sheet_name = 'SatisfactionArbitration'
    _display = 'story_quest'
    rank_condition: int_t = RowData(0)
    rank_operator: 'SatisfactionNpc' = RowForeign(1, 'SatisfactionNpc')
    story_quest: 'Quest' = RowForeign(2, 'Quest')
    story_quest_condition: int_t = RowData(3)


class SatisfactionBonusGuarantee(DataRow):
    _sign = b'SatisfactionBonusGuarantee|eJzLywMBAAkMApU='
    sheet_name = 'SatisfactionBonusGuarantee'
    crafter_bonus: List[int_t] = ListData(ir((0, 2, 1)), RowData)
    miner_harvester_bonus: List[int_t] = ListData(ir((2, 2, 1)), RowData)
    fisherman_bonus: List[int_t] = ListData(ir((4, 2, 1)), RowData)


class SatisfactionNpc(DataRow):
    _sign = b'SatisfactionNpc|eJzLy8MNksCAVBEEAAAKRSax'
    sheet_name = 'SatisfactionNpc'
    _display = 'enpc_id'
    enpc_id: 'ENpcResident' = RowForeign(0, 'ENpcResident')
    accept_quest: 'Quest' = RowForeign(1, 'Quest')
    supply_limit_level: int_t = RowData(2)
    weekly_supply_count_max: int_t = RowData(3)
    satisfaction_rank_supply_list: List[int_t] = ListData(ir((4, 6, 1)), RowData)
    satisfaction_rank_rankup_point: List[int_t] = ListData(ir((10, 6, 1)), RowData)
    satisfaction_rank_reward_item: List[List[int_t]] = ListData(ir(((16, 3, 18), 6, 1)), ListData, RowData)
    satisfaction_rank_reward_num: List[List[int_t]] = ListData(ir(((22, 3, 18), 6, 1)), ListData, RowData)
    satisfaction_rank_reward_hq: List[List[bool_t]] = ListData(ir(((28, 3, 18), 6, 1)), ListData, RowData)
    satisfaction_npc_ui_detail_face: List[Icon] = ListData(ir((70, 6, 1)), IconRow)
    satisfaction_npc_ui_detail_signature: List[int_t] = ListData(ir((76, 6, 1)), RowData)
    satisfaction_npc_ui_detail_quest: List[int_t] = ListData(ir((82, 6, 1)), RowData)
    face_icon: int_t = RowData(88)
    dress_up_work_index: int_t = RowData(89)
    arbitration_gather_crafter: int_t = RowData(90)
    arbitration_battle: int_t = RowData(91)


class SatisfactionSupply(DataRow):
    _sign = b'SatisfactionSupply|eJzLywODtLw8ABeUBEU='
    sheet_name = 'SatisfactionSupply'
    _display = 'need_item'
    slot: int_t = RowData(0)
    rate: int_t = RowData(1)
    need_item: 'Item' = RowForeign(2, 'Item')
    refine_threshold: List[int_t] = ListData(ir((3, 3, 1)), RowData)
    supply_reward: 'SatisfactionSupplyReward' = RowForeign(6, 'SatisfactionSupplyReward')
    is_bonus: bool_t = RowData(7)
    fishing_spot_data: int_t = RowData(8)
    spearfishing_spot_data: int_t = RowData(9)


class SatisfactionSupplyReward(DataRow):
    _sign = b'SatisfactionSupplyReward|eJzLy0MFADqABuE='
    sheet_name = 'SatisfactionSupplyReward'
    reward_bonus_rate: int_t = RowData(0)
    reward_currency_a: int_t = RowData(1)
    reward_num_a: List[int_t] = ListData(ir((2, 3, 1)), RowData)
    reward_currency_b: int_t = RowData(5)
    reward_num_b: List[int_t] = ListData(ir((6, 3, 1)), RowData)
    reward_limit_level_b: int_t = RowData(9)
    reward_point: List[int_t] = ListData(ir((10, 3, 1)), RowData)
    reward_gil: List[int_t] = ListData(ir((13, 3, 1)), RowData)


class SatisfactionSupplyRewardExp(DataRow):
    _sign = b'SatisfactionSupplyRewardExp|eJzLy8sDAAKXAUs='
    sheet_name = 'SatisfactionSupplyRewardExp'
    reward_exp_rate: List[int_t] = ListData(ir((0, 3, 1)), RowData)


class ScenarioTree(DataRow):
    _sign = b'ScenarioTree|eJzLy8vLK87LAwAMHgMI'
    sheet_name = 'ScenarioTree'
    _display = 'uds__object_id'
    scenario_type: 'ScenarioType' = RowForeign(0, 'ScenarioType')
    scenario_number: int_t = RowData(1)
    scenario_name: 'Addon' = RowForeign(2, 'Addon')
    uds__activity: 'QuestChapter' = RowForeign(3, 'QuestChapter')
    uds__object_id: str_t = RowData(4)
    uds__display_order: int_t = RowData(5)
    uds__scenario_number: int_t = RowData(6)


class ScenarioTreeTips(DataRow):
    _sign = b'ScenarioTreeTips|eJzLy8vLAwAEUAG5'
    sheet_name = 'ScenarioTreeTips'
    next: int_t = RowData(0)
    target_quest: 'ScenarioTreeTipsQuest' = RowForeign(1, 'ScenarioTreeTipsQuest')
    level: int_t = RowData(2)
    prev_quest: 'ScenarioTree' = RowForeign(3, 'ScenarioTree')


class ScenarioTreeTipsClassQuest(DataRow):
    _sign = b'ScenarioTreeTipsClassQuest|eJzLy8vLS0sDAAj0AoU='
    sheet_name = 'ScenarioTreeTipsClassQuest'
    _display = 'quest'
    quest: 'Quest' = RowForeign(0, 'Quest')
    level: int_t = RowData(1)
    need_ex_version: 'ExVersion' = RowForeign(2, 'ExVersion')
    prev_quest: 'Quest' = RowForeign(3, 'Quest')
    first_class: bool_t = RowData(4)
    not_first_class: bool_t = RowData(5)


class ScenarioType(DataRow):
    _sign = b'ScenarioType|eJwrzgMAAVYA4g=='
    sheet_name = 'ScenarioType'
    _display = 'text'
    text: str_t = RowData(0)
    digit: int_t = RowData(1)


class ScreenImage(DataRow):
    _sign = b'ScreenImage|eJzLy8tLAwAESAGx'
    sheet_name = 'ScreenImage'
    image: 'Icon' = IconRow(0)
    jingle: 'Jingle' = RowForeign(1, 'Jingle')
    type: int_t = RowData(2)
    lang: bool_t = RowData(3)


class SecretRecipeBook(DataRow):
    _sign = b'SecretRecipeBook|eJzLKwYAAVEA4g=='
    sheet_name = 'SecretRecipeBook'
    _display = 'sub_division_name'
    item: 'Item' = RowForeign(0, 'Item')
    sub_division_name: str_t = RowData(1)


class SequentialEvent(DataRow):
    _sign = b'SequentialEvent|eJzLyxsFlAEAT2WKXQ=='
    sheet_name = 'SequentialEvent'
    valid_range: int_t = RowData(0)
    out_of_range_log_message_id: int_t = RowData(1)
    event_list_command: List[int_t] = ListData(ir((2, 64, 1)), RowData)
    event_list_param0: List[int_t] = ListData(ir((66, 64, 1)), RowData)
    event_list_param1: List[int_t] = ListData(ir((130, 64, 1)), RowData)
    event_list_param2: List[int_t] = ListData(ir((194, 64, 1)), RowData)
    event_list_param3: List[int_t] = ListData(ir((258, 64, 1)), RowData)


class SequentialEventMultipleRange(DataRow):
    _sign = b'SequentialEventMultipleRange|eJzLSwMAAUQA1Q=='
    sheet_name = 'SequentialEventMultipleRange'
    layout_id: int_t = RowData(0)
    is_hint: bool_t = RowData(1)


class SharlayanCraftWorks(DataRow):
    _sign = b'SharlayanCraftWorks|eJzLyysGAAKcAVA='
    sheet_name = 'SharlayanCraftWorks'
    reception_npc: int_t = RowData(0)
    faculty: int_t = RowData(1)
    text: str_t = RowData(2)


class SharlayanCraftWorksSupply(DataRow):
    _sign = b'SharlayanCraftWorksSupply|eJzLyyMeAACpnxLp'
    sheet_name = 'SharlayanCraftWorksSupply'
    supply_required_level: List[int_t] = ListData(ir((0, 4, 1)), RowData)
    supply_supply_catalog_id: List[int_t] = ListData(ir((4, 4, 1)), RowData)
    supply_supply_item_refine_min: List[int_t] = ListData(ir((8, 4, 1)), RowData)
    supply_supply_item_refine_threshold: List[int_t] = ListData(ir((12, 4, 1)), RowData)
    supply_reward_exp: List[int_t] = ListData(ir((16, 4, 1)), RowData)
    supply_high_refine_reward_exp_rate: List[int_t] = ListData(ir((20, 4, 1)), RowData)
    supply_reward_gil: List[int_t] = ListData(ir((24, 4, 1)), RowData)
    supply_high_refine_reward_gil_rate: List[int_t] = ListData(ir((28, 4, 1)), RowData)
    supply_reward_currency_rotation: List[int_t] = ListData(ir((32, 4, 1)), RowData)
    supply_reward_currency: List[int_t] = ListData(ir((36, 4, 1)), RowData)
    supply_high_refine_reward_currency_rate: List[int_t] = ListData(ir((40, 4, 1)), RowData)


class ShellFixedFromCommand(DataRow):
    _sign = b'ShellFixedFromCommand|eJxLS8vLSwPiYhDIgwEAa4gJbg=='
    sheet_name = 'ShellFixedFromCommand'
    is_local_command: bool_t = RowData(0)
    is_gm_command: bool_t = RowData(1)
    gm_command_id: int_t = RowData(2)
    need_gm_rank: int_t = RowData(3)
    is_packet_command: bool_t = RowData(4)
    is_debug_packet_command: bool_t = RowData(5)
    packet_command_id: int_t = RowData(6)
    identifier_count: int_t = RowData(7)
    identifier: List[str_t] = ListData(ir((8, 5, 1)), RowData)
    argument_count: int_t = RowData(13)
    argument_type: List[int_t] = ListData(ir((14, 8, 1)), RowData)


class Skirmish(DataRow):
    _sign = b'Skirmish|eJzLAwAAbwBv'
    sheet_name = 'Skirmish'
    dynamic_event: int_t = RowData(0)


class SkyIsland(DataRow):
    _sign = b'SkyIsland|eJzLAwAAbwBv'
    sheet_name = 'SkyIsland'
    num_0: int_t = RowData(0)


class SkyIsland2(DataRow):
    _sign = b'SkyIsland2|eJzLywMAAUwA3Q=='
    sheet_name = 'SkyIsland2'
    type: int_t = RowData(0)
    airship: int_t = RowData(1)


class SkyIsland2Mission(DataRow):
    _sign = b'SkyIsland2Mission|eJzLy8MCikEAAJc3C0Y='
    sheet_name = 'SkyIsland2Mission'
    _display = 'item_1'
    item_1: 'EventItem' = RowForeign(0, 'EventItem')
    item_2: 'EventItem' = RowForeign(1, 'EventItem')
    place_name: 'PlaceName' = RowForeign(2, 'PlaceName')
    field_3: int_t = RowData(3)
    objective_1: 'SkyIsland2MissionDetail' = RowForeign(4, 'SkyIsland2MissionDetail')
    pop_range: List[int_t] = ListData(ir((5, 3, 5)), RowData)
    required_amount_1: int_t = RowData(6)
    field_7: int_t = RowData(7)
    field_8: int_t = RowData(8)
    objective2: 'SkyIsland2MissionDetail' = RowForeign(9, 'SkyIsland2MissionDetail')
    required_amount_2: int_t = RowData(11)
    field_12: int_t = RowData(12)
    field_13: int_t = RowData(13)
    objective3: 'SkyIsland2MissionDetail' = RowForeign(14, 'SkyIsland2MissionDetail')
    field_16: int_t = RowData(16)
    field_17: int_t = RowData(17)
    field_18: int_t = RowData(18)
    field_19: int_t = RowData(19)
    image: 'Icon' = IconRow(20)
    field_21: str_t = RowData(21)
    field_22: str_t = RowData(22)
    field_23: str_t = RowData(23)
    field_24: str_t = RowData(24)
    field_25: str_t = RowData(25)


class SkyIsland2MissionDetail(DataRow):
    _sign = b'SkyIsland2MissionDetail|eJzLywODYiAAAByZBM8='
    sheet_name = 'SkyIsland2MissionDetail'
    _display = 'objective'
    type: 'SkyIsland2MissionType' = RowForeign(0, 'SkyIsland2MissionType')
    field_1: int_t = RowData(1)
    range: 'SkyIsland2RangeType' = RowForeign(2, 'SkyIsland2RangeType')
    field_3: int_t = RowData(3)
    e_obj: 'EObjName' = RowForeign(4, 'EObjName')
    field_5: int_t = RowData(5)
    field_6: int_t = RowData(6)
    objective: str_t = RowData(7)
    field_8: str_t = RowData(8)
    field_9: str_t = RowData(9)
    field_10: str_t = RowData(10)


class SkyIsland2MissionType(DataRow):
    _sign = b'SkyIsland2MissionType|eJxLAwAAZwBn'
    sheet_name = 'SkyIsland2MissionType'
    _display = 'free_exploration'
    free_exploration: bool_t = RowData(0)


class SkyIsland2RangeType(DataRow):
    _sign = b'SkyIsland2RangeType|eJzLAwAAbwBv'
    sheet_name = 'SkyIsland2RangeType'
    _display = 'range_size'
    range_size: int_t = RowData(0)


class SkyIslandMapMarker(DataRow):
    _sign = b'SkyIslandMapMarker|eJzLy0MDAEHPB08='
    sheet_name = 'SkyIslandMapMarker'
    num_0: int_t = RowData(0)
    num_1: int_t = RowData(1)
    num_2: int_t = RowData(2)
    num_3: int_t = RowData(3)
    num_4: int_t = RowData(4)
    num_5: int_t = RowData(5)
    num_6: int_t = RowData(6)
    num_7: int_t = RowData(7)
    num_8: int_t = RowData(8)
    num_9: int_t = RowData(9)
    num_10: int_t = RowData(10)
    num_11: int_t = RowData(11)
    num_12: int_t = RowData(12)
    num_13: int_t = RowData(13)
    num_14: int_t = RowData(14)
    num_15: int_t = RowData(15)
    num_16: int_t = RowData(16)


class SkyIslandSubject(DataRow):
    _sign = b'SkyIslandSubject|eJzLy0MHAEmMB70='
    sheet_name = 'SkyIslandSubject'
    num_0: int_t = RowData(0)
    num_1: int_t = RowData(1)
    num_2: int_t = RowData(2)
    num_3: int_t = RowData(3)
    num_4: int_t = RowData(4)
    num_5: int_t = RowData(5)
    num_6: int_t = RowData(6)
    num_7: int_t = RowData(7)
    num_8: int_t = RowData(8)
    num_9: int_t = RowData(9)
    num_10: int_t = RowData(10)
    num_11: int_t = RowData(11)
    num_12: int_t = RowData(12)
    num_13: int_t = RowData(13)
    num_14: int_t = RowData(14)
    num_15: int_t = RowData(15)
    num_16: int_t = RowData(16)
    num_17: int_t = RowData(17)


class Snipe(DataRow):
    _sign = b'Snipe|eJzLy0vLg4JiIEDwqAGKkUBeHgC27i47'
    sheet_name = 'Snipe'
    position: int_t = RowData(0)
    time_limit: int_t = RowData(1)
    time_limit_game_over: bool_t = RowData(2)
    bg_collision: int_t = RowData(3)
    camera_up: int_t = RowData(4)
    camera_down: int_t = RowData(5)
    camera_left: int_t = RowData(6)
    camera_right: int_t = RowData(7)
    camera_zoom: int_t = RowData(8)
    action_hit_time: int_t = RowData(9)
    action_lock_time: int_t = RowData(10)
    action_vfx: str_t = RowData(11)
    hit_vfx: str_t = RowData(12)
    miss_vfx: str_t = RowData(13)
    invincible_vfx: str_t = RowData(14)
    not_hit_talk: int_t = RowData(15)
    last_hit_camera: bool_t = RowData(16)
    actor_layout: List[int_t] = ListData(ir((17, 8, 1)), RowData)
    actor_hit_event: List[int_t] = ListData(ir((25, 8, 1)), RowData)
    actor_behavior_miss_camera: List[int_t] = ListData(ir((33, 8, 1)), RowData)
    actor_event_object_reaction: List[int_t] = ListData(ir((41, 8, 1)), RowData)
    actor_camera_distance_min: List[int_t] = ListData(ir((49, 8, 1)), RowData)
    actor_camera_distance_max: List[int_t] = ListData(ir((57, 8, 1)), RowData)
    actor_todo: List[int_t] = ListData(ir((65, 8, 1)), RowData)
    lively_layout: List[int_t] = ListData(ir((73, 8, 1)), RowData)
    start_camera: List[int_t] = ListData(ir((81, 4, 1)), RowData)
    start_camera_target: List[int_t] = ListData(ir((85, 4, 1)), RowData)
    start_camera_target_param: List[int_t] = ListData(ir((89, 4, 1)), RowData)
    text_title: str_t = RowData(93)
    text_description: str_t = RowData(94)
    text_failure_condition: str_t = RowData(95)
    text_todo: List[str_t] = ListData(ir((96, 8, 1)), RowData)
    text_action: str_t = RowData(104)
    skin_zoom_min_scale: int_t = RowData(105)
    skin_zoom_max_scale: int_t = RowData(106)


class SnipeCollision(DataRow):
    _sign = b'SnipeCollision|eJzLywMCAAZ3Aic='
    sheet_name = 'SnipeCollision'
    eid: int_t = RowData(0)
    type: int_t = RowData(1)
    x: int_t = RowData(2)
    y: int_t = RowData(3)
    z: int_t = RowData(4)


class SnipeElementId(DataRow):
    _sign = b'SnipeElementId|eJzLAwAAbwBv'
    sheet_name = 'SnipeElementId'
    element_id: int_t = RowData(0)


class SnipeHitEvent(DataRow):
    _sign = b'SnipeHitEvent|eJzLywMCAAZ3Aic='
    sheet_name = 'SnipeHitEvent'
    type: int_t = RowData(0)
    collision: int_t = RowData(1)
    camera: int_t = RowData(2)
    talk: int_t = RowData(3)
    talk_condition: int_t = RowData(4)


class SnipePerformanceCamera(DataRow):
    _sign = b'SnipePerformanceCamera|eJzLy4MBABesBE0='
    sheet_name = 'SnipePerformanceCamera'
    eid: int_t = RowData(0)
    offset_up_down: int_t = RowData(1)
    offset_left_right: int_t = RowData(2)
    yaw: int_t = RowData(3)
    pitch: int_t = RowData(4)
    distance: int_t = RowData(5)
    target_yaw: int_t = RowData(6)
    target_pitch: int_t = RowData(7)
    target_distance: int_t = RowData(8)
    time: int_t = RowData(9)


class SnipeTalk(DataRow):
    _sign = b'SnipeTalk|eJzLy8srLi4GAAkqAqQ='
    sheet_name = 'SnipeTalk'
    log_kind: int_t = RowData(0)
    shape: int_t = RowData(1)
    talker: 'SnipeTalkName' = RowForeign(2, 'SnipeTalkName')
    text: List[str_t] = ListData(ir((3, 3, 1)), RowData)


class SnipeTalkName(DataRow):
    _sign = b'SnipeTalkName|eJwrBgAAdAB0'
    sheet_name = 'SnipeTalkName'
    _display = 'text'
    text: str_t = RowData(0)


class SpearfishingComboTarget(DataRow):
    _sign = b'SpearfishingComboTarget|eJwrLgYAAVsA5w=='
    sheet_name = 'SpearfishingComboTarget'
    field_0: str_t = RowData(0)
    field_1: str_t = RowData(1)


class SpearfishingEcology(DataRow):
    _sign = b'SpearfishingEcology|eJwrLi4uBgAEggHN'
    sheet_name = 'SpearfishingEcology'
    text_0: str_t = RowData(0)
    text_1: str_t = RowData(1)
    text_2: str_t = RowData(2)
    text_3: str_t = RowData(3)


class SpearfishingItem(DataRow):
    _sign = b'SpearfishingItem|eJwrzstLS8vLA5FpACEUBQY='
    sheet_name = 'SpearfishingItem'
    _display = 'item_id'
    text: str_t = RowData(0)
    item_id: 'Item' = RowForeign(1, 'Item')
    level: 'GatheringItemLevelConvertTable' = RowForeign(2, 'GatheringItemLevelConvertTable')
    is_mask_condition: bool_t = RowData(3)
    is_special_condition: bool_t = RowData(4)
    record_type: 'FishingRecordType' = RowForeign(5, 'FishingRecordType')
    territory: 'TerritoryType' = RowForeign(6, 'TerritoryType')
    typical_spearfishing_spot: int_t = RowData(7)
    folklore: int_t = RowData(8)
    is_fish_print: bool_t = RowData(9)
    is_catch_time: bool_t = RowData(10)
    is_weather_condition: bool_t = RowData(11)


class SpearfishingItem(DataRow):
    _sign = b'SpearfishingItem|eJwrzstLywNiAA94A2Y='
    sheet_name = 'SpearfishingItem'
    _display = 'item_id'
    text: str_t = RowData(0)
    item_id: 'Item' = RowForeign(1, 'Item')
    level: 'GatheringItemLevelConvertTable' = RowForeign(2, 'GatheringItemLevelConvertTable')
    is_mask_condition: bool_t = RowData(3)
    record_type: 'FishingRecordType' = RowForeign(4, 'FishingRecordType')
    typical_spearfishing_spot: int_t = RowData(5)
    folklore: int_t = RowData(6)
    is_fish_print: bool_t = RowData(7)


class SpearfishingItemReverse(DataRow):
    _sign = b'SpearfishingItemReverse|eJxLAwAAZwBn'
    sheet_name = 'SpearfishingItemReverse'
    masked: bool_t = RowData(0)


class SpearfishingNotebook(DataRow):
    _sign = b'SpearfishingNotebook|eJzLS8uDAwAhOAUh'
    sheet_name = 'SpearfishingNotebook'
    _display = 'spot_name_id'
    level: int_t = RowData(0)
    rare: bool_t = RowData(1)
    territory_type: 'TerritoryType' = RowForeign(2, 'TerritoryType')
    maker_pos_x: int_t = RowData(3)
    maker_pos_y: int_t = RowData(4)
    maker_type: int_t = RowData(5)
    name_layout: int_t = RowData(6)
    spot_name_id: 'PlaceName' = RowForeign(7, 'PlaceName')
    sort_key: int_t = RowData(8)
    base_id: 'List[GatheringPointBase]' = ListData(ir((9, 3, 1)), RowForeign, 'GatheringPointBase')


class SpearfishingRecordPage(DataRow):
    _sign = b'SpearfishingRecordPage|eJzLywMDAAwPAwM='
    sheet_name = 'SpearfishingRecordPage'
    record_type: List[int_t] = ListData(ir((0, 3, 1)), RowData)
    area_name: 'PlaceName' = RowForeign(3, 'PlaceName')
    area_icon: 'Icon' = IconRow(4)
    open_level: int_t = RowData(5)
    sort_order: int_t = RowData(6)


class SpearfishingSilhouette(DataRow):
    _sign = b'SpearfishingSilhouette|eJzLAwAAbwBv'
    sheet_name = 'SpearfishingSilhouette'
    shadow_width: int_t = RowData(0)


class SpecialShop(DataRow):
    _sign = b'SpecialShop|eJwrzhuCIIkCMNBuJweMNP+OglEwCoY4SAMiADn/ttg='
    sheet_name = 'SpecialShop'
    _display = 'text'
    text: str_t = RowData(0)
    item_item_id: List[List[int_t]] = ListData(ir(((1, 2, 240), 60, 1)), ListData, RowData)
    item_set_num: List[List[int_t]] = ListData(ir(((61, 2, 240), 60, 1)), ListData, RowData)
    item_category: List[List[int_t]] = ListData(ir(((121, 2, 240), 60, 1)), ListData, RowData)
    item_is_item_hq: List[List[bool_t]] = ListData(ir(((181, 2, 240), 60, 1)), ListData, RowData)
    item_currency: List[List[int_t]] = ListData(ir(((481, 3, 240), 60, 1)), ListData, RowData)
    item_num_of_currency: List[List[int_t]] = ListData(ir(((541, 3, 240), 60, 1)), ListData, RowData)
    item_currency_type: List[List[int_t]] = ListData(ir(((601, 3, 240), 60, 1)), ListData, RowData)
    item_currency_masterpiece: List[List[int_t]] = ListData(ir(((661, 3, 240), 60, 1)), ListData, RowData)
    item_quest: List[List[int_t]] = ListData(ir(((1201, 2, 60), 60, 1)), ListData, RowData)
    item_quest_sequence: List[List[int_t]] = ListData(ir(((1321, 2, 60), 60, 1)), ListData, RowData)
    item_achievement: List[int_t] = ListData(ir((1441, 60, 1)), RowData)
    item_sort: List[int_t] = ListData(ir((1501, 60, 1)), RowData)
    item_added_version: List[int_t] = ListData(ir((1561, 60, 1)), RowData)
    shop_type_pattern: int_t = RowData(1621)
    disclosure_reward_or_quest: int_t = RowData(1622)
    qualified_talk: int_t = RowData(1623)
    unqualified_talk: int_t = RowData(1624)
    item_obtain_event: int_t = RowData(1625)
    system: bool_t = RowData(1626)
    festival: int_t = RowData(1627)
    content: int_t = RowData(1628)
    content_completed: bool_t = RowData(1629)


class SpecialShopItemCategory(DataRow):
    _sign = b'SpecialShopItemCategory|eJwrBgAAdAB0'
    sheet_name = 'SpecialShopItemCategory'
    _display = 'name'
    name: str_t = RowData(0)


class Spectator(DataRow):
    _sign = b'Spectator|eJzLyyMSAAByLhGf'
    sheet_name = 'Spectator'
    camera_x: List[float_t] = ListData(ir((0, 8, 1)), RowData)
    camera_y: List[float_t] = ListData(ir((8, 8, 1)), RowData)
    camera_z: List[float_t] = ListData(ir((16, 8, 1)), RowData)
    camera_rotation_x: List[float_t] = ListData(ir((24, 8, 1)), RowData)
    camera_rotation_y: List[float_t] = ListData(ir((32, 8, 1)), RowData)
    party_list_layout: int_t = RowData(40)


class Stain(DataRow):
    _sign = b'Stain|eJzLy8srLk5LAwAMGgL9'
    sheet_name = 'Stain'
    _display = 'text_color_name'
    color: int_t = RowData(0)
    category: int_t = RowData(1)
    sort_id: int_t = RowData(2)
    text_name: str_t = RowData(3)
    metal: bool_t = RowData(5)
    furniture: bool_t = RowData(6)


class Stain(DataRow):
    _sign = b'Stain|eJzLy8srTksDAAkDAoo='
    sheet_name = 'Stain'
    _display = 'text'
    color: int_t = RowData(0)
    category: int_t = RowData(1)
    sort_id: int_t = RowData(2)
    text: str_t = RowData(3)
    metal: bool_t = RowData(4)
    furniture: bool_t = RowData(5)


class StainTransient(DataRow):
    _sign = b'StainTransient|eJzLywMAAUwA3Q=='
    sheet_name = 'StainTransient'
    _display = 'item'
    item: 'List[Item]' = ListData(ir((0, 2, 1)), RowForeign, 'Item')


class StanceChange(DataRow):
    _sign = b'StanceChange|eJzLywMCAAZ3Aic='
    sheet_name = 'StanceChange'
    transformation_id: int_t = RowData(0)
    timeline: int_t = RowData(1)
    timeline2: int_t = RowData(2)
    sync_timeline: int_t = RowData(3)
    update_model_radius_delay: float_t = RowData(4)


class Status(DataRow):
    _sign = b'Status|eJwrLs6DgDQYADGBGAyBNADrXA3B'
    sheet_name = 'Status'
    _display = 'text_name'
    text_name: str_t = RowData(0)
    text_help: str_t = RowData(1)
    icon: 'Icon' = IconRow(2)
    group_id: int_t = RowData(3)
    stack: int_t = RowData(4)
    class_job: 'ClassJobCategory' = RowForeign(5, 'ClassJobCategory')
    category: int_t = RowData(6)
    hit_effect: 'StatusHitEffect' = RowForeign(7, 'StatusHitEffect')
    loop_vfx: 'StatusLoopVFX' = RowForeign(8, 'StatusLoopVFX')
    not_move: bool_t = RowData(9)
    not_move_can_turn: bool_t = RowData(10)
    not_action: bool_t = RowData(11)
    not_control: bool_t = RowData(12)
    shape_shift: bool_t = RowData(13)
    not_look_at: bool_t = RowData(14)
    clear_esuna: bool_t = RowData(15)
    forever: bool_t = RowData(16)
    hide_timer: bool_t = RowData(17)
    party_list_priority: int_t = RowData(18)
    hud_category: int_t = RowData(19)
    disp_off: bool_t = RowData(20)
    multiple: bool_t = RowData(21)
    value: int_t = RowData(22)
    system_param_effect: int_t = RowData(23)
    inconvenience_clear: bool_t = RowData(24)
    log: int_t = RowData(25)
    fc_action: bool_t = RowData(26)
    attack_type: int_t = RowData(27)
    semi_transparent: bool_t = RowData(28)
    target_type: int_t = RowData(29)
    flag: int_t = RowData(30)
    flag2: int_t = RowData(31)
    group_pose: bool_t = RowData(32)


class StatusHitEffect(DataRow):
    _sign = b'StatusHitEffect|eJzLAwAAbwBv'
    sheet_name = 'StatusHitEffect'
    _display = 'hit_effect'
    hit_effect: 'VFX' = RowForeign(0, 'VFX')


class StatusLoopVFX(DataRow):
    _sign = b'StatusLoopVFX|eJzLywODtLQ0ABd8BDU='
    sheet_name = 'StatusLoopVFX'
    _display = 'vfx'
    vfx: 'VFX' = RowForeign(0, 'VFX')
    stack2: int_t = RowData(1)
    vfx2: 'VFX' = RowForeign(2, 'VFX')
    stack3: int_t = RowData(3)
    vfx3: 'VFX' = RowForeign(4, 'VFX')
    slot: int_t = RowData(5)
    priority: int_t = RowData(6)
    control_chara_only: bool_t = RowData(7)
    vfx_high_priority: bool_t = RowData(8)
    hide_transformation: bool_t = RowData(9)


class Story(DataRow):
    _sign = b'Story|eJwrLiYS5I2CUTAKRsEoGAWjAA0AAM9+IX0='
    sheet_name = 'Story'
    script: str_t = RowData(0)
    define_name: List[str_t] = ListData(ir((1, 40, 1)), RowData)
    define_value: List[int_t] = ListData(ir((41, 40, 1)), RowData)
    sequence_sequence: List[int_t] = ListData(ir((81, 110, 1)), RowData)
    sequence_completed_quest_operator: List[int_t] = ListData(ir((191, 110, 1)), RowData)
    sequence_completed_quest: List[List[int_t]] = ListData(ir(((301, 3, 110), 110, 1)), ListData, RowData)
    sequence_accepted_quest_operator: List[int_t] = ListData(ir((631, 110, 1)), RowData)
    sequence_accepted_quest: List[List[int_t]] = ListData(ir(((741, 3, 220), 110, 1)), ListData, RowData)
    sequence_accepted_quest_sequence: List[List[int_t]] = ListData(ir(((851, 3, 220), 110, 1)), ListData, RowData)
    sequence_layer_set: List[List[int_t]] = ListData(ir(((1401, 2, 110), 110, 1)), ListData, RowData)
    visible_listener_sequence_begin: List[int_t] = ListData(ir((1621, 80, 1)), RowData)
    visible_listener_sequence_end: List[int_t] = ListData(ir((1701, 80, 1)), RowData)
    visible_listener_listener: List[int_t] = ListData(ir((1781, 80, 1)), RowData)
    layer_set_territory_type: 'List[TerritoryType]' = ListData(ir((1861, 2, 1)), RowForeign, 'TerritoryType')


class StorySystemDefine(DataRow):
    _sign = b'StorySystemDefine|eJwrzgMAAVYA4g=='
    sheet_name = 'StorySystemDefine'
    define_name: str_t = RowData(0)
    define_value: int_t = RowData(1)


class SubmarineExploration(DataRow):
    _sign = b'SubmarineExploration|eJwrLs4DgrQ8MAAAJ2wFmQ=='
    sheet_name = 'SubmarineExploration'
    _display = 'name_name'
    name_name: str_t = RowData(0)
    name_abbreviation: str_t = RowData(1)
    x: int_t = RowData(2)
    y: int_t = RowData(3)
    z: int_t = RowData(4)
    submarine_map: 'SubmarineMap' = RowForeign(5, 'SubmarineMap')
    is_start_point: bool_t = RowData(6)
    difficulty: int_t = RowData(7)
    rank: int_t = RowData(8)
    energy_item_num: int_t = RowData(9)
    time: int_t = RowData(10)
    survey_distance: int_t = RowData(11)
    reward_exp: int_t = RowData(12)


class SubmarineExplorationLog(DataRow):
    _sign = b'SubmarineExplorationLog|eJwrBgAAdAB0'
    sheet_name = 'SubmarineExplorationLog'
    text: str_t = RowData(0)


class SubmarineMap(DataRow):
    _sign = b'SubmarineMap|eJwrzgMAAVYA4g=='
    sheet_name = 'SubmarineMap'
    _display = 'name'
    name: str_t = RowData(0)
    icon: 'Icon' = IconRow(1)


class SubmarinePart(DataRow):
    _sign = b'SubmarinePart|eJzLy4MBABesBE0='
    sheet_name = 'SubmarinePart'
    _display = 'category'
    category: int_t = RowData(0)
    need_rank: int_t = RowData(1)
    cost: int_t = RowData(2)
    exploration: int_t = RowData(3)
    collection: int_t = RowData(4)
    cruise_speed: int_t = RowData(5)
    cruise_distance: int_t = RowData(6)
    luck: int_t = RowData(7)
    pattern_id: int_t = RowData(8)
    repair_item_num: int_t = RowData(9)


class SubmarineRank(DataRow):
    _sign = b'SubmarineRank|eJzLywMDAAwPAwM='
    sheet_name = 'SubmarineRank'
    cost_limit: int_t = RowData(0)
    rank_up_exp: int_t = RowData(1)
    rank_bonus_exploration: int_t = RowData(2)
    rank_bonus_collection: int_t = RowData(3)
    rank_bonus_cruise_speed: int_t = RowData(4)
    rank_bonus_cruise_distance: int_t = RowData(5)
    rank_bonus_luck: int_t = RowData(6)


class SubmarineSpecCategory(DataRow):
    _sign = b'SubmarineSpecCategory|eJwrBgAAdAB0'
    sheet_name = 'SubmarineSpecCategory'
    text: str_t = RowData(0)


class SwitchTalk(DataRow):
    _sign = b'SwitchTalk|eJzLSwMAAUQA1Q=='
    sheet_name = 'SwitchTalk'
    layout_id: int_t = RowData(0)
    system: bool_t = RowData(1)


class SwitchTalkVariation(DataRow):
    _sign = b'SwitchTalkVariation|eJzLy8vLAwAEUAG5'
    sheet_name = 'SwitchTalkVariation'
    case_condition: int_t = RowData(0)
    case_condition_accepted: 'Quest' = RowForeign(1, 'Quest')
    case_condition_accepted_sequence: int_t = RowData(2)
    talk: 'DefaultTalk' = RowForeign(3, 'DefaultTalk')


class SystemGraphicPreset(DataRow):
    _sign = b'SystemGraphicPreset|eJzLyyMAAPEvDi8='
    sheet_name = 'SystemGraphicPreset'
    hdr_quality: int_t = RowData(0)
    water_wet: int_t = RowData(1)
    occlusion_culling: int_t = RowData(2)
    lod_enable: int_t = RowData(3)
    lod_stream: int_t = RowData(4)
    reflection: int_t = RowData(5)
    anti_alias: int_t = RowData(6)
    translucent_quality: int_t = RowData(7)
    grass_quality: int_t = RowData(8)
    parallax_occlusion: int_t = RowData(9)
    tessellation: int_t = RowData(10)
    glare_representation: int_t = RowData(11)
    map_res: int_t = RowData(12)
    shadow_self: int_t = RowData(13)
    shadow_party: int_t = RowData(14)
    shadow_other: int_t = RowData(15)
    shadow_enemy: int_t = RowData(16)
    shadow_lod: int_t = RowData(17)
    shadow_tex_size: int_t = RowData(18)
    shadow_cascade: int_t = RowData(19)
    soft_shadow: int_t = RowData(20)
    texture_filter: int_t = RowData(21)
    texture_anisotropic: int_t = RowData(22)
    physics_self: int_t = RowData(23)
    physics_party: int_t = RowData(24)
    physics_other: int_t = RowData(25)
    physics_enemy: int_t = RowData(26)
    vignetting: int_t = RowData(27)
    radial_blur: int_t = RowData(28)
    ssao: int_t = RowData(29)
    glare: int_t = RowData(30)
    distortion_water: int_t = RowData(31)
    dof: int_t = RowData(32)


class TelepoRelay(DataRow):
    _sign = b'TelepoRelay|eJzLy0MHAEmMB70='
    sheet_name = 'TelepoRelay'
    relay_point_relay_territory_source: List[int_t] = ListData(ir((0, 6, 1)), RowData)
    relay_point_relay_territory_destination: List[int_t] = ListData(ir((6, 6, 1)), RowData)
    relay_point_cost: List[int_t] = ListData(ir((12, 6, 1)), RowData)


class TerritoryChatRule(DataRow):
    _sign = b'TerritoryChatRule|eJxLy4MAAA9AA2k='
    sheet_name = 'TerritoryChatRule'
    area_chat_only_same_force: bool_t = RowData(0)
    enable_range_chat: int_t = RowData(1)
    enable_zone_chat: int_t = RowData(2)
    enable_contents_tell_chat: int_t = RowData(3)
    enable_tell_chat: int_t = RowData(4)
    enable_party_chat: int_t = RowData(5)
    enable_world_chat: int_t = RowData(6)
    enable_pvp_team_chat: int_t = RowData(7)


class TerritoryIntendedUse(DataRow):
    _sign = b'TerritoryIntendedUse|eJxLS8MAeXkoPDBKSwMAWQYQdw=='
    sheet_name = 'TerritoryIntendedUse'
    craft: bool_t = RowData(0)
    gathering: bool_t = RowData(1)
    repair: bool_t = RowData(2)
    class_job_change: bool_t = RowData(3)
    battle_class_only: bool_t = RowData(4)
    sp_job_change: bool_t = RowData(5)
    enable_buddy: bool_t = RowData(6)
    enable_pet: bool_t = RowData(7)
    enable_mount_link: bool_t = RowData(8)
    immediately_logout: bool_t = RowData(9)
    enable_teleport: bool_t = RowData(10)
    enable_return: bool_t = RowData(11)
    enable_companion: bool_t = RowData(12)
    enable_ornament: bool_t = RowData(13)
    enable_home_point: bool_t = RowData(14)
    enable_recommend: bool_t = RowData(15)
    enable_discovery_notification: bool_t = RowData(16)
    enable_invalid_discovery: bool_t = RowData(17)
    alone: bool_t = RowData(18)
    area_horizon_range: int_t = RowData(19)
    buzz_type: int_t = RowData(20)
    se_limit: bool_t = RowData(21)
    enable_action: bool_t = RowData(22)
    enable_using_item: bool_t = RowData(23)
    recast_penalty: bool_t = RowData(24)
    enable_table_game: bool_t = RowData(25)
    disable_table_game_range: bool_t = RowData(26)
    enable_triple_triad_competition: bool_t = RowData(27)
    enable_triple_triad_matching: bool_t = RowData(28)
    enable_idle_camera_raycast: bool_t = RowData(29)
    enable_group_pose_env_stop: bool_t = RowData(30)
    enable_orchestrion: bool_t = RowData(31)
    enable_quick_chat: bool_t = RowData(32)
    chat_rule: int_t = RowData(33)
    enable_organization_party: bool_t = RowData(34)
    enable_perform: bool_t = RowData(35)
    ensemble: int_t = RowData(36)
    enable_mirage_plate: bool_t = RowData(37)
    kick_afk: bool_t = RowData(38)
    field_marker_preset: bool_t = RowData(39)
    field_marker_in_battle: bool_t = RowData(40)


class TerritoryType(DataRow):
    _sign = b'TerritoryType|eJwrLs6DgTQQBAIkATAJEU3LAwCRfxIV'
    sheet_name = 'TerritoryType'
    _display = 'name'
    name: str_t = RowData(0)
    lvb: str_t = RowData(1)
    battalion_mode: int_t = RowData(2)
    region: 'PlaceName' = RowForeign(3, 'PlaceName')
    sub_region: 'PlaceName' = RowForeign(4, 'PlaceName')
    area: 'PlaceName' = RowForeign(5, 'PlaceName')
    map: 'Map' = RowForeign(6, 'Map')
    loading_image: 'LoadingImage' = RowForeign(7, 'LoadingImage')
    exclusive_type: int_t = RowData(8)
    intended_use: int_t = RowData(9)
    content_finder_condition: 'ContentFinderCondition' = RowForeign(10, 'ContentFinderCondition')
    log_range_limit_off: bool_t = RowData(11)
    weather: int_t = RowData(12)
    festival_weather: bool_t = RowData(13)
    breath: int_t = RowData(14)
    pc_search: bool_t = RowData(15)
    stealth: bool_t = RowData(16)
    mount: bool_t = RowData(17)
    mount_in_battle: bool_t = RowData(18)
    bgm: int_t = RowData(19)
    region_icon: 'Icon' = IconRow(20)
    area_icon: 'Icon' = IconRow(21)
    event_handler: 'ArrayEventHandler' = RowForeign(22, 'ArrayEventHandler')
    quest_battle: 'QuestBattle' = RowForeign(23, 'QuestBattle')
    aetheryte: 'Aetheryte' = RowForeign(24, 'Aetheryte')
    client_fixed_time: int_t = RowData(25)
    resident: int_t = RowData(26)
    achievement_index: int_t = RowData(27)
    is_pvp_action: bool_t = RowData(28)
    need_ex_version: 'ExVersion' = RowForeign(29, 'ExVersion')
    time_line_control: int_t = RowData(30)
    shared_group_control: int_t = RowData(31)
    aether_current_comp_flg_set: int_t = RowData(32)
    mount_speed: 'MountSpeed' = RowForeign(33, 'MountSpeed')
    diving_raycast_long: bool_t = RowData(34)
    enable_packet_disguise: bool_t = RowData(35)
    individual_weather: int_t = RowData(36)
    e_npc_y_limit: bool_t = RowData(37)
    private_priority_actor: bool_t = RowData(38)
    party_npc_filter_enemy: bool_t = RowData(39)
    battle_with_height_differrence: bool_t = RowData(40)
    enable_vfx_priority: bool_t = RowData(41)
    notorious_monster_territory: int_t = RowData(42)


class TerritoryTypeTelepo(DataRow):
    _sign = b'TerritoryTypeTelepo|eJzLy8vLAwAEUAG5'
    sheet_name = 'TerritoryTypeTelepo'
    pos_x: int_t = RowData(0)
    pos_y: int_t = RowData(1)
    cost_patch_ratio: int_t = RowData(2)
    world_type: int_t = RowData(3)


class TerritoryTypeTransient(DataRow):
    _sign = b'TerritoryTypeTransient|eJzLAwAAbwBv'
    sheet_name = 'TerritoryTypeTransient'
    _display = 'position_base_y'
    position_base_y: int_t = RowData(0)


class TextCommand(DataRow):
    _sign = b'TextCommand|eJzLywOCYhDIywMAIg0FQg=='
    sheet_name = 'TextCommand'
    _display = 'command'
    field_0: int_t = RowData(0)
    field_1: int_t = RowData(1)
    field_2: int_t = RowData(2)
    field_3: int_t = RowData(3)
    field_4: int_t = RowData(4)
    command: str_t = RowData(5)
    short_command: str_t = RowData(6)
    description: str_t = RowData(7)
    alias: str_t = RowData(8)
    short_alias: str_t = RowData(9)
    param: 'TextCommandParam' = RowForeign(10, 'TextCommandParam')
    field_11: int_t = RowData(11)


class TextCommandParam(DataRow):
    _sign = b'TextCommandParam|eJwrBgAAdAB0'
    sheet_name = 'TextCommandParam'
    _display = 'param'
    param: str_t = RowData(0)


class Title(DataRow):
    _sign = b'Title|eJwrLk7LAwAEYwG7'
    sheet_name = 'Title'
    _display = 'text_female'
    text_male: str_t = RowData(0)
    text_female: str_t = RowData(1)
    text_front: bool_t = RowData(2)
    sort_id: int_t = RowData(3)


class TofuEditParam(DataRow):
    _sign = b'TofuEditParam|eJwrBgAAdAB0'
    sheet_name = 'TofuEditParam'
    name: str_t = RowData(0)


class TofuObject(DataRow):
    _sign = b'TofuObject|eJzLywODYjCZlpYGADp9Bs4='
    sheet_name = 'TofuObject'
    cateogry: int_t = RowData(0)
    sort: int_t = RowData(1)
    icon: int_t = RowData(2)
    width: int_t = RowData(3)
    height: int_t = RowData(4)
    min_scale: int_t = RowData(5)
    max_scale: int_t = RowData(6)
    name: str_t = RowData(7)
    edit_param: List[int_t] = ListData(ir((8, 5, 1)), RowData)
    is_flip_h: bool_t = RowData(13)
    is_flip_v: bool_t = RowData(14)


class TofuObject(DataRow):
    _sign = b'TofuObject|eJzLywODYjCZlgYAM68GaA=='
    sheet_name = 'TofuObject'
    cateogry: int_t = RowData(0)
    sort: int_t = RowData(1)
    icon: int_t = RowData(2)
    width: int_t = RowData(3)
    height: int_t = RowData(4)
    min_scale: int_t = RowData(5)
    max_scale: int_t = RowData(6)
    name: str_t = RowData(7)
    edit_param: List[int_t] = ListData(ir((8, 5, 1)), RowData)
    is_flip_h: bool_t = RowData(13)
    is_flip_v: bool_t = RowData(14)


class TofuObjectCategory(DataRow):
    _sign = b'TofuObjectCategory|eJxLy8srBgAENQG2'
    sheet_name = 'TofuObjectCategory'
    is_use: bool_t = RowData(0)
    sort: int_t = RowData(1)
    icon_state: int_t = RowData(2)
    name: str_t = RowData(3)


class TofuPreset(DataRow):
    _sign = b'TofuPreset|eJzLK85Ly4MDAC0VBgI='
    sheet_name = 'TofuPreset'


class TofuPresetCategory(DataRow):
    _sign = b'TofuPresetCategory|eJwrTksDAAKOAUA='
    sheet_name = 'TofuPresetCategory'


class TofuPresetObject(DataRow):
    _sign = b'TofuPresetObject|eJzLywOCtDQAC/cC8w=='
    sheet_name = 'TofuPresetObject'


class TomestoneConvert(DataRow):
    _sign = b'TomestoneConvert|eJxLy8vLKwYABlQCJA=='
    sheet_name = 'TomestoneConvert'
    visible: bool_t = RowData(0)
    from_tomestone: int_t = RowData(1)
    to_tomestone: int_t = RowData(2)
    exchange_rate: int_t = RowData(3)
    text: str_t = RowData(4)


class Tomestones(DataRow):
    _sign = b'Tomestones|eJzLAwAAbwBv'
    sheet_name = 'Tomestones'
    weekly_cap: int_t = RowData(0)


class TomestonesItem(DataRow):
    _sign = b'TomestonesItem|eJzLy8sDAAKXAUs='
    sheet_name = 'TomestonesItem'
    _display = 'catalog_id'
    catalog_id: 'Item' = RowForeign(0, 'Item')
    slot: int_t = RowData(1)
    type: 'Tomestones' = RowForeign(2, 'Tomestones')


class TopicSelect(DataRow):
    _sign = b'TopicSelect|eJwrTstDAgAtCgYC'
    sheet_name = 'TopicSelect'
    _display = 'text'
    text: str_t = RowData(0)
    menu_title: bool_t = RowData(1)
    accept_cond: int_t = RowData(2)
    accept_arg: int_t = RowData(3)
    event_handler: List[int_t] = ListData(ir((4, 10, 1)), RowData)


class Town(DataRow):
    _sign = b'Town|eJwrzgMAAVYA4g=='
    sheet_name = 'Town'
    _display = 'name'
    name: str_t = RowData(0)
    icon: 'Icon' = IconRow(1)


class Trait(DataRow):
    _sign = b'Trait|eJwrzoMAAA+oA3Y='
    sheet_name = 'Trait'
    _display = 'text'
    text: str_t = RowData(0)
    icon: 'Icon' = IconRow(1)
    class_job: 'ClassJob' = RowForeign(2, 'ClassJob')
    level: int_t = RowData(3)
    reward: 'Quest' = RowForeign(4, 'Quest')
    param_value: int_t = RowData(5)
    use_class: 'ClassJobCategory' = RowForeign(6, 'ClassJobCategory')
    normalize_trait_group: int_t = RowData(7)


class TraitRecast(DataRow):
    _sign = b'TraitRecast|eJzLy8sDAAKXAUs='
    sheet_name = 'TraitRecast'
    _display = 'trait'
    trait: 'Trait' = RowForeign(0, 'Trait')
    action: 'Action' = RowForeign(1, 'Action')
    recast_time: int_t = RowData(2)


class TraitTransient(DataRow):
    _sign = b'TraitTransient|eJwrBgAAdAB0'
    sheet_name = 'TraitTransient'
    _display = 'text'
    text: str_t = RowData(0)


class Transformation(DataRow):
    _sign = b'Transformation|eJzLywOCJBSYl5aWlwYigSAPAtLSAFNTEI0='
    sheet_name = 'Transformation'
    type: int_t = RowData(0)
    model_chara: 'ModelChara' = RowForeign(1, 'ModelChara')
    name_id: 'BNpcName' = RowForeign(2, 'BNpcName')
    customize: 'BNpcCustomize' = RowForeign(3, 'BNpcCustomize')
    equip: 'NpcEquip' = RowForeign(4, 'NpcEquip')
    combo: List[bool_t] = ListData(ir((5, 7, 2)), RowData)
    action: 'List[RPParameter]' = ListData(ir((6, 7, 2)), RowForeign, 'RPParameter')
    action_right_align: 'Action' = RowForeign(19, 'Action')
    is_disp_ex_hotbar: bool_t = RowData(20)
    ex_hotbar_enable_config: bool_t = RowData(21)
    ex_hotbar_crossbar_index_type: int_t = RowData(22)
    ex_hotbar_play_se: bool_t = RowData(23)
    height_float: float_t = RowData(24)
    scale: float_t = RowData(25)
    pc_radius_scale: bool_t = RowData(26)
    emote: bool_t = RowData(27)
    cast_cancel: bool_t = RowData(28)
    drawn_sword_begin: bool_t = RowData(29)
    disable_auto_diactivate: bool_t = RowData(30)
    vfx_begin: 'VFX' = RowForeign(31, 'VFX')
    vfx_end: 'VFX' = RowForeign(32, 'VFX')
    auto_attack_id: 'Action' = RowForeign(33, 'Action')
    combo_position_ignored: int_t = RowData(34)
    move_speed_rate: int_t = RowData(35)
    se_pack: 'Action' = RowForeign(36, 'Action')
    rp_parameter: int_t = RowData(37)
    enter_water: bool_t = RowData(38)
    dive: bool_t = RowData(39)


class Treasure(DataRow):
    _sign = b'Treasure|eJwrzivOA4O0NAAcswS1'
    sheet_name = 'Treasure'
    _display = 'shared_group'
    text_sgl: str_t = RowData(0)
    text_sgg: int_t = RowData(1)
    text_plr: str_t = RowData(2)
    text_plg: int_t = RowData(3)
    text_vow: int_t = RowData(4)
    text_cnt: int_t = RowData(5)
    text_gen: int_t = RowData(6)
    text_def_: int_t = RowData(7)
    shared_group: 'Item' = RowForeign(8, 'Item')
    is_ground: bool_t = RowData(9)
    is_overlap_open: bool_t = RowData(10)


class TreasureHuntRank(DataRow):
    _sign = b'TreasureHuntRank|eJzLy4OANAATVwPX'
    sheet_name = 'TreasureHuntRank'
    mode: int_t = RowData(0)
    icon: 'Icon' = IconRow(1)
    map_item: 'Item' = RowForeign(2, 'Item')
    event_map_item: 'EventItem' = RowForeign(3, 'EventItem')
    reopen_potal_event_map_item: 'EventItem' = RowForeign(4, 'EventItem')
    recommend_member: int_t = RowData(5)
    texture: int_t = RowData(6)
    map_scale: int_t = RowData(7)
    net_cafe_ko: bool_t = RowData(8)


class TreasureHuntTexture(DataRow):
    _sign = b'TreasureHuntTexture|eJwrBgAAdAB0'
    sheet_name = 'TreasureHuntTexture'
    texture_name: str_t = RowData(0)


class TreasureModel(DataRow):
    _sign = b'TreasureModel|eJwrBgAAdAB0'
    sheet_name = 'TreasureModel'
    _display = 'file'
    file: str_t = RowData(0)


class TreasureSpot(DataRow):
    _sign = b'TreasureSpot|eJzLy8sDAAKXAUs='
    sheet_name = 'TreasureSpot'
    _display = 'location'
    location: 'Level' = RowForeign(0, 'Level')
    map_offset_x: float_t = RowData(1)
    map_offset_y: float_t = RowData(2)


class Tribe(DataRow):
    _sign = b'Tribe|eJwrLs6DAgAYCwRX'
    sheet_name = 'Tribe'
    _display = 'text_name_female'
    text_name: str_t = RowData(0)
    text_name_female: str_t = RowData(1)
    hp: int_t = RowData(2)
    mp: int_t = RowData(3)
    str: int_t = RowData(4)
    vit: int_t = RowData(5)
    dex: int_t = RowData(6)
    int: int_t = RowData(7)
    mnd: int_t = RowData(8)
    pie: int_t = RowData(9)


class TriggerEffect(DataRow):
    _sign = b'TriggerEffect|eJzLy4MAAA+AA3E='
    sheet_name = 'TriggerEffect'
    left_type: int_t = RowData(0)
    left_param1: int_t = RowData(1)
    left_param2: int_t = RowData(2)
    left_param3: int_t = RowData(3)
    right_type: int_t = RowData(4)
    right_param1: int_t = RowData(5)
    right_param2: int_t = RowData(6)
    right_param3: int_t = RowData(7)


class TripleTriad(DataRow):
    _sign = b'TripleTriad|eJzLy0OAtDx0DgDHNAzV'
    sheet_name = 'TripleTriad'
    regular_card: List[int_t] = ListData(ir((0, 5, 1)), RowData)
    sub_card: List[int_t] = ListData(ir((5, 5, 1)), RowData)
    npc_rule: List[int_t] = ListData(ir((10, 2, 1)), RowData)
    disable_trend_rule: bool_t = RowData(12)
    play_coin: int_t = RowData(13)
    quest_operator: int_t = RowData(14)
    quest: List[int_t] = ListData(ir((15, 3, 1)), RowData)
    time_begin: int_t = RowData(18)
    time_end: int_t = RowData(19)
    qualified_talk: 'DefaultTalk' = RowForeign(20, 'DefaultTalk')
    unqualified_talk: 'DefaultTalk' = RowForeign(21, 'DefaultTalk')
    npc_win_talk: 'DefaultTalk' = RowForeign(22, 'DefaultTalk')
    npc_lose_talk: 'DefaultTalk' = RowForeign(23, 'DefaultTalk')
    draw_talk: 'DefaultTalk' = RowForeign(24, 'DefaultTalk')
    disable_timeline: bool_t = RowData(25)
    reward: List[int_t] = ListData(ir((26, 4, 1)), RowData)


class TripleTriadCard(DataRow):
    _sign = b'TripleTriadCard|eJwrzivOA4FiABO0A+4='
    sheet_name = 'TripleTriadCard'
    _display = 'text_sgl'
    text_sgl: str_t = RowData(0)
    text_sgg: int_t = RowData(1)
    text_plr: str_t = RowData(2)
    text_plg: int_t = RowData(3)
    text_vow: int_t = RowData(4)
    text_cnt: int_t = RowData(5)
    text_gen: int_t = RowData(6)
    text_def_: int_t = RowData(7)
    text_flavor: str_t = RowData(8)


class TripleTriadCardObtain(DataRow):
    _sign = b'TripleTriadCardObtain|eJzLywMAAUwA3Q=='
    sheet_name = 'TripleTriadCardObtain'
    icon: int_t = RowData(0)
    obtain_format: int_t = RowData(1)


class TripleTriadCardRarity(DataRow):
    _sign = b'TripleTriadCardRarity|eJzLAwAAbwBv'
    sheet_name = 'TripleTriadCardRarity'
    deck_level: int_t = RowData(0)


class TripleTriadCardResident(DataRow):
    _sign = b'TripleTriadCardResident|eJzLy4ODNBABADpYBtk='
    sheet_name = 'TripleTriadCardResident'
    work_index: int_t = RowData(0)
    strength: List[int_t] = ListData(ir((1, 4, 1)), RowData)
    rarity: 'TripleTriadCardRarity' = RowForeign(5, 'TripleTriadCardRarity')
    type: 'TripleTriadCardType' = RowForeign(6, 'TripleTriadCardType')
    sell_price: int_t = RowData(7)
    sort: int_t = RowData(8)
    no: int_t = RowData(9)
    category: int_t = RowData(10)
    pick_up: bool_t = RowData(11)
    obtain_type: int_t = RowData(12)
    obtain_arg: List[int_t] = ListData(ir((13, 2, 1)), RowData)
    obtain_unlock: 'Quest' = RowForeign(15, 'Quest')


class TripleTriadCardType(DataRow):
    _sign = b'TripleTriadCardType|eJwrBgAAdAB0'
    sheet_name = 'TripleTriadCardType'
    _display = 'text'
    text: str_t = RowData(0)


class TripleTriadCompetition(DataRow):
    _sign = b'TripleTriadCompetition|eJwrBgAAdAB0'
    sheet_name = 'TripleTriadCompetition'
    _display = 'text'
    text: str_t = RowData(0)


class TripleTriadDefine(DataRow):
    _sign = b'TripleTriadDefine|eJzLAwAAbwBv'
    sheet_name = 'TripleTriadDefine'
    value: int_t = RowData(0)


class TripleTriadResident(DataRow):
    _sign = b'TripleTriadResident|eJzLAwAAbwBv'
    sheet_name = 'TripleTriadResident'
    work_index: int_t = RowData(0)


class TripleTriadRule(DataRow):
    _sign = b'TripleTriadRule|eJwrLs7LS8vLAwAMOAMF'
    sheet_name = 'TripleTriadRule'
    _display = 'text_name'
    text_name: str_t = RowData(0)
    text_help: str_t = RowData(1)
    exclude_rule: List[int_t] = ListData(ir((2, 2, 1)), RowData)
    exclude_tournament: bool_t = RowData(4)
    sort: int_t = RowData(5)
    timeline_time: int_t = RowData(6)


class TripleTriadTournament(DataRow):
    _sign = b'TripleTriadTournament|eJzLy8vLAwAEUAG5'
    sheet_name = 'TripleTriadTournament'
    rule: List[int_t] = ListData(ir((0, 4, 1)), RowData)


class Tutorial(DataRow):
    _sign = b'Tutorial|eJzLy4MBABesBE0='
    sheet_name = 'Tutorial'
    _display = 'todo'
    role: int_t = RowData(0)
    flag: List[int_t] = ListData(ir((1, 3, 1)), RowData)
    reward_exp: int_t = RowData(4)
    reward_gil: int_t = RowData(5)
    reward_item: 'List[Item]' = ListData(ir((6, 3, 1)), RowForeign, 'Item')
    todo: 'InstanceContentTextData' = RowForeign(9, 'InstanceContentTextData')


class TutorialDPS(DataRow):
    _sign = b'TutorialDPS|eJzLAwAAbwBv'
    sheet_name = 'TutorialDPS'
    tutorial_id: 'Tutorial' = RowForeign(0, 'Tutorial')


class TutorialHealer(DataRow):
    _sign = b'TutorialHealer|eJzLAwAAbwBv'
    sheet_name = 'TutorialHealer'
    tutorial_id: 'Tutorial' = RowForeign(0, 'Tutorial')


class TutorialTank(DataRow):
    _sign = b'TutorialTank|eJzLAwAAbwBv'
    sheet_name = 'TutorialTank'
    tutorial_id: 'Tutorial' = RowForeign(0, 'Tutorial')


class UDS_Event(DataRow):
    _sign = b'UDS_Event|eJwrLs4jAAABKg6n'
    sheet_name = 'UDS_Event'
    _display = 'text'
    text: str_t = RowData(0)
    type: str_t = RowData(1)
    field_2: int_t = RowData(2)
    field_3: int_t = RowData(3)
    field_4: int_t = RowData(4)
    field_5: int_t = RowData(5)
    field_6: int_t = RowData(6)
    field_7: int_t = RowData(7)
    field_8: int_t = RowData(8)
    field_9: int_t = RowData(9)
    field_10: int_t = RowData(10)
    field_11: int_t = RowData(11)
    field_12: int_t = RowData(12)
    field_13: int_t = RowData(13)
    field_14: int_t = RowData(14)
    field_15: int_t = RowData(15)
    field_16: int_t = RowData(16)
    field_17: int_t = RowData(17)
    field_18: int_t = RowData(18)
    field_19: int_t = RowData(19)
    field_20: int_t = RowData(20)
    field_21: int_t = RowData(21)
    field_22: int_t = RowData(22)
    field_23: int_t = RowData(23)
    field_24: int_t = RowData(24)
    field_25: int_t = RowData(25)
    field_26: int_t = RowData(26)
    field_27: int_t = RowData(27)
    field_28: int_t = RowData(28)
    field_29: int_t = RowData(29)
    field_30: int_t = RowData(30)
    field_31: int_t = RowData(31)
    field_32: int_t = RowData(32)
    field_33: int_t = RowData(33)


class UDS_Object(DataRow):
    _sign = b'UDS_Object|eJwrBgAAdAB0'
    sheet_name = 'UDS_Object'
    object_id: str_t = RowData(0)


class UDS_Property(DataRow):
    _sign = b'UDS_Property|eJwrLgYAAVsA5w=='
    sheet_name = 'UDS_Property'
    _display = 'text'
    text: str_t = RowData(0)
    type: str_t = RowData(1)


class UDS_Stats(DataRow):
    _sign = b'UDS_Stats|eJwrLgYAAVsA5w=='
    sheet_name = 'UDS_Stats'
    text_0: str_t = RowData(0)
    text_1: str_t = RowData(1)


class UIColor(DataRow):
    _sign = b'UIColor|eJzLy8vLAwAEUAG5'
    sheet_name = 'UIColor'
    _display = 'ui_foreground'
    ui_foreground: int_t = RowData(0)
    ui_glow: int_t = RowData(1)
    field_2: int_t = RowData(2)
    field_3: int_t = RowData(3)


class UIConst(DataRow):
    _sign = b'UIConst|eJzLAwAAbwBv'
    sheet_name = 'UIConst'
    value: int_t = RowData(0)


class VFX(DataRow):
    _sign = b'VFX|eJwrBgAAdAB0'
    sheet_name = 'VFX'
    _display = 'path'
    path: str_t = RowData(0)


class VVDData(DataRow):
    _sign = b'VVDData|eJzLywMBAAkMApU='
    sheet_name = 'VVDData'
    content_id: int_t = RowData(0)
    type: int_t = RowData(1)
    finder_condition: int_t = RowData(2)
    token: int_t = RowData(3)
    ex_action: int_t = RowData(4)
    archive_quest: int_t = RowData(5)


class VVDNotebookContents(DataRow):
    _sign = b'VVDNotebookContents|eJzLyysuBgAEXwHD'
    sheet_name = 'VVDNotebookContents'
    _display = 'text_title'
    thumbnail: 'Icon' = IconRow(0)
    image: 'Icon' = IconRow(1)
    text_title: str_t = RowData(2)
    text_text: str_t = RowData(3)


class VVDNotebookSeries(DataRow):
    _sign = b'VVDNotebookSeries|eJwrzkMCACdoBZw='
    sheet_name = 'VVDNotebookSeries'
    _display = 'title'
    title: str_t = RowData(0)
    data_contents: List[int_t] = ListData(ir((1, 12, 1)), RowData)


class VVDRouteData(DataRow):
    _sign = b'VVDRouteData|eJzLAwAAbwBv'
    sheet_name = 'VVDRouteData'
    save_flag_index: int_t = RowData(0)


class VVDVariantAction(DataRow):
    _sign = b'VVDVariantAction|eJzLAwAAbwBv'
    sheet_name = 'VVDVariantAction'
    _display = 'action'
    action: 'Action' = RowForeign(0, 'Action')


class Vase(DataRow):
    _sign = b'Vase|eJzLywMAAUwA3Q=='
    sheet_name = 'Vase'
    vase_flower_start_index: int_t = RowData(0)
    vase_flower_end_index: int_t = RowData(1)


class VaseFlower(DataRow):
    _sign = b'VaseFlower|eJzLy8vLAwAEUAG5'
    sheet_name = 'VaseFlower'
    kind: int_t = RowData(0)
    step: int_t = RowData(1)
    step2: int_t = RowData(2)
    item: 'Item' = RowForeign(3, 'Item')


class Warp(DataRow):
    _sign = b'Warp|eJzLy4OCtOJiACGHBSs='
    sheet_name = 'Warp'
    pop_range: 'Level' = RowForeign(0, 'Level')
    pop_range_territory_type: 'TerritoryType' = RowForeign(1, 'TerritoryType')
    qualified_pre_talk: 'DefaultTalk' = RowForeign(2, 'DefaultTalk')
    unqualified_pre_talk: 'DefaultTalk' = RowForeign(3, 'DefaultTalk')
    unqualified_gil_pre_talk: 'DefaultTalk' = RowForeign(4, 'DefaultTalk')
    warp_condition: 'WarpCondition' = RowForeign(5, 'WarpCondition')
    logic: 'WarpLogic' = RowForeign(6, 'WarpLogic')
    pre_cut_scene: 'Cutscene' = RowForeign(7, 'Cutscene')
    post_cut_scene: 'Cutscene' = RowForeign(8, 'Cutscene')
    skip_cut_scene_config: bool_t = RowData(9)
    text_name: str_t = RowData(10)
    text_question: str_t = RowData(11)


class WarpCondition(DataRow):
    _sign = b'WarpCondition|eJzLy4MAAA+AA3E='
    sheet_name = 'WarpCondition'
    gil: int_t = RowData(0)
    completed_quest_operator: int_t = RowData(1)
    completed_quest: 'List[Quest]' = ListData(ir((2, 3, 1)), RowForeign, 'Quest')
    not_accepted_quest: 'Quest' = RowForeign(5, 'Quest')
    reward: int_t = RowData(6)
    class_level: int_t = RowData(7)


class WarpLogic(DataRow):
    _sign = b'WarpLogic|eJzLK04rhoM8OAByAJpkC2s='
    sheet_name = 'WarpLogic'
    _display = 'script'
    map_icon: int_t = RowData(0)
    script: str_t = RowData(1)
    accept_callback: bool_t = RowData(2)
    define_name: List[str_t] = ListData(ir((3, 10, 1)), RowData)
    define_value: List[int_t] = ListData(ir((13, 10, 1)), RowData)
    text_name: str_t = RowData(23)
    text_yes: str_t = RowData(24)
    text_no: str_t = RowData(25)


class WeaponTimeline(DataRow):
    _sign = b'WeaponTimeline|eJwrzksDAAKeAUg='
    sheet_name = 'WeaponTimeline'
    file: str_t = RowData(0)
    next_weapon_timeline: int_t = RowData(1)
    not_overwritten_by_sword_on: bool_t = RowData(2)


class Weather(DataRow):
    _sign = b'Weather|eJzLKwYDAAx4AyE='
    sheet_name = 'Weather'
    _display = 'text_name'
    icon: 'Icon' = IconRow(0)
    text_name: str_t = RowData(1)
    text_name_adjective: str_t = RowData(2)
    text_weather_first: str_t = RowData(3)
    text_weather_second: str_t = RowData(4)
    text_weather_third: str_t = RowData(5)
    text_weather_fourth: str_t = RowData(6)


class WeatherGroup(DataRow):
    _sign = b'WeatherGroup|eJzLywMAAUwA3Q=='
    sheet_name = 'WeatherGroup'
    field_0: int_t = RowData(0)
    weather_rate: 'WeatherRate' = RowForeign(1, 'WeatherRate')


class WeatherRate(DataRow):
    _sign = b'WeatherRate|eJzLy0MFADqABuE='
    sheet_name = 'WeatherRate'
    weather: List[int_t] = ListData(ir((0, 8, 2)), RowData)
    rate: List[int_t] = ListData(ir((1, 8, 2)), RowData)


class WeatherReportReplace(DataRow):
    _sign = b'WeatherReportReplace|eJzLywMAAUwA3Q=='
    sheet_name = 'WeatherReportReplace'
    src: 'PlaceName' = RowForeign(0, 'PlaceName')
    dst: 'PlaceName' = RowForeign(1, 'PlaceName')


class WebGuidance(DataRow):
    _sign = b'WebGuidance|eJzLyysuLgYABpUCNg=='
    sheet_name = 'WebGuidance'
    _display = 'text_title'
    banner: 'Icon' = IconRow(0)
    url: 'WebURL' = RowForeign(1, 'WebURL')
    text_title: str_t = RowData(2)
    text_sub_title: str_t = RowData(3)
    text_description: str_t = RowData(4)


class WebURL(DataRow):
    _sign = b'WebURL|eJwrBgAAdAB0'
    sheet_name = 'WebURL'
    _display = 'text'
    text: str_t = RowData(0)


class WeddingBGM(DataRow):
    _sign = b'WeddingBGM|eJzLKwYAAVEA4g=='
    sheet_name = 'WeddingBGM'
    _display = 'bgm'
    bgm: 'BGM' = RowForeign(0, 'BGM')
    text: str_t = RowData(1)


class WeddingFlowerColor(DataRow):
    _sign = b'WeddingFlowerColor|eJzLy8sDAAKXAUs='
    sheet_name = 'WeddingFlowerColor'
    param: List[int_t] = ListData(ir((0, 3, 1)), RowData)


class WeddingPlan(DataRow):
    _sign = b'WeddingPlan|eJzLy8MEAFpQCJk='
    sheet_name = 'WeddingPlan'
    base_color_end: int_t = RowData(0)
    base_color_default: int_t = RowData(1)
    flower_color_end: int_t = RowData(2)
    flower_color_default: int_t = RowData(3)
    atmosphere_type_end: int_t = RowData(4)
    atmosphere_type_default: int_t = RowData(5)
    cloth_color_end: int_t = RowData(6)
    cloth_color_default: int_t = RowData(7)
    style_end: int_t = RowData(8)
    style_default: int_t = RowData(9)
    enter_type_end: int_t = RowData(10)
    enter_type_default: int_t = RowData(11)
    exit_type_end: int_t = RowData(12)
    exit_type_default: int_t = RowData(13)
    bgm_start: List[int_t] = ListData(ir((14, 2, 1)), RowData)
    bgm_end: List[int_t] = ListData(ir((16, 2, 1)), RowData)
    bgm_default: List[int_t] = ListData(ir((18, 2, 1)), RowData)


class WeeklyBingoOrderData(DataRow):
    _sign = b'WeeklyBingoOrderData|eJzLywMBAAkMApU='
    sheet_name = 'WeeklyBingoOrderData'
    type: int_t = RowData(0)
    value: int_t = RowData(1)
    bonus: int_t = RowData(2)
    text: 'WeeklyBingoText' = RowForeign(3, 'WeeklyBingoText')
    icon: 'Icon' = IconRow(4)
    tool_tip_type: int_t = RowData(5)


class WeeklyBingoRewardData(DataRow):
    _sign = b'WeeklyBingoRewardData|eJzLy0vLA4IkMAYAJm8Fdw=='
    sheet_name = 'WeeklyBingoRewardData'
    type: int_t = RowData(0)
    value: int_t = RowData(1)
    hq: bool_t = RowData(2)
    num: int_t = RowData(3)
    sub: int_t = RowData(4)
    sub__types: List[int_t] = ListData(ir((5, 2, 4)), RowData)
    sub__values: List[int_t] = ListData(ir((6, 2, 4)), RowData)
    sub__h_qs: List[bool_t] = ListData(ir((7, 2, 4)), RowData)
    sub__nums: List[int_t] = ListData(ir((8, 2, 4)), RowData)


class WeeklyBingoText(DataRow):
    _sign = b'WeeklyBingoText|eJwrBgAAdAB0'
    sheet_name = 'WeeklyBingoText'
    _display = 'text'
    text: str_t = RowData(0)


class WeeklyLotBonus(DataRow):
    _sign = b'WeeklyLotBonus|eJzLy6MtAADRaSlB'
    sheet_name = 'WeeklyLotBonus'
    params_target: List[int_t] = ListData(ir((0, 32, 1)), RowData)
    params_param: List[int_t] = ListData(ir((32, 32, 1)), RowData)
    params_rate: List[int_t] = ListData(ir((64, 32, 1)), RowData)


class WeeklyLotBonusThreshold(DataRow):
    _sign = b'WeeklyLotBonusThreshold|eJzLywMDAAwPAwM='
    sheet_name = 'WeeklyLotBonusThreshold'
    number: List[int_t] = ListData(ir((0, 7, 1)), RowData)


class World(DataRow):
    _sign = b'World|eJwrLs7Ly0sDAAk7Apc='
    sheet_name = 'World'
    name: str_t = RowData(0)
    display_name: str_t = RowData(1)
    management_group: int_t = RowData(2)
    user_type: int_t = RowData(3)
    dc_group: 'WorldDCGroupType' = RowForeign(4, 'WorldDCGroupType')
    public: bool_t = RowData(5)


class WorldDCGroupType(DataRow):
    _sign = b'WorldDCGroupType|eJwrzgMAAVYA4g=='
    sheet_name = 'WorldDCGroupType'
    _display = 'name'
    name: str_t = RowData(0)
    region_group: int_t = RowData(1)


class XPVPGroupActivity(DataRow):
    _sign = b'XPVPGroupActivity|eJwrzsvLAwAEZAG+'
    sheet_name = 'XPVPGroupActivity'
    text: str_t = RowData(0)
    self_param_kind: int_t = RowData(1)
    target_param_kind: int_t = RowData(2)
    param_num: int_t = RowData(3)


class YKW(DataRow):
    _sign = b'YKW|eJzLy4OAYgATZAPk'
    sheet_name = 'YKW'
    minion: int_t = RowData(0)
    legend_medal: 'Item' = RowForeign(1, 'Item')
    area: List[int_t] = ListData(ir((2, 6, 1)), RowData)
    text: str_t = RowData(8)


class YardCatalogCategory(DataRow):
    _sign = b'YardCatalogCategory|eJwrzssDAAKmAVA='
    sheet_name = 'YardCatalogCategory'
    _display = 'category'
    category: str_t = RowData(0)
    field_1: int_t = RowData(1)
    field_2: int_t = RowData(2)


class YardCatalogItemList(DataRow):
    _sign = b'YardCatalogItemList|eJzLy8sDAAKXAUs='
    sheet_name = 'YardCatalogItemList'
    _display = 'item'
    category: 'YardCatalogCategory' = RowForeign(0, 'YardCatalogCategory')
    item: 'Item' = RowForeign(1, 'Item')
    patch: int_t = RowData(2)


class ZoneSharedGroup(DataRow):
    _sign = b'ZoneSharedGroup|eJzLy8vLS8KFAbbDDCM='
    sheet_name = 'ZoneSharedGroup'
    layout_id: int_t = RowData(0)
    condition: List[int_t] = ListData(ir((1, 7, 4)), RowData)
    param_a: 'List[Quest]' = ListData(ir((2, 7, 4)), RowForeign, 'Quest')
    param_b: List[int_t] = ListData(ir((3, 7, 4)), RowData)
    anim_flag: List[bool_t] = ListData(ir((4, 7, 4)), RowData)


class ZoneTimeline(DataRow):
    _sign = b'ZoneTimeline|eJzLy8vLAwAEUAG5'
    sheet_name = 'ZoneTimeline'
    layout_id: int_t = RowData(0)
    timeline_index: int_t = RowData(1)
    start_time: int_t = RowData(2)
    end_time: int_t = RowData(3)
