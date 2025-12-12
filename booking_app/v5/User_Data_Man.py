import hashlib
import secrets
import Data_Man as dm


class User_Data(dm.Database_Management):
    def __init__(self, filename="database.json"):
        super().__init__(filename)

    def hash_password(self, password, salt=None):
        if salt is None:
            salt = secrets.token_hex(16)
        combined = salt + password
        hashed = hashlib.sha256(combined.encode()).hexdigest()
        return f"{salt}${hashed}"

    def verify_password(self, password, stored_hash):
        salt, hashed = stored_hash.split("$")
        check_hash = hashlib.sha256((salt + password).encode()).hexdigest()
        return check_hash == hashed

    def register_user(self, username, password, role, managed_rooms=None):
        if managed_rooms is None:
            managed_rooms = []
        data = self.load_data()
        if "users" not in data:
            data["users"] = []
        for u in data["users"]:
            if u["username"] == username:
                return False 
        new_user = {
            "username": username,
            "password_hash": self.hash_password(password),
            "role": role,
            "managed_rooms": managed_rooms
        }
        data["users"].append(new_user)
        self.save_data(data)
        return True

    def login_user(self, username, password):
        data = self.load_data()
        users = data.get("users", [])

        for user in users:
            if user["username"] == username:
                if self.verify_password(password, user["password_hash"]):
                    return user       # logowanie OK
                else:
                    return None       # złe hasło

        return "User not found"

    def get_user_role(self, username):
        data = self.load_data()
        for user in data.get("users", []):
            if user["username"] == username:
                return user.get("role")
        return None
    def get_user_rooms(self, username):
        data = self.load_data()
        for user in data.get("users", []):
            if user["username"] == username:
                return user.get("managed_rooms", [])
        return []
    
    def add_user_rooms(self, username, id):
        data = self.load_data()
        for user in data.get("users", []):
            if user["username"] == username:
                if id not in user["managed_rooms"]:
                    user["managed_rooms"].append(id)
                    self.save_data(data)
                    return True
    
    def remove_user_rooms(self, username, id):
        data = self.load_data()
        for user in data.get("users", []):
            if user["username"] == username:
                if id in user["managed_rooms"]:
                    user["managed_rooms"].remove(id)
                    self.save_data(data)
                    return True





    def initial_data(self):
        data = self.load_data()

        if "users" not in data:
            data["users"] = []

        # sprawdzamy czy admin istnieje
        for user in data["users"]:
            if user["username"] == "admin":
                return

        # tworzymy admina
        self.register_user("admin", "admin123", "admin", managed_rooms=[])

    def delete_user(self, login):
        data = self.load_data()
        users = data.get("users", [])

        # admin nie może być usunięty
        if self.get_user_role(login) == "admin":
            return False

        # szukamy usera do usunięcia
        for user in users:
            if user["username"] == login:
                users.remove(user)
                self.save_data(data)
                return True

        return False  
        