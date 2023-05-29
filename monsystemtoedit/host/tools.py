import hashlib


def get_md5(content):
    """шифр md5"""
    md1 = hashlib.md5(content)
    return md1.hexdigest()
