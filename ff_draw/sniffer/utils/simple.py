import enum
import math
import pathlib
import typing
from csv import DictReader


def load_pno_map(path: pathlib.Path, game_version, t: typing.Type[enum.Enum]) -> tuple[dict[int, enum.Enum], dict[str, list[int]]]:
    data = {}
    k2pno = {}
    if path.exists():
        with open(path, 'r', encoding='utf-8') as f:
            for row in DictReader(f):
                if not row['key'].startswith('_') and (sv := row.get(game_version)):
                    try:
                        e = t[row['key']]
                    except KeyError:
                        continue
                    if isinstance((pnos := eval(sv)), int):
                        pnos = pnos,
                    for pno in pnos:
                        data[pno] = e
                        k2pno.setdefault(row['key'], []).append(pno)
    return data, k2pno


c = 200000 / 65535 * 0.01
c_r = math.pi / 0xffff * 2


def pos_web_to_raw(pos):
    return pos * c - 1000


def pos_raw_to_web(pos):
    return int((pos + 1000) // c)


def dir_web_to_raw(dir_):
    return dir_ * c_r - math.pi


def dir_raw_to_web(dir_):
    return int((dir_ + math.pi) // c_r)
