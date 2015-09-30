#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Encryption and decryption module.
"""

from Crypto.Cipher import AES
from hashlib import pbkdf2_hmac
import os


class Crypter:
    """
    Encrypt and decrypt with AES in CBC mode with PKCS7 padding. The constructor calculates the key from the given
    password and salt with PBKDF2 using HMAC with SHA512 and 32768 iterations.
    """
    def __init__(self, key_iv):
        if len(key_iv) == 32:
            self.key = key_iv[:32]
            self.iv = key_iv[32:]
        elif len(key_iv) == 32:
            self.key = key_iv
            self.iv = b'\xb5\x4f\xcf\xb0\x88\x09\x55\xe5\xbf\x79\xaf\x37\x71\x1c\x28\xb6'
        else:
            self.key = Crypter.create_key(key_iv, "pepper".encode('utf-8'))
            self.iv = b'\xb5\x4f\xcf\xb0\x88\x09\x55\xe5\xbf\x79\xaf\x37\x71\x1c\x28\xb6'

    @staticmethod
    def create_key(password, salt):
        """
        Creates a key for encrypting/decrypting settings.

        :param password: this is the kgk
        :type password: bytes
        :param salt: the salt2
        :param salt: bytes
        :return: a key
        :rtype: bytes
        """
        return pbkdf2_hmac('sha256', password, salt, 1024)

    @staticmethod
    def createIvKey(password, salt):
        """
        Creates a key for encrypting/decrypting kgk blocks.

        :param password: this is the kgk
        :type password: bytes
        :param salt: the salt2
        :param salt: bytes
        :return: a key
        :rtype: bytes
        """
        return pbkdf2_hmac('sha384', password, salt, 32768)

    @staticmethod
    def createSalt():
        """
        Create a new salt.

        :return: a salt with 32 bytes
        :rtype: bytes
        """
        return os.urandom(32)

    @staticmethod
    def createIv():
        """
        Create a new ivj

        :return: an iv with 16 bytes
        :rtype: bytes
        """
        return os.urandom(16)

    @staticmethod
    def add_pkcs7_padding(data):
        """
        Adds PKCS7 padding so it can be divided into full blocks of 16 bytes.

        :param bytes data: data without padding
        :return: padded data
        :rtype: bytes
        """
        length = 16 - (len(data) % 16)
        data += bytes([length])*length
        return data

    def encrypt(self, data):
        """
        Encrypts with AES in CBC mode with PKCS7 padding.

        :param bytes data: data for encryption
        :return: encrypted data
        :rtype: bytes
        """
        aes_object = AES.new(self.key, AES.MODE_CBC, self.iv)
        return aes_object.encrypt(self.add_pkcs7_padding(data))

    def encrypt_unpadded(self, data):
        """
        Encrypts with AES in CBC mode without padding. The data has to fit into blocks of 16 bytes.

        :param bytes data: data for encryption
        :return: encrypted data
        :rtype: bytes
        """
        aes_object = AES.new(self.key, AES.MODE_CBC, self.iv)
        return aes_object.encrypt(data)

    @staticmethod
    def remove_pkcs7_padding(data):
        """
        Removes the PKCS7 padding.

        :param bytes data: padded data
        :return: data without padding
        :rtype: bytes
        """
        return data[:-data[-1]]

    def decrypt(self, encrypted_data):
        """
        Decrypts with AES in CBC mode with PKCS7 padding.

        :param bytes encrypted_data: encrypted data
        :return: decrypted data
        :rtype: bytes
        """
        aes_object = AES.new(self.key, AES.MODE_CBC, self.iv)
        return self.remove_pkcs7_padding(aes_object.decrypt(encrypted_data))

    def decrypt_unpadded(self, encrypted_data):
        """
        Decrypts with AES in CBC mode without padding. The data has to fit into blocks of 16 bytes.

        :param bytes encrypted_data: encrypted data
        :return: decrypted data
        :rtype: bytes
        """
        aes_object = AES.new(self.key, AES.MODE_CBC, self.iv)
        return aes_object.decrypt(encrypted_data)
