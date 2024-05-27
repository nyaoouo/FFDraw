import re

import imgui
from ff_draw.mem import XivMem
from ff_draw.mem.scanners import CachedStaticPatternSearcherV2 as CachedStaticPatternSearcher
from fpt4.utils.sqpack import SqPack

sq_pack = SqPack.get()
def imgui_display_data(name, val):
    s = str(val)
    imgui.input_text(name, s, len(s.encode('utf-8')) + 1, imgui.INPUT_TEXT_READ_ONLY)


def make_shell(base_shell):
    scanner = XivMem.instance.scanner

    def repl(m: re.Match):
        try:
            match m.group(2):
                case 'sp':
                    val, = scanner.find_point(m.group(3))
                case 'sp_nu':
                    val, = scanner.find_points(m.group(3))[0]
                case 'sa':
                    val = scanner.find_address(m.group(3))
                case 'sa_nu':
                    val = scanner.find_addresses(m.group(3))[0]
                case _:
                    raise ValueError(f'unknown shell pattern {m.group(2)}')
        except Exception:
            raise ValueError(f'unknown shell pattern {m.group(2)} {m.group(3)}')
        return f'{m.group(1)}{val:#x}'

    return re.sub(r'(\W)(sp(?:_nu)?|sa(?:_nu)?)\("(.*)"\)', repl, base_shell)


U8_MAX = 1 << 8 - 1
U16_MAX = 1 << 16 - 1
U32_MAX = 1 << 32 - 1
U64_MAX = 1 << 64 - 1
I8_MAX = 1 << 7 - 1
I16_MAX = 1 << 15 - 1
I32_MAX = 1 << 31 - 1
I64_MAX = 1 << 63 - 1


