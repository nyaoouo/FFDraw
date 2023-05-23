import re


def wild_card(count: int):
    if not count:
        return b''
    ans = b"(?:.|\\n)"
    if count > 1:
        ans += ("{" + str(count) + "}").encode()
    return ans


def sig_to_pattern(sig: str):
    ans = bytearray()
    flag1 = False
    wild_card_counter = 0
    offset = []
    i = 0
    for i, s in enumerate(sig.strip().split(' ')):
        if not s:
            continue
        if s.startswith('*'):
            if not flag1:
                ans += wild_card(wild_card_counter)
                wild_card_counter = 0
                ans += b'('
                flag1 = True
        elif flag1:
            ans += wild_card(wild_card_counter)
            wild_card_counter = 0
            ans += b')'
            flag1 = False
            offset.append(i)
        if flag1 or s.startswith('?'):
            wild_card_counter += 1
        else:
            if wild_card_counter:
                ans += wild_card(wild_card_counter)
                wild_card_counter = 0
            temp = int(s, 16)
            if temp in special_chars_map:
                ans += b'\\'
            ans.append(temp)
    ans += wild_card(wild_card_counter)
    if flag1:
        ans += b')'
        offset.append(i + 1)
    return bytes(ans), offset


special_chars_map = {i for i in b'()[]{}?*+-|^$\\.&~# \t\n\r\v\f'}


class StaticPatternSearcher:
    def __init__(self, pe, base_address=0):
        self.pe = pe
        self.text_sections = [sect for sect in self.pe.sections if sect.Name.rstrip(b'\0') == b'.text']
        self.section_datas = [sect.get_data() for sect in self.text_sections]
        self.section_virtual_addresses = [sect.VirtualAddress for sect in self.text_sections]
        self.base_address = base_address

    def get_original_text(self, address, size):
        i = 0
        for i, a in enumerate(self.section_virtual_addresses):
            if a > address: break
        i -= 1
        section_address = address - self.base_address - self.section_virtual_addresses[i]
        return self.section_datas[i][section_address:section_address + size]

    def search_raw_pattern(self, pattern: bytes):
        res = []
        for i in range(len(self.text_sections)):
            va = self.section_virtual_addresses[i]
            res.extend(
                (
                    match.span()[0] + va + self.base_address,
                    [int.from_bytes(g, byteorder='little', signed=True) for g in match.groups()]
                ) for match in re.finditer(bytes(pattern), self.section_datas[i])
            )
        return res

    def search_from_text(self, pattern: str) -> list[tuple[int, list[int]]]:
        _pattern, offsets = sig_to_pattern(pattern)
        return [(
            address, [g + offsets[i] for i, g in enumerate(groups)]
        ) for address, groups in self.search_raw_pattern(_pattern)]

    def find_addresses(self, pattern: str):
        return [address for address, offsets in self.search_from_text(pattern)]

    def find_points(self, pattern: str):
        return [[address + offset for offset in offsets] for address, offsets in self.search_from_text(pattern)]

    def find_vals(self, pattern: str) -> list[list[int]]:
        return [v for a, v in self.search_raw_pattern(sig_to_pattern(pattern)[0])]

    def find_address(self, pattern: str):
        if len(res := self.find_addresses(pattern)) != 1:
            raise KeyError(f'pattern is not unique, {len(res)} is found, use find_addresses to deal with this error')
        return res[0]

    def find_point(self, pattern: str):
        if len(res := self.find_points(pattern)) != 1:
            raise KeyError(f'pattern is not unique, {len(res)} is found, use find_points to deal with this error')
        return res[0]

    def find_val(self, pattern: str):
        if len(res := self.find_vals(pattern)) != 1:
            raise KeyError(f'pattern is not unique, {len(res)} is found, use find_vals to deal with this error')
        return res[0]


class MemoryPatternSearcher:
    pass
