import time
import json
import os
from plyer import notification
from datetime import datetime

TASK_FILE = "tasks.json"

def load_tasks():
    """Load tasks from a JSON file."""
    if os.path.exists(TASK_FILE):
        with open(TASK_FILE, "r") as file:
            return json.load(file)
    return []

def save_tasks(tasks):
    """Save tasks to a JSON file."""
    with open(TASK_FILE, "w") as file:
        json.dump(tasks, file, indent=4)

def add_task():
    """Allow user to add a new task with a reminder time."""
    task_name = input("Enter task name: ")
    reminder_time = input("Enter reminder time (HH:MM, 24-hour format): ")

    try:
        reminder_datetime = datetime.strptime(reminder_time, "%H:%M").time()
        task = {"task": task_name, "time": reminder_time}
        tasks = load_tasks()
        tasks.append(task)
        save_tasks(tasks)
        print(f"Task '{task_name}' scheduled for {reminder_time}.")
    except ValueError:
        print("Invalid time format! Use HH:MM (24-hour format).")

def check_reminders():
    """Check if any task is due and send a notification."""
    tasks = load_tasks()
    current_time = datetime.now().strftime("%H:%M")

    for task in tasks:
        if task["time"] == current_time:
            notification.notify(
                title="Task Reminder",
                message=task["task"],
                timeout=10
            )
            tasks.remove(task)  # Remove the task after notification
            save_tasks(tasks)

def main():
    """Main loop for checking tasks and handling user input."""
    while True:
        print("\n1. Add Task\n2. Start Reminder Bot\n3. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            add_task()
        elif choice == "2":
            print("Task Reminder Bot is running. Press Ctrl+C to stop.")
            while True:
                check_reminders()
                time.sleep(60)  # Check every minute
        elif choice == "3":
            print("Exiting Task Reminder Bot.")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()