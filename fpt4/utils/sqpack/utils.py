from enum import Enum


class Language(Enum):
    none = 0
    ja = 1
    en = 2
    de = 3
    fr = 4
    chs = 5
    cht = 6
    ko = 7
    suffix = property(lambda self: "_" + self.name if self.value else '')


def icon_path(icon_id: int, is_hq: bool = False, language: Language | str = None):
    if language is None:
        language = ''
    elif isinstance(language, Language):
        language = language.name + '/'
    elif not language.endswith('/'):
        language += '/'
    return f"ui/icon/{icon_id // 1000:03d}000/{language}{icon_id:06d}" + ('_hr1.tex' if is_hq else '.tex')
