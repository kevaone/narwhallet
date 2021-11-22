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
from narwhallet.core.kcl.bip_utils.ecc.ed25519 import Ed25519Const
from narwhallet.core.kcl.bip_utils.ecc.ed25519_keys import Ed25519Point
from narwhallet.core.kcl.bip_utils.ecc.ed25519_blake2b_keys import Ed25519Blake2bPublicKey, Ed25519Blake2bPrivateKey


class Ed25519Blake2bConst:
    """ Class container for Ed25519-Blake2b constants. """

    # Curve name
    NAME: str = "Ed25519-Blake2b"
    # Curve order
    CURVE_ORDER: int = Ed25519Const.CURVE_ORDER
    # Curve generator point
    GENERATOR: Ed25519Point = Ed25519Const.GENERATOR


# Ed25519-Blake2b curve definition
Ed25519Blake2b: EllipticCurve = EllipticCurve(Ed25519Blake2bConst.NAME,
                                              Ed25519Blake2bConst.CURVE_ORDER,
                                              Ed25519Blake2bConst.GENERATOR,
                                              Ed25519Point,
                                              Ed25519Blake2bPublicKey,
                                              Ed25519Blake2bPrivateKey)
