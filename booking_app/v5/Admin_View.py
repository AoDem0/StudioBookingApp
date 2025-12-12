import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
import Studios_Data_Man as sdm
import Bookings_Data_Man as bdm
import User_Views as uv

class AdminView(uv.View):
    def __init__(self, master, app, database, username):
        super().__init__(master, app, database, username)
        self.dataMAn = sdm.Studio_Data()
        self.bookingMan = bdm.Booking_Data()
        self.build_admin_nav()
        self.build_profile_screen()
    #-------------edit-employees----------------------
    def build_workers_manage_screen(self):
        self.clear_view()
        self.current_view = tk.Frame(self)
        self.current_view.pack(fill="both", expand=True)
        self.nav.pack_propagate(False)

        row1 = tk.Frame(self.current_view)
        row1.pack(fill="x")

        ttk.Label(row1, text="Pracownik:").pack(side="left", padx=5, pady=10)

        ttk.Button(row1, text="Dodaj pracownika", command=self.register_employee)\
            .pack(side="left", padx=5, pady=10)
        ttk.Button(row1, text="Dodaj studio do pracownika",command=self.add_studio_to_employee).pack(side="left", padx=5, pady=10)
        

        ttk.Button(row1, text="Edytuj pracownik", command=self.edit_employee)\
            .pack(side="left", padx=5, pady=10)

        ttk.Button(row1, text="Usuń pracownik", command=self.remove_employee)\
            .pack(side="left", padx=5, pady=10)
        ttk.Button(row1, text="Usuń studio dla pracownika",command=self.remove_studio_to_employee).pack(side="left", padx=5, pady=10)
        
        ttk.Separator(self.current_view, orient=tk.HORIZONTAL)\
            .pack(fill="x", pady=5)
        
        ttk.Separator(self.current_view, orient=tk.HORIZONTAL).pack(fill="x", pady=10)
        ttk.Label(self.current_view, text="Lista użytkowników (employee)").pack(anchor="w", padx=5)

        list_frame = tk.Frame(self.current_view)
        list_frame.pack(fill="both", expand=True, padx=5, pady=(5,0))
        cols = ("username", "managed_rooms")
        self.users_tree = ttk.Treeview(list_frame, columns=cols, show="headings", height=8)
        for c in cols:
            self.users_tree.heading(c, text=c)
        vsb = ttk.Scrollbar(list_frame, orient="vertical", command=self.users_tree.yview)
        self.users_tree.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        self.users_tree.pack(side="left", fill="both", expand=True)

        # Przycisk odśwież
        btn_frame = tk.Frame(self.current_view)
        btn_frame.pack(fill="x", pady=6, padx=5)
        ttk.Button(btn_frame, text="Odśwież listę użytkowników", command=self.refresh_employees).pack(side="left")

        # Pierwsze wczytanie danych
        self.refresh_employees()

    def add_studio_to_employee(self):
        login = simpledialog.askstring("Dodanie studia do pracownika","Nazwa użytkownika:")
        id = simpledialog.askstring("Dodanie studia do pracownika","ID studia do dodania:")
        if self.database.add_user_rooms(login, id):
            messagebox.showinfo("Sukces", f"Dodano studio z ID: {id} do pracownika {login}")
            
        else:
            messagebox.showerror("Błąd", "Niepoprawne ID lub login")

    def remove_studio_to_employee(self):
        login = simpledialog.askstring("Usunięcie studia pracownika","Nazwa użytkownika:")
        id = simpledialog.askstring("Usunięcie studia pracownika","ID studia:")
        if self.database.remove_user_rooms(login, id):
            messagebox.showinfo("Sukces", f"Usunięto studio z ID: {id} dla pracownika {login}")
            
        else:
            messagebox.showerror("Błąd", "Niepoprawne ID lub login")


    def refresh_employees(self):
        for i in self.users_tree.get_children():
            self.users_tree.delete(i)

        # Wczytuje użytkowników z rolą 'employee'
        data = self.database.load_data()
        users = data.get("users", [])
        for u in users:
            if u.get("role") == "employee":
                managed_rooms_str = ", ".join(u.get("managed_rooms", []))
                self.users_tree.insert("", "end", values=(u["username"], managed_rooms_str)) 

    def register_employee(self):
        login = simpledialog.askstring("Rejestracja","Nazwa użytkownika:")
        password = simpledialog.askstring("Nowe studio","Hasło:", show="*")

        
        role = 'employee'

        if self.database.register_user(login, password, role):
            messagebox.showinfo("Sukces", "Konto utworzone!")
            self.refresh_employees()
        else:
            messagebox.showerror("Błąd", "Użytkownik już istnieje!")

    def remove_employee(self):
        login = simpledialog.askstring("Usuwanie","Nazwa użytkownika:")
        if self.database.delete_user(login):
            messagebox.showinfo("Sukces", "Konto usunięte!")
            self.refresh_employees()
        else:
            messagebox.showerror("Błąd", "Użytkownik nie znaleziony!")

    def edit_employee(self):
        login0 = simpledialog.askstring("Edycja", "Znajdź użytkownika:")
        data = self.database.load_data()
        users = data.get("users", [])

        # szukamy użytkownika
        for user in users:
            if user["username"] == login0:
                # jeśli znajdziemy użytkownika
                login1 = simpledialog.askstring("Edycja", f"Stary login: {login0}\nNowy login:")
                password = simpledialog.askstring("Edycja", "Nowe hasło:", show="*")
                if self.database.register_user(login1, password, role='employee'):
                    messagebox.showinfo("Sukces", "Konto zmienione!")
                    self.database.delete_user(login0)
                    self.refresh_employees()
                else:
                    messagebox.showerror("Błąd", "Użytkownik o nowej nazwie już istnieje!")
                return

        # nic nie znaleziono
        messagebox.showerror("Błąd", "Użytkownik nie znaleziony!")
    #-------------edit-studios----------------------     
    def build_studio_manage_screen(self):
        self.clear_view()
        self.current_view = tk.Frame(self)
        self.current_view.pack(fill="both", expand=True)
        self.nav.pack_propagate(False)
        row2 = tk.Frame(self.current_view)
        row2.pack(fill="x")

        ttk.Label(row2, text="Studia").pack(side="left", padx=5, pady=10)
        ttk.Button(row2, text="Dodaj studio",command=self.register_studio).pack(side="left", padx=5, pady=10)
        ttk.Button(row2, text="Edytuj studio", command=self.edit_studio).pack(side="left", padx=5, pady=10)
        ttk.Button(row2, text="Dodaj sprzęt do studia",command=self.add_eq_to_studio).pack(side="left", padx=5, pady=10)
        ttk.Button(row2, text="Usuń studio", command=self.remove_studio).pack(side="left", padx=5, pady=10)
        
        ttk.Separator(self.current_view, orient=tk.HORIZONTAL).pack(fill="x", pady=10)
        ttk.Label(self.current_view, text="Lista sal (wszystkie)").pack(anchor="w", padx=5)

        list_frame = tk.Frame(self.current_view)
        list_frame.pack(fill="both", expand=True, padx=5, pady=(5,0))
        cols = ("id", "name", "city", "price_for_h", "equipment")
        self.admin_rooms_tree = ttk.Treeview(list_frame, columns=cols, show="headings", height=8)
        for c in cols:
            self.admin_rooms_tree.heading(c, text=c)
        vsb = ttk.Scrollbar(list_frame, orient="vertical", command=self.admin_rooms_tree.yview)
        self.admin_rooms_tree.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        self.admin_rooms_tree.pack(side="left", fill="both", expand=True)

        # Przycisk odśwież
        btn_frame = tk.Frame(self.current_view)
        btn_frame.pack(fill="x", pady=6, padx=5)
        ttk.Button(btn_frame, text="Odśwież listę sal", command=self.refresh_studios).pack(side="left")

        # Pierwsze wczytanie danych
        self.refresh_studios()

    def add_eq_to_studio(self):
        id = simpledialog.askstring("Nowe sprzęt","ID studia:")
        if not id: return
        name = simpledialog.askstring("Nowe sprzęt","Nazwa sprzętu:")
        if not name: return
        total = simpledialog.askstring("Nowe sprzęt","Ilość sprzętu:")
        if not total: return

        id_int = int(id)
        total_int = int(total)
        used = 0
        if self.dataMAn.add_equipment(id_int, name, used, total_int):
            messagebox.showinfo("Sukces", "Dodano sprzęt")
            
        else:
            messagebox.showerror("Błąd", "Nie można dodać sprzętu")

    def remove_eq_from_studio(self):
        return

    def refresh_studios(self):
        # Czyści tabelę
        for i in self.admin_rooms_tree.get_children():
            self.admin_rooms_tree.delete(i)

        # Wczytuje dane z JSON
        data = self.database.load_data()
        studios = data.get("studios", [])
        for s in studios:
            # Equipment jako string, żeby wyświetlić w tabeli
            equipment_str = ", ".join(s.get("equipment", []))
            self.admin_rooms_tree.insert("", "end", values=(s["id"], s["name"], s["city"], s.get("price_for_h", ""), equipment_str))

    def register_studio(self):
        
        name = simpledialog.askstring("Nowe studio","Nazwa studia:")
        if not name: return
        city = simpledialog.askstring("Nowe studio","Miasto:")
        if not city: return
        price = simpledialog.askstring("Nowe studio","Cena za godzine:")
        if not price: return

        id = self.dataMAn.next_id()

        if self.dataMAn.register_studio(id, name, city, price):
            messagebox.showinfo("Sukces", "Studio utworzone!")
            self.refresh_studios()
        else:
            messagebox.showerror("Błąd", "Studio już istnieje!")

    def remove_studio(self):
        id = simpledialog.askstring("Usuń studio","ID studia:")
        if not id: return
        
        id_int = int(id)
        if self.dataMAn.remove_studio(id_int):
            messagebox.showinfo("Sukces", "Studio usunięte!")
            self.refresh_studios()
        else:
            messagebox.showerror("Błąd", "Studio nie znalezione!")

    def edit_studio(self):
        id0 = simpledialog.askstring("Edytuj studio","ID studia:")
        if not id0: return
        
        id_int = int(id0)

        data = self.database.load_data()
        studios = data.get("studios", [])

        # szukamy użytkownika
        for studio in studios:
            if studio["id"] == id_int:

                name = simpledialog.askstring("Edycja", f"Stara nazwa: \nNowa nazwa:")
                city = simpledialog.askstring("Edycja", "Nazwa miasta")
                price = simpledialog.askstring("Edycja", "Nowa cena za godzinę")

                id1 = self.dataMAn.next_id()

                if self.dataMAn.register_studio(id1, name, city, price):
                    messagebox.showinfo("Sukces", "Studio zmienione!")
                    self.dataMAn.remove_studio(id_int)
                    self.refresh_studios()
                else:
                    messagebox.showerror("Błąd", "Studio o nowej nazwie już istnieje!")
                return

        # jeśli pętla się zakończyła i nic nie znaleziono
        messagebox.showerror("Błąd", "Studio nie znalezione!")
    #-------------edit-reservations----------------------
    def build_reservation_manage_screen(self):
        self.clear_view()
        self.current_view = tk.Frame(self)
        self.current_view.pack(fill="both", expand=True)
        self.nav.pack_propagate(False)
        row2 = tk.Frame(self.current_view)
        row2.pack(fill="x")

        ttk.Label(row2, text="Rezerwacje").pack(side="left", padx=5, pady=10)
        ttk.Button(row2, text="Edytuj rezerwację", command=self.edit_reservation).pack(side="left", padx=5, pady=10)
        ttk.Button(row2, text="Usuń rezerwację", command=self.remove_reservation).pack(side="left", padx=5, pady=10)
        ttk.Button(row2, text="Zatwierdź rezerwację", command=self.approve_reservation).pack(side="left", padx=5, pady=10)

        ttk.Separator(self.current_view, orient=tk.HORIZONTAL).pack(fill="x", pady=10)
        ttk.Label(self.current_view, text="Lista rezerwacji (wszystkie)").pack(anchor="w", padx=5)
        
        list_frame = tk.Frame(self.current_view)
        list_frame.pack(fill="both", expand=True, padx=5, pady=(5,0))
        cols = ("id", "studio_id", "studio_name", "username", "date", "time_from", "time_to", "status")
        self.reservations_tree = ttk.Treeview(list_frame, columns=cols, show="headings", height=8)
        for c in cols:
            self.reservations_tree.heading(c, text=c)
        vsb = ttk.Scrollbar(list_frame, orient="vertical", command=self.reservations_tree.yview)
        self.reservations_tree.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        self.reservations_tree.pack(side="left", fill="both", expand=True)
        
        btn_frame = tk.Frame(self.current_view)
        btn_frame.pack(fill="x", pady=6, padx=5)
        ttk.Button(btn_frame, text="Odśwież listę rezerwacji", command=self.refresh_reservations).pack(side="left")

        # Pierwsze wczytanie danych
        self.refresh_reservations()

    def refresh_reservations(self):
        # Czyści tabelę
        for i in self.reservations_tree.get_children():
            self.reservations_tree.delete(i)

        # Wczytuje dane z JSON
        data = self.database.load_data()
        reservations = data.get("reservations", [])
        studios = data.get("studios", [])
        
        # Tworzymy mapę studio_id -> studio_name
        studio_map = {s["id"]: s["name"] for s in studios}
        
        for r in reservations:
            studio_name = studio_map.get(r.get("studio_id"), "Unknown")
            self.reservations_tree.insert("", "end", values=(
                r.get("id", ""),
                r.get("studio_id", ""),
                studio_name,
                r.get("username", ""),
                r.get("date", ""),
                r.get("time_from", ""),
                r.get("time_to", ""),
                r.get("status", "")
            ))

    def edit_reservation(self):
        selected = self.reservations_tree.selection()
        if not selected:
            messagebox.showwarning("Uwaga", "Wybierz rezerwację do edycji!")
            return
        
        item = self.reservations_tree.item(selected[0])
        reservation_id = int(item['values'][0])
        
        date = simpledialog.askstring("Edycja", "Nowa data (DD-MM-YYYY):")
        time_from = simpledialog.askstring("Edycja", "Nowa godzina rozpoczęcia (HH:MM):")
        time_to = simpledialog.askstring("Edycja", "Nowa godzina zakończenia (HH:MM):")
        
        if self.bookingMan.update_reservation(reservation_id, date, time_from, time_to):
            messagebox.showinfo("Sukces", "Rezerwacja zaktualizowana!")
            self.refresh_reservations()
        else:
            messagebox.showerror("Błąd", "Nie udało się zaktualizować rezerwacji!")

    def remove_reservation(self):
        selected = self.reservations_tree.selection()
        if not selected:
            messagebox.showwarning("Uwaga", "Wybierz rezerwację do usunięcia!")
            return
        
        item = self.reservations_tree.item(selected[0])
        reservation_id = int(item['values'][0])
        
        confirm = messagebox.askyesno("Potwierdzenie", "Czy na pewno chcesz usunąć tę rezerwację?")
        if confirm:
            if self.bookingMan.remove_reservation(reservation_id):
                messagebox.showinfo("Sukces", "Rezerwacja usunięta!")
                self.refresh_reservations()
            else:
                messagebox.showerror("Błąd", "Nie udało się usunąć rezerwacji!")

    def approve_reservation(self):
        selected = self.reservations_tree.selection()
        if not selected:
            messagebox.showwarning("Uwaga", "Wybierz rezerwację do zatwierdzenia!")
            return
        
        item = self.reservations_tree.item(selected[0])
        reservation_id = int(item['values'][0])
        
        if self.bookingMan.update_reservation_status(reservation_id, "approved"):
            messagebox.showinfo("Sukces", "Rezerwacja zatwierdzona!")
            self.refresh_reservations()
        else:
            messagebox.showerror("Błąd", "Nie udało się zatwierdzić rezerwacji!")

    def build_admin_nav(self):
        self.nav = tk.Frame(self, height=60)
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