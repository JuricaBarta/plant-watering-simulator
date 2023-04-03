import sqlalchemy as db
import tkinter as tk
from tkinter import messagebox
from database import User, engine
from notebook_main import MainScreen


class LoginScreen(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("PyFloraPosuda - Prijava")
        self.geometry("600x400")

        # Create a frame to hold the widgets
        self.frame = tk.Frame(self)
        self.frame.grid(row=0, column=0)

        # Connect to the database
        self.connection = engine.connect()

        # Create the login form
        self.label_naslov = tk.Label(self.frame, text="Prijava", font=("Arial", "34", "bold"), anchor=tk.CENTER)
        self.label_naslov.grid(row=0, column=0, padx=10, pady=10)

        self.label_user_name = tk.Label(self.frame, text="User Name", font=("Arial", "12"))
        self.label_user_name.grid(row=1, column=0, padx=10, pady=10)
        
        self.entry_user_name = tk.Entry(self.frame)
        self.entry_user_name.grid(row=2, column=0, padx=2, pady=2)

        self.label_password = tk.Label(self.frame, text="Password", font=("Arial", "12"))
        self.label_password.grid(row=3, column=0, padx=10, pady=10)
        
        self.entry_password = tk.Entry(self.frame, show="*")
        self.entry_password.grid(row=4, column=0, padx=2, pady=2)

        self.password_show = tk.IntVar(value=0)
        self.show_password = tk.Checkbutton(self.frame, text="Show password", font="Arial", variable=self.password_show, onvalue=1, offvalue=0, command=self.hide_password)
        self.show_password.grid(row=5, column=0, padx=10, pady=10)

        self.prijavi_button = tk.Button(self.frame, text='Prijavi me', font="Arial", command=self.login)
        self.prijavi_button.grid(row=6, column=0, padx=10, pady=10)

        # Center the frame in the middle of the window
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure(1, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)

    def hide_password(self):
        if self.password_show.get() == 1:
            self.entry_password.config(show="")
        else:
            self.entry_password.config(show="*")

    def login(self):
        entered_username = self.entry_user_name.get()
        entered_password = self.entry_password.get()
    
        # Create the query using the select() method
        query = db.select(User).where(User.username == entered_username).where(User.password == entered_password)
        
        # Execute the query
        result = self.connection.execute(query).first()
    
        if result:
            # Credentials match, open the main screen
            self.destroy()
            main_screen = MainScreen()
            main_screen.mainloop()
        else:
            # Credentials don't match, show an error message
            messagebox.showerror("Error", "Incorrect username or password.")


try:
    engine = db.create_engine("sqlite:///users.db")
except Exception as e:
    print(f'Error: {e}')
    
if __name__ == "__main__":
    login_screen = LoginScreen()
    login_screen.mainloop()
    