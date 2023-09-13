import json
import typing
from nylib import pattern_v2, pattern

if typing.TYPE_CHECKING:
    from ff_draw.mem import XivMem


class CachedStaticPatternSearcherV2(pattern_v2.StaticPatternSearcher):
    def __init__(self, mem: 'XivMem', pe, base_address):
        super().__init__(pe, base_address)
        self.mem = mem
        self._cache_file = mem.main.app_data_path / 'sig_cache_v2' / (mem.game_build_date + '.json')
        self._cache = self._load_cache()

    def _search(self, pattern: pattern_v2.Pattern) -> list[tuple[int, list[int]]]:
        key = pattern.pattern
        if not (res := self._cache.get(key)):
            res = []
            for sect_off, data in zip(self.section_virtual_addresses, self.section_datas):
                for offset, args in pattern.finditer(data):
                    res.append([sect_off + offset, [a + sect_off if r else a for a, r in zip(args, pattern.res_is_ref)]])
            if res:
                self._cache[key] = res
                self._save_cache()
        return res

    def search(self, pattern: str | pattern_v2.Pattern) -> typing.Generator[tuple[int, list[int]], None, None]:
        if isinstance(pattern, str):
            pattern = pattern_v2.compile_pattern(pattern)
        for offset, args in self._search(pattern):
            yield self.base_address + offset, [a + self.base_address if r else a for a, r in zip(args, pattern.res_is_ref)]

    def _load_cache(self):
        if not self._cache_file.exists(): return {}
        try:
            with self._cache_file.open('r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return {}

    def _save_cache(self):
        self._cache_file.parent.mkdir(parents=True, exist_ok=True)
        with self._cache_file.open('w', encoding='utf-8') as f:
            json.dump(self._cache, f, indent=4, ensure_ascii=False)


class CachedStaticPatternSearcherV1(pattern.StaticPatternSearcher):
    def __init__(self, mem: 'XivMem', pe, base_address):
        super().__init__(pe, base_address)
        self.mem = mem
        self._cache_file = mem.main.app_data_path / 'sig_cache' / (mem.game_build_date + '.json')
        self._cache = self._load_cache()

    def find_address(self, pattern):
        cache = self._cache.setdefault('address', {})
        if pattern in cache:
            return cache[pattern] + self.base_address
        address = super().find_address(pattern)
        cache[pattern] = address - self.base_address
        self._save_cache()
        return address

    def find_point(self, pattern: str):
        cache = self._cache.setdefault('point', {})
        if pattern in cache:
            return [a + self.base_address for a in cache[pattern]]
        point = super().find_point(pattern)
        cache[pattern] = [a - self.base_address for a in point]
        self._save_cache()
        return point

    def find_val(self, pattern: str):
        cache = self._cache.setdefault('val', {})
        if pattern in cache:
            return cache[pattern]
        val = super().find_val(pattern)
        cache[pattern] = val
        self._save_cache()
        return val

    def _load_cache(self):
        if not self._cache_file.exists(): return {}
        try:
            with self._cache_file.open('r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return {}

    def _save_cache(self):
        self._cache_file.parent.mkdir(parents=True, exist_ok=True)
        with self._cache_file.open('w', encoding='utf-8') as f:
            json.dump(self._cache, f, indent=4, ensure_ascii=False)
