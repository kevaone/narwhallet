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
from narwhallet.core.kcl.bip_utils.base58 import Base58Encoder
from narwhallet.core.kcl.bip_utils.conf import Bip44Neo
from narwhallet.core.kcl.bip_utils.ecc import Nist256p1PublicKey
from narwhallet.core.kcl.bip_utils.utils import CryptoUtils


class NeoAddrConst:
    """ Class container for Neo address constants. """

    # Prefix
    PREFIX: bytes = b"\x21"
    # Suffix
    SUFFIX: bytes = b"\xac"


class NeoAddr:
    """ Neo address class. It allows the Neo address generation. """

    @staticmethod
    def EncodeKey(pub_key: Union[bytes, Nist256p1PublicKey],
                  ver: bytes = Bip44Neo.AddrConfKey("ver")) -> str:
        """ Get address in Neo format.

        Args:
            pub_key (bytes or Nist256p1PublicKey): Public key bytes or object
            ver (bytes)                          : Version

        Returns:
            str: Address string

        Raises:
            ValueError: If the public key is not valid
            TypeError: If the public key is not ed25519
        """
        pub_key_obj = AddrUtils.ValidateAndGetNist256p1Key(pub_key)

        # Get payload
        payload = NeoAddrConst.PREFIX + pub_key_obj.RawCompressed().ToBytes() + NeoAddrConst.SUFFIX
        # Encode
        return Base58Encoder.CheckEncode(ver + CryptoUtils.Hash160(payload))
