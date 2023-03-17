import enum

from nylib.utils.enum import auto_missing


@auto_missing
class ZoneServer(enum.Enum):
    ActorCast = enum.auto()
    ActorControl = enum.auto()
    ActorControlSelf = enum.auto()
    ActorControlTarget = enum.auto()
    ActorDelete = enum.auto()
    ActorGauge = enum.auto()
    ActorMove = enum.auto()
    ActorSetPos = enum.auto()
    AirshipExplorationResult = enum.auto()
    AirshipStatus = enum.auto()
    AirshipStatusList = enum.auto()
    AoeEffect16 = enum.auto()
    AoeEffect24 = enum.auto()
    AoeEffect32 = enum.auto()
    AoeEffect8 = enum.auto()
    BossStatusEffectList = enum.auto()
    CEDirector = enum.auto()
    CFPreferredRole = enum.auto()
    ContainerItemInfo = enum.auto()
    ContentFinderNotifyPop = enum.auto()
    Effect = enum.auto()
    EffectResult = enum.auto()
    EffectResult4 = enum.auto()
    EffectResult8 = enum.auto()
    EffectResult16 = enum.auto()
    EventActionResultN = enum.auto()
    EventFinish = enum.auto()
    EventPlayN = enum.auto()
    EventStart = enum.auto()
    Examine = enum.auto()
    ExamineSearchInfo = enum.auto()
    FateInfo = enum.auto()
    FreeCompanyDialog = enum.auto()
    FreeCompanyInfo = enum.auto()
    InitZone = enum.auto()
    InventoryActionAck = enum.auto()
    InventoryTransaction = enum.auto()
    InventoryTransactionFinish = enum.auto()
    ItemMarketBoardInfo = enum.auto()
    Logout = enum.auto()
    MapEffect = enum.auto()
    MarketBoardItemListing = enum.auto()
    MarketBoardItemListingCount = enum.auto()
    MarketBoardItemListingHistory = enum.auto()
    MarketBoardPurchase = enum.auto()
    MarketBoardSearchResult = enum.auto()
    NpcSpawn = enum.auto()
    NpcSpawn2 = enum.auto()
    NpcYell = enum.auto()
    ObjectSpawn = enum.auto()
    PartyUpdate = enum.auto()
    PlaceFieldMarker = enum.auto()
    PlaceFieldMarkerPreset = enum.auto()
    PlayerSetup = enum.auto()
    PlayerSpawn = enum.auto()
    PlayerStats = enum.auto()
    Playtime = enum.auto()
    PrepareZoning = enum.auto()
    RetainerInformation = enum.auto()
    RsvString = enum.auto()
    StartActionTimelineMulti = enum.auto()
    StatusEffectList = enum.auto()
    StatusEffectList2 = enum.auto()
    StatusEffectList3 = enum.auto()
    SubmarineExplorationResult = enum.auto()
    SubmarineProgressionStatus = enum.auto()
    SubmarineStatusList = enum.auto()
    SystemLogMessage = enum.auto()
    UpdateClassInfo = enum.auto()
    UpdateHpMpGp = enum.auto()
    UpdateInventorySlot = enum.auto()
    UpdateSearchInfo = enum.auto()
    WardLandInfo = enum.auto()
    Unk = -1


@auto_missing
class ZoneClient(enum.Enum):
    ActionSend = enum.auto()
    ChatHandler = enum.auto()
    ClientTrigger = enum.auto()
    EventAction = enum.auto()
    EventAction4 = enum.auto()
    EventAction8 = enum.auto()
    EventFinish = enum.auto()
    EventStart = enum.auto()
    InventoryModifyHandler = enum.auto()
    MarketBoardPurchaseHandler = enum.auto()
    MarketBoardQueryItemCount = enum.auto()
    SetSearchInfoHandler = enum.auto()
    UpdatePositionHandler = enum.auto()
    UpdatePositionInstance = enum.auto()
    Unk = -1


@auto_missing
class ChatServer(enum.Enum):
    Unk = -1


@auto_missing
class ChatClient(enum.Enum):
    Unk = -1


class ActorControlId(enum.Enum):
    SetCombatState = 0X4
    ChangeClassJob = 0x5
    Death = 0x6
    CancelCast = 0XF
    SetRecastGroupDuration = 0X11
    SetRecastGroupMax = 0X11
    AddStatus = 0X14
    RemoveStatus = 0X15
    SetStatusParam = 0X16
    StatusEffect = 0X17
    SetLockOn = 0X22
    SetChanneling = 0X23
    RemoveChanneling = 0X2F
    SetModelAttr = 0X31
    SetTargetable = 0X36
    EventDirector = 0X6D
    SetLimitBreak = 0X1F9
    PlayActionTimeLine = 0X197
    SetActorTimeLine = 0X19D
    RejectSendAction = 0X2BC
    InterruptCast = 0X5F1
    FateInit = 0X931
    FateProgress = 0X934
    FateStart = 0X935
    FateEnd = 0X936


class ClientTriggerId(enum.Enum):
    pass
