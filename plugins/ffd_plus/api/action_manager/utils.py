import enum

from ff_draw.main import FFDraw
from ffd_plus.api.utils import sq_pack
from fpt4.utils.sqpack.exd.define import Action


class RecastGroup(enum.IntEnum):
    gcd = 58


class ActionKind(enum.IntEnum):
    normal = 1
    item = 2
    event_item = 3
    event_action = 4
    general = 5
    buddy = 6
    craft = 9
    fishing = 10
    pet = 11
    mount = 13
    pvp_action = 14
    field_marker = 15
    ornament = 20


def get_real_action_id(action_kind, key):
    # e8 * * * * c6 44 24 ? ? 44 ? ? ? 8b
    match action_kind:
        case ActionKind.normal:  # normal
            return key
        case ActionKind.item:  # item
            try:
                return FFDraw.instance.sq_pack.sheets.item_sheet[key].action.key
            except KeyError:
                return 0
        case ActionKind.event_item:  # event item
            try:
                return FFDraw.instance.sq_pack.sheets.event_item_sheet[key].action.key
            except KeyError:
                return 0
        case ActionKind.event_action:  # event action
            return 2
        case ActionKind.mount:  # mount
            return 4
        case ActionKind.ornament:  # ornament
            return 20061
        case ActionKind.general:  # general
            if key == 26:
                from ffd_plus.api.framework import Framework
                if (cd := Framework.instance.content_director) and (cea := cd.content_ex_action):
                    return cea.get_action_id(0)
            elif key == 27:
                from ffd_plus.api.framework import Framework
                if (cd := Framework.instance.content_director) and (cea := cd.content_ex_action):
                    return cea.get_action_id(1)
            else:
                try:
                    return FFDraw.instance.sq_pack.sheets.general_action_sheet[key].action.key
                except KeyError:
                    return 0
    return 0


def get_action_recast_index(action_kind, key, check_self=True):
    # e8 * * * * 8b ? 48 ? ? e8 ? ? ? ? 48 ? ? 75 ? 0f
    sheets = FFDraw.instance.sq_pack.sheets
    match action_kind:
        case ActionKind.normal:  # normal
            try:
                action = sheets.action_sheet[key]
            except KeyError:
                return -1
            recast_index = action.recast_group - 1

            if 80 <= recast_index <= 81:
                from ffd_plus.api.framework import Framework
                if check_self and (cd := Framework.instance.content_director) and (cea := cd.content_ex_action) and (ex_slot := cea.get_action_idx(key)) >= 0:
                    return ex_slot + recast_index
                return -1
            if check_self:
                if required_class_job := action.learn.key:
                    from ffd_plus.api.ui.player_status import PlayerStatus
                    current_class_job = PlayerStatus.instance.get_class_job(True)
                    if required_class_job != current_class_job:
                        try:
                            main_class_job = sheets.class_job_sheet[current_class_job].main_class.key
                        except KeyError:
                            return -1
                        if required_class_job != main_class_job:
                            return -1
            return recast_index
        case ActionKind.item:  # item
            try:
                action = sheets.item_sheet[key].action.action
            except (KeyError, AttributeError):
                return -1
            return action.recast_group - 1
        case ActionKind.event_item:  # event item
            return 64
        case ActionKind.event_action:  # event action
            if 26 <= key <= 27:
                if check_self:
                    from ffd_plus.api.framework import Framework
                    if (cd := Framework.instance.content_director) and (cea := cd.content_ex_action):
                        return get_action_recast_index(1, cea.get_action_id(key - 26), check_self)
            else:
                try:
                    return sheets.general_action_sheet[key].recast - 1
                except (KeyError, AttributeError):
                    return -1
        case ActionKind.mount:  # mount
            from ffd_plus.api import GameMain
            if not check_self or GameMain.instance.territory_intended_use == 25:
                return 65
        case ActionKind.pvp_action:  # pvp
            try:
                action = sheets.pvp_action_sheet[key].action
            except (KeyError, AttributeError):
                return -1
            return get_action_recast_index(1, action.key, check_self)
    return -1


def pvp_action_allowed(action: int | Action):
    # 40 ? 48 ? ? ? 0f ? ? ? 48 ? ? 3c ? 72 ? 3c
    if isinstance(action, int):
        action = sq_pack.sheets.action_sheet[action]
    cate = action.category
    match cate:
        case 2 | 3 | 4:
            if (l := action.learn).key and l.kind == 33: return True
            if not action.pvp_only: return False
        case 9 | 15:
            if not action.pvp_only: return False
    return True
