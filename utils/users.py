import hashlib
import uuid as uuid_lib

def generate_uuid():
    return uuid_lib.uuid4().hex

def generate_token(uuid, password):
    string = uuid+":"+password
    return hashlib.sha256(string.encode()).hexdigest()

class User:
    def __init__(self, data):
        pass