from ctypes import Structure
from nylib.struct import fctypes, set_fields_from_annotations


@set_fields_from_annotations
class VersionInfo(Structure):
    _size_ = 0X400

    magic_str: 'fctypes.c_char*8' = eval('0X0')
    platform_id: 'fctypes.c_uint8' = eval('0X8')
    size: 'fctypes.c_uint32' = eval('0XC')
    version: 'fctypes.c_uint32' = eval('0X10')
    type: 'fctypes.c_uint32' = eval('0X14')
    date: 'fctypes.c_uint32' = eval('0X18')
    time: 'fctypes.c_uint32' = eval('0X1C')
    region_id: 'fctypes.c_uint32' = eval('0X20')
    language_id: 'fctypes.c_uint32' = eval('0X24')
    self_hash: 'fctypes.c_uint8*64' = eval('0X3C0')


@set_fields_from_annotations
class IndexFileInfo(Structure):
    _size_ = 0X400
    size: 'fctypes.c_uint32' = eval('0X0')
    version: 'fctypes.c_uint32' = eval('0X4')
    index_data_offset: 'fctypes.c_uint32' = eval('0X8')
    index_data_size: 'fctypes.c_uint32' = eval('0XC')
    index_data_hash: 'fctypes.c_uint8*64' = eval('0X10')
    number_of_data_file: 'fctypes.c_uint32' = eval('0X50')
    synonym_data_offset: 'fctypes.c_uint32' = eval('0X54')
    synonym_data_size: 'fctypes.c_uint32' = eval('0X58')
    synonym_data_hash: 'fctypes.c_uint8*64' = eval('0X5C')
    empty_block_data_offset: 'fctypes.c_uint32' = eval('0X9C')
    empty_block_data_size: 'fctypes.c_uint32' = eval('0XA0')
    empty_block_data_hash: 'fctypes.c_uint8*64' = eval('0XA4')
    dir_index_data_offset: 'fctypes.c_uint32' = eval('0XE4')
    dir_index_data_size: 'fctypes.c_uint32' = eval('0XE8')
    dir_index_data_hash: 'fctypes.c_uint8*64' = eval('0XEC')
    index_type: 'fctypes.c_uint32' = eval('0X12C')
    self_hash: 'fctypes.c_uint8*64' = eval('0X3C0')


@set_fields_from_annotations
class DirectoryIndexInfo(Structure):
    _size_ = 0X10
    dir_hash: 'fctypes.c_uint32' = eval('0X0')
    offset: 'fctypes.c_uint32' = eval('0X4')
    size: 'fctypes.c_uint32' = eval('0X8')


@set_fields_from_annotations
class SynonymTableElem_Hash32(Structure):
    _size_ = 0X100

    hash_hoge32: 'fctypes.c_uint32' = eval('0X0')
    reserve: 'fctypes.c_uint32' = eval('0X4')
    reserved: 'fctypes.c_uint32|1' = eval('0X8, 0')
    data_file_id: 'fctypes.c_uint32|3' = eval('0X8, 1')
    block_offset: 'fctypes.c_uint32|28' = eval('0X8, 4')
    synonym_index: 'fctypes.c_uint32' = eval('0XC')
    path: 'fctypes.c_char*240' = eval('0X10')


@set_fields_from_annotations
class SynonymTableElem_Hash64(Structure):
    _size_ = 0X100

    hash_hoge64: 'fctypes.c_uint64' = eval('0X0')
    reserved: 'fctypes.c_uint32|1' = eval('0X8, 0')
    data_file_id: 'fctypes.c_uint32|3' = eval('0X8, 1')
    block_offset: 'fctypes.c_uint32|28' = eval('0X8, 4')
    synonym_index: 'fctypes.c_uint32' = eval('0XC')
    path: 'fctypes.c_char*240' = eval('0X10')


@set_fields_from_annotations
class HashTableElem_Hash32(Structure):
    _size_ = 0X8

    hash_hoge32: 'fctypes.c_uint32' = eval('0X0')
    is_synonym: 'fctypes.c_uint32|1' = eval('0X4, 0')
    data_file_id: 'fctypes.c_uint32|3' = eval('0X4, 1')
    block_offset: 'fctypes.c_uint32|28' = eval('0X4, 4')


@set_fields_from_annotations
class HashTableElem_Hash64(Structure):
    _size_ = 0X10

    hash_hoge64: 'fctypes.c_uint64' = eval('0X0')
    is_synonym: 'fctypes.c_uint32|1' = eval('0X8, 0')
    data_file_id: 'fctypes.c_uint32|3' = eval('0X8, 1')
    block_offset: 'fctypes.c_uint32|28' = eval('0X8, 4')
