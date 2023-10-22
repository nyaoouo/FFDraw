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
    EffectResult = EffectResult4 = EffectResult8 = EffectResult16 = enum.auto()
    # EffectResult4 = enum.auto()
    # EffectResult8 = enum.auto()
    # EffectResult16 = enum.auto()
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
    PingRes = enum.auto()
    PlaceFieldMarker = enum.auto()
    PlaceFieldMarkerPreset = enum.auto()
    PlayerSetup = enum.auto()
    PlayerSpawn = enum.auto()
    PlayerStats = enum.auto()
    Playtime = enum.auto()
    PrepareZoning = enum.auto()
    RetainerInformation = enum.auto()
    RsvString = enum.auto()
    RsfHeader = enum.auto()
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
    ActionSendPos = enum.auto()
    ChatHandler = enum.auto()
    ClientTrigger = enum.auto()
    EventAction = enum.auto()
    EventAction2 = EventAction
    EventAction4 = EventAction
    EventAction8 = EventAction
    EventAction16 = EventAction
    EventAction32 = EventAction
    EventAction64 = EventAction
    EventAction128 = EventAction
    EventAction255 = EventAction
    EventFinish = enum.auto()
    EventFinish2 = EventFinish
    EventFinish4 = EventFinish
    EventFinish8 = EventFinish
    EventFinish16 = EventFinish
    EventFinish32 = EventFinish
    EventFinish64 = EventFinish
    EventFinish128 = EventFinish
    EventFinish255 = EventFinish
    EventStart = enum.auto()
    InventoryModifyHandler = enum.auto()
    MarketBoardPurchaseHandler = enum.auto()
    MarketBoardQueryItemCount = enum.auto()
    PingReq = enum.auto()
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
    AddStatus = 0X14
    RemoveStatus = 0X15
    SetStatusParam = 0X16
    StatusEffect = 0X17
    SetRestExp = 0X18
    SetLockOn = 0X22
    SetChanneling = 0X23
    RemoveChanneling = 0X2F
    SetModelScale = 0X30
    SetModelAttr = 0X31
    SetTargetable = 0X36
    SetTimelineModelSkin = 0x3E
    SetTimelineModelFlag = 0x3F
    EventDirector = 0X6D
    RejectEventFinish = 0X8C
    SetMoveFlag2 = 0xEc
    SetLimitBreak = 0X1F9
    PlayActionTimeLine = 0X197
    SetActorTimeLine = 0X19D
    RejectSendAction = 0X2BC
    InterruptCast = 0X5F1
    FateState = 0X931
    FateStart = 0X934
    FateEnd = 0X935
    FateProgress = 0X93C


class ClientTriggerId(enum.Enum):
    pass
