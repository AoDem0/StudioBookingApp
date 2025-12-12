import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
import Studios_Data_Man as sdm
import Bookings_Data_Man as bdm


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
        self.bookingMan = bdm.Booking_Data()
        self.build_client_nav()
        self.build_profile_screen()

    def build_search_screen(self):
        self.clear_view()
        self.current_view = tk.Frame(self)
        self.current_view.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Search filters frame
        filter_frame = tk.LabelFrame(self.current_view, text="Filtry wyszukiwania", padx=10, pady=10)
        filter_frame.pack(fill="x", pady=(0, 10))
        
        row = 0
        ttk.Label(filter_frame, text="Miasto:").grid(column=0, row=row, sticky=tk.W, pady=5)
        self.city_entry = ttk.Entry(filter_frame, width=30)
        self.city_entry.grid(column=1, row=row, pady=5, padx=5)
        
        row += 1
        ttk.Label(filter_frame, text="Data (DD-MM-YYYY):").grid(column=0, row=row, sticky=tk.W, pady=5)
        self.date_entry = ttk.Entry(filter_frame, width=30)
        self.date_entry.grid(column=1, row=row, pady=5, padx=5)
        
        row += 1
        ttk.Label(filter_frame, text="Godzina od (HH:MM):").grid(column=0, row=row, sticky=tk.W, pady=5)
        self.time_from_entry = ttk.Entry(filter_frame, width=30)
        self.time_from_entry.grid(column=1, row=row, pady=5, padx=5)
        
        row += 1
        ttk.Label(filter_frame, text="Godzina do (HH:MM):").grid(column=0, row=row, sticky=tk.W, pady=5)
        self.time_to_entry = ttk.Entry(filter_frame, width=30)
        self.time_to_entry.grid(column=1, row=row, pady=5, padx=5)
        
        row += 1
        button_frame = tk.Frame(filter_frame)
        button_frame.grid(column=0, row=row, columnspan=2, pady=10)
        ttk.Button(button_frame, text="Szukaj", command=self.search_studios).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Wyczyść filtry", command=self.clear_filters).pack(side="left", padx=5)
        
        # Results frame
        results_frame = tk.LabelFrame(self.current_view, text="Dostępne studia", padx=10, pady=10)
        results_frame.pack(fill="both", expand=True)
        
        # Treeview for results
        tree_frame = tk.Frame(results_frame)
        tree_frame.pack(fill="both", expand=True)
        
        cols = ("id", "name", "city", "price_for_h", "equipment")
        self.user_tree = ttk.Treeview(tree_frame, columns=cols, show="headings", height=10)
        
        self.user_tree.heading("id", text="ID")
        self.user_tree.heading("name", text="Nazwa")
        self.user_tree.heading("city", text="Miasto")
        self.user_tree.heading("price_for_h", text="Cena/godz")
        self.user_tree.heading("equipment", text="Wyposażenie")
        
        self.user_tree.column("id", width=50)
        self.user_tree.column("name", width=150)
        self.user_tree.column("city", width=100)
        self.user_tree.column("price_for_h", width=100)
        self.user_tree.column("equipment", width=250)
        
        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.user_tree.yview)
        self.user_tree.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        self.user_tree.pack(side="left", fill="both", expand=True)
        
        # Reserve button
        reserve_frame = tk.Frame(results_frame)
        reserve_frame.pack(fill="x", pady=(10, 0))
        ttk.Button(reserve_frame, text="Rezerwuj wybrane studio", command=self.reserve_studio).pack(side="left")
        
        # Initial search - show all studios
        self.search_studios()

    def clear_filters(self):
        """Clear all search filters"""
        self.city_entry.delete(0, tk.END)
        self.date_entry.delete(0, tk.END)
        self.time_from_entry.delete(0, tk.END)
        self.time_to_entry.delete(0, tk.END)
        self.search_studios()

    def search_studios(self):
        """Search for studios based on filters"""
        # Clear current results
        for i in self.user_tree.get_children():
            self.user_tree.delete(i)
        
        # Get filter values
        city_filter = self.city_entry.get().strip().lower()
        date_filter = self.date_entry.get().strip()
        time_from_filter = self.time_from_entry.get().strip()
        time_to_filter = self.time_to_entry.get().strip()
        
        # Load data
        data = self.database.load_data()
        studios = data.get("studios", [])
        
        # Filter studios
        filtered_studios = []
        for studio in studios:
            # Filter by city
            if city_filter and city_filter not in studio.get("city", "").lower():
                continue
            
            # Filter by availability (if date and time provided)
            if date_filter and time_from_filter and time_to_filter:
                if not self.bookingMan.check_availability(
                    studio["id"], 
                    date_filter, 
                    time_from_filter, 
                    time_to_filter
                ):
                    continue  # Skip if not available
            
            filtered_studios.append(studio)
        
        # Display results
        if not filtered_studios:
            messagebox.showinfo("Brak wyników", "Nie znaleziono studiów spełniających kryteria!")
        
        for studio in filtered_studios:
            # Handle both dict and string equipment formats
            equipment_list = studio.get("equipment", [])
            if equipment_list:
                if isinstance(equipment_list[0], dict):
                    # New format: list of dicts with name, used, total
                    equipment_str = ", ".join([f"{eq['name']} ({eq['total']-eq['used']}/{eq['total']})" for eq in equipment_list])
                else:
                    # Old format: list of strings
                    equipment_str = ", ".join(equipment_list)
            else:
                equipment_str = ""
            
            self.user_tree.insert("", "end", values=(
                studio["id"],
                studio["name"],
                studio["city"],
                studio.get("price_for_h", ""),
                equipment_str
            ))

    def reserve_studio(self):
        """Reserve selected studio"""
        selected = self.user_tree.selection()
        if not selected:
            messagebox.showwarning("Uwaga", "Wybierz studio do rezerwacji!")
            return
        
        item = self.user_tree.item(selected[0])
        studio_id = int(item['values'][0])
        studio_name = item['values'][1]
        
        # Get studio equipment
        data = self.database.load_data()
        studios = data.get("studios", [])
        studio = next((s for s in studios if s["id"] == studio_id), None)
        
        if not studio:
            messagebox.showerror("Błąd", "Studio nie znalezione!")
            return
        
        studio_equipment = studio.get("equipment", [])
        
        # Create popup window for reservation details
        reservation_window = tk.Toplevel(self)
        reservation_window.title("Szczegóły rezerwacji")
        reservation_window.geometry("450x550")
        reservation_window.grab_set()  # Make window modal
        
        tk.Label(reservation_window, text=f"Rezerwacja: {studio_name}", font=("Arial", 14, "bold")).pack(pady=10)
        
        # Date field
        date_frame = tk.Frame(reservation_window)
        date_frame.pack(pady=5, padx=20, fill="x")
        tk.Label(date_frame, text="Data (DD-MM-YYYY):", width=20, anchor="w").pack(side="left")
        date_entry = tk.Entry(date_frame, width=20)
        date_entry.pack(side="left", padx=5)
        if self.date_entry.get().strip():
            date_entry.insert(0, self.date_entry.get().strip())
        
        # Time from field
        time_from_frame = tk.Frame(reservation_window)
        time_from_frame.pack(pady=5, padx=20, fill="x")
        tk.Label(time_from_frame, text="Godzina od (HH:MM):", width=20, anchor="w").pack(side="left")
        time_from_entry = tk.Entry(time_from_frame, width=20)
        time_from_entry.pack(side="left", padx=5)
        if self.time_from_entry.get().strip():
            time_from_entry.insert(0, self.time_from_entry.get().strip())
        
        # Time to field
        time_to_frame = tk.Frame(reservation_window)
        time_to_frame.pack(pady=5, padx=20, fill="x")
        tk.Label(time_to_frame, text="Godzina do (HH:MM):", width=20, anchor="w").pack(side="left")
        time_to_entry = tk.Entry(time_to_frame, width=20)
        time_to_entry.pack(side="left", padx=5)
        if self.time_to_entry.get().strip():
            time_to_entry.insert(0, self.time_to_entry.get().strip())
        
        # Equipment selection
        ttk.Separator(reservation_window, orient=tk.HORIZONTAL).pack(fill="x", pady=10)
        tk.Label(reservation_window, text="Dodatkowy sprzęt:", font=("Arial", 11, "bold")).pack(pady=5)
        
        equipment_frame = tk.Frame(reservation_window)
        equipment_frame.pack(pady=5, padx=20, fill="both", expand=True)
        
        # Create spinboxes for studio equipment
        equipment_spinboxes = {}
        if studio_equipment:
            canvas = tk.Canvas(equipment_frame, height=180)
            scrollbar = ttk.Scrollbar(equipment_frame, orient="vertical", command=canvas.yview)
            scrollable_frame = tk.Frame(canvas)
            
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            for equip in studio_equipment:
                if isinstance(equip, dict):
                    # New format: dict with name, used, total
                    equip_name = equip['name']
                    available = equip['total'] - equip['used']
                    if available > 0:
                        row_frame = tk.Frame(scrollable_frame)
                        row_frame.pack(anchor="w", pady=3, fill="x")
                        
                        tk.Label(row_frame, text=f"{equip_name}:", width=20, anchor="w").pack(side="left")
                        tk.Label(row_frame, text=f"(dostępne: {available})", width=15, anchor="w", fg="gray").pack(side="left")
                        
                        spinbox = tk.Spinbox(row_frame, from_=0, to=available, width=5)
                        spinbox.pack(side="left", padx=5)
                        spinbox.delete(0, tk.END)
                        spinbox.insert(0, "0")
                        
                        equipment_spinboxes[equip_name] = {'spinbox': spinbox, 'max': available}
                else:
                    # Old format: string (treat as 1 available)
                    row_frame = tk.Frame(scrollable_frame)
                    row_frame.pack(anchor="w", pady=3, fill="x")
                    
                    tk.Label(row_frame, text=f"{equip}:", width=20, anchor="w").pack(side="left")
                    
                    spinbox = tk.Spinbox(row_frame, from_=0, to=1, width=5)
                    spinbox.pack(side="left", padx=5)
                    spinbox.delete(0, tk.END)
                    spinbox.insert(0, "0")
                    
                    equipment_spinboxes[equip] = {'spinbox': spinbox, 'max': 1}
            
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
        else:
            tk.Label(equipment_frame, text="Brak dostępnego sprzętu w tym studiu", fg="gray").pack()
        
        def confirm_reservation():
            date = date_entry.get().strip()
            time_from = time_from_entry.get().strip()
            time_to = time_to_entry.get().strip()
            
            if not date or not time_from or not time_to:
                messagebox.showwarning("Uwaga", "Wypełnij wszystkie pola!", parent=reservation_window)
                return
            
            # Collect selected equipment with quantities
            selected_equipment = []
            for equip_name, equip_data in equipment_spinboxes.items():
                quantity = int(equip_data['spinbox'].get())
                if quantity > 0:
                    selected_equipment.append({
                        "name": equip_name,
                        "quantity": quantity
                    })
            
            # Check availability
            if not self.bookingMan.check_availability(studio_id, date, time_from, time_to):
                messagebox.showerror("Błąd", "Studio nie jest dostępne w wybranym terminie!", parent=reservation_window)
                return
            
            # Create reservation with equipment
            if self.bookingMan.create_reservation(
                studio_id, 
                self.username, 
                date, 
                time_from, 
                time_to, 
                status="pending",
                equipment=selected_equipment
            ):
                equipment_info = ""
                if selected_equipment:
                    equip_list = [f"{eq['name']} x{eq['quantity']}" for eq in selected_equipment]
                    equipment_info = f"\nSprzęt: {', '.join(equip_list)}"
                
                messagebox.showinfo(
                    "Sukces", 
                    f"Rezerwacja studia '{studio_name}' została utworzona!\n"
                    f"Data: {date}\n"
                    f"Godziny: {time_from} - {time_to}{equipment_info}\n"
                    f"Status: Oczekuje na zatwierdzenie",
                    parent=reservation_window
                )
                reservation_window.destroy()
                self.search_studios()  # Refresh results
            else:
                messagebox.showerror("Błąd", "Nie udało się utworzyć rezerwacji!", parent=reservation_window)
        
        # Buttons
        button_frame = tk.Frame(reservation_window)
        button_frame.pack(pady=20)
        tk.Button(button_frame, text="Potwierdź", command=confirm_reservation, width=15, bg="green", fg="white").pack(side="left", padx=5)
        tk.Button(button_frame, text="Anuluj", command=reservation_window.destroy, width=15).pack(side="left", padx=5)
        
        # Buttons
        button_frame = tk.Frame(reservation_window)
        button_frame.pack(pady=20)
        tk.Button(button_frame, text="Potwierdź", command=confirm_reservation, width=15, bg="green", fg="white").pack(side="left", padx=5)
        tk.Button(button_frame, text="Anuluj", command=reservation_window.destroy, width=15).pack(side="left", padx=5)

    def build_my_reservations_screen(self):
        """Show user's reservations"""
        self.clear_view()
        self.current_view = tk.Frame(self)
        self.current_view.pack(fill="both", expand=True, padx=20, pady=20)
        
        ttk.Label(
            self.current_view, 
            text="Moje rezerwacje", 
            font=("Arial", 16)
        ).pack(pady=(0, 10))
        
        # Treeview for reservations
        list_frame = tk.Frame(self.current_view)
        list_frame.pack(fill="both", expand=True)
        
        cols = ("id", "studio_name", "date", "time_from", "time_to", "equipment", "status")
        self.my_reservations_tree = ttk.Treeview(list_frame, columns=cols, show="headings", height=12)
        
        self.my_reservations_tree.heading("id", text="ID")
        self.my_reservations_tree.heading("studio_name", text="Studio")
        self.my_reservations_tree.heading("date", text="Data")
        self.my_reservations_tree.heading("time_from", text="Od")
        self.my_reservations_tree.heading("time_to", text="Do")
        self.my_reservations_tree.heading("equipment", text="Sprzęt")
        self.my_reservations_tree.heading("status", text="Status")
        
        self.my_reservations_tree.column("id", width=50)
        self.my_reservations_tree.column("studio_name", width=120)
        self.my_reservations_tree.column("date", width=100)
        self.my_reservations_tree.column("time_from", width=70)
        self.my_reservations_tree.column("time_to", width=70)
        self.my_reservations_tree.column("equipment", width=150)
        self.my_reservations_tree.column("status", width=100)
        
        vsb = ttk.Scrollbar(list_frame, orient="vertical", command=self.my_reservations_tree.yview)
        self.my_reservations_tree.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        self.my_reservations_tree.pack(side="left", fill="both", expand=True)
        
        # Buttons
        btn_frame = tk.Frame(self.current_view)
        btn_frame.pack(fill="x", pady=(10, 0))
        ttk.Button(btn_frame, text="Odśwież", command=self.refresh_my_reservations).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Anuluj wybraną", command=self.cancel_reservation).pack(side="left", padx=5)
        
        # Load reservations
        self.refresh_my_reservations()

    def refresh_my_reservations(self):
        """Refresh user's reservations"""
        # Clear tree
        for i in self.my_reservations_tree.get_children():
            self.my_reservations_tree.delete(i)
        
        # Load data
        data = self.database.load_data()
        reservations = data.get("reservations", [])
        studios = data.get("studios", [])
        
        # Create studio map
        studio_map = {s["id"]: s["name"] for s in studios}
        
        # Filter user's reservations
        user_reservations = [r for r in reservations if r.get("username") == self.username]
        
        # Display
        for r in user_reservations:
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
                
            self.my_reservations_tree.insert("", "end", values=(
                r.get("id"),
                studio_name,
                r.get("date"),
                r.get("time_from"),
                r.get("time_to"),
                equipment_str,
                r.get("status")
            ))

    def cancel_reservation(self):
        """Cancel selected reservation"""
        selected = self.my_reservations_tree.selection()
        if not selected:
            messagebox.showwarning("Uwaga", "Wybierz rezerwację do anulowania!")
            return
        
        item = self.my_reservations_tree.item(selected[0])
        reservation_id = int(item['values'][0])
        status = item['values'][6]
        
        if status == "cancelled":
            messagebox.showinfo("Info", "Ta rezerwacja jest już anulowana!")
            return
        
        confirm = messagebox.askyesno("Potwierdzenie", "Czy na pewno chcesz anulować tę rezerwację?")
        if confirm:
            if self.bookingMan.update_reservation_status(reservation_id, "cancelled"):
                messagebox.showinfo("Sukces", "Rezerwacja anulowana!")
                self.refresh_my_reservations()
            else:
                messagebox.showerror("Błąd", "Nie udało się anulować rezerwacji!")

    def build_client_nav(self):
        self.nav = tk.Frame(self, bg="lightblue", height=60)
        self.nav.pack(side="top", fill="x")
        self.nav.pack_propagate(False)

        tk.Button(
            self.nav,
            text="Profil",
            command=self.build_profile_screen,
            width=20
        ).pack(side="left", padx=5, pady=10)

        tk.Button(
            self.nav,
            text="Szukaj studiów",
            command=self.build_search_screen,
            width=20
        ).pack(side="left", padx=5, pady=10)
        
        tk.Button(
            self.nav,
            text="Moje rezerwacje",
            command=self.build_my_reservations_screen,
            width=20
        ).pack(side="left", padx=5, pady=10)

#-------------employee-------------------------------------------------------
class EmployeeView(View):
    def __init__(self, master, app, database, username):
        super().__init__(master, app, database, username)
        self.build_profile_screen()
#-----------------admin-------------------------------------