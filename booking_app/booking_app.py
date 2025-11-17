# rental_app.py
import json, os, hashlib, datetime, itertools
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

DATA_FILE = "data.json"

# ---------- Helpers for data ----------
def load_data():
    if not os.path.exists(DATA_FILE):
        return initial_data()
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(d):
    tmp = DATA_FILE + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(d, f, indent=2, ensure_ascii=False)
    os.replace(tmp, DATA_FILE)

def initial_data():
    # default admin account: admin / admin123 (hashed)
    admin_pass = hash_pw("admin123")
    d = {"users":[{"username":"admin","password_hash":admin_pass,"role":"admin","managed_rooms":[]}],
         "rooms":[],
         "bookings":[]}
    save_data(d)
    return d

def hash_pw(pw):
    return hashlib.sha256(pw.encode("utf-8")).hexdigest()

def find_user(data, username):
    for u in data["users"]:
        if u["username"] == username:
            return u
    return None

def next_id(seq):
    if not seq:
        return 1
    return max(item["id"] for item in seq) + 1

# ---------- Business logic ----------
def check_availability(data, room_id, date_str, start_str, end_str, ignore_booking_id=None):
    # date format YYYY-MM-DD, time HH:MM
    s = datetime.datetime.strptime(f"{date_str} {start_str}", "%Y-%m-%d %H:%M")
    e = datetime.datetime.strptime(f"{date_str} {end_str}", "%Y-%m-%d %H:%M")
    if e <= s:
        return False, "Godzina zakończenia musi być później niż początek."
    for b in data["bookings"]:
        if b["room_id"] != room_id:
            continue
        if ignore_booking_id and b["id"] == ignore_booking_id:
            continue
        if b["date"] != date_str:
            continue
        bs = datetime.datetime.strptime(f"{b['date']} {b['start']}", "%Y-%m-%d %H:%M")
        be = datetime.datetime.strptime(f"{b['date']} {b['end']}", "%Y-%m-%d %H:%M")
        # overlap check
        if not (e <= bs or s >= be):
            return False, f"Kolizja z rezerwacją {b['user']} {b['start']}-{b['end']}."
    return True, ""

def search_rooms(data, city, date_str):
    # return rooms in city (case-insensitive)
    city = city.strip().lower()
    res = [r for r in data["rooms"] if r["city"].lower() == city]
    # availability per room for that date can be checked later
    return res

def create_booking(data, user, room_id, date_str, start, end, equipment):
    ok, msg = check_availability(data, room_id, date_str, start, end)
    if not ok:
        return False, msg
    bid = next_id(data["bookings"])
    data["bookings"].append({
        "id": bid,
        "room_id": room_id,
        "user": user,
        "date": date_str,
        "start": start,
        "end": end,
        "equipment": equipment
    })
    save_data(data)
    return True, "Zarezerwowano."

def delete_booking(data, booking_id):
    for i,b in enumerate(data["bookings"]):
        if b["id"] == booking_id:
            data["bookings"].pop(i)
            save_data(data)
            return True
    return False

def add_room(data, name, city, owner, capacity):
    rid = next_id(data["rooms"])
    data["rooms"].append({"id":rid,"name":name,"city":city,"owner":owner,"capacity":capacity,"equipment":[]})
    save_data(data)
    return rid

def add_user(data, username, password, role, managed_rooms=None):
    if find_user(data, username):
        return False, "Użytkownik istnieje."
    data["users"].append({"username":username,"password_hash":hash_pw(password),"role":role,"managed_rooms":managed_rooms or []})
    save_data(data)
    return True, "Dodano użytkownika."

def add_equipment_to_room(data, room_id, equip_name):
    for r in data["rooms"]:
        if r["id"] == room_id:
            if equip_name not in r["equipment"]:
                r["equipment"].append(equip_name)
                save_data(data)
                return True
            else:
                return False
    return False

