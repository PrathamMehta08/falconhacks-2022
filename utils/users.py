import __main__
import hashlib
import uuid as uuid_lib

def generate_uuid():
    return uuid_lib.uuid4().hex

def generate_token(uuid, password):
    string = uuid+":"+password
    return hashlib.sha256(string.encode()).hexdigest()

def get_user(**kwargs):
    data = __main__.users.find_one(kwargs)
    if data:
        return User(data)
    return data

def check_cookies(cookies):
    if "uuid" in cookies and "token" in cookies:
        uuid = cookies["uuid"]
        token = cookies["token"]
        user = get_user(uuid=uuid)

        if user == None:
            return user
        elif user.token == token:
            return user
    return

def cache_user_agent(request):
    user_agent = request.headers.get('User-Agent')


def is_authenticated(cookies):
    return check_cookies(cookies) != None

class User:
    def __init__(self, data):
        self.data = data
        self.uuid = data.get("uuid")
        self.email = data.get("email")
        self.token = data.get("token")
        self.preferences = data.get("prefs")
        self.interested = data.get("interested")