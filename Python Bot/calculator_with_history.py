import tkinter as tk
import sqlite3

class Calculator:
    def __init__(self, root):  # Ensure the __init_ method accepts the root parameter
        self.root = root
        self.root.title("Calculator")
        self.root.geometry("300x500")
        self.expression = ""
        self.history_button = None

        # Create or connect to SQLite database
        self.conn = sqlite3.connect('calculator_history.db')
        self.cursor = self.conn.cursor()
        self.create_table()

        # Entry field to display input and results
        self.entry = tk.Entry(root, font=("Arial", 20), bd=5, relief=tk.SUNKEN, justify="right")
        self.entry.grid(row=0, column=0, columnspan=4, ipadx=8, ipady=8, pady=10)

        # Define button layout
        buttons = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
            ('0', 4, 0), ('.', 4, 1), ('C', 4, 2), ('+', 4, 3),
            ('=', 5, 0, 1, 4)  # Span across 4 columns
        ]

        # Create buttons dynamically
        for btn in buttons:
            text, row, col = btn[:3]
            rowspan = btn[3] if len(btn) > 3 else 1
            colspan = btn[4] if len(btn) > 4 else 1

            button = tk.Button(root, text=text, font=("Arial", 18), width=5, height=2, command=lambda t=text: self.on_button_click(t))
            button.grid(row=row, column=col, rowspan=rowspan, columnspan=colspan, sticky="nsew", padx=5, pady=5)

        # History button
        self.history_button = tk.Button(root, text="History", font=("Arial", 18), width=5, height=2, command=self.show_history)
        self.history_button.grid(row=6, column=0, columnspan=4, sticky="nsew", padx=5, pady=5)

    def create_table(self):
        """Create table in database to store history."""
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                expression TEXT NOT NULL,
                result TEXT NOT NULL
            )
        """)
        self.conn.commit()

    def save_to_history(self, expression, result):
        """Save calculation result to history in database."""
        self.cursor.execute("INSERT INTO history (expression, result) VALUES (?, ?)", (expression, result))
        self.conn.commit()

    def on_button_click(self, button_text):
        """Handles button clicks."""
        if button_text == "=":
            try:
                result = str(eval(self.expression))  # Evaluate expression safely
                self.save_to_history(self.expression, result)  # Save to history
                self.expression = result
            except Exception:
                self.expression = "Error"
        elif button_text == "C":
            self.expression = ""  # Clear entry field
        else:
            self.expression += button_text  # Append button press

        self.update_entry()

    def update_entry(self):
        """Update the calculator display."""
        self.entry.delete(0, tk.END)
        self.entry.insert(tk.END, self.expression)

    def show_history(self):
        """Show the calculation history in a new window."""
        history_window = tk.Toplevel(self.root)
        history_window.title("History")
        history_window.geometry("400x300")
        
        # Retrieve and display history from database
        self.cursor.execute("SELECT * FROM history")
        rows = self.cursor.fetchall()

        history_text = tk.Text(history_window, font=("Arial", 12), height=15, width=35)
        history_text.pack(padx=10, pady=10)

        for row in rows:
            history_text.insert(tk.END, f"{row[1]} = {row[2]}\n")

        history_text.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()  # Create the Tkinter window (root)
    calculator = Calculator(root)  # Pass root window to the Calculator class
    root.mainloop()  # Start the Tkinter event loop