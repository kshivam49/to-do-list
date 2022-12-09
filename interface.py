from todo import TaskList
from todo import tasks_collection
import pymongo
import tkinter as tk


class TaskListInterface(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()
        self.tasks = []

    def create_widgets(self):
        self.add_task_label = tk.Label(self, text="Add Task:")
        self.add_task_label.pack()

        self.add_task_entry = tk.Entry(self)
        self.add_task_entry.pack()

        self.add_task_button = tk.Button(
            self, text="Add Task", command=self.add_task)
        self.add_task_button.pack()

        self.remove_task_label = tk.Label(self, text="Remove Task (Index):")
        self.remove_task_label.pack()

        self.remove_task_entry = tk.Entry(self)
        self.remove_task_entry.pack()

        self.remove_task_button = tk.Button(
            self, text="Remove Task", command=self.remove_task)
        self.remove_task_button.pack()

        self.completed_tasks_label = tk.Label(self, text="Completed Tasks:")
        self.completed_tasks_label.pack()

        self.completed_tasks_listbox = tk.Listbox(self)
        self.completed_tasks_listbox.pack()

        self.complete_task_button = tk.Button(
            self, text="Complete Task", command=self.complete_task)
        self.complete_task_button.pack()

        self.complete_task_button.bind(
            "<Button-1>", lambda event: self.complete_task())

        self.incomplete_tasks_label = tk.Label(self, text="Incomplete Tasks:")
        self.incomplete_tasks_label.pack()

        self.incomplete_tasks_listbox = tk.Listbox(self)
        # Call the selectmode method and pass the tk.SINGLE constant as an argument
        self.incomplete_tasks_listbox = tk.Listbox(self, selectmode=tk.SINGLE)
        self.incomplete_tasks_listbox.pack()

    def add_task(self):
        # Get the task name from the entry field
        task_name = self.add_task_entry.get()

        # Create a task dictionary and add it to the TaskList
        task = {"name": task_name, "completed": False}
        task_list.add_task(task)

        # Clear the entry field
        self.add_task_entry.delete(0, tk.END)

    def remove_task(self):
        # Get the task index from the entry field
        task_index = int(self.remove_task_entry.get())

        # Remove the task from the TaskList
        task_list.remove_task(task_index)

        # Clear the entry field
        self.remove_task_entry.delete(0, tk.END)

    def update_tasks(self):
        # Clear the listboxes
        self.completed_tasks_listbox.delete(0, tk.END)
        self.incomplete_tasks_listbox.delete(0, tk.END)

        # Loop through the tasks in the TaskList
        for i, task in enumerate(task_list.tasks):
            # Add the task to the appropriate listbox
            if task["completed"]:
                self.completed_tasks_listbox.insert(tk.END, task["name"])
            else:
                self.incomplete_tasks_listbox.insert(tk.END, task["name"])

    def complete_task(self):
        # Get the index of the selected item in the incomplete tasks listbox
        selection = self.incomplete_tasks_listbox.curselection()

        # If no items are selected, return without doing anything
        if not selection:
            return

        # Get the first selected item
        task_index = selection[0]

        client = pymongo.MongoClient("mongodb://localhost:27017/")

        db = client["todo-app"]

        tasks_collection = db["tasks"]

        result = tasks_collection.update_one(
            {"id": task_index}, {"$set": {"completed": True}})

        # Use the selected index to complete the task in the TaskList
        task_list.complete_task(task_index)

        # Update the tasks in the listboxes
        self.update_tasks()


task_list = TaskList()
app = TaskListInterface()

# Update the tasks in the listboxes
app.update_tasks()

# Start the event loop
app.mainloop()
