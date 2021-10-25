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
from typing import List, Optional, Union
from core.kcl.bip_utils.bip39 import Bip39Languages, IBip39SeedGenerator, Bip39MnemonicValidator, Bip39Utils
from core.kcl.bip_utils.bip39.bip39_seed_generator import Bip39SeedGeneratorConst
from core.kcl.bip_utils.utils import CryptoUtils


class SubstrateBip39SeedGenerator(IBip39SeedGenerator):
    """ Substrate BIP39 seed generator class. It implements a variant for generating seed introduced by Polkadot.
    Reference: https://github.com/paritytech/substrate-bip39
    """

    def __init__(self,
                 mnemonic: Union[str, List[str]],
                 lang: Optional[Bip39Languages] = None) -> None:
        """ Construct the class from a specified mnemonic.

        Args:
            mnemonic (str or list): Mnemonic
            lang (Bip39Languages, optional): Language, None for automatic detection

        Raises:
            ValueError: If the mnemonic is not valid
        """

        # Make sure that the given mnemonic is valid
        mnemonic_validator = Bip39MnemonicValidator(mnemonic, lang)
        mnemonic_validator.Validate()

        self.m_entropy = mnemonic_validator.GetEntropy()

    def Generate(self,
                 passphrase: str = "") -> bytes:
        """ Generate the seed using the specified passphrase.

        Args:
            passphrase (str, optional): Passphrase, empty if not specified

        Returns:
            bytes: Generated seed
        """

        # Get salt
        salt = Bip39Utils.NormalizeNfkd(Bip39SeedGeneratorConst.SEED_SALT_MOD + passphrase)
        # Compute key
        key = CryptoUtils.Pbkdf2HmacSha512(self.m_entropy,
                                           salt,
                                           Bip39SeedGeneratorConst.SEED_PBKDF2_ROUNDS)

        return key[:Bip39SeedGeneratorConst.SEED_BYTE_LEN]
