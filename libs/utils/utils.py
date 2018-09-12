# -*- coding: utf-8 -*-
import re
import os
import sys

from cryptography.fernet import Fernet
from kivy.storage.jsonstore import JsonStore


# Func which validate fields: email, password and password confirmation.
# In future write validate funcs for all item.
def validate_values(email, password, re_password=None, username=None):
    email_pattern = re.compile(r'\w{4,35}@\w{2,10}\.\w{2,6}')
    username_pattern = re.compile(r'\w{6,20}')

    try:
        re.match(email_pattern, email).group()

        if len(password) < 6:
            return False

        if re_password is not None:
            if password != re_password:
                return False

            try:
                result = re.match(username_pattern, username).group()

                if len(result) < 6:
                    return False

                else:
                    return True

            except AttributeError:
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


# Func which decrypt string.
def decrypt_string(string_, cipher_key):
    # Decrypt string.
    cipher = Fernet(cipher_key)
    decrypted_string = cipher.decrypt(string_)

    # Decode string.
    decoded_string = decrypted_string.decode('utf-8')

    return decoded_string


# Func which return json store.
def get_store(user_dir):
    return JsonStore(os.path.join(user_dir, 'creds.json'))


# Func which write data into config file.
def write_into_cfg(config, section, key, value):
    config.set(section, key, value)
    config.write()


# Func which return path to dir.
def get_path():
    path = sys.argv[0]
    path = os.path.join(os.path.dirname(path), 'data')

    return path


# Check on coincidence.
def coincidence_check(val1, val2):
    try:
        res = re.match(val1, val2)
    except AttributeError:
        res = None

    return res
