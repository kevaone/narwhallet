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
from narwhallet.core.kcl.bip_utils.ecc.elliptic_curve import EllipticCurve
from narwhallet.core.kcl.bip_utils.ecc.sr25519_keys import Sr25519Point, Sr25519PublicKey, Sr25519PrivateKey


class Sr25519Const:
    """ Class container for Sr25519 constants. """

    # Curve name
    NAME: str = "Sr25519"
    # Curve order (not needed)
    CURVE_ORDER: int = 0
    # Curve generator point (not needed)
    GENERATOR: Sr25519Point = Sr25519Point(0, 0, 0)


# Sr25519 curve definition
Sr25519: EllipticCurve = EllipticCurve(Sr25519Const.NAME,
                                       Sr25519Const.CURVE_ORDER,
                                       Sr25519Const.GENERATOR,
                                       Sr25519Point,
                                       Sr25519PublicKey,
                                       Sr25519PrivateKey)
