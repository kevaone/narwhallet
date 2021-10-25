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
from core.kcl.bip_utils.addr.utils import AddrUtils
from core.kcl.bip_utils.base58 import Base58Encoder
from core.kcl.bip_utils.bech32 import BchBech32Encoder
from core.kcl.bip_utils.conf import Bip49BitcoinMainNet
from core.kcl.bip_utils.ecc import IPublicKey, Secp256k1PublicKey
from core.kcl.bip_utils.utils import CryptoUtils


class P2SHAddrConst:
    """ Class container for P2SH constants. """

    # Script bytes
    SCRIPT_BYTES: bytes = b"\x00\x14"


class P2SHAddrUtils:
    """ Class container for P2SH utility functions. """

    @staticmethod
    def AddScriptSig(pub_key: IPublicKey) -> bytes:
        """ Add script signature to public key and get address bytes.

        Args:
            pub_key (Secp256k1PublicKey object) : Public key object

        Returns:
            bytes: Address bytes
        """
        # Key hash: Hash160(public_key)
        key_hash = CryptoUtils.Hash160(pub_key.RawCompressed().ToBytes())
        # Script signature: 0x0014 | Hash160(public_key)
        script_sig = P2SHAddrConst.SCRIPT_BYTES + key_hash
        # Address bytes = Hash160(script_signature)
        return CryptoUtils.Hash160(script_sig)


class P2SHAddr:
    """ P2SH class. It allows the Pay-to-Script-Hash address generation. """

    @staticmethod
    def EncodeKey(pub_key: Union[bytes, Secp256k1PublicKey],
                  net_addr_ver: bytes = Bip49BitcoinMainNet.AddrConfKey("net_ver")) -> str:
        """ Get address in P2SH format.

        Args:
            pub_key (bytes or Secp256k1PublicKey): Public key bytes or object
            net_addr_ver (bytes, optional)       : Net address version, default is Bitcoin main network

        Returns:
            str: Address string

        Raises:
            ValueError: If the public key is not valid
            TypeError: If the public key is not secp256k1
        """
        pub_key_obj = AddrUtils.ValidateAndGetSecp256k1Key(pub_key)

        # Final address: Base58Check(addr_prefix | address_bytes)
        return Base58Encoder.CheckEncode(net_addr_ver + P2SHAddrUtils.AddScriptSig(pub_key_obj))


class BchP2SHAddr:
    """ Bitcoin Cash P2SH class. It allows the Bitcoin Cash P2SH generation. """

    @staticmethod
    def EncodeKey(pub_key: Union[bytes, Secp256k1PublicKey],
                  hrp: str,
                  net_addr_ver: bytes) -> str:
        """ Get address in Bitcoin Cash P2SH format.

        Args:
            pub_key (bytes or Secp256k1PublicKey): Public key bytes or object
            hrp (str)                            : HRP
            net_addr_ver (bytes)                 : Net address version

        Returns:
            str: Address string

        Raises:
            ValueError: If the public key is not valid
            TypeError: If the public key is not secp256k1
        """
        pub_key_obj = AddrUtils.ValidateAndGetSecp256k1Key(pub_key)

        return BchBech32Encoder.Encode(hrp, net_addr_ver, P2SHAddrUtils.AddScriptSig(pub_key_obj))
