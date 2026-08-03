import re

def is_valid_username(username):
    if len(username) < 5:
        return False

    if not re.search(r"[A-Z]", username):
        return False

    if not re.search(r"[a-z]", username):
        return False

    return True
def is_valid_password(password):

    if len(password) < 5:
        return False

    if not re.search(r"[A-Za-z]", password):
        return False

    if not re.search(r"[0-9]", password):
        return False

    if not re.search(r"[$%*&]", password):
        return False

    return True