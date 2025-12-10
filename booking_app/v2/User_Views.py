import tkinter as tk
from tkinter import messagebox, ttk


#STARA WERSJA W MIARE DZIALAJĄCA
class ClientViewOLD:
    def __init__(self, master, main_area, username):
        self.master = master
        self.main_area = main_area
        self.username = username
        self.current_view = None

        self.build_nav()
        self.show_profile()  # domyślny widok

    def build_nav(self):
        # Każdy widok może mieć inną nawigację, więc robimy ją tutaj
        self.nav = tk.Frame(self.master, bg="green", height=60)
        self.nav.pack(side="top", fill="x")
        self.nav.pack_propagate(False)

        # Przykładowe przyciski
        tk.Button(self.nav, text="Profile", width=20,
                  command=self.show_profile).pack(side="left", padx=5, pady=10)

        tk.Button(self.nav, text="Test2", width=20,
                  command=self.show_test).pack(side="left", padx=5, pady=10)

    def clear_view(self):
        if self.current_view:
            self.current_view.destroy()

    def show_profile(self):
        self.clear_view()
        self.current_view = tk.Frame(self.main_area, bg="red")
        self.current_view.pack(fill="both", expand=True)
        tk.Label(self.current_view,
                 text=f"Zalogowany jako: {self.username}",
                 bg="red", fg="white",
                 font=("Arial", 20)).pack(pady=50)

    def show_test(self):
        self.clear_view()
        self.current_view = tk.Frame(self.main_area, bg="orange")
        self.current_view.pack(fill="both", expand=True)
        tk.Label(self.current_view,
                 text="TEST VIEW",
                 bg="orange",
                 font=("Arial", 30, "bold")).pack(pady=100)

class MainScreenOLD(tk.Frame):

    def __init__(self, master, app, username):
        super().__init__(master)
        self.app = app
        self.username = username

        self.build_main_area()

        # ClientView teraz zarządza nawigacją i widokami
        self.client_view = ClientViewOLD(self, self.main_area, self.username)

    def build_main_area(self):
        self.main_area = tk.Frame(self, bg="blue")
        self.main_area.pack(fill="both", expand=True)

    def clear_view(self):
        # Ta funkcja może być wywoływana przez ClientView, jeśli potrzeba
        if hasattr(self, "client_view"):
            self.client_view.clear_view()
#____________NOWE________
class ClientView(tk.Frame):
    def __init__(self, master, app, database, username):
        super().__init__(master)
        self.pack(fill="both", expand=True)

        self.app = app
        self.database = database
        self.username = username
        self.current_view = None        

        self.build_client_nav()
        self.build_profile_screen()

    def clear_view(self):
        if self.current_view:
            self.current_view.destroy()    

    def build_profile_screen(self):
        self.clear_view()

        self.current_view = tk.Frame(self)
        self.current_view.pack(expand=True)

        tk.Label(
            self.current_view,
            text=f"Zalogowany jako: {self.username}",
            font=("Arial", 18)
        ).pack(pady=20)

        tk.Button(
            self.current_view,
            text="Wyloguj się",
            command=self.app.show_login
        ).pack(pady=10)

    def build_search_screen(self):
        self.clear_view()
        self.current_view = tk.Frame(self, bg="green")
        self.current_view.pack(fill="both", expand=True)

        tk.Label(
            self.current_view,
            text="Szukaj",
            fg="white",
            font=("Arial", 20)
        ).pack()

    def search_studios(self):
        return

    def build_client_nav(self):
        self.nav = tk.Frame(self, bg="green", height=60)
        self.nav.pack(side="top", fill="x")
        self.nav.pack_propagate(False)

        tk.Button(
            self.nav,
            text="Profile",
            command=self.build_profile_screen,
            width=20
        ).pack(side="left", padx=5, pady=10)

        tk.Button(
            self.nav,
            text="Search",
            command=self.build_search_screen,
            width=20
        ).pack(side="left", padx=5, pady=10)

class AdminView(tk.Frame):
    def __init__(self, master, app, database, username):
        super().__init__(master)
        self.pack(fill="both", expand=True)

        self.app = app
        self.database = database
        self.username = username
        self.current_view = None        

        self.build_admin_nav()
        self.build_profile_screen()

    def clear_view(self):
        if self.current_view:
            self.current_view.destroy()    

    def build_profile_screen(self):
        self.clear_view()

        self.current_view = tk.Frame(self)
        self.current_view.pack(expand=True)

        tk.Label(
            self.current_view,
            text=f"Zalogowany jako: {self.username}",
            font=("Arial", 18)
        ).pack(pady=20)

        tk.Button(
            self.current_view,
            text="Wyloguj się",
            command=self.app.show_login
        ).pack(pady=10)

    def build_search_screen(self):
        self.app.clear_view()
        self.current_view = tk.Frame(self, bg="green")
        self.current_view.pack(fill="both", expand=True)

        tk.Label(
            self.current_view,
            text="Szukaj",
            fg="white",
            font=("Arial", 20)
        ).pack()


    def build_workers_manage_screen(self):
        return

    def build_admin_nav(self):
        self.nav = tk.Frame(self, bg="green", height=60)
        self.nav.pack(side="top", fill="x")
        self.nav.pack_propagate(False)

        tk.Button(
            self.nav,
            text="Profile",
            command=self.build_profile_screen,
            width=20
        ).pack(side="left", padx=5, pady=10)

        tk.Button(
            self.nav,
            text="Search",
            command=self.build_search_screen,
            width=20
        ).pack(side="left", padx=5, pady=10)

        tk.Button(
            self.nav,
            text="Zarządzaj pracownikami",
            command=self.build_workers_manage_screen,
            width=20
        ).pack(side="left", padx=5, pady=10)
