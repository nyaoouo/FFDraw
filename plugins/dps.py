import enum
import time

import imgui

from nylib.utils.imgui.window_mgr import Window

from ff_draw.gui.default_style import set_style, pop_style
from ff_draw.plugins import FFDrawPlugin
from ff_draw.sniffer.utils.message import NetworkMessage, ActorControlMessage
from ff_draw.sniffer.message_structs import zone_server, actor_control, ZoneServer, ActorControlId


class EffectType:
    damage_hp = 3
    heal_hp = 4
    block_damage_hp = 5
    parry_damage_hp = 6


def is_valid_id(actor_id):
    return actor_id != 0 and actor_id != 0xe0000000


class Data:
    def __init__(self):
        self.taken_damage = 0
        self.cause_damage = 0
        self.cause_damage_count = 0
        self.cause_damage_critical = 0
        self.cause_damage_direct = 0
        self.taken_heal = 0
        self.cause_heal = 0
        self.cause_heal_count = 0
        self.cause_heal_critical = 0


class Actor:
    def __init__(self, actor_id):
        self.actor_id = actor_id
        self.data = Data()
        self.data_in_window = Data()
        self.death_count = 0


class Monitor:
    window_sec = 60
    damage_event = 1
    heal_event = 2
    actors: dict[int, Actor]

    def __init__(self, territory_id=0):
        self.territory_id = territory_id
        self.actors = {}
        self.events = []
        self.start_at = 0
        self.pet_cache = {}

    @property
    def last_event_at(self):
        if not self.events: return 0
        return self.events[-1][0]

    def get_actor(self, actor_id):
        if not is_valid_id(actor_id): return None
        if actor_id not in self.actors:
            self.actors[actor_id] = Actor(actor_id)
        return self.actors[actor_id]

    def on_damage(self, time_stamp, source, target, value, is_status=False, is_critical=False, is_direct=False, owner_id=0):
        if is_valid_id(source):
            if is_valid_id(owner_id):
                self.pet_cache.setdefault(owner_id, set()).add(source)
            source_actor = self.get_actor(source)
            source_actor.data.cause_damage += value
            source_actor.data_in_window.cause_damage += value
            if not is_status:
                source_actor.data.cause_damage_count += 1
                source_actor.data_in_window.cause_damage_count += 1
                if is_critical:
                    source_actor.data.cause_damage_critical += 1
                    source_actor.data_in_window.cause_damage_critical += 1
                if is_direct:
                    source_actor.data.cause_damage_direct += 1
                    source_actor.data_in_window.cause_damage_direct += 1
        if is_valid_id(target):
            target_actor = self.get_actor(target)
            target_actor.data.taken_damage += value
            target_actor.data_in_window.taken_damage += value
        self.events.append((time_stamp, self.damage_event, (source, target, value, is_status, is_critical, is_direct)))
        if not self.start_at: self.start_at = time_stamp
        self.dequeue_events(time_stamp - self.window_sec)

    def on_heal(self, time_stamp, source, target, value, is_status=False, is_critical=False, owner_id=0):
        if is_valid_id(source):
            if is_valid_id(owner_id):
                self.pet_cache.setdefault(owner_id, set()).add(source)
            source_actor = self.get_actor(source)
            source_actor.data.cause_heal += value
            source_actor.data_in_window.cause_heal += value
            if not is_status:
                source_actor.data.cause_heal_count += 1
                source_actor.data_in_window.cause_heal_count += 1
                if is_critical:
                    source_actor.data.cause_heal_critical += 1
                    source_actor.data_in_window.cause_heal_critical += 1
        if is_valid_id(target):
            target_actor = self.get_actor(target)
            target_actor.data.taken_heal += value
            target_actor.data_in_window.taken_heal += value
        self.events.append((time_stamp, self.heal_event, (source, target, value, is_status, is_critical)))
        if not self.start_at: self.start_at = time_stamp
        self.dequeue_events(time_stamp - self.window_sec)

    def on_death(self, actor_id):
        if is_valid_id(actor_id):
            self.get_actor(actor_id).death_count += 1

    def dequeue_events(self, before):
        while self.events:
            if self.events[0][0] >= before: break
            _, event_type, event_args = self.events.pop(0)
            if event_type == self.damage_event:
                self.dequeue_on_damage(*event_args)
            elif event_type == self.heal_event:
                self.dequeue_on_heal(*event_args)

    def dequeue_on_damage(self, source, target, value, is_status, is_critical, is_direct):
        if source and source in self.actors:
            source_actor = self.actors[source]
            source_actor.data_in_window.cause_damage -= value
            if not is_status:
                source_actor.data_in_window.cause_damage_count -= 1
                if is_critical:
                    source_actor.data_in_window.cause_damage_critical -= 1
                if is_direct:
                    source_actor.data_in_window.cause_damage_direct -= 1
        if target and target in self.actors:
            target_actor = self.actors[target]
            target_actor.data_in_window.taken_damage -= value

    def dequeue_on_heal(self, source, target, value, is_status, is_critical):
        if source and source in self.actors:
            source_actor = self.actors[source]
            source_actor.data_in_window.cause_heal -= value
            if not is_status:
                source_actor.data_in_window.cause_heal_count -= 1
                if is_critical:
                    source_actor.data_in_window.cause_heal_critical -= 1
        if target and target in self.actors:
            target_actor = self.actors[target]
            target_actor.data_in_window.taken_heal -= value

    def actor_dps(self, actor_id, in_window, calc_pet=False):
        if not (dur := self.last_event_at - self.start_at):
            dur = 1
        if in_window:
            get_data = lambda actor: actor.data_in_window
            dur = min(self.window_sec, dur)
        else:
            get_data = lambda actor: actor.data
        total_damage = get_data(self.actors[actor_id]).cause_damage if actor_id in self.actors else 0
        if calc_pet:
            total_damage = sum((
                get_data(self.actors[pet_id]).cause_damage
                for pet_id in self.pet_cache.get(actor_id, ())
                if pet_id in self.actors
            ), total_damage)
        return total_damage / dur

    def actor_hps(self, actor_id, in_window, calc_pet=False):
        if not (dur := self.last_event_at - self.start_at):
            dur = 1
        if in_window:
            get_data = lambda actor: actor.data_in_window
            dur = min(self.window_sec, dur)
        else:
            get_data = lambda actor: actor.data
        total_heal = get_data(self.actors[actor_id]).cause_heal if actor_id in self.actors else 0
        if calc_pet:
            total_heal = sum((
                get_data(self.actors[pet_id]).cause_heal
                for pet_id in self.pet_cache.get(actor_id, ())
                if pet_id in self.actors
            ), total_heal)
        return total_heal / dur

    def actor_dtps(self, actor_id, in_window):
        if actor_id not in self.actors: return 0
        if not (dur := self.last_event_at - self.start_at): dur = 1
        if in_window:
            data = self.actors[actor_id].data_in_window
            dur = min(self.window_sec, dur)
        else:
            data = self.actors[actor_id].data
        return data.taken_damage / dur

    def actor_htps(self, actor_id, in_window):
        if actor_id not in self.actors: return 0
        if not (dur := self.last_event_at - self.start_at): dur = 1
        if in_window:
            data = self.actors[actor_id].data_in_window
            dur = min(self.window_sec, dur)
        else:
            data = self.actors[actor_id].data
        return data.taken_heal / dur

    def actor_critical_rate(self, actor_id, in_window, include_heal=False, calc_pet=False):
        get_data = (lambda actor: actor.data_in_window) if in_window else (lambda actor: actor.data)
        total = 0
        c_total = 0
        if actor_id in self.actors:
            data = get_data(self.actors[actor_id])
            total = data.cause_damage_count
            if include_heal: total += data.cause_heal_count
            c_total = data.cause_damage_critical
            if include_heal: c_total += data.cause_heal_critical
        if calc_pet:
            for pet_id in self.pet_cache.get(actor_id, ()):
                if pet_id not in self.actors: continue
                data = get_data(self.actors[pet_id])
                total += data.cause_damage_count
                if include_heal: total += data.cause_heal_count
                c_total += data.cause_damage_critical
                if include_heal: c_total += data.cause_heal_critical
        return c_total / total if total else 0

    def actor_direct_rate(self, actor_id, in_window, calc_pet=False):
        get_data = (lambda actor: actor.data_in_window) if in_window else (lambda actor: actor.data)
        total = 0
        d_total = 0
        if actor_id in self.actors:
            data = get_data(self.actors[actor_id])
            total = data.cause_damage_count
            d_total = data.cause_damage_direct
        if calc_pet:
            for pet_id in self.pet_cache.get(actor_id, ()):
                if pet_id not in self.actors: continue
                data = get_data(self.actors[pet_id])
                total += data.cause_damage_count
                d_total += data.cause_damage_direct
        return d_total / total if total else 0

    def death_count(self, actor_id):
        if actor_id not in self.actors: return 0
        return self.actors[actor_id].death_count


