import struct
import dataclasses
from ff_draw.mem.actor import is_invalid_id
from . import TypeMap, ActorControlId

type_map = TypeMap()


@type_map.set(ActorControlId.SetCombatState)  # 0x4
@dataclasses.dataclass
class SetCombatState:
    is_in_combat: int


@type_map.set(ActorControlId.ChangeClassJob)  # 0x5
@dataclasses.dataclass
class ChangeClassJob:
    class_job: int


@type_map.set(ActorControlId.Death)  # 0x6
@dataclasses.dataclass
class Death:
    _killer1: int
    _killer2: int

    @property
    def killer(self):
        if not is_invalid_id(self._killer1): return self._killer1
        if not is_invalid_id(self._killer2): return self._killer2
        return 0


@type_map.set(ActorControlId.CancelCast)  # 0XF
@dataclasses.dataclass
class CancelCast:
    log_type: int
    action_kind: int
    action_id: int
    is_passive: int


@type_map.set(ActorControlId.InterruptCast)  # 0X931
@dataclasses.dataclass
class InterruptCast:
    action_id: int
    _remain_time: int
    source_id: int
    action_kind = 1

    remain_time = property(lambda self: struct.unpack('f', struct.pack('i', self.remain_time))[0])


@type_map.set(ActorControlId.SetRecastGroupDuration)  # 0X10
@dataclasses.dataclass
class SetRecastGroupDuration:
    recast_group_id: int
    _duration: int
    _max_time: int

    duration = property(lambda self: self._duration / 100)
    max_time = property(lambda self: self._max_time / 100)


@type_map.set(ActorControlId.SetRecastGroupMax)  # 0X11
@dataclasses.dataclass
class SetRecastGroupMax:
    recast_group_id: int
    action_id: int
    _max_time: int

    max_time = property(lambda self: self._max_time / 100)


@type_map.set(ActorControlId.AddStatus)  # 0X14
@dataclasses.dataclass
class AddStatus:
    status_id: int
    param: int


@type_map.set(ActorControlId.RemoveStatus)  # 0X15
@dataclasses.dataclass
class RemoveStatus:
    status_id: int
    param: int
    source_id: int
    is_extra: int


@type_map.set(ActorControlId.SetStatusParam)  # 0X16
@dataclasses.dataclass
class SetStatusParam:
    status_idx: int
    status_id: int
    param: int


@type_map.set(ActorControlId.StatusEffect)  # 0X17
@dataclasses.dataclass
class StatusEffect:
    status_id: int
    effect_type: int
    value: int
    source_id: int


@type_map.set(ActorControlId.SetLockOn)  # 0X22
@dataclasses.dataclass
class SetLockOn:
    lockon_id: int


@type_map.set(ActorControlId.SetChanneling)  # 0X23
@dataclasses.dataclass
class SetChanneling:
    idx: int
    channel_id: int
    target_id: int
    _width: int

    width = property(lambda self: self._width / 100)


@type_map.set(ActorControlId.RemoveChanneling)  # 0X2F
@dataclasses.dataclass
class RemoveChanneling:
    idx: int
    channel_id: int


@type_map.set(ActorControlId.SetModelAttr)  # 0X31
@dataclasses.dataclass
class SetModelAttr:
    value: int


@type_map.set(ActorControlId.SetTargetable)  # 0X36
@dataclasses.dataclass
class SetTargetable:
    is_targetable: int


@type_map.set(ActorControlId.EventDirector)  # 0X6D
@dataclasses.dataclass
class EventDirector:
    pass


@type_map.set(ActorControlId.SetLimitBreak)  # 0X1F9
@dataclasses.dataclass
class SetLimitBreak:
    # 0:party, 1:single player, 2:gc trust, 3:trust, 4:special
    max_level: int
    value: int
    value_first: int
    is_fine_play: int
    type: int


@type_map.set(ActorControlId.PlayActionTimeLine)  # 0X197
@dataclasses.dataclass
class PlayActionTimeLine:
    action_timeline_id: int


@type_map.set(ActorControlId.SetActorTimeLine)  # 0X19D
@dataclasses.dataclass
class SetActorTimeLine:
    param1: int
    param2: int


@type_map.set(ActorControlId.RejectSendAction)  # 0X2BC
@dataclasses.dataclass
class RejectSendAction:
    log_type: int
    action_kind: int
    action_id: int
    _recast_duration: int
    _recast_max: int
    request_id: int

    recast_duration = property(lambda self: self._recast_duration / 100)
    recast_max = property(lambda self: self._recast_max / 100)


@type_map.set(ActorControlId.FateInit)  # 0X931
@dataclasses.dataclass
class FateInit:
    pass


@type_map.set(ActorControlId.FateProgress)  # 0X934
@dataclasses.dataclass
class FateProgress:
    pass


@type_map.set(ActorControlId.FateStart)  # 0X935
@dataclasses.dataclass
class FateStart:
    pass


@type_map.set(ActorControlId.FateEnd)  # 0X936
@dataclasses.dataclass
class FateEnd:
    pass
