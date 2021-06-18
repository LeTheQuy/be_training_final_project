from main.app import bcrypt


def generate_password_hash(password):
    return bcrypt.generate_password_hash(password)


def verify_password_with_password_hash(password, password_hash):
    return bcrypt.check_password_hash(password_hash, password)
