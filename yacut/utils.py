import secrets
import string


def get_unique_short_id():
    lenth = 6
    res = ''.join(secrets.choice(string.digits + string.ascii_letters) for _ in range(lenth))
    return res
