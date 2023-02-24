from os import environ
from typing import TYPE_CHECKING, Set, Dict, Type, TypeVar
from enum import Enum
from logging import getLogger
from .row import DataRow
from .sheet import Sheet
from ..utils import Language

if not (_pure_exd := bool(environ.get('__sqpack_pure_exd__'))):
    from . import define

if TYPE_CHECKING:
    from ..pack import PackManager

_T = TypeVar("_T", bound=DataRow)


class ExdManager:
    available_sheets: Set[str] = set()
    sheet_identifiers: Dict[int, str] = dict()
    exd_pack: 'Pack | None' = None
    logger = getLogger('SqPack/ExdManager')

    def __init__(self, pack: 'PackManager', default_language: Language = Language.en, res_path = b"exd/root.exl"):
        self.default_language = default_language
        self.sheets = {}
        self.pack = pack
        self.logger.debug('init exd with language %s', self.default_language.name)
        self._build(res_path)
        self.rsv_string = {}

    def get_exd_data(self, name_or_hash: str | int):
        return self.exd_pack.get_file(name_or_hash).data_buffer

    def _build(self, res_path):
        self.exd_pack = self.pack.get_pack(res_path)
        self.exd_pack.keep_in_memory = True  # freq used data
        root_data = self.get_exd_data(res_path).decode('utf-8').splitlines(False)
        root_data.pop(0)  # EXLT,2
        available_sheets = set()
        sheet_identifiers = dict()
        for _line in root_data:
            try:
                sheet_name, _sheet_id = _line.split(',')
                sheet_id = int(_sheet_id)
            except ValueError:
                continue
            available_sheets.add(sheet_name)
            if sheet_id >= 0: sheet_identifiers[sheet_id] = sheet_name
        self.available_sheets = available_sheets
        self.sheet_identifiers = sheet_identifiers

    def get_sheet_raw(self, name_or_id: str | int, lazy=True, row_type=None) -> Sheet:
        sheet_name = name_or_id if isinstance(name_or_id, str) else self.sheet_identifiers[name_or_id]
        if sheet_name in self.sheets: return self.sheets[sheet_name]
        assert sheet_name in self.available_sheets, f'Sheet name {sheet_name} is not supported'
        if not row_type:
            try:
                if _pure_exd or not issubclass(row_type := getattr(define, sheet_name, None), DataRow):
                    row_type = DataRow
            except TypeError:
                row_type = DataRow
        self.sheets[sheet_name] = _sheet = Sheet(self, sheet_name, lazy, row_type)
        return _sheet

    def get_sheet(self, row_type: Type[_T]) -> Sheet[_T]:
        return self.get_sheet_raw(row_type.sheet_name, row_type=row_type)

    def iter_sheets(self):
        for _sheet in self.available_sheets:
            yield self.get_sheet_raw(_sheet)
