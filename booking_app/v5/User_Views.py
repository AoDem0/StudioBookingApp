import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
import Studios_Data_Man as sdm


#klasa matka na powtarzajace sie funkcje
class View(tk.Frame):
    def __init__(self, master, app, database, username):
        super().__init__(master)
        self.pack(fill="both", expand=True)
        self.app = app
        self.database = database
        self.username = username
        self.current_view = None        

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

#-------------client-----------------------------------------------------
class ClientView(View):
    def __init__(self, master, app, database, username):
        super().__init__(master, app, database, username)
        self.build_client_nav()
        self.build_profile_screen()

    def build_search_screen(self):
        self.clear_view()
        self.current_view = tk.Frame(self, bg="red")
        self.current_view.pack(fill="both", expand=True)
        row=0
        ttk.Label(self.current_view, text="Miasto:").grid(column=0,row=row, sticky=tk.W); self.city_entry = ttk.Entry(self.current_view); self.city_entry.grid(column=1,row=row)
        row+=1
        ttk.Label(self.current_view, text="Data (DD-MM-YYYY):").grid(column=0,row=row, sticky=tk.W); self.date_entry = ttk.Entry(self.current_view); self.date_entry.grid(column=1,row=row)
        row+=1
        ttk.Button(self.current_view, text="Szukaj").grid(column=0,row=row, pady=6)
        row+=1
        cols = ("id","name","city","capacity","equipment")
        self.user_tree = ttk.Treeview(self.current_view, columns=cols, show="headings", height=8)
        for c in cols: self.user_tree.heading(c, text=c)
        self.user_tree.grid(column=0,row=row, columnspan=3, sticky="nsew")
        self.current_view.rowconfigure(row, weight=1); self.current_view.columnconfigure(2, weight=1)
        row+=1
        ttk.Button(self.current_view, text="Rezerwuj wybraną").grid(column=0,row=row,pady=6)

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
#-------------employee-------------------------------------------------------
class EmployeeView(View):
    def __init__(self, master, app, database, username):
        super().__init__(master, app, database, username)
        self.build_profile_screen()
#-----------------admin-------------------------------------
