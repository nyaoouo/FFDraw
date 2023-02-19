import os.path
from ctypes import *

size = 64 if sizeof(c_void_p) == 8 else 32

res_path = os.path.join(os.environ['ExcPath'],'res','oo2net_9_win64.dll')
# lib_path = find_library(res_path)
clib = cdll.LoadLibrary(res_path)

# Fill a OodleNetwork1_Shared from provided data
OodleNetwork1_Shared_SetWindow = clib.OodleNetwork1_Shared_SetWindow
OodleNetwork1_Shared_SetWindow.argtypes = [
    c_void_p,  # data: OodleNetwork1_Shared object to fill
    c_int,  # htbits: size of the OodleNetwork1 hash table (log2) ; typically 18-21 such as OODLENETWORK1_HASH_BITS_DEFAULT
    c_void_p,  # window: bytes of static dictionary data to use for compression
    c_int  # window_size: size of window ; should be <= OODLENETWORK1_MAX_DICTIONARY_SIZE
]

# Returns the size of memory required for an OodleNetwork1_Shared object
OodleNetwork1_Shared_Size = clib.OodleNetwork1_Shared_Size
OodleNetwork1_Shared_Size.argtypes = [
    c_int,  # htbits: size of the OodleNetwork1 hash table (log2) ; typically 18-21 such as OODLENETWORK1_HASH_BITS_DEFAULT
]
OodleNetwork1_Shared_Size.restype = c_int

# Returns the size of memory required for an OodleNetwork1UDP_State object
OodleNetwork1UDP_State_Size = clib.OodleNetwork1UDP_State_Size
OodleNetwork1UDP_State_Size.restype = c_int

# Fill a OodleNetwork1UDP_State from training data
OodleNetwork1UDP_Train = clib.OodleNetwork1UDP_Train
OodleNetwork1UDP_Train.argtypes = [
    c_void_p,  # OodleNetwork1UDP_State * state: the OodleNetwork1UDP_State which is filled out; should not need to be initialized in any way before calling Train, it will be reset internally.
    c_void_p,  # const OodleNetwork1_Shared * shared: the OodleNetwork1_Shared data to use in compression ; this shared data should already have had OodleNetwork1_Shared_SetWindow done on it.
    c_void_p,  # const void * * training_packet_pointersonst: array of pointers to packet data; array of size num_training_packets
    c_void_p,  # const OO_S32 * training_packet_sizes: array of sizes of packets; array of size num_training_packets
    c_int,  # OO_S32 num_training_packets: number of packets to train on
]

# Decode a packet
OodleNetwork1UDP_Decode = clib.OodleNetwork1UDP_Decode
OodleNetwork1UDP_Decode.argtypes = [
    c_void_p,  # const OodleNetwork1UDP_State * state: const shared compression state
    c_void_p,  # const OodleNetwork1_Shared * shared: const shared compression state
    c_void_p,  # const void * comp: compressed packet received
    c_int,  # OO_SINTa compLen: size of compressed data
    c_void_p,  # void * raw: output decompressed packet
    c_int  # OO_SINTa rawLen: size of the packet to write
]
OodleNetwork1UDP_Decode.restype = c_bool  # false for failure

# Encode a packet
OodleNetwork1UDP_Encode = clib.OodleNetwork1UDP_Encode
OodleNetwork1UDP_Encode.argtypes = [
    c_void_p,  # const OodleNetwork1UDP_State * state: const shared compression state
    c_void_p,  # const OodleNetwork1_Shared * shared: const shared compression state
    c_void_p,  # const void * raw: packet bytes to compress
    c_int,  # OO_SINTa rawLen: size of the packet to compress ; can be >= 0
    c_void_p,  # void * comp: output compressed bytes; must be allocated to at least OodleNetwork1_CompressedBufferSizeNeeded bytes
]
OodleNetwork1UDP_Encode.restype = c_int  # length of output compressed data written to comp ; the returned compLen is strictly <= rawLen

# Returns the size of memory required for an OodleNetwork1TCP_State object
OodleNetwork1TCP_State_Size = clib.OodleNetwork1TCP_State_Size
OodleNetwork1TCP_State_Size.restype = c_int

# Fill a OodleNetwork1UDP_State from training data
OodleNetwork1TCP_Train = clib.OodleNetwork1TCP_Train
OodleNetwork1TCP_Train.argtypes = [
    c_void_p,  # OodleNetwork1TCP_State * state: the OodleNetwork1UDP_State which is filled out; should not need to be initialized in any way before calling Train, it will be reset internally.
    c_void_p,  # const OodleNetwork1_Shared * shared: the OodleNetwork1_Shared data to use in compression ; this shared data should already have had OodleNetwork1_Shared_SetWindow done on it.
    c_void_p,  # const void * * training_packet_pointersonst: array of pointers to packet data; array of size num_training_packets
    c_void_p,  # const OO_S32 * training_packet_sizes: array of sizes of packets; array of size num_training_packets
    c_int,  # OO_S32 num_training_packets: number of packets to train on
]

# Decode a packet
OodleNetwork1TCP_Decode = clib.OodleNetwork1TCP_Decode
OodleNetwork1TCP_Decode.argtypes = [
    c_void_p,  # const OodleNetwork1TCP_State * state: const shared compression state
    c_void_p,  # const OodleNetwork1_Shared * shared: const shared compression state
    c_void_p,  # const void * comp: compressed packet received
    c_int,  # OO_SINTa compLen: size of compressed data
    c_void_p,  # void * raw: output decompressed packet
    c_int  # OO_SINTa rawLen: size of the packet to write
]
OodleNetwork1TCP_Decode.restype = c_bool  # false for failure

# Encode a packet
OodleNetwork1TCP_Encode = clib.OodleNetwork1TCP_Encode
OodleNetwork1TCP_Encode.argtypes = [
    c_void_p,  # const OodleNetwork1TCP_State * state: const shared compression state
    c_void_p,  # const OodleNetwork1_Shared * shared: const shared compression state
    c_void_p,  # const void * raw: packet bytes to compress
    c_int,  # OO_SINTa rawLen: size of the packet to compress ; can be >= 0
    c_void_p,  # void * comp: output compressed bytes; must be allocated to at least OodleNetwork1_CompressedBufferSizeNeeded bytes
]
OodleNetwork1TCP_Encode.restype = c_int  # length of output compressed data written to comp ; the returned compLen is strictly <= rawLen

# Returns the size of memory required for the compressed buffer passed to OodleNetwork1TCP_Encode
OodleNetwork1_CompressedBufferSizeNeeded = clib.OodleNetwork1_CompressedBufferSizeNeeded
OodleNetwork1_CompressedBufferSizeNeeded.argtypes = [
    c_int  # OO_SINTa rawLen: size of the packet to compress
]
OodleNetwork1_CompressedBufferSizeNeeded.restype = c_int
