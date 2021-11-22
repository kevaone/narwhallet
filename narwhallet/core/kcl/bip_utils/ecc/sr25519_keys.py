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
import sr25519
from typing import Any
from narwhallet.core.kcl.bip_utils.ecc.dummy_point import DummyPoint
from narwhallet.core.kcl.bip_utils.ecc.elliptic_curve_types import EllipticCurveTypes
from narwhallet.core.kcl.bip_utils.ecc.ikeys import IPoint, IPublicKey, IPrivateKey
from narwhallet.core.kcl.bip_utils.utils import DataBytes


class Sr25519KeysConst:
    """ Class container for ed25519 keys constants. """

    # Compressed public key length in bytes
    PUB_KEY_COMPRESSED_BYTE_LEN: int = 32
    # Uncompressed public key length in bytes
    PUB_KEY_UNCOMPRESSED_BYTE_LEN: int = 32
    # Private key length in bytes
    PRIV_KEY_BYTE_LEN: int = 64


class Sr25519Point(DummyPoint):
    """ Sr25519 point class. Dummy class since not needed. """
    pass


class Sr25519PublicKey(IPublicKey):
    """ Sr25519 public key class. """

    @classmethod
    def FromBytes(cls,
                  key_bytes: bytes) -> IPublicKey:
        """ Construct class from key bytes.

        Args:
            key_bytes (bytes): Key bytes

        Returns:
            IPublicKey: IPublicKey object

        Raises:
            ValueError: If key bytes are not valid
        """

        # Check here because the library does not raise any exception
        if len(key_bytes) != cls.CompressedLength():
            raise ValueError("Invalid public key bytes")

        return cls(key_bytes)

    @classmethod
    def FromPoint(cls,
                  key_point: IPoint) -> IPublicKey:
        """ Construct class from key point.

        Args:
            key_point (IPoint object): Key point

        Returns:
            IPublicKey: IPublicKey object

        Raises:
            ValueError: If key point is not valid
        """

        # Not needed
        pass

    def __init__(self,
                 key_obj: Any) -> None:
        """ Construct class from key object.

        Args:
            key_obj (class): Key object

        Raises:
            TypeError: If key object is not of the correct type
        """
        if isinstance(key_obj, bytes):
            self.m_ver_key = key_obj
        else:
            raise TypeError("Invalid public key object type")

    @staticmethod
    def CurveType() -> EllipticCurveTypes:
        """ Get the elliptic curve type.

        Returns:
           EllipticCurveTypes: Elliptic curve type
        """
        return EllipticCurveTypes.SR25519

    @staticmethod
    def CompressedLength() -> int:
        """ Get the compressed key length.

        Returns:
           int: Compressed key length
        """
        return Sr25519KeysConst.PUB_KEY_COMPRESSED_BYTE_LEN

    @staticmethod
    def UncompressedLength() -> int:
        """ Get the uncompressed key length.

        Returns:
           int: Uncompressed key length
        """
        return Sr25519KeysConst.PUB_KEY_UNCOMPRESSED_BYTE_LEN

    def UnderlyingObject(self) -> Any:
        """ Get the underlying object.

        Returns:
           Any: Underlying object
        """
        return self.m_ver_key

    def RawCompressed(self) -> DataBytes:
        """ Return raw compressed public key.

        Returns:
            DataBytes object: DataBytes object
        """
        return DataBytes(self.m_ver_key)

    def RawUncompressed(self) -> DataBytes:
        """ Return raw uncompressed public key.

        Returns:
            DataBytes object: DataBytes object
        """

        # Same as compressed
        return self.RawCompressed()

    def Point(self) -> IPoint:
        """ Get public key point.

        Returns:
            IPoint object: IPoint object
        """

        # Not needed
        pass


class Sr25519PrivateKey(IPrivateKey):
    """ Sr25519 private key class. """

    @classmethod
    def FromBytes(cls,
                  key_bytes: bytes) -> IPrivateKey:
        """ Construct class from key bytes.

        Args:
            key_bytes (bytes): Key bytes

        Returns:
            IPrivateKey: IPrivateKey object

        Raises:
            ValueError: If key bytes are not valid
        """

        # Check here because the library does not raise any exception
        if len(key_bytes) != cls.Length():
            raise ValueError("Invalid private key bytes")

        return cls(key_bytes)

    def __init__(self,
                 key_obj: Any) -> None:
        """ Construct class from key object.

        Args:
            key_obj (class): Key object

        Raises:
            TypeError: If key object is not of the correct type
        """
        if isinstance(key_obj, bytes):
            self.m_sign_key = key_obj
        else:
            raise TypeError("Invalid private key object type")

    @staticmethod
    def CurveType() -> EllipticCurveTypes:
        """ Get the elliptic curve type.

        Returns:
           EllipticCurveTypes: Elliptic curve type
        """
        return EllipticCurveTypes.SR25519

    @staticmethod
    def Length() -> int:
        """ Get the key length.

        Returns:
           int: Key length
        """
        return Sr25519KeysConst.PRIV_KEY_BYTE_LEN

    def UnderlyingObject(self) -> Any:
        """ Get the underlying object.

        Returns:
           Any: Underlying object
        """
        return self.m_sign_key

    def Raw(self) -> DataBytes:
        """ Return raw private key.

        Returns:
            DataBytes object: DataBytes object
        """
        return DataBytes(self.m_sign_key)

    def PublicKey(self) -> IPublicKey:
        """ Get the public key correspondent to the private one.

        Returns:
            IPublicKey object: IPublicKey object
        """
        return Sr25519PublicKey(sr25519.public_from_secret_key(self.m_sign_key))
