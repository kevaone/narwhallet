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
from narwhallet.core.kcl.bip_utils.bech32 import Bech32Encoder
from narwhallet.core.kcl.bip_utils.conf import Bip44Elrond
from narwhallet.core.kcl.bip_utils.ecc import Ed25519PublicKey


class EgldAddr:
    """ Elrond address class. It allows the Elrond address generation. """

    @staticmethod
    def EncodeKey(pub_key: Union[bytes, Ed25519PublicKey]) -> str:
        """ Get address in Elrond format.

        Args:
            pub_key (bytes or Ed25519PublicKey): Public key bytes or object

        Returns:
            str: Address string

        Raises:
            ValueError: If the public key is not valid
            TypeError: If the public key is not ed25519
        """
        pub_key_obj = AddrUtils.ValidateAndGetEd25519Key(pub_key)

        return Bech32Encoder.Encode(Bip44Elrond.AddrConfKey("hrp"), pub_key_obj.RawCompressed().ToBytes()[1:])
