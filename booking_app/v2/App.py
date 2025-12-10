import tkinter as tk
from tkinter import messagebox, ttk
import User_Data_Man as udm
import User_Views as uv



class LoginScreen(tk.Frame):
    def __init__(self, master, app, database):
        super().__init__(master)
        self.app = app
        self.database = database
        self.build_login_screen()

    def build_login_screen(self):
        tk.Label(self, text="LOGOWANIE", font=("Arial", 20)).pack(pady=10)

        tk.Label(self, text="Login").pack()
        self.login_entry = tk.Entry(self)
        self.login_entry.pack()

        tk.Label(self, text="Hasło").pack()
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack()

        tk.Button(self, text="Zaloguj", command=self.login).pack(pady=5)
        tk.Button(self, text="Rejestracja", command=self.app.show_register).pack()
#screen operations
    def login(self):
        login = self.login_entry.get()
        password = self.password_entry.get()

        if self.database.login_user(login, password):
            self.app.show_main(login)
        else:
            messagebox.showerror("Błąd", "Nieprawidłowe dane!")

# EKRAN REJESTRACJI
class RegisterScreen(tk.Frame):
    def __init__(self, master, app, database):
        super().__init__(master)
        self.app = app
        self.database = database
        self.build_register_screen()

#screen look
    def build_register_screen(self):
        tk.Label(self, text="REJESTRACJA", font=("Arial", 20)).pack(pady=10)

        tk.Label(self, text="Nowy login").pack()
        self.login_entry = tk.Entry(self)
        self.login_entry.pack()

        tk.Label(self, text="Nowe hasło").pack()
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack()

        tk.Button(self, text="Zarejestruj", command=self.register).pack(pady=5)
        tk.Button(self, text="Powrót", command=self.app.show_login).pack()
#screen operations
    def register(self):
        login = self.login_entry.get()
        password = self.password_entry.get()
        role = 'client'

        if self.database.register_user(login, password, role):
            messagebox.showinfo("Sukces", "Konto utworzone!")
            self.app.show_login()
        else:
            messagebox.showerror("Błąd", "Użytkownik już istnieje!")

# EKRAN PO ZALOGOWANIU


# GŁÓWNA APLIKACJA
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("System logowania")
        self.geometry("1200x750")

        self.database = udm.User_Data()
        self.database.initial_data()
        self.current_screen = None

        self.show_login()

    def clear_screen(self):
        if self.current_screen:
            self.current_screen.destroy()

    def show_login(self):
        self.clear_screen()
        self.current_screen = LoginScreen(self, self, self.database)
        self.current_screen.pack(expand=True)

    def show_register(self):
        self.clear_screen()
        self.current_screen = RegisterScreen(self, self, self.database)
        self.current_screen.pack(expand=True)

    def show_main(self, username):
        self.clear_screen()
        role = self.database.get_user_role(username)
        #NOWE
        if role == "admin":
            self.current_screen = uv.AdminView(self, self, self.database, username )
            self.current_screen.pack(fill="both", expand=True)
        #self.current_screen = MainScreen(self, self, username)
        elif role == "client":
            self.current_screen = uv.ClientView(self, self, self.database, username )
            self.current_screen.pack(fill="both", expand=True)
        
        else:
            print("Nieznana rola lub użytkownik nie istnieje")
            messagebox.showerror("Błąd", "Nieprawidłowy użytkownik")

        return




# START PROGRAMU

if __name__ == "__main__":
    app = App()
    app.mainloop()
