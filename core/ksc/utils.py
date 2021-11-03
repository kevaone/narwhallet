import struct
from core.kcl.bip_utils.utils import CryptoUtils, ConvUtils


class Ut():
    @staticmethod
    def to_cuint(value: int) -> bytes:
        if value < 0xfd:
            return value.to_bytes(1, 'little')
        elif value <= 2 ** 16 - 1:
            return b'\xfd' + value.to_bytes(2, 'little')
        elif value <= 2 ** 32 - 1:
            return b'\xfe' + value.to_bytes(4, 'little')
        elif value <= 2**64 - 1:
            return b'\xff' + value.to_bytes(8, 'little')
        else:
            raise ValueError('{0} too large for u64'.format(value))

    @staticmethod
    def encode_pushdata(data: bytes) -> bytes:
        if len(data) < 0x4c:
            return b'' + bytes([len(data)]) + data # OP_PUSHDATA
        elif len(data) <= 0xff:
            return b'\x4c' + bytes([len(data)]) + data # OP_PUSHDATA1
        elif len(data) <= 0xffff:
            return b'\x4d' + struct.pack(b'<H', len(data)) + data # OP_PUSHDATA2
        elif len(data) <= 0xffffffff:
            return b'\x4e' + struct.pack(b'<I', len(data)) + data # OP_PUSHDATA4
        else:
            raise ValueError('Data too long to encode in a PUSHDATA op')

    @staticmethod
    def hex_to_bytes(data: str) -> bytes:
        return ConvUtils.HexStringToBytes(data)

    @staticmethod
    def bytes_to_hex(data: bytes) -> str:
        return ConvUtils.BytesToHexString(data)

    @staticmethod
    def reverse_bytes(data: bytes) -> bytes:
        return ConvUtils.ReverseBytes(data)

    @staticmethod
    def int_to_bytes(value: int, size: int, endianness: str) -> bytes:
        return ConvUtils.IntegerToBytes(value, size, endianness)

    @staticmethod
    def bytes_to_int(value: bytes, endianness: str) -> int:
        return ConvUtils.BytesToInteger(value, endianness)

    @staticmethod
    def hash160(data: str) -> bytes:
        return CryptoUtils.Hash160(data)

    @staticmethod
    def sha256(data: str) -> bytes:
        return CryptoUtils.Sha256(data)
