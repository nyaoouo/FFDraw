import re
import keyword
import string



underline = re.compile(r'_*[A-Z]+')
pvp_ = re.compile(r'P[vV][pP]([A-Z])')
kwlist = list(keyword.kwlist) + ['None', 'match', 'case']
invalid_char = re.compile(r'[$!@#%^&*()"\',./;]')


def safe_name(name: str):
    if name[0] in string.digits:
        name = '_' + name
    elif name in kwlist:
        name += '_'
    return invalid_char.sub('_', name)


def underline_set(m: re.Match):
    s = m.group(0)
    if (
            len(s) == 1 or m.group(1) is not None or
            s.endswith('_') or
            m.end() == len(m.string) or
            (c := ord(m.string[m.end()])) < 65 or
            122 < c or
            90 < c < 97
    ): return '_' + s.lower()
    return '_' + s[:-1].lower() + '_' + s[-1].lower()


underline_re = re.compile(r'[A-Z]+_?($)?')


def safe_name_underline(name: str):
    s = underline_re.sub(underline_set, re.sub(r'P[vV][Pp]', 'Pvp', name)).strip('_')
    return safe_name(s)


def safe_name_hump(name: str):
    return safe_name(name)
