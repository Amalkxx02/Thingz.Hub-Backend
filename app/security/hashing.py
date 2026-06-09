import bcrypt
import hashlib
import secrets


def hash_password(pwd: str) -> bytes:
    return bcrypt.hashpw(pwd.encode(), bcrypt.gensalt())


def verify_password(plain_pwd: str, hashed_pwd: bytes) -> bool:
    return bcrypt.checkpw(plain_pwd.encode(), hashed_pwd)


def get_fingerprint(value: str) -> bytes:
    return hashlib.sha256(value.encode()).hexdigest().encode()


def verify_fingerprint(value: str, fingerprint: bytes) -> bool:
    return secrets.compare_digest(get_fingerprint(value), fingerprint)
