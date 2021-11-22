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
from typing import Union
from narwhallet.core.kcl.bip_utils.addr.utils import AddrUtils
from narwhallet.core.kcl.bip_utils.conf import Bip44Filecoin
from narwhallet.core.kcl.bip_utils.ecc import Secp256k1PublicKey
from narwhallet.core.kcl.bip_utils.utils import Base32, ConvUtils, CryptoUtils


class FilAddrConst:
    """ Class container for Filecoin address constants. """

    # Alphabet for base32
    BASE32_ALPHABET: str = "abcdefghijklmnopqrstuvwxyz234567"
    # Digest length in bytes
    DIGEST_BYTE_LEN: int = 20
    # Checksum length in bytes
    CHECKSUM_BYTE_LEN: int = 4


class FilAddr:
    """ Filecoin address class. It allows the Filecoin address generation. """

    @staticmethod
    def EncodeKey(pub_key: Union[bytes, Secp256k1PublicKey]) -> str:
        """ Get address in Filecoin format.

        Args:
            pub_key (bytes or Secp256k1PublicKey): Public key bytes or object

        Returns:
            str: Address string

        Raised:
            ValueError: If the public key is not valid
            TypeError: If the public key is not secp256k1
        """
        pub_key_obj = AddrUtils.ValidateAndGetSecp256k1Key(pub_key)
        pub_key_bytes = pub_key_obj.RawUncompressed().ToBytes()

        # Get address type
        addr_type_str = Bip44Filecoin.AddrConfKey("type")
        addr_type_byte = ConvUtils.IntegerToBytes(ord(addr_type_str) - ord("0"))

        # Compute public key hash and checksum
        pub_key_hash = CryptoUtils.Blake2b(pub_key_bytes,
                                           digest_size=FilAddrConst.DIGEST_BYTE_LEN)
        chksum = CryptoUtils.Blake2b(addr_type_byte + pub_key_hash,
                                     digest_size=FilAddrConst.CHECKSUM_BYTE_LEN)
        # Encode to base32
        b32_enc = Base32.EncodeNoPadding(pub_key_hash + chksum, FilAddrConst.BASE32_ALPHABET)

        return Bip44Filecoin.AddrConfKey("prefix") + addr_type_str + b32_enc
