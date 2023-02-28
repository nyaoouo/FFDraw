import enum
import functools
import threading
import typing

from ff_draw.main import FFDraw

main = FFDraw.instance


class Role(enum.Enum):
    mt = 0
    st = 1
    h1 = 2
    h2 = 3
    d1 = 4
    d2 = 5
    d3 = 6
    d4 = 7


dps = [Role.d1.value, Role.d2.value, Role.d3.value, Role.d4.value]
healer = [Role.h1.value, Role.h2.value]
tank = [Role.mt.value, Role.st.value]


@functools.cache
def make(desc: str):
    res = []
    p = 0
    while p < len(desc):
        k = desc[p].lower()
        p += 1
        match k:
            case 't':
                res.extend(tank)
                continue
            case 'h':
                if p < len(desc) and 48 < (v := ord(desc[p])) < 51:
                    res.append(Role.h1.value + v - 49)
                    p += 1
                    continue
                res.extend(healer)
                continue
            case 'd':
                if p < len(desc) and 48 < (v := ord(desc[p])) < 53:
                    res.append(Role.d1.value + v - 49)
                    p += 1
                    continue
                res.extend(dps)
                continue
            case 'm' | 's':
                if p < len(desc) and desc[p].lower() == 't':
                    res.append((Role.mt if k == 'm' else Role.st).value)
                    p += 1
                    continue
        raise ValueError(f'Unknown key {k} in desc {desc} idx {p}')
    return [res.index(i) for i in range(8)]


class_job_cate_sheet = main.sq_pack.sheets.class_job_category_sheet
class_job_sheet = main.sq_pack.sheets.class_job_sheet
world_sheet = main.sq_pack.sheets.world_sheet

check_job_group = lambda cjc: (lambda job: class_job_cate_sheet[cjc][job + 1])
is_tank = check_job_group(121)
is_healer = check_job_group(125)
is_melee = check_job_group(114)
is_range = check_job_group(115)
is_caster = check_job_group(116)
default_job_order = [
    class_job_sheet[v].main_class.key for v in [
        21,  # 战士WAR
        19,  # 骑士PLD
        37,  # 绝枪战士GNB
        32,  # 暗黑骑士DRK
        24,  # 白魔法师WHM
        33,  # 占星术士AST
        28,  # 学者SCH
        40,  # SGE
        34,  # 武士SAM
        39,  # RPR
        22,  # 龙骑士DRG
        20,  # 武僧MNK
        30,  # 忍者NIN
        23,  # 吟游诗人BRD
        31,  # 机工士MCH
        38,  # 舞者DNC
        27,  # 召唤师SMN
        35,  # 赤魔法师RDM
        25,  # 黑魔法师BLM
    ]
]


def default_job_order_key(job):
    job = class_job_sheet[job].main_class.key
    try:
        return default_job_order.index(job)
    except ValueError:
        return 99


class PartyRole:
    data: list[typing.TypedDict('member', {'name': str, 'id': int, 'job': int}) | None]

    def __init__(self):
        self.lock = threading.Lock()
        self.data = [None for _ in range(8)]
        self.role_map = {}

    def update_role_map(self):
        self.role_map = {r['id']: i for i, r in enumerate(self.data) if r}

    def update(self, data: list[tuple[str, int, int, int]], reload):
        with self.lock:
            new_data: list[typing.Any] = [None for _ in range(8)]
            if len(data) >= 2:
                tanks = []
                healers = []
                melee_dps = []
                range_dps = []
                magic_dps = []
                for name, home_world, actor_id, job in data:
                    p_name = f'{name}@{world_sheet[home_world].display_name}'
                    row = {
                        'name': f'[{class_job_sheet[job].text_abbreviation}] {p_name}',
                        'p_name': p_name,
                        'id': actor_id,
                        'job': job
                    }
                    for i in range(8 if not reload else 0):
                        if not (o_r := self.data[i]): continue
                        if actor_id:
                            if o_r['id'] == actor_id:
                                new_data[i] = row
                                break
                        elif o_r['p_name'] == p_name:
                            new_data[i] = o_r
                            break
                    else:
                        if is_tank(job):
                            tanks.append(row)
                        elif is_healer(job):
                            healers.append(row)
                        elif is_melee(job):
                            melee_dps.append(row)
                        elif is_caster(job):
                            magic_dps.append(row)
                        elif is_range(job):
                            range_dps.append(row)
                tanks.sort(key=lambda r: default_job_order_key(r['job']))
                healers.sort(key=lambda r: default_job_order_key(r['job']))
                melee_dps.sort(key=lambda r: default_job_order_key(r['job']))
                range_dps.sort(key=lambda r: default_job_order_key(r['job']))
                magic_dps.sort(key=lambda r: default_job_order_key(r['job']))
                if new_data[Role.mt.value] is None and tanks: new_data[Role.mt.value] = tanks.pop(0)
                if new_data[Role.st.value] is None and tanks: new_data[Role.st.value] = tanks.pop(0)
                if new_data[Role.h1.value] is None and healers: new_data[Role.h1.value] = healers.pop(0)
                if new_data[Role.h2.value] is None and healers: new_data[Role.h2.value] = healers.pop(0)
                if new_data[Role.d1.value] is None and melee_dps: new_data[Role.d1.value] = melee_dps.pop(0)
                if new_data[Role.d3.value] is None and range_dps: new_data[Role.d3.value] = range_dps.pop(0)
                if new_data[Role.d4.value] is None and magic_dps: new_data[Role.d4.value] = magic_dps.pop(0)
                if (remain_dps := melee_dps + range_dps + magic_dps) and new_data[Role.d2.value] is None:
                    new_data[Role.d2.value] = remain_dps.pop(0)
                if remain_member := tanks + healers + remain_dps:
                    for i in range(8):
                        if new_data[i] is None:
                            new_data[i] = remain_member.pop(0)
                            if not remain_member: break
            self.data = new_data
            self.update_role_map()
