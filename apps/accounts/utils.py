"""account util module"""

import shortuuid


def generate_otp(length=12):
    """generate a random string identifier with [length] characters"""
    uuid_key = shortuuid.uuid()
    return uuid_key[:length]
