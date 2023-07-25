import typing
from enum import Enum


class Language(Enum):
    none = 0
    ja = 1
    en = 2
    de = 3
    fr = 4
    chs = 5
    cht = 6
    ko = 7
    suffix = property(lambda self: "_" + self.name if self.value else '')


class EventType(Enum):
    Quest = 1
    Warp = 2
    GatheringPoint = 3
    GilShop = 4
    Aetheryte = 5
    GuildleveAssignment = 6
    DefaultTalk = 9
    Craft = 10
    CustomTalk = 11
    Array = 13
    CraftLeve = 14
    GimmickAccessor = 15
    GimmickBill = 16
    GimmickRect = 17
    ChocoboTaxiStand = 18
    Opening = 19
    GCShop = 22
    GuildOrderGuide = 23
    GuildOrderOfficer = 24
    Story = 26
    SpecialShop = 27
    InstanceContentGuide = 29
    HousingAethernet = 30
    SwitchTalk = 31
    Adventure = 33
    TripleTriad = 35
    GoldSaucerArcadeMachine = 36
    FccShop = 42
    AetherCurrent = 43
    ContentEntry = 44
    DpsChallengeOfficer = 47
    TopicSelect = 50
    LotteryExchangeShop = 52
    DisposalShop = 53
    PreHandler = 54
    Description = 55
    InclusionShop = 58
    CollectablesShop = 59
    EventPathMove = 61


def icon_path(icon_id: int, is_hq: bool = False, language: Language | str = None):
    if language is None:
        language = ''
    elif isinstance(language, Language):
        language = language.name + '/'
    elif not language.endswith('/'):
        language += '/'
    return f"ui/icon/{icon_id // 1000:03d}000/{language}{icon_id:06d}" + ('_hr1.tex' if is_hq else '.tex')


def map_path(sq_pack, map_id, size='m'):
    _path = sq_pack.sheets.map_sheet[map_id].path
    t_name, map_idx = _path.split('/', 1)
    return f'ui/map/{t_name}/{map_idx}/{t_name}{map_idx}_{size}.tex'
