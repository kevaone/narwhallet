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


# Imports
from abc import ABC, abstractmethod
from typing import List, Tuple, Union
from core.kcl.bip_utils.bech32.bech32_ex import Bech32ChecksumError, Bech32FormatError
from core.kcl.bip_utils.utils import AlgoUtils, ConvUtils


class Bech32BaseConst:
    """ Class container for Bech32 constants. """

    # Character set
    CHARSET: str = "qpzry9x8gf2tvdw0s3jn54khce6mua7l"
    # Maximum string length in bytes
    MAX_STR_BYTE_LEN: int = 90
    # Data part minimum length in bytes
    MIN_DATA_PART_BYTE_LEN: int = 7


class Bech32BaseUtils:
    """ Class container for Bech32 utility functions. """

    @staticmethod
    def ConvertToBase32(data: Union[List[int], bytes]) -> List[int]:
        """ Convert data to base32.

        Args:
            data (list or bytes): Data to be converted
        Returns:
            list: Converted data

        Raises:
            Bech32FormatError: If the string is not valid
        """

        # Convert to base32
        conv_data = ConvUtils.ConvertToBits(data, 8, 5)
        if conv_data is None:
            raise Bech32FormatError("Invalid data, cannot perform conversion to base32")

        return conv_data

    @staticmethod
    def ConvertFromBase32(data: Union[List[int], bytes]) -> List[int]:
        """ Convert data from base32.

        Args:
            data (list or bytes): Data to be converted
        Returns:
            list: Converted data

        Raises:
            Bech32FormatError: If the string is not valid
        """

        # Convert to base32
        conv_data = ConvUtils.ConvertToBits(data, 5, 8, False)
        if conv_data is None:
            raise Bech32FormatError("Invalid data, cannot perform conversion from base32")

        return conv_data


class Bech32EncoderBase(ABC):
    """ Bech32 encoder base class. It provides methods for encoding to Bech32 format. """

    @classmethod
    def _EncodeBech32(cls,
                      hrp: str,
                      data: List[int],
                      sep: str) -> str:
        """ Encode a Bech32 string from the specified HRP and data.

        Args:
            hrp (str)  : HRP
            data (list): Data part
            sep (str)  : Bech32 separator

        Returns:
            str: Encoded data
        """

        # Add checksum to data
        data += cls._ComputeChecksum(hrp, data)
        # Encode to alphabet
        return hrp + sep + "".join([Bech32BaseConst.CHARSET[d] for d in data])

    @staticmethod
    @abstractmethod
    def _ComputeChecksum(hrp: str,
                         data: List[int]) -> List[int]:
        """ Compute the checksum from the specified HRP and data.

        Args:
            hrp (str)  : HRP
            data (list): Data part

        Returns:
            list: Computed checksum
        """
        pass


class Bech32DecoderBase(ABC):
    """ Bech32 decoder base class. It provides methods for decoding Bech32 format. """

    @classmethod
    def _DecodeBech32(cls,
                      bech_str: str,
                      sep: str,
                      checksum_len: int) -> Tuple[str, List[int]]:
        """ Decode and validate a Bech32 string, determining its HRP and data.

        Args:
            bech_str (str)    : Bech32 string
            sep (str)         : Bech32 separator
            checksum_len (int): Checksum length

        Returns:
            tuple: HRP (index 0) and data part (index 1)

        Raises:
            Bech32FormatError: If the string is not valid
            Bech32ChecksumError: If the checksum is not valid
        """

        # Check string length and case
        if len(bech_str) > Bech32BaseConst.MAX_STR_BYTE_LEN or AlgoUtils.IsStringMixed(bech_str):
            raise Bech32FormatError("Invalid bech32 format (length not valid)")

        # Lower string
        bech_str = bech_str.lower()

        # Find separator and check its position
        sep_pos = bech_str.rfind(sep)
        if sep_pos == -1:
            raise Bech32FormatError("Invalid bech32 format (no separator found)")

        # Get HRP and check it
        hrp = bech_str[:sep_pos]
        if len(hrp) == 0 or any(ord(x) < 33 or ord(x) > 126 for x in hrp):
            raise Bech32FormatError("Invalid bech32 format (HRP not valid)")

        # Get data and check it
        data_part = bech_str[sep_pos + 1:]
        if (len(data_part) < Bech32BaseConst.MIN_DATA_PART_BYTE_LEN or
                not all(x in Bech32BaseConst.CHARSET for x in data_part)):
            raise Bech32FormatError("Invalid bech32 format (data part not valid)")

        # Convert back from alphabet and verify checksum
        int_data = [Bech32BaseConst.CHARSET.find(x) for x in data_part]
        if not cls._VerifyChecksum(hrp, int_data):
            raise Bech32ChecksumError("Invalid bech32 checksum")

        return hrp, int_data[:-checksum_len]

    @staticmethod
    @abstractmethod
    def _VerifyChecksum(hrp: str,
                        data: List[int]) -> bool:
        """ Verify the checksum from the specified HRP and converted data characters.

        Args:
            hrp  (str) : HRP
            data (list): Data part

        Returns:
            bool: True if valid, false otherwise
        """
        pass
