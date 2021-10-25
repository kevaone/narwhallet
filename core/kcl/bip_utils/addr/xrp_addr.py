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
from core.kcl.bip_utils.addr.P2PKH_addr import P2PKHAddr
from core.kcl.bip_utils.base58 import Base58Alphabets
from core.kcl.bip_utils.conf import Bip44Ripple
from core.kcl.bip_utils.ecc import Secp256k1PublicKey


class XrpAddr:
    """ Ripple address class. It allows the Ripple address generation. """

    @staticmethod
    def EncodeKey(pub_key: Union[bytes, Secp256k1PublicKey]) -> str:
        """ Get address in Ripple format.

        Args:
            pub_key (bytes or Secp256k1PublicKey): Public key bytes or object

        Returns:
            str: Address string

        Raises:
            ValueError: If the public key is not valid
            TypeError: If the public key is not secp256k1
        """

        # Ripple address is just a P2PKH address with a different Base58 alphabet
        return P2PKHAddr.EncodeKey(pub_key,
                                   Bip44Ripple.AddrConfKey("net_ver"),
                                   Base58Alphabets.RIPPLE)
