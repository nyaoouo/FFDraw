from .api import *


class Oodle:

    def decompress(self, data: bytearray, raw_len: int) -> bytearray: ...

    def compress(self, data: bytearray) -> bytearray: ...


class OodleUdp(Oodle):
    dictionary_size = 4096 * 4 * 2  # size_t
    hash_table_size = 19  # OODLENETWORK1_HASH_BITS_DEFAULT

    def __init__(self):
        self.dictionary = create_string_buffer(self.dictionary_size)
        self.shared = create_string_buffer(OodleNetwork1_Shared_Size(self.hash_table_size))
        OodleNetwork1_Shared_SetWindow(byref(self.shared), self.hash_table_size, byref(self.dictionary), self.dictionary_size)
        self.state = create_string_buffer(OodleNetwork1UDP_State_Size())
        OodleNetwork1UDP_Train(byref(self.state), byref(self.shared), 0, 0, 0)

    def decompress(self, data: bytearray, raw_len: int):
        compressed = (c_char * len(data)).from_buffer_copy(data)
        decompressed = (c_char * raw_len)()
        res = OodleNetwork1UDP_Decode(byref(self.state), byref(self.shared), byref(compressed), len(data), byref(decompressed), raw_len)
        if not res: raise Exception("Oodle decompression failed")
        return bytearray(decompressed)

    def compress(self, data: bytearray):
        compressed = (c_char * OodleNetwork1_CompressedBufferSizeNeeded(len(data)))()
        raw = (c_char * len(data)).from_buffer_copy(data)
        res = OodleNetwork1UDP_Encode(byref(self.state), byref(self.shared), byref(raw), len(data), byref(compressed))
        if not res: raise Exception("Oodle compression failed")
        return bytearray(compressed[:res])


class OodleTcp(Oodle):
    dictionary_size = 1 * 1024 * 1024
    hash_table_size = 17

    def __init__(self):
        self.dictionary = create_string_buffer(self.dictionary_size)
        self.shared = create_string_buffer(OodleNetwork1_Shared_Size(self.hash_table_size))
        OodleNetwork1_Shared_SetWindow(self.shared, self.hash_table_size, self.dictionary, self.dictionary_size)
        self.state = create_string_buffer(OodleNetwork1TCP_State_Size())
        OodleNetwork1TCP_Train(byref(self.state), byref(self.shared), 0, 0, 0)

    def decompress(self, data: bytearray, raw_len: int):
        compressed = (c_char * len(data)).from_buffer_copy(data)
        decompressed = (c_char * raw_len)()
        res = OodleNetwork1TCP_Decode(byref(self.state), byref(self.shared), byref(compressed), len(data), byref(decompressed), raw_len)
        if not res: raise Exception("Oodle decompression failed")
        return bytearray(decompressed)

    def compress(self, data: bytearray):
        compressed = (c_char * OodleNetwork1_CompressedBufferSizeNeeded(len(data)))()
        raw = (c_char * len(data)).from_buffer_copy(data)
        res = OodleNetwork1TCP_Encode(byref(self.state), byref(self.shared), byref(raw), len(data), byref(compressed))
        if not res: raise Exception("Oodle compression failed")
        return bytearray(compressed[:res])
