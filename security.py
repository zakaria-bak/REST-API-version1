from werkzeug.security import safe_str_cmp
from user import User

users = [
    User(1, "zakaria", "abcd")
]

username_table = {u.username : u for u in users}
userid_table = {u.id : u for u in users}

def authenticate(usernmae, password):
    user = username_table.get(usernmae, None)
    if user and safe_str_cmp(user.password, password):
        return user
    
def identity(payload):
    user_id = payload['identity']
    return userid_table.get(user_id, None)

