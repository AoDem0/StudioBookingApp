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

        ttk.Button(row1, text="Edytuj pracownik", command=self.edit_employee)\
            .pack(side="left", padx=5, pady=10)

        ttk.Button(row1, text="Usuń pracownik", command=self.remove_employee)\
            .pack(side="left", padx=5, pady=10)
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
        ttk.Button(row2, text="Zarządzaj sprzętem", command=self.manage_equipment).pack(side="left", padx=5, pady=10)
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

    def refresh_studios(self):
        # Czyści tabelę
        for i in self.admin_rooms_tree.get_children():
            self.admin_rooms_tree.delete(i)

        # Wczytuje dane z JSON
        data = self.database.load_data()
        studios = data.get("studios", [])
        for s in studios:
            # Equipment jako string, żeby wyświetlić w tabeli
            equipment_list = s.get("equipment", [])
            if equipment_list and isinstance(equipment_list[0], dict):
                # New format: list of dicts
                equipment_str = ", ".join([f"{eq['name']} ({eq['total']-eq['used']}/{eq['total']})" for eq in equipment_list])
            else:
                # Old format: list of strings
                equipment_str = ", ".join(equipment_list)
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
    
    def manage_equipment(self):
        """Manage equipment for a studio"""
        studio_id = simpledialog.askstring("Zarządzanie sprzętem", "Podaj ID studia:")
        if not studio_id:
            return
        
        try:
            studio_id_int = int(studio_id)
        except ValueError:
            messagebox.showerror("Błąd", "Nieprawidłowe ID!")
            return
        
        data = self.database.load_data()
        studios = data.get("studios", [])
        
        # Find studio
        studio = None
        for s in studios:
            if s["id"] == studio_id_int:
                studio = s
                break
        
        if not studio:
            messagebox.showerror("Błąd", "Studio nie znalezione!")
            return
        
        # Create equipment management window
        equipment_window = tk.Toplevel(self)
        equipment_window.title(f"Zarządzanie sprzętem - {studio['name']}")
        equipment_window.geometry("600x450")
        equipment_window.grab_set()
        
        tk.Label(equipment_window, text=f"Studio: {studio['name']}", font=("Arial", 14, "bold")).pack(pady=10)
        
        # Current equipment list (treeview)
        tk.Label(equipment_window, text="Aktualny sprzęt:", font=("Arial", 11)).pack(pady=5)
        
        list_frame = tk.Frame(equipment_window)
        list_frame.pack(fill="both", expand=True, padx=20, pady=5)
        
        cols = ("name", "used", "total", "available")
        equipment_tree = ttk.Treeview(list_frame, columns=cols, show="headings", height=10)
        equipment_tree.heading("name", text="Nazwa")
        equipment_tree.heading("used", text="Używane")
        equipment_tree.heading("total", text="Całkowita ilość")
        equipment_tree.heading("available", text="Dostępne")
        
        equipment_tree.column("name", width=200)
        equipment_tree.column("used", width=100)
        equipment_tree.column("total", width=100)
        equipment_tree.column("available", width=100)
        
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=equipment_tree.yview)
        equipment_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        equipment_tree.pack(side="left", fill="both", expand=True)
        
        # Load current equipment
        def refresh_equipment_list():
            equipment_tree.delete(*equipment_tree.get_children())
            equipment_list = studio.get("equipment", [])
            for equip in equipment_list:
                if isinstance(equip, dict):
                    available = equip['total'] - equip['used']
                    equipment_tree.insert("", "end", values=(
                        equip['name'],
                        equip['used'],
                        equip['total'],
                        available
                    ))
                else:
                    # Old format - convert to new format
                    equipment_tree.insert("", "end", values=(equip, 0, 1, 1))
        
        refresh_equipment_list()
        
        # Buttons
        button_frame = tk.Frame(equipment_window)
        button_frame.pack(pady=10)
        
        def add_equipment():
            add_window = tk.Toplevel(equipment_window)
            add_window.title("Dodaj sprzęt")
            add_window.geometry("350x200")
            add_window.grab_set()
            
            tk.Label(add_window, text="Nazwa sprzętu:").pack(pady=5)
            name_entry = tk.Entry(add_window, width=30)
            name_entry.pack(pady=5)
            
            tk.Label(add_window, text="Całkowita ilość:").pack(pady=5)
            total_entry = tk.Entry(add_window, width=30)
            total_entry.pack(pady=5)
            
            def save_equipment():
                name = name_entry.get().strip()
                total_str = total_entry.get().strip()
                
                if not name or not total_str:
                    messagebox.showwarning("Uwaga", "Wypełnij wszystkie pola!", parent=add_window)
                    return
                
                try:
                    total = int(total_str)
                    if total < 1:
                        raise ValueError
                except ValueError:
                    messagebox.showerror("Błąd", "Ilość musi być liczbą całkowitą większą od 0!", parent=add_window)
                    return
                
                if "equipment" not in studio:
                    studio["equipment"] = []
                
                # Check if equipment already exists
                for eq in studio["equipment"]:
                    if isinstance(eq, dict) and eq['name'] == name:
                        messagebox.showwarning("Uwaga", "Ten sprzęt już istnieje!", parent=add_window)
                        return
                    elif isinstance(eq, str) and eq == name:
                        messagebox.showwarning("Uwaga", "Ten sprzęt już istnieje!", parent=add_window)
                        return
                
                studio["equipment"].append({
                    "name": name,
                    "used": 0,
                    "total": total
                })
                self.database.save_data(data)
                refresh_equipment_list()
                self.refresh_studios()
                add_window.destroy()
                messagebox.showinfo("Sukces", "Sprzęt dodany!", parent=equipment_window)
            
            tk.Button(add_window, text="Zapisz", command=save_equipment, bg="green", fg="white").pack(pady=10)
        
        def edit_equipment():
            selected = equipment_tree.selection()
            if not selected:
                messagebox.showwarning("Uwaga", "Wybierz sprzęt do edycji!", parent=equipment_window)
                return
            
            item = equipment_tree.item(selected[0])
            old_name = item['values'][0]
            old_total = item['values'][2]
            
            edit_window = tk.Toplevel(equipment_window)
            edit_window.title("Edytuj sprzęt")
            edit_window.geometry("350x200")
            edit_window.grab_set()
            
            tk.Label(edit_window, text="Nazwa sprzętu:").pack(pady=5)
            name_entry = tk.Entry(edit_window, width=30)
            name_entry.insert(0, old_name)
            name_entry.pack(pady=5)
            
            tk.Label(edit_window, text="Całkowita ilość:").pack(pady=5)
            total_entry = tk.Entry(edit_window, width=30)
            total_entry.insert(0, old_total)
            total_entry.pack(pady=5)
            
            def save_changes():
                new_name = name_entry.get().strip()
                total_str = total_entry.get().strip()
                
                if not new_name or not total_str:
                    messagebox.showwarning("Uwaga", "Wypełnij wszystkie pola!", parent=edit_window)
                    return
                
                try:
                    new_total = int(total_str)
                    if new_total < 1:
                        raise ValueError
                except ValueError:
                    messagebox.showerror("Błąd", "Ilość musi być liczbą całkowitą większą od 0!", parent=edit_window)
                    return
                
                # Find and update equipment
                for eq in studio.get("equipment", []):
                    if isinstance(eq, dict) and eq['name'] == old_name:
                        eq['name'] = new_name
                        eq['total'] = new_total
                        # Make sure used doesn't exceed new total
                        if eq['used'] > new_total:
                            eq['used'] = new_total
                        break
                
                self.database.save_data(data)
                refresh_equipment_list()
                self.refresh_studios()
                edit_window.destroy()
                messagebox.showinfo("Sukces", "Sprzęt zaktualizowany!", parent=equipment_window)
            
            tk.Button(edit_window, text="Zapisz", command=save_changes, bg="green", fg="white").pack(pady=10)
        
        def remove_equipment():
            selected = equipment_tree.selection()
            if not selected:
                messagebox.showwarning("Uwaga", "Wybierz sprzęt do usunięcia!", parent=equipment_window)
                return
            
            item = equipment_tree.item(selected[0])
            equipment_name = item['values'][0]
            
            confirm = messagebox.askyesno("Potwierdzenie", f"Czy na pewno chcesz usunąć '{equipment_name}'?", parent=equipment_window)
            if not confirm:
                return
            
            # Remove equipment
            equipment_list = studio.get("equipment", [])
            studio["equipment"] = [
                eq for eq in equipment_list 
                if not (isinstance(eq, dict) and eq['name'] == equipment_name or eq == equipment_name)
            ]
            
            self.database.save_data(data)
            refresh_equipment_list()
            self.refresh_studios()
            messagebox.showinfo("Sukces", "Sprzęt usunięty!", parent=equipment_window)
        
        ttk.Button(button_frame, text="Dodaj sprzęt", command=add_equipment).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Edytuj wybrany", command=edit_equipment).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Usuń wybrany", command=remove_equipment).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Zamknij", command=equipment_window.destroy).pack(side="left", padx=5)
    
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
        cols = ("id", "studio_id", "studio_name", "username", "date", "time_from", "time_to", "equipment", "status")
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
            equipment = r.get("equipment", [])
            
            # Format equipment display
            if equipment:
                if isinstance(equipment[0], dict):
                    # New format with quantities
                    equipment_str = ", ".join([f"{eq['name']} x{eq['quantity']}" for eq in equipment])
                else:
                    # Old format: list of strings
                    equipment_str = ", ".join(equipment)
            else:
                equipment_str = "Brak"
                
            self.reservations_tree.insert("", "end", values=(
                r.get("id", ""),
                r.get("studio_id", ""),
                studio_name,
                r.get("username", ""),
                r.get("date", ""),
                r.get("time_from", ""),
                r.get("time_to", ""),
                equipment_str,
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