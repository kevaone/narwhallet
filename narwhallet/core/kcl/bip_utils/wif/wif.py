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
from narwhallet.core.kcl.bip_utils.base58 import Base58Decoder, Base58Encoder
from narwhallet.core.kcl.bip_utils.ecc import Secp256k1PrivateKey
from narwhallet.core.kcl.bip_utils.conf import Bip44BitcoinMainNet
from narwhallet.core.kcl.bip_utils.utils import ConvUtils


class WifConst:
    """ Class container for WIF constants. """

    # Suffix to be added if the private key correspond to a compressed public key
    COMPR_PUB_KEY_SUFFIX: bytes = b"\x01"


class WifEncoder:
    """ WIF encoder class. It provides methods for encoding to WIF format. """

    @staticmethod
    def Encode(priv_key: Union[bytes, Secp256k1PrivateKey],
               compr_pub_key: bool = True,
               net_ver: bytes = Bip44BitcoinMainNet.WifNetVersion()) -> str:
        """ Encode key bytes into a WIF string.

        Args:
            priv_key (bytes or Secp256k1PrivateKey object): Private key bytes or object
            compr_pub_key (bools, optional)               : True if private key corresponds to a compressed public key, false otherwise
            net_ver (bytes, optional)                     : Net version, default is Bitcoin main network

        Returns:
            str: WIF encoded string

        Raises:
            ValueError: If the key is not valid
        """

        # Convert to private key to check if bytes are valid
        if isinstance(priv_key, bytes):
            priv_key = Secp256k1PrivateKey.FromBytes(priv_key)
        elif not isinstance(priv_key, Secp256k1PrivateKey):
            raise TypeError("A secp256k1 private key is required")

        priv_key = priv_key.Raw().ToBytes()

        # Add suffix if correspond to a compressed public key
        if compr_pub_key:
            priv_key += WifConst.COMPR_PUB_KEY_SUFFIX

        # Add net address version
        priv_key = net_ver + priv_key

        # Encode key
        return Base58Encoder.CheckEncode(priv_key)


class WifDecoder:
    """ WIF encoder class. It provides methods for encoding to WIF format."""

    @staticmethod
    def Decode(wif_str: str,
               net_ver: bytes = Bip44BitcoinMainNet.WifNetVersion()) -> bytes:
        """ Decode key bytes from a WIF string.

        Args:
            wif_str (str)            : WIF string
            net_ver (bytes, optional): Net version, default is Bitcoin main network

        Returns:
            bytes: Key bytes

        Raises:
            Base58ChecksumError: If the base58 checksum is not valid
            ValueError: If the resulting key is not valid
        """

        # Decode string
        key_bytes = Base58Decoder.CheckDecode(wif_str)

        # Check net version
        if key_bytes[0] != ord(net_ver):
            raise ValueError("Invalid net version (expected %x, got %x)" % (ord(net_ver), key_bytes[0]))

        # Remove net version
        key_bytes = key_bytes[1:]

        # Remove suffix if correspond to a compressed public key
        if Secp256k1PrivateKey.IsValidBytes(key_bytes[:-1]):
            # Check the compressed public key suffix
            if key_bytes[-1] != ord(WifConst.COMPR_PUB_KEY_SUFFIX):
                raise ValueError("Invalid compressed public key suffix (expected %x, got %x)" %
                                 (ord(WifConst.COMPR_PUB_KEY_SUFFIX), key_bytes[-1]))
            # Remove it
            key_bytes = key_bytes[:-1]
        elif not Secp256k1PrivateKey.IsValidBytes(key_bytes):
            raise ValueError("Invalid decoded key (%s)" % ConvUtils.BytesToHexString(key_bytes))

        return key_bytes