class DisplayColumn(enum.Enum):
    ActorName = 0
    ActorJob = 1

    Dps = 2
    Hps = 3
    Dtps = 4
    Htps = 5
    CriticalRate = 6
    DirectRate = 7

    DpsInWindow = 8
    HpsInWindow = 9
    DtpsInWindow = 10
    HtpsInWindow = 11
    CriticalRateInWindow = 12
    DirectRateInWindow = 13

    DeathCount = 14


ColumnName = {
    DisplayColumn.ActorName.value: 'Name',
    DisplayColumn.ActorJob.value: 'Job',
    DisplayColumn.Dps.value: 'DPS',
    DisplayColumn.Hps.value: 'HPS',
    DisplayColumn.Dtps.value: 'DTPS',
    DisplayColumn.Htps.value: 'HTPS',
    DisplayColumn.CriticalRate.value: 'CR',
    DisplayColumn.DirectRate.value: 'DR',
    DisplayColumn.DpsInWindow.value: 'DPS(min)',
    DisplayColumn.HpsInWindow.value: 'HPS(min)',
    DisplayColumn.DtpsInWindow.value: 'DTPS(min)',
    DisplayColumn.HtpsInWindow.value: 'HTPS(min)',
    DisplayColumn.CriticalRateInWindow.value: 'CR(min)',
    DisplayColumn.DirectRateInWindow.value: 'DR(min)',
    DisplayColumn.DeathCount.value: 'Death',
}


