from enum import Enum


class SIGHASH_TYPE(Enum):
    ALL = 1  # b'\x01\x00\x00\x00' #0x01
    NONE = 2  # b'\x02\x00\x00\x00' #0x02
    SINGLE = 3  # b'\x03\x00\x00\x00' #0x03
    ALL_ANYONECANPAY = 129  # b'\x81\x00\x00\x00' #0x81
    NONE_ANYONECANPAY = 130  # b'\x82\x00\x00\x00' #0x82
    SINGLE_ANYONECANPAY = 131  # b'\x83\x00\x00\x00' #0x83
