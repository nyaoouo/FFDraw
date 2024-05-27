import enum

NULL_ENTITY_ID = 0xE0000000


def is_entity_id_valid(e_id):
    return e_id and e_id != NULL_ENTITY_ID


class ClassJob(enum.IntEnum):
    ADV = 0  # 冒险者
    GLA = 1  # 剑术师
    PGL = 2  # 格斗家
    MRD = 3  # 斧术师
    LNC = 4  # 枪术师
    ARC = 5  # 弓箭手
    CNJ = 6  # 幻术师
    THM = 7  # 咒术师
    CRP = 8  # 刻木匠
    BSM = 9  # 锻铁匠
    ARM = 10  # 铸甲匠
    GSM = 11  # 雕金匠
    LTW = 12  # 制革匠
    WVR = 13  # 裁衣匠
    ALC = 14  # 炼金术士
    CUL = 15  # 烹调师
    MIN = 16  # 采矿工
    BTN = 17  # 园艺工
    FSH = 18  # 捕鱼人
    PLD = 19  # 骑士
    MNK = 20  # 武僧
    WAR = 21  # 战士
    DRG = 22  # 龙骑士
    BRD = 23  # 吟游诗人
    WHM = 24  # 白魔法师
    BLM = 25  # 黑魔法师
    ACN = 26  # 秘术师
    SMN = 27  # 召唤师
    SCH = 28  # 学者
    ROG = 29  # 双剑师
    NIN = 30  # 忍者
    MCH = 31  # 机工士
    DRK = 32  # 暗黑骑士
    AST = 33  # 占星术士
    SAM = 34  # 武士
    RDM = 35  # 赤魔法师
    BLU = 36  # 青魔法师
    GNB = 37  # 绝枪战士
    DNC = 38  # 舞者
    RPR = 39  # 钐镰客
    SGE = 40  # 贤者
