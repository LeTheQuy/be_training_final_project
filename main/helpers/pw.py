import bcrypt


def generate_password_hash(password):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password, salt)


def verify_password_with_password_hash(password, password_hash):
    return bcrypt.checkpw(password, password_hash)
