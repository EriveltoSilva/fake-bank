""" accounts enum module"""

from enum import Enum


class UserGenderEnum(Enum):
    """Enum representing a user's gender"""

    MALE = 1
    FEMALE = 2
    OTHER = 3
