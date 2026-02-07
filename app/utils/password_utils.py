"""
password_utils.py
-----------------
Utility functions for hashing and verifying passwords using bcrypt.

Functions:
- password_hashing: Hash a plaintext password.
- password_check: Verify a plaintext password against a hashed password.
"""

import bcrypt


def password_hashing(password: str) -> bytes:
    """
    Hash a plaintext password using bcrypt.

    Args:
        password (str): Plaintext password

    Returns:
        bytes: Hashed password, suitable for storage in database

    Notes:
        - bcrypt automatically generates a salt with gensalt().
        - Stored hashed passwords include the salt internally.
    """
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_pwd = bcrypt.hashpw(pwd_bytes, salt)
    return hashed_pwd


def password_check(hashed_pwd: bytes, entered_pwd: str) -> bool:
    """
    Verify if an entered password matches the stored hashed password.

    Args:
        hashed_pwd (bytes): Password hash stored in database
        entered_pwd (str): Password entered by user

    Returns:
        bool: True if passwords match, False otherwise

    Notes:
        - bcrypt handles salt internally when checking.
        - Always store hashed passwords; never store plaintext.
    """
    entered_bytes = entered_pwd.encode('utf-8')
    return bcrypt.checkpw(entered_bytes, hashed_pwd)
