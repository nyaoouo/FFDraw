from typing import Generic, TypeVar, TYPE_CHECKING, Callable, Tuple, Type, Iterable

from nylib.utils import Counter
from ..utils import Language, icon_path

if TYPE_CHECKING:
    from .sheet import Sheet
    from .row import DataRow
    from ..pack import PackManager

_T = TypeVar("_T")
counter = Counter()


class RowData(Generic[_T]):
    def __init__(self, col_id: int):
        self.col_id = col_id
        self.offset = 0

    def __get__(self, instance: 'DataRow | None', owner) -> '_T|RowData':
        if instance is None: return self
        return instance[self.col_id]


class RowForeign(Generic[_T]):
    def __init__(self, col_id: int, sheet: str):
        self.col_id = col_id
        self.sheet = sheet
        self.cache_key = f'__cached_{counter.get()}'

    def __get__(self, instance: 'DataRow | None', owner) -> '_T | None | RowForeign':
        if instance is None: return self
        if not hasattr(instance, self.cache_key):
            sheet = instance.row_base.sheet.mgr.get_sheet_raw(self.sheet)
            key = instance[self.col_id]
            try:
                lang = instance.row_base.lang_sheet.lang
                item = sheet.get_row(key, lang if lang.value else None)
            except KeyError:
                item = key
            setattr(instance, self.cache_key, item)
        return getattr(instance, self.cache_key, None)


class Icon:
    def __init__(self, icon_id: int, pack_mgr: 'PackManager', language: 'Language|None'):
        self.icon_id = icon_id
        self.language = language.name if isinstance(language, Language) else None
        self.pack_mgr = pack_mgr

    def __repr__(self):
        return f'Icon({self.icon_id}/{self.language})'

    def get_image(self, is_hq=False):
        if not self.icon_id: return None
        try:
            file = self.pack_mgr.get_texture_file(icon_path(self.icon_id, is_hq, self.language))
        except FileNotFoundError:
            if self.language is not None:
                file = self.pack_mgr.get_texture_file(icon_path(self.icon_id, is_hq))
            else:
                raise
        return file.get_image()


class IconRow:
    def __init__(self, col_id: int):
        self.col_id = col_id

    def __get__(self, instance: 'DataRow | None', owner) -> 'Icon | IconRow|None':
        if instance is None: return self
        assert isinstance(icon_id := instance[self.col_id], int), 'icon row should be integer'
        lang = instance.row_base.lang_sheet.lang
        return Icon(icon_id, instance.row_base.sheet.mgr.pack, lang if lang.value else None)


class DynamicForeign(Generic[_T]):
    def __init__(self, col_id: int, sheet_determiner: 'Callable[[DataRow,int],Sheet|str]'):
        self.col_id = col_id
        self.func = sheet_determiner
        self.cache_key = f'__cached_{counter.get()}'

    def __get__(self, instance: 'DataRow | None', owner) -> '_T | None | RowForeign':
        if instance is None: return self
        if not hasattr(instance, self.cache_key):
            key = instance[self.col_id]
            sheet = self.func(instance, key)
            if sheet is None:
                item = key
            else:
                if isinstance(sheet, str):
                    sheet = instance.row_base.sheet.mgr.get_sheet_raw(sheet)
                try:
                    lang = instance.row_base.lang_sheet.lang
                    item = sheet.get_row(key, lang if lang.value else None)
                except KeyError:
                    item = key
            setattr(instance, self.cache_key, item)
        return getattr(instance, self.cache_key, None)


class ListData(Generic[_T]):
    def __init__(self, cols: Iterable, _t, *args):
        self.cols = [_t(col, *args) for col in cols]
        self.cache_key = f'__cached_{counter.get()}'

    def __get__(self, instance: 'DataRow | None', owner) -> 'List[_T] | ListData':
        if instance is None: return self
        if not hasattr(instance, self.cache_key):
            setattr(instance, self.cache_key, tuple(col.__get__(instance, owner) for col in self.cols))
        return getattr(instance, self.cache_key, None)


class ComplexSheetMask:
    def __init__(self, mask: int, *sheets: str):
        self.sheets = sheets
        self.mask = mask
        self.func = {}

    def make_func(self, row: 'DataRow', lang: 'Language' = None):
        hex_mask = hex(self.mask)
        index = {}
        for sheet_name in self.sheets:
            k = '__complex_sheet_mask_' + hex_mask
            sheet = row.row_base.sheet.mgr.get_sheet_raw(sheet_name)
            if not hasattr(sheet, k):
                mask_value = {row.key & self.mask for row in sheet.iter_rows(user_lang=lang)}
                setattr(sheet, k, mask_value)
            else:
                mask_value = getattr(sheet, k)
            for _v in mask_value:
                assert _v not in index, KeyError(f'{sheet_name} and {index[mask_value].name} has same mask value {mask_value:X}')
                index[_v] = sheet
        self.func[lang] = func = lambda key: index.get(key & self.mask)
        return func

    def __call__(self, row: 'DataRow', key: int):
        lang = row.row_base.lang_sheet.lang
        if not lang.value: lang = None
        return (self.func.get(lang) or self.make_func(row, lang))(key)


class ComplexSheetKey:
    def __init__(self, key: int | str, *cond: Tuple[int, str]):
        self.key = key
        self.cond = cond
        self.func = None

    def make_func(self, row: 'DataRow'):
        value_sheet_map = {v: row.row_base.sheet.mgr.get_sheet_raw(_s) for v, _s in self.cond}
        if isinstance(self.key, int):
            self.func = lambda _row: value_sheet_map.get(_row[self.key])
        else:
            self.func = lambda _row: value_sheet_map.get(getattr(row, self.key))
        return self.func

    def __call__(self, row: 'DataRow', key: int):
        return (self.func or self.make_func(row))(row)
