import base64
import struct
from typing import Optional, Union
from narwhallet.core.kcl.bip_utils.utils import CryptoUtils, ConvUtils


class Ut():
    @staticmethod
    def to_cuint(value: int) -> bytes:
        if value < 0xfd:
            _return = value.to_bytes(1, 'little')
        elif value <= 2 ** 16 - 1:
            _return = b'\xfd' + value.to_bytes(2, 'little')
        elif value <= 2 ** 32 - 1:
            _return = b'\xfe' + value.to_bytes(4, 'little')
        elif value <= 2**64 - 1:
            _return = b'\xff' + value.to_bytes(8, 'little')
        else:
            raise ValueError(f'{value} too large for u64')
        return _return

    @staticmethod
    def read_csuint(value):
        size = struct.unpack('<B', value.read(1))[0]
        if size == 253:
            _return = struct.unpack('<H', value.read(2))[0]
            _read = 2
        elif size == 254:
            _return = struct.unpack('<I', value.read(4))[0]
            _read = 4
        elif size == 255:
            _return = struct.unpack('<Q', value.read(8))[0]
            _read = 8
        else:
            _return = size
            _read = 1
        return _return, _read

    @staticmethod
    def encode_pushdata(data: bytes) -> bytes:
        if len(data) < 0x4c:
            _return = b'' + bytes([len(data)]) + data  # OP_PD
        elif len(data) <= 0xff:
            _return = b'\x4c' + bytes([len(data)]) + data  # OP_PD1
        elif len(data) <= 0xffff:
            _return = b'\x4d' + struct.pack(b'<H', len(data)) + data  # OP_PD2
        elif len(data) <= 0xffffffff:
            _return = b'\x4e' + struct.pack(b'<I', len(data)) + data  # OP_PD4
        else:
            raise ValueError('Data too long to encode in a PUSHDATA op')
        return _return

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
    def int_to_bytes(value: int, size: Optional[int], endianness: str) -> bytes:
        return ConvUtils.IntegerToBytes(value, size, endianness)

    @staticmethod
    def bytes_to_int(value: bytes, endianness: str) -> int:
        return ConvUtils.BytesToInteger(value, endianness)

    @staticmethod
    def hash160(data: Union[str, bytes]) -> bytes:
        return CryptoUtils.Hash160(data)

    @staticmethod
    def sha256(data: Union[str, bytes]) -> bytes:
        return CryptoUtils.Sha256(data)

    @staticmethod
    def to_sats(value: float) -> int:
        return int(value * 100000000)

    @staticmethod
    def from_sats(value: int) -> float:
        return float(value / 100000000)

    @staticmethod
    def base64_decode(data: str) -> bytes:
        return base64.b64decode(data)

    @staticmethod
    def base64_encode(data: bytes) -> bytes:
        return base64.b64encode(data)
