# Copyright (c) 2021 Emanuele Bellocchia
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

# Reference: https://github.com/bitcoin/bips/blob/master/bip-0173.mediawiki

# Imports
from typing import List, Tuple
from narwhallet.core.kcl.bip_utils.bech32.bech32_base import Bech32DecoderBase, Bech32EncoderBase, Bech32BaseUtils
from narwhallet.core.kcl.bip_utils.bech32.bech32_ex import Bech32FormatError
from narwhallet.core.kcl.bip_utils.bech32.bech32 import Bech32Const, Bech32Utils
from narwhallet.core.kcl.bip_utils.utils import ConvUtils


class SegwitBech32Const:
    """ Class container for Segwit Bech32 constants. """

    # Separator
    SEPARATOR: str = Bech32Const.SEPARATOR
    # Checkum length in bytes
    CHECKSUM_BYTE_LEN: int = Bech32Const.CHECKSUM_BYTE_LEN
    # Minimum data length in bytes
    DATA_MIN_BYTE_LEN: int = Bech32Const.DATA_MIN_BYTE_LEN
    # Maximum data length in bytes
    DATA_MAX_BYTE_LEN: int = Bech32Const.DATA_MAX_BYTE_LEN
    # Witness version maximum value
    WITNESS_VER_MAX_VAL: int = 16
    # Accepted data lengths when witness version is zero
    WITNESS_VER_ZERO_DATA_BYTE_LEN: Tuple[int, int] = (20, 32)


class SegwitBech32Encoder(Bech32EncoderBase):
    """ Segwit Bech32 encoder class. It provides methods for encoding to Segwit Bech32 format. """

    @staticmethod
    def Encode(hrp: str,
               wit_ver: int,
               wit_prog: bytes) -> str:
        """ Encode to Segwit Bech32.

        Args:
            hrp (str)       : HRP
            wit_ver (int)   : Witness version
            wit_prog (bytes): Witness program

        Returns:
            str: Encoded address

        Raises:
            Bech32FormatError: If the data is not valid
        """

        return SegwitBech32Encoder._EncodeBech32(hrp,
                                                 [wit_ver] + Bech32BaseUtils.ConvertToBase32(wit_prog),
                                                 SegwitBech32Const.SEPARATOR)

    @staticmethod
    def _ComputeChecksum(hrp: str,
                         data: List[int]) -> List[int]:
        """ Compute the checksum from the specified HRP and data.

        Args:
            hrp (str)  : HRP
            data (list): Data part

        Returns:
            list: Computed checksum
        """
        return Bech32Utils.ComputeChecksum(hrp, data)


class SegwitBech32Decoder(Bech32DecoderBase):
    """ Segwit Bech32 decoder class. It provides methods for decoding Segwit Bech32 format. """

    @staticmethod
    def Decode(hrp: str,
               addr: str) -> Tuple[int, bytes]:
        """ Decode from Segwit Bech32.

        Args:
            hrp (str) : Human readable part
            addr (str): Address

        Returns:
            tuple: Witness version (index 0) and witness program (index 1)

        Raises:
            Bech32FormatError: If the bech32 string is not valid
            Bech32ChecksumError: If the checksum is not valid
        """

        # Decode string
        hrpgot, data = SegwitBech32Decoder._DecodeBech32(addr,
                                                         SegwitBech32Const.SEPARATOR,
                                                         SegwitBech32Const.CHECKSUM_BYTE_LEN)
        # Check HRP
        if hrpgot != hrp:
            raise Bech32FormatError("Invalid format (HRP not valid, expected %s, got %s)" % (hrp, hrpgot))

        # Convert back from base32
        conv_data = Bech32BaseUtils.ConvertFromBase32(data[1:])

        # Check converted data
        if (len(conv_data) < SegwitBech32Const.DATA_MIN_BYTE_LEN or
                len(conv_data) > SegwitBech32Const.DATA_MAX_BYTE_LEN):
            raise Bech32FormatError("Invalid format (length not valid)")
        elif data[0] > SegwitBech32Const.WITNESS_VER_MAX_VAL:
            raise Bech32FormatError("Invalid format (witness version not valid)")
        elif data[0] == 0 and not len(conv_data) in SegwitBech32Const.WITNESS_VER_ZERO_DATA_BYTE_LEN:
            raise Bech32FormatError("Invalid format (length not valid)")

        return data[0], ConvUtils.ListToBytes(conv_data)

    @staticmethod
    def _VerifyChecksum(hrp: str,
                        data: List[int]) -> bool:
        """ Verify the checksum from the specified HRP and converted data characters.

        Args:
            hrp  (str) : HRP
            data (list): Data part

        Returns:
            bool: True if valid, false otherwise
        """
        return Bech32Utils.VerifyChecksum(hrp, data)
