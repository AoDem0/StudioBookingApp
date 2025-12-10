import json
import os
import hashlib
import secrets
import Data_Man as dm


class User_Data(dm.Database_Management):
    def __init__(self, filename="users.json"):
        super().__init__(filename)

    # ---------- HASHOWANIE ----------
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

    # ---------- REJESTRACJA ----------
    def register_user(self, username, password, role, rooms_to_manage=None):
        if rooms_to_manage is None:
            rooms_to_manage = []

        users = self.load_data()

        #jezeli user istnieje to go nie rejestrujemy
        if username in users:
            return False

        #jak wyglada user w database
        users[username] = {
            "password": self.hash_password(password),
            "role": role,
            "rooms_to_manage": rooms_to_manage
        }

        #zapis do db
        self.save_data(users)
        return True

    # ---------- LOGOWANIE ----------
    def login_user(self, username, password):
        #zaladowanie danych
        users = self.load_data()

        #jesli nie ma usera to tekst
        if username not in users:
            return "User not found"

        if self.verify_password(password, users[username]["password"]):
            return users[username]   # ZWRACA CAŁY OBIEKT USERA

        return None   # złe hasło

    # ---------- POBIERANIE DANYCH ----------
    def get_user_role(self, username):
        users = self.load_data()
        return users.get(username, {}).get("role")

    def get_rooms(self, username):
        users = self.load_data()
        return users.get(username, {}).get("rooms_to_manage", [])

    def initial_data(self):
        # Sprawdź, czy admin już istnieje, żeby nie nadpisać
        users = self.load_data()
        if "admin" not in users:
            self.register_user(username="admin", password="admin123", role="admin", rooms_to_manage=[])
