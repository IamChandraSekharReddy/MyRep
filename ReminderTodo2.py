import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import threading
import time

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List App with Reminders")

        # Create the frame for the task list
        self.frame = tk.Frame(root)
        self.frame.pack(pady=10)

        # Listbox to display tasks
        self.listbox = tk.Listbox(
            self.frame, 
            width=50, 
            height=10, 
            font=('Arial', 14), 
            bd=0, 
            selectbackground="gray", 
            activestyle="none"
        )
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH)

        # Scrollbar for the listbox
        self.scrollbar = tk.Scrollbar(self.frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.BOTH)

        self.listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.listbox.yview)

        # Entry box to add new tasks
        self.task_entry = tk.Entry(
            root, 
            font=('Arial', 14), 
            width=42, 
            bd=2
        )
        self.task_entry.pack(pady=10)

        # Entry box to add task reminder time
        self.time_entry = tk.Entry(
            root, 
            font=('Arial', 14), 
            width=42, 
            bd=2
        )
        self.time_entry.pack(pady=10)
        self.time_entry.insert(0, "Enter time in HH:MM format (24-hour)")

        # Button to add tasks with reminder
        self.add_button = tk.Button(
            root, 
            text="Add Task with Reminder", 
            font=('Arial', 14), 
            width=42, 
            bg="lightgreen", 
            command=self.add_task_with_reminder
        )
        self.add_button.pack(pady=10)

        # Button to mark tasks as completed
        self.complete_button = tk.Button(
            root, 
            text="Complete Task", 
            font=('Arial', 14), 
            width=42, 
            bg="lightblue", 
            command=self.complete_task
        )
        self.complete_button.pack(pady=10)

        # Button to delete tasks
        self.delete_button = tk.Button(
            root, 
            text="Delete Task", 
            font=('Arial', 14), 
            width=42, 
            bg="lightcoral", 
            command=self.delete_task
        )
        self.delete_button.pack(pady=10)

    def add_task_with_reminder(self):
        task = self.task_entry.get()
        reminder_time = self.time_entry.get()

        if task != "":
            self.listbox.insert(tk.END, f"{task} (Reminder set for {reminder_time})")
            self.task_entry.delete(0, tk.END)
            self.time_entry.delete(0, tk.END)

            # Start a thread to handle the reminder
            threading.Thread(target=self.set_reminder, args=(task, reminder_time)).start()
        else:
            messagebox.showwarning("Warning", "You must enter a task.")

    def set_reminder(self, task, reminder_time):
        try:
            # Wait until the specified time
            while True:
                current_time = datetime.now().strftime("%H:%M")
                if current_time == reminder_time:
                    messagebox.showinfo("Task Reminder", f"Reminder: {task}")
                    break
                time.sleep(60)  # Check every minute
        except Exception as e:
            print("Error in reminder thread:", e)

    def complete_task(self):
        try:
            task_index = self.listbox.curselection()[0]
            task = self.listbox.get(task_index)
            self.listbox.delete(task_index)
            self.listbox.insert(tk.END, f"{task} (Completed)")
        except:
            messagebox.showwarning("Warning", "You must select a task to complete.")

    def delete_task(self):
        try:
            task_index = self.listbox.curselection()[0]
            self.listbox.delete(task_index)
        except:
            messagebox.showwarning("Warning", "You must select a task to delete.")

if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()
