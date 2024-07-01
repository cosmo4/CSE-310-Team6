import datetime
import tkinter as tk
from tkinter import messagebox
from send_email import send_email

class DateReminderApp(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Test Date Reminder")

        # Labels and Entries for user inputs
        tk.Label(self, text="What day is your next test? ").grid(row=0, column=0)
        self.test_day_entry = tk.Entry(self)
        self.test_day_entry.grid(row=0, column=1)

        tk.Label(self, text="What month is your next test? ").grid(row=1, column=0)
        self.test_month_entry = tk.Entry(self)
        self.test_month_entry.grid(row=1, column=1)

        tk.Label(self, text="What is your email? ").grid(row=2, column=0)
        self.email_entry = tk.Entry(self)
        self.email_entry.grid(row=2, column=1)

        # Button to submit the data
        self.submit_button = tk.Button(self, text="Submit", command=self.submit_data)
        self.submit_button.grid(row=3, columnspan=2)

    def submit_data(self):
        try:
            test_day = int(self.test_day_entry.get())
            test_month = int(self.test_month_entry.get())
            email = self.email_entry.get()

            # Get the current date and time
            current_time = datetime.datetime.now()

            # Calculate the next test date and the reminder date
            next_test = datetime.datetime(2024, test_month, test_day)
            reminder_day = next_test - datetime.timedelta(days=2, hours=13)

            print("Current Time: ", current_time)
            print("Next Test: ", next_test)
            print("Day for Reminder: ", reminder_day)

            if current_time >= reminder_day:
                send_email(email)
                messagebox.showinfo("Reminder", "Reminder email sent!")
            else:
                messagebox.showinfo("Reminder", "It's not time for the reminder yet.")
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid day and month.")
       # except Exception as e:
       #     messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = DateReminderApp(root)
    app.mainloop()