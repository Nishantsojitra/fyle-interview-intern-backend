import random
import string
from datetime import datetime

TIMESTAMP_WITH_TIMEZONE_FORMAT = '%Y-%m-%dT%H:%M:%S.%f%z'


class GeneralObject:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


def get_utc_now():
    return datetime.utcnow()

# core/libs/helpers.py

def validate_principal(principal):
    if not isinstance(principal, dict):
        return False

    # Add your specific validation logic here
    required_fields = ['name', 'email']
    for field in required_fields:
        if field not in principal:
            return False

    # Example additional validation logic
    if not isinstance(principal['email'], str) or '@' not in principal['email']:
        return False

    return True

