from .utils import *


class SchedulerItem(AVfxStruct):
    is_enable = KeyAttr.bool(b'bEna', False, s_int32)
    scheduler_no = KeyAttr.simple(b'TlNo', 0, s_int16)
    timeline_no = KeyAttr.simple(b'TN', 0, s_int32)
    start_time_ = KeyAttr.simple(b'StTm', 0, s_int16)
    start_time = KeyAttr.simple(b'ST', 0, s_int32)


class Scheduler(AVfxStruct):
    item_list = KeyListAttr.struct(b'ItCn', b'Item', SchedulerItem)
    trigger_list = KeyListAttr.struct(b'TrCn', b'Trgr', SchedulerItem)
