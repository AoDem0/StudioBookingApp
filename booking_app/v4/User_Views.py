import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
import User_Data_Man as udm


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
class AdminView(tk.Frame):
    def __init__(self, master, app, database, username):
        super().__init__(master, app, database, username)
        self.build_admin_nav()
        self.build_profile_screen()

    def build_workers_manage_screen(self):
        self.clear_view()
        self.current_view = tk.Frame(self)
        self.current_view.pack(fill="both", expand=True)
        self.nav.pack_propagate(False)

        row1 = tk.Frame(self.current_view)
        row1.pack(fill="x")

        ttk.Label(row1, text="Pracownik:").pack(side="left", padx=5, pady=10)

        ttk.Button(row1, text="Dodaj użytkownika (pracownik)", command=self.register_employee)\
            .pack(side="left", padx=5, pady=10)

        ttk.Button(row1, text="Edytuj użytkownika (pracownik)", command=self.edit_employee)\
            .pack(side="left", padx=5, pady=10)

        ttk.Button(row1, text="Usuń użytkownika (pracownik)", command=self.remove_employee)\
            .pack(side="left", padx=5, pady=10)
        ttk.Separator(self.current_view, orient=tk.HORIZONTAL)\
            .pack(fill="x", pady=5)
        
        ttk.Separator(self.current_view, orient=tk.HORIZONTAL).pack(fill="x", pady=10)
        ttk.Label(self.current_view, text="Lista wszystkich pracowników").pack(anchor="w", padx=5)
        list_frame = tk.Frame(self.current_view)
        list_frame.pack(fill="both", expand=True, padx=5, pady=(5,0))
        cols = ("login","rooms")
        self.admin_rooms_tree = ttk.Treeview(list_frame, columns=cols, show="headings", height=8)
        for c in cols:
            self.admin_rooms_tree.heading(c, text=c)
        vsb = ttk.Scrollbar(list_frame, orient="vertical", command=self.admin_rooms_tree.yview)
        self.admin_rooms_tree.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        self.admin_rooms_tree.pack(side="left", fill="both", expand=True)
        btn_frame = tk.Frame(self.current_view)
        btn_frame.pack(fill="x", pady=6, padx=5)
        
        ttk.Button(btn_frame, text="Odśwież listę pracowników").pack(side="left")
    
    def build_studio_manage_screen(self):
        self.clear_view()
        self.current_view = tk.Frame(self)
        self.current_view.pack(fill="both", expand=True)
        self.nav.pack_propagate(False)
        row2 = tk.Frame(self.current_view)
        row2.pack(fill="x")

        ttk.Label(row2, text="Studia").pack(side="left", padx=5, pady=10)
        ttk.Button(row2, text="Dodaj studio").pack(side="left", padx=5, pady=10)
        ttk.Button(row2, text="Edytuj studio").pack(side="left", padx=5, pady=10)
        ttk.Button(row2, text="Usuń studio").pack(side="left", padx=5, pady=10)
        
        ttk.Separator(self.current_view, orient=tk.HORIZONTAL).pack(fill="x", pady=10)
        ttk.Label(self.current_view, text="Lista sal (wszystkie)").pack(anchor="w", padx=5)
        list_frame = tk.Frame(self.current_view)
        list_frame.pack(fill="both", expand=True, padx=5, pady=(5,0))
        cols = ("id","name","city","owner","capacity","equipment")
        self.admin_rooms_tree = ttk.Treeview(list_frame, columns=cols, show="headings", height=8)
        for c in cols:
            self.admin_rooms_tree.heading(c, text=c)
        vsb = ttk.Scrollbar(list_frame, orient="vertical", command=self.admin_rooms_tree.yview)
        self.admin_rooms_tree.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        self.admin_rooms_tree.pack(side="left", fill="both", expand=True)
        btn_frame = tk.Frame(self.current_view)
        btn_frame.pack(fill="x", pady=6, padx=5)
        ttk.Button(btn_frame, text="Odśwież listę sal").pack(side="left")
    
    def build_reservation_manage_screen(self):
        self.clear_view()
        self.current_view = tk.Frame(self)
        self.current_view.pack(fill="both", expand=True)
        self.nav.pack_propagate(False)
        row2 = tk.Frame(self.current_view)
        row2.pack(fill="x")

        ttk.Label(row2, text="Rezerwacje").pack(side="left", padx=5, pady=10)
        ttk.Button(row2, text="Edytuj rezerwację").pack(side="left", padx=5, pady=10)
        ttk.Button(row2, text="Usuń rezerwację").pack(side="left", padx=5, pady=10)
        ttk.Button(row2, text="Zatwierdź rezerwację").pack(side="left", padx=5, pady=10)

        ttk.Separator(self.current_view, orient=tk.HORIZONTAL).pack(fill="x", pady=10)
        ttk.Label(self.current_view, text="Lista sal (wszystkie)").pack(anchor="w", padx=5)
        list_frame = tk.Frame(self.current_view)
        list_frame.pack(fill="both", expand=True, padx=5, pady=(5,0))
        cols = ("id","name","city","owner","capacity","equipment")
        self.admin_rooms_tree = ttk.Treeview(list_frame, columns=cols, show="headings", height=8)
        for c in cols:
            self.admin_rooms_tree.heading(c, text=c)
        vsb = ttk.Scrollbar(list_frame, orient="vertical", command=self.admin_rooms_tree.yview)
        self.admin_rooms_tree.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        self.admin_rooms_tree.pack(side="left", fill="both", expand=True)
        btn_frame = tk.Frame(self.current_view)
        btn_frame.pack(fill="x", pady=6, padx=5)
        ttk.Button(btn_frame, text="Odśwież listę sal").pack(side="left")

    def register_employee(self):
        login = simpledialog.askstring("Rejestracja","Nazwa użytkownika:")
        password = simpledialog.askstring("Rejestracja","Hasło:", show="*")

        
        role = 'employee'

        if self.database.register_user(login, password, role):
            messagebox.showinfo("Sukces", "Konto utworzone!")
            
        else:
            messagebox.showerror("Błąd", "Użytkownik już istnieje!")

    def remove_employee(self):
        login = simpledialog.askstring("Usuwanie","Nazwa użytkownika:")
        if self.database.delete_user(login):
            messagebox.showinfo("Sukces", "Konto usunięte!")
            
        else:
            messagebox.showerror("Błąd", "Użytkownik nie znaleziony!")

    def edit_employee(self):
        login0 = simpledialog.askstring("Edycja","Znajdź użytkownika:")
        users = self.database.load_data()

        if login0 not in users:
            return "User not found"
        else:
            login1 = simpledialog.askstring("Edycja", f"Stary login użytkownika: {login0}\nNowa nazwa:")
            password =  simpledialog.askstring("Edycja", f"Nowe hasło:", show="*")
            if self.database.register_user(login1, password, role= 'employee'):
                messagebox.showinfo("Sukces", "Konto zmienione!")
                self.database.delete_user(login0)
                
            else:
                messagebox.showerror("Błąd", "Użytkownik już istnieje!")
            
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
            text="Zarządzaj pracownikami",
            command=self.build_workers_manage_screen,
            width=20
        ).pack(side="left", padx=5, pady=10)
        tk.Button(
            self.nav,
            text="Zarządzaj studiami",
            command=self.build_studio_manage_screen,
            width=20
        ).pack(side="left", padx=5, pady=10)
        tk.Button(
            self.nav,
            text="Zarządzaj rezerwacjami",
            command=self.build_reservation_manage_screen,
            width=20
        ).pack(side="left", padx=5, pady=10)
