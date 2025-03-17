import hashlib

password = "adminpass"

ADMIN_PASSWORD_HASH = hashlib.sha256(password.encode()).hexdigest()