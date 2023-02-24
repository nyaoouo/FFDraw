import enum


class ActionEffectType(enum.Enum):
    miss = 0X1
    resist = 0X2
    damage = 0X3
    healing = 0X4
    blocked_damage = 0X5
    parry_damage = 0X6
    invincible = 0X7
    damage_mp = 0XA
    healing_mp = 0XB
    healing_gp = 0XD
    add_status_target = 0XE
    add_status_source = 0XF
    threat_top = 0X18
    threat_extra = 0X19
    combo = 0X1B
    combo_hit = 0X1C
    knock_back = 0X20
    absorb = 0X21
    status_resist = 0X37