# ---------- GUI ----------
class App:
    
    def __init__(self, root):
        self.root = root
        self.root.title("RentalApp")
        self.data = load_data()
        self.current_user = None
        self.build_login()

    def build_login(self):
        for w in self.root.winfo_children(): w.destroy()
        frm = ttk.Frame(self.root, padding=20)
        frm.pack(fill=tk.BOTH, expand=True)
        ttk.Label(frm, text="Login").grid(column=0,row=0, sticky=tk.W)
        self.login_entry = ttk.Entry(frm); self.login_entry.grid(column=1,row=0)
        ttk.Label(frm, text="Hasło").grid(column=0,row=1, sticky=tk.W)
        self.pw_entry = ttk.Entry(frm, show="*"); self.pw_entry.grid(column=1,row=1)
        ttk.Button(frm, text="Zaloguj", command=self.try_login).grid(column=0,row=2, pady=10)
        ttk.Button(frm, text="Zarejestruj (klient)", command=self.register_client).grid(column=1,row=2)

    def try_login(self):
        username = self.login_entry.get().strip()
        pw = self.pw_entry.get()
        if not username or not pw:
            messagebox.showwarning("Błąd","Wypełnij pola")
            return
        u = find_user(self.data, username)
        if not u or u["password_hash"] != hash_pw(pw):
            messagebox.showerror("Błąd","Niepoprawne dane")
            return
        self.current_user = u
        self.build_main_window()

    def register_client(self):
        username = simpledialog.askstring("Rejestracja","Nazwa użytkownika:")
        if not username:
            return
        if find_user(self.data, username):
            messagebox.showerror("Błąd","Nazwa zajęta")
            return
        pw = simpledialog.askstring("Rejestracja","Hasło:", show="*")
        if not pw:
            messagebox.showerror("Błąd","Hasło wymagane")
            return
        ok,msg = add_user(self.data, username, pw, "user")
        if ok:
            messagebox.showinfo("OK", "Zarejestrowano. Zaloguj się.")
        else:
            messagebox.showerror("Błąd", msg)

    def build_main_window(self):
        for w in self.root.winfo_children(): w.destroy()
        nb = ttk.Notebook(self.root)
        nb.pack(fill=tk.BOTH, expand=True)
        role = self.current_user["role"]
        # Always: profile tab (logout)
        tab_profile = ttk.Frame(nb); nb.add(tab_profile, text="Profil")
        ttk.Label(tab_profile, text=f"Zalogowany jako: {self.current_user['username']} ({role})").pack(anchor=tk.W, padx=10, pady=10)
        ttk.Button(tab_profile, text="Wyloguj", command=self.logout).pack(padx=10, pady=5, anchor=tk.W)

        if role in ("user","admin"):
            tab_search = ttk.Frame(nb); nb.add(tab_search, text="Szukaj sal")
            self.build_user_tab(tab_search)

        if role in ("employee","admin"):
            tab_employee = ttk.Frame(nb); nb.add(tab_employee, text="Pracownik: zarządzaj salami")
            self.build_employee_tab(tab_employee)

        if role == "admin":
            tab_admin = ttk.Frame(nb); nb.add(tab_admin, text="Admin: zarządzaj")
            self.build_admin_tab(tab_admin)

    def logout(self):
        self.current_user = None
        self.data = load_data()  # reload
        self.build_login()

    # ----- user tab -----
    def build_user_tab(self, frame):
        frm = ttk.Frame(frame, padding=8); frm.pack(fill=tk.BOTH, expand=True)
        row=0
        ttk.Label(frm, text="Miasto:").grid(column=0,row=row, sticky=tk.W); self.city_entry = ttk.Entry(frm); self.city_entry.grid(column=1,row=row)
        row+=1
        ttk.Label(frm, text="Data (YYYY-MM-DD):").grid(column=0,row=row, sticky=tk.W); self.date_entry = ttk.Entry(frm); self.date_entry.grid(column=1,row=row)
        row+=1
        ttk.Button(frm, text="Szukaj", command=self.user_search).grid(column=0,row=row, pady=6)
        row+=1
        cols = ("id","name","city","capacity","equipment")
        self.user_tree = ttk.Treeview(frm, columns=cols, show="headings", height=8)
        for c in cols: self.user_tree.heading(c, text=c)
        self.user_tree.grid(column=0,row=row, columnspan=3, sticky="nsew")
        frm.rowconfigure(row, weight=1); frm.columnconfigure(2, weight=1)
        row+=1
        ttk.Button(frm, text="Rezerwuj wybraną", command=self.user_book_selected).grid(column=0,row=row,pady=6)
        ttk.Button(frm, text="Dodaj sprzęt do sali (tylko admin/pracownik)", command=self.add_equip_to_room).grid(column=1,row=row,pady=6)

    def user_search(self):
        city = self.city_entry.get().strip()
        date_str = self.date_entry.get().strip()
        try:
            datetime.datetime.strptime(date_str, "%Y-%m-%d")
        except Exception:
            messagebox.showwarning("Błąd","Niepoprawna data. Format YYYY-MM-DD")
            return
        rooms = search_rooms(self.data, city, date_str)
        for r in self.user_tree.get_children(): self.user_tree.delete(r)
        for r in rooms:
            self.user_tree.insert("", tk.END, values=(r["id"], r["name"], r["city"], r.get("capacity",""), ", ".join(r.get("equipment",[]))))

    def user_book_selected(self):
        sel = self.user_tree.selection()
        if not sel:
            messagebox.showwarning("Błąd","Wybierz salę")
            return
        item = self.user_tree.item(sel[0])["values"]
        room_id = item[0]
        date_str = self.date_entry.get().strip()
        start = simpledialog.askstring("Start","Start (HH:MM):")
        if not start: return
        end = simpledialog.askstring("End","End (HH:MM):")
        if not end: return
        # equipment choice: ask comma-separated
        equip = simpledialog.askstring("Sprzęt (opcjonalnie)","Wpisz sprzęt oddzielony przecinkami (np. głośnik,mikrofon):")
        equipment = [e.strip() for e in (equip.split(",") if equip else []) if e.strip()]
        ok,msg = create_booking(self.data, self.current_user["username"], room_id, date_str, start, end, equipment)
        if ok:
            messagebox.showinfo("OK", msg)
        else:
            messagebox.showerror("Błąd", msg)

    def add_equip_to_room(self):
        # available to admin or employee only
        if self.current_user["role"] not in ("admin","employee"):
            messagebox.showwarning("Brak uprawnień","Tylko admin/pracownik może dodawać sprzęt do sali")
            return
        rid = simpledialog.askinteger("ID sali", "ID sali:")
        if rid is None: return
        equip = simpledialog.askstring("Sprzęt","Nazwa sprzętu:")
        if not equip:
            messagebox.showwarning("Błąd","Brak nazwy sprzętu")
            return
        ok = add_equipment_to_room(self.data, rid, equip.strip())
        if ok:
            messagebox.showinfo("OK","Dodano sprzęt")
        else:
            messagebox.showerror("Błąd","Nie udało się (może już istnieje lub sala nie istnieje)")

    # ----- employee tab -----
    def build_employee_tab(self, frame):
        frm = ttk.Frame(frame, padding=8); frm.pack(fill=tk.BOTH, expand=True)
        ttk.Label(frm, text="Twoje sale (lista)").pack(anchor=tk.W)
        cols = ("id","name","city","capacity","equipment")
        self.emp_rooms_tree = ttk.Treeview(frm, columns=cols, show="headings", height=6)
        for c in cols: self.emp_rooms_tree.heading(c, text=c)
        self.emp_rooms_tree.pack(fill=tk.BOTH, expand=False)
        ttk.Button(frm, text="Odśwież sale", command=self.emp_load_rooms).pack(pady=4, anchor=tk.W)

        ttk.Separator(frm, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=6)
        ttk.Label(frm, text="Kalendarz rezerwacji / zarządzaj").pack(anchor=tk.W)
        cols2 = ("id","room","user","date","start","end","equipment")
        self.emp_bookings_tree = ttk.Treeview(frm, columns=cols2, show="headings", height=8)
        for c in cols2: self.emp_bookings_tree.heading(c, text=c)
        self.emp_bookings_tree.pack(fill=tk.BOTH, expand=True)
        btnfrm = ttk.Frame(frm); btnfrm.pack(fill=tk.X, pady=6)
        ttk.Button(btnfrm, text="Odśwież rezerwacje", command=self.emp_load_bookings).pack(side=tk.LEFT)
        ttk.Button(btnfrm, text="Usuń zaznaczoną rezerwację", command=self.emp_delete_selected_booking).pack(side=tk.LEFT, padx=5)
        self.emp_load_rooms()
        self.emp_load_bookings()

    def emp_load_rooms(self):
        for r in self.emp_rooms_tree.get_children(): self.emp_rooms_tree.delete(r)
        # if employee has managed_rooms list, use it; admin can manage all own? we use managed_rooms from user
        managed = self.current_user.get("managed_rooms", [])
        rows = [rm for rm in self.data["rooms"] if (self.current_user["role"]=="admin") or (rm["id"] in managed) or (rm["owner"]==self.current_user["username"])]
        for r in rows:
            self.emp_rooms_tree.insert("", tk.END, values=(r["id"],r["name"],r["city"],r.get("capacity",""), ", ".join(r.get("equipment",[]))))

    def emp_load_bookings(self):
        for r in self.emp_bookings_tree.get_children(): self.emp_bookings_tree.delete(r)
        managed_ids = {rm["id"] for rm in self.data["rooms"] if (self.current_user["role"]=="admin") or (rm["owner"]==self.current_user["username"]) or (rm["id"] in self.current_user.get("managed_rooms",[]))}
        for b in sorted(self.data["bookings"], key=lambda x:(x["date"], x["start"])):
            if b["room_id"] in managed_ids:
                room = next((r for r in self.data["rooms"] if r["id"]==b["room_id"]), None)
                room_name = room["name"] if room else str(b["room_id"])
                self.emp_bookings_tree.insert("", tk.END, values=(b["id"], room_name, b["user"], b["date"], b["start"], b["end"], ", ".join(b.get("equipment",[]))))

    def emp_delete_selected_booking(self):
        sel = self.emp_bookings_tree.selection()
        if not sel:
            messagebox.showwarning("Błąd","Zaznacz rezerwację")
            return
        bid = int(self.emp_bookings_tree.item(sel[0])["values"][0])
        if not messagebox.askyesno("Potwierdź","Usunąć rezerwację?"):
            return
        ok = delete_booking(self.data, bid)
        if ok:
            messagebox.showinfo("OK","Usunięto")
            self.emp_load_bookings()
        else:
            messagebox.showerror("Błąd","Nie znaleziono rezerwacji")

    # ----- admin tab -----
    def build_admin_tab(self, frame):
        frm = ttk.Frame(frame, padding=8); frm.pack(fill=tk.BOTH, expand=True)
        ttk.Label(frm, text="Dodaj pracownika").grid(column=0,row=0, sticky=tk.W)
        ttk.Button(frm, text="Dodaj użytkownika (pracownik)", command=self.admin_add_worker).grid(column=1,row=0, sticky=tk.W)
        ttk.Label(frm, text="Dodaj salę").grid(column=0,row=1, sticky=tk.W, pady=6)
        ttk.Button(frm, text="Dodaj salę", command=self.admin_add_room).grid(column=1,row=1, sticky=tk.W)

        ttk.Separator(frm, orient=tk.HORIZONTAL).grid(column=0,row=2, columnspan=3, sticky="ew", pady=10)
        ttk.Label(frm, text="Lista sal (wszystkie)").grid(column=0,row=3, sticky=tk.W)
        cols = ("id","name","city","owner","capacity","equipment")
        self.admin_rooms_tree = ttk.Treeview(frm, columns=cols, show="headings", height=8)
        for c in cols: self.admin_rooms_tree.heading(c, text=c)
        self.admin_rooms_tree.grid(column=0,row=4, columnspan=3, sticky="nsew")
        frm.rowconfigure(4, weight=1)
        ttk.Button(frm, text="Odśwież listę sal", command=self.admin_load_rooms).grid(column=0,row=5, sticky=tk.W, pady=6)
        self.admin_load_rooms()

    def admin_add_worker(self):
        username = simpledialog.askstring("Nowy pracownik","Nazwa użytkownika:")
        if not username: return
        if find_user(self.data, username):
            messagebox.showerror("Błąd","Użytkownik istnieje")
            return
        pw = simpledialog.askstring("Hasło","Hasło:", show="*")
        if not pw: return
        # option to choose managed rooms later; for now empty
        ok,msg = add_user(self.data, username, pw, "employee", managed_rooms=[])
        if ok:
            messagebox.showinfo("OK","Dodano pracownika")
        else:
            messagebox.showerror("Błąd", msg)

    def admin_add_room(self):
        name = simpledialog.askstring("Nowa sala","Nazwa sali:")
        if not name: return
        city = simpledialog.askstring("Miasto","Miasto:")
        if not city: return
        owner = simpledialog.askstring("Właściciel (nazwa pracownika):","Właściciel (username):")
        if not owner:
            messagebox.showwarning("Błąd","Właściciel wymagany")
            return
        if not find_user(self.data, owner):
            messagebox.showerror("Błąd","Brak takiego użytkownika")
            return
        cap = simpledialog.askinteger("Pojemność","Pojemność (liczba):", minvalue=1, initialvalue=10)
        rid = add_room(self.data, name, city, owner, cap)
        # optionally add this room to owner's managed_rooms
        u = find_user(self.data, owner)
        if u is not None:
            u.setdefault("managed_rooms", []).append(rid)
            save_data(self.data)
        messagebox.showinfo("OK","Dodano salę")
        self.admin_load_rooms()

    def admin_load_rooms(self):
        for r in self.admin_rooms_tree.get_children(): self.admin_rooms_tree.delete(r)
        for rm in self.data["rooms"]:
            self.admin_rooms_tree.insert("", tk.END, values=(rm["id"], rm["name"], rm["city"], rm["owner"], rm.get("capacity",""), ", ".join(rm.get("equipment",[]))))

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("900x600")
    app = App(root)
    root.mainloop()
