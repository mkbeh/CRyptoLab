# -*- coding: utf-8 -*-
import re

from cryptography.fernet import Fernet


# Func which validate fields: email, password and password confirmation.
def validate_values(email, password, re_password=None):
    pattern = re.compile(r'\w{4,35}@\w{2,10}\.\w{2,6}')

    try:
        re.match(pattern, email).group()

        if len(password) < 6:
            return False

        if re_password is not None:
            if password != re_password:
                return False

        return True

    except AttributeError:
        return False


# Func which encrypt string.
def encrypt_string(string_, cipher_key):
    # Encode string.
    encode_string_ = string_.encode('utf-8')

    # Make obj and encrypt string.
    cipher = Fernet(cipher_key)
    encrypted_string = cipher.encrypt(encode_string_)

    return encrypted_string


# Func which decrypt string
def decrypt_string(string_, cipher_key):
    # Decrypt string.
    cipher = Fernet(cipher_key)
    decrypted_string = cipher.decrypt(string_)

    # Decode string.
    decoded_string = decrypted_string.decode('utf-8')

    return decoded_string