class DpsWindow:
    def __init__(self, main: 'Dps'):
        self.main = main
        self.window = None

    def on_want_close(self, w: Window):
        self.main.window = None
        self.window = None
        return True

    def before_draw_window(self, w: Window):
        if self.window is None:
            self.window = w
        set_style(self.main.main.gui.panel.style_color)

    def after_draw_window(self, w: Window):
        pop_style()

    def draw(self, w: Window):
        self.main.draw_table()


class Dps(FFDrawPlugin):
    monitor: Monitor = None
    _member_ids = []

    def __init__(self, main):
        super().__init__(main)
        self.cutoff = self.data.setdefault('cutoff', 60)  # sec to cut off
        self.cols = self.data.setdefault('cols', [0, 2, 8, 3, 6, 7, 14])
        self.separate_owner = self.data.setdefault('separate_owner', True)
        self.sort_by = self.data.setdefault('sort_by', 2)

        self._sort_by_key = lambda actor_id: 0
        self._cols_getter = []
        self._cached_owner = {}
        self._cached_name = {}
        self.__must_cut = False

        self._class_job_sheet = self.main.sq_pack.sheets.class_job_sheet
        self._world_sheet = self.main.sq_pack.sheets.world_sheet

        self.main.sniffer.on_action_effect.append(self.on_effect)
        self.main.sniffer.on_actor_control[ActorControlId.StatusEffect].append(self.on_actor_control_status_effect)
        self.main.sniffer.on_actor_control[ActorControlId.Death].append(self.on_actor_control_death)

        self.update_cols_getter()
        self.update_sort_by_key()

        self.window = None

    def on_unload(self):
        self.main.sniffer.on_action_effect.remove(self.on_effect)
        self.main.sniffer.on_actor_control[ActorControlId.StatusEffect].remove(self.on_actor_control_status_effect)
        self.main.sniffer.on_actor_control[ActorControlId.Death].remove(self.on_actor_control_death)
        try:
            self.window.window.close()
        except:
            pass

    def update_sort_by_key(self):
        if self.sort_by == DisplayColumn.Dps.value:
            self._sort_by_key = lambda actor_id: self.monitor.actor_dps(actor_id, False, not self.separate_owner) if self.monitor else 0
        elif self.sort_by == DisplayColumn.Hps.value:
            self._sort_by_key = lambda actor_id: self.monitor.actor_hps(actor_id, False, not self.separate_owner) if self.monitor else 0
        elif self.sort_by == DisplayColumn.Dtps.value:
            self._sort_by_key = lambda actor_id: self.monitor.actor_dtps(actor_id, False) if self.monitor else 0
        elif self.sort_by == DisplayColumn.Htps.value:
            self._sort_by_key = lambda actor_id: self.monitor.actor_htps(actor_id, False) if self.monitor else 0
        elif self.sort_by == DisplayColumn.CriticalRate.value:
            self._sort_by_key = lambda actor_id: self.monitor.actor_critical_rate(actor_id, False, not self.separate_owner) if self.monitor else 0
        elif self.sort_by == DisplayColumn.DirectRate.value:
            self._sort_by_key = lambda actor_id: self.monitor.actor_direct_rate(actor_id, False, not self.separate_owner) if self.monitor else 0
        elif self.sort_by == DisplayColumn.DpsInWindow.value:
            self._sort_by_key = lambda actor_id: self.monitor.actor_dps(actor_id, True, not self.separate_owner) if self.monitor else 0
        elif self.sort_by == DisplayColumn.HpsInWindow.value:
            self._sort_by_key = lambda actor_id: self.monitor.actor_hps(actor_id, True, not self.separate_owner) if self.monitor else 0
        elif self.sort_by == DisplayColumn.DtpsInWindow.value:
            self._sort_by_key = lambda actor_id: self.monitor.actor_dtps(actor_id, True) if self.monitor else 0
        elif self.sort_by == DisplayColumn.HtpsInWindow.value:
            self._sort_by_key = lambda actor_id: self.monitor.actor_htps(actor_id, True) if self.monitor else 0
        elif self.sort_by == DisplayColumn.CriticalRateInWindow.value:
            self._sort_by_key = lambda actor_id: self.monitor.actor_critical_rate(actor_id, True, not self.separate_owner) if self.monitor else 0
        elif self.sort_by == DisplayColumn.DirectRateInWindow.value:
            self._sort_by_key = lambda actor_id: self.monitor.actor_direct_rate(actor_id, True, not self.separate_owner) if self.monitor else 0
        elif self.sort_by == DisplayColumn.DeathCount.value:
            self._sort_by_key = lambda actor_id: self.monitor.death_count(actor_id) if self.monitor else 0
        else:
            self._sort_by_key = lambda actor_id: 0

    def get_cols_getter(self, col):
        if col == DisplayColumn.ActorName.value:
            return self.actor_name
        elif col == DisplayColumn.ActorJob.value:
            return lambda actor_id: self._class_job_sheet[getattr(self.main.mem.actor_table.get_actor_by_id(actor_id), 'class_job', 0)].text_abbreviation
        elif col == DisplayColumn.Dps.value:
            return lambda actor_id: f'{self.monitor.actor_dps(actor_id, False, not self.separate_owner):.0f}' if self.monitor else 'N/A'
        elif col == DisplayColumn.Hps.value:
            return lambda actor_id: f'{self.monitor.actor_hps(actor_id, False, not self.separate_owner):.0f}' if self.monitor else 'N/A'
        elif col == DisplayColumn.Dtps.value:
            return lambda actor_id: f'{self.monitor.actor_dtps(actor_id, False):.0f}' if self.monitor else 'N/A'
        elif col == DisplayColumn.Htps.value:
            return lambda actor_id: f'{self.monitor.actor_htps(actor_id, False):.0f}' if self.monitor else 'N/A'
        elif col == DisplayColumn.CriticalRate.value:
            return lambda actor_id: f'{self.monitor.actor_critical_rate(actor_id, False, not self.separate_owner):.0%}' if self.monitor else 'N/A'
        elif col == DisplayColumn.DirectRate.value:
            return lambda actor_id: f'{self.monitor.actor_direct_rate(actor_id, False, not self.separate_owner):.0%}' if self.monitor else 'N/A'
        elif col == DisplayColumn.DpsInWindow.value:
            return lambda actor_id: f'{self.monitor.actor_dps(actor_id, True, not self.separate_owner):.0f}' if self.monitor else 'N/A'
        elif col == DisplayColumn.HpsInWindow.value:
            return lambda actor_id: f'{self.monitor.actor_hps(actor_id, True, not self.separate_owner):.0f}' if self.monitor else 'N/A'
        elif col == DisplayColumn.DtpsInWindow.value:
            return lambda actor_id: f'{self.monitor.actor_dtps(actor_id, True):.0f}' if self.monitor else 'N/A'
        elif col == DisplayColumn.HtpsInWindow.value:
            return lambda actor_id: f'{self.monitor.actor_htps(actor_id, True):.0f}' if self.monitor else 'N/A'
        elif col == DisplayColumn.CriticalRateInWindow.value:
            return lambda actor_id: f'{self.monitor.actor_critical_rate(actor_id, True, not self.separate_owner):.0%}' if self.monitor else 'N/A'
        elif col == DisplayColumn.DirectRateInWindow.value:
            return lambda actor_id: f'{self.monitor.actor_direct_rate(actor_id, True, not self.separate_owner):.0%}' if self.monitor else 'N/A'
        elif col == DisplayColumn.DeathCount.value:
            return lambda actor_id: f'{self.monitor.death_count(actor_id)}' if self.monitor else 'N/A'
        else:
            return lambda actor_id: f'Unk Col {col}'

    def update_cols_getter(self):
        self._cols_getter = [self.get_cols_getter(col) for col in self.cols]

    def get_evnet_monitor(self, refresh=False):
        self._update_member_ids()
        if not self.monitor or self.__must_cut:
            if not refresh: return None
            self.__must_cut = False
            self._cached_owner.clear()
            self._cached_name.clear()
            self.monitor = Monitor(self.main.mem.territory_info.territory_id)
            return self.monitor
        monitor = self.monitor
        if (tid := self.main.mem.territory_info.territory_id) != monitor.territory_id:
            if not refresh: return None
            self._cached_owner.clear()
            self._cached_name.clear()
            self.monitor = monitor = Monitor(tid)
        if monitor.events and time.time() - monitor.last_event_at > self.cutoff:
            if not refresh: return None
            self._cached_owner.clear()
            self._cached_name.clear()
            self.monitor = monitor = Monitor(tid)
        return monitor

    def wrap_owner(self, actor_id):
        if actor_id in self._cached_owner:
            return self._cached_owner[actor_id]
        if not is_valid_id(actor_id): return actor_id, 0
        actor = self.main.mem.actor_table.get_actor_by_id(actor_id)
        owner_id = getattr(actor, 'owner_id', 0)
        if owner_id == actor_id or not is_valid_id(owner_id): return actor_id, 0
        while owner := self.main.mem.actor_table.get_actor_by_id(owner_id):
            if is_valid_id(owner.owner_id):
                owner_id = owner.owner_id
            else:
                break
        _actor_id = actor.base_id << 32 | owner_id
        if _actor_id not in self._cached_name:
            self._cached_name[_actor_id] = self.actor_name(actor_id)
        self._cached_owner[actor_id] = _actor_id, owner_id
        return _actor_id, owner_id

    def on_effect(self, evt: NetworkMessage[zone_server.ActionEffect]):
        source_id, owner_id = self.wrap_owner(evt.header.source_id)
        effect: 'zone_server._ActionEffect'
        for target_id, effects in zip(evt.message.target_ids, evt.message.effects):
            if target_id == 0 or target_id == 0xe0000000: break
            for effect in effects:
                if not effect.type: break
                if effect.type == EffectType.damage_hp or effect.type == EffectType.block_damage_hp or effect.type == EffectType.parry_damage_hp:
                    if effect.arg1 & 0xf == 8: continue  # limit break damage is not calculated
                    value = effect.value
                    if effect.flag & (1 << 6):
                        value += effect.arg3 * 65536
                    self.get_evnet_monitor(True).on_damage(
                        time_stamp=time.time(),
                        source=source_id,
                        target=target_id,
                        value=value,
                        is_status=False,
                        is_critical=bool(effect.arg0 & (1 << 5)),
                        is_direct=bool(effect.arg0 & (1 << 6)),
                        owner_id=owner_id,
                    )
                elif effect.type == EffectType.heal_hp:
                    value = effect.value
                    if effect.flag & (1 << 6):
                        value += effect.arg3 * 65536
                    if monitor := self.get_evnet_monitor():
                        monitor.on_heal(
                            time_stamp=time.time(),
                            source=source_id,
                            target=target_id,
                            value=value,
                            is_status=False,
                            is_critical=bool(effect.arg1 & (1 << 5)),
                            owner_id=owner_id,
                        )

    def on_actor_control_death(self, evt: ActorControlMessage[actor_control.Death]):
        self.get_evnet_monitor().on_death(evt.source_id)

    def on_actor_control_status_effect(self, evt: ActorControlMessage[actor_control.StatusEffect]):
        source_id, owner_id = self.wrap_owner(evt.param.source_id)
        if evt.param.effect_type == EffectType.damage_hp:
            self.get_evnet_monitor(True).on_damage(
                time_stamp=time.time(),
                source=source_id,
                target=evt.source_id,
                value=evt.param.value,
                is_status=True,
                owner_id=owner_id,
            )
        elif evt.param.effect_type == EffectType.heal_hp:
            if monitor := self.get_evnet_monitor():
                monitor.on_heal(
                    time_stamp=time.time(),
                    source=source_id,
                    target=evt.source_id,
                    value=evt.param.value,
                    is_status=True,
                    owner_id=owner_id,
                )

    def on_reset(self, _):
        self.__must_cut = True

    def actor_name(self, actor_id, with_job=True, with_server=True):
        if actor_id in self._cached_name: return self._cached_name[actor_id]
        actor = self.main.mem.actor_table.get_actor_by_id(actor_id)
        if not actor: return f'Unknown Actor {actor_id:x}'
        if is_valid_id(actor.owner_id):
            owner = self.main.mem.actor_table.get_actor_by_id(actor.owner_id)
            if owner:
                return self.actor_name(owner.id, with_job=with_job, with_server=with_server) + f'({actor.name})'
        name = actor.name
        if with_job:
            name = f'[{self._class_job_sheet[actor.class_job].text_abbreviation}]{name}'
        if with_server:
            name = f'{name}@{self._world_sheet[actor.home_world].display_name}'
        self._cached_name[actor_id] = name
        return name

    def _update_member_ids(self):
        if (p_list := self.main.mem.party.party_list).party_size:
            self._member_ids = [member.id for member in p_list]
        elif me := self.main.mem.actor_table.me:
            self._member_ids = [me.id]
        else:
            self._member_ids = []

    def draw_table(self):
        changed, self.separate_owner = imgui.checkbox('Separate Owner', self.separate_owner)
        if changed:
            self.data['separate_owner'] = self.separate_owner
            self.storage.save()

        member_ids = self._member_ids.copy()
        if self.separate_owner:
            for actor_id in self._member_ids:
                # imgui.text(f'{actor_id=:x} = ' + ','.join(f'{i:x}' for i in self.monitor.pet_cache.get(actor_id, [])))
                member_ids.extend(self.monitor.pet_cache.get(actor_id, []))
        imgui.columns(len(self.cols))
        for col in self.cols:
            if col != DisplayColumn.ActorName.value:
                imgui.set_column_width(-1, 100)
            else:
                imgui.set_column_width(-1, 500)
            imgui.text(ColumnName[col])
            imgui.next_column()
        imgui.separator()
        for actor_id in sorted(member_ids, key=self._sort_by_key, reverse=True):
            for getter in self._cols_getter:
                imgui.text(getter(actor_id))
                imgui.next_column()
        imgui.columns(1)

    def draw_panel(self):
        changed, new_val = imgui.checkbox('sub_window', self.window is not None)
        if changed:
            if new_val:
                self.window = DpsWindow(self)
                self.main.gui.window_manager.new_window(
                    'dps window',
                    self.window.draw,
                    before_window_draw=self.window.before_draw_window,
                    after_window_draw=self.window.after_draw_window,
                    on_want_close=self.window.on_want_close,
                )
            else:
                try:
                    self.window.window.close()
                except:
                    pass
        if self.window is None:
            self.draw_table()
