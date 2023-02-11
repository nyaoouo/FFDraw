import enum


class MacroType(enum.Enum):
    BEGIN = 0x02
    END = 0x03

    # control
    SETRESETTIME = 0x06  # Set the value of the specified day of the week as the time (hour[, weekday])
    SETTIME = 0x07  # set numeric value as time (time_val)
    IF = 0x08  # replace first or second parameter by number (cond, true, false)
    SWITCH = 0x09  # Substitute by numeric value for its numeric-th parameter (key, *state)=>state[key]

    # special
    PCNAME = 0x0A  # player's name string from entity_id (entity_id)
    IFPCGENDER = 0x0B  # Convert entity_id to player's gender and process if_else (entity_id, any1, any2)
    IfPcName = 0x0C  # Get player's name string from entity_id and process if_else (entity_id, any1, any2, any3)
    IFPCNAME = 0x0F  # Determine if it is your character from entity_id and process if_else
    LINK = 0x27  # Text link (link type, number value, color, hover color, string)
    SOUND = 0x60  # (number1, number2)
    LEVELPOS = 0x61  # (number)

    # Korean Particle
    JOSA = 0x0D  # (string1, string2, string3)
    JOSARO = 0x0E  # (string1, string2, string3)

    # display
    BR = 0x10  # break line
    WAIT = 0x11  # wait (time ms)
    ICON = 0x12  # icon(icon_id)
    FONTCOLOR = 0x13  # set font color (color_val[, num1])
    EDGECOLOR = 0x14  # set edge color (color_val[, num1])
    SHADOWCOLOR = 0x15  # set shadow color (color_val[, num1])
    HYPHEN = 0x16  # hyphen
    KEY = 0x17  # equal to WAIT(0)

    SCALE = 0x18  # Scale change (scale in %)
    BOLD = 0x19  # Bold (1/0)
    ITALIC = 0x1A  # italic (1/0)
    EDGE = 0x1B  # Edge (1/0)
    SHADOW = 0x1C  # shadow (1/0)
    NBSP = 0x1D  # non-breaking space
    ICON2 = 0x1E  # icon(icon_id[, size in %])
    NBHYPHEN = 0x1F  # non-breaking hyphen

    COLORTYPE = 0x48  # Font color specification (color_val)
    EDGECOLORTYPE = 0x49  # Specify character edge color (color_val)
    RUBY = 0x4a  # Ruby (string, upper string)

    # number
    NUM = 0x20  # (number)
    HEX = 0x21  # (number)
    KILO = 0x22  # (number, sep)
    BYTE = 0x23  # (number)
    SEC = 0x24  # (number)
    TIME = 0x25  # (number)
    FLOAT = 0x26  # (number1, number2,sep)
    DIGIT = 0x50  # (number1, number2)
    ORDINAL = 0x51  # (number)

    # strings
    SHEET = 0x28  # String of specified sheet (sheet name, row, column)
    STRING = 0x29  # (string)
    CAPS = 0x2A  # (string)
    HEAD = 0x2B  # (string)
    SPLIT = 0x2C  # (string,string,number)
    HEADALL = 0x2D  # (string)
    FIXED = 0x2E  # (data_size, type, *args)
    LOWER = 0x2F  # (string)
    LOWERHEAD = 0x40  # (string)

    # localize
    JA_NOUN = 0x30  # Japanese noun
    EN_NOUN = 0x31  # English noun
    DE_NOUN = 0x32  # German noun
    FR_NOUN = 0x33  # French noun
    CH_NOUN = 0x34  # Chinese noun
    KO_NOUN = 0x35  # Korean noun


class MACRODEFPARAM(enum.Enum):
    # Immediate data that is sufficient up to IMD_MAX is added by 1
    IMD_BEGIN = 0x01
    IMD_MAX = 0xCE
    IMD_END = 0xCF

    # current time
    TIME_MS = 0xD8  # milliseconds
    TIME_SEC = 0xD9  # seconds
    TIME_MIN = 0xDA  # minutes
    TIME_HOUR = 0xDB  # hour
    TIME_DAY = 0xDC  # days
    TIME_WDAY = 0xDD  # day of the week
    TIME_MON = 0xDE  # month
    TIME_YEAR = 0xDF  # year

    # cond
    COND_GTEQ = 0xE0  # int(a1 >= a2)
    COND_GT = 0xE1  # int(a1 > a2)
    COND_LTEQ = 0xE2  # int(a1 <= a2)
    COND_LT = 0xE3  # int(a1 < a2)
    COND_EQ = 0xE4  # int(a1 == a2)
    COND_NEQ = 0xE5  # int(a1 != a2)

    # parameter reference
    PARAM_LOC_NUM = 0xE8  # int(local[a1])
    PARAM_GLOB_NUM = 0xE9  # int(global[a1])
    PARAM_LOC_STR = 0xEA  # str(local[a1])
    PARAM_GLOB_STR = 0xEB  # str(global[a1])
    PARAM_PREV_COLOR = 0xEC  # last set color


class LinkType(enum.Enum):
    PLAYER = 0
    SELF = 1
    ITEM = 2
    MAP = 3
    QUEST = 4
    ACHIEVE = 5
    HOWTO = 6
    PARTYFINDER = 7
    STATUS = 8
    PARTYFINDER_DETAIL = 9
    UNENDING_CODEX = 10
