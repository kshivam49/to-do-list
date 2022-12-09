import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")

db = client["todo-app"]

tasks_collection = db["tasks"]

# Define a TaskList class to manage the tasks in the collection


class TaskList:
    def __init__(self):
        # Load the tasks from the collection into a list
        self.tasks = []
        cursor = tasks_collection.find()
        for task in cursor:
            self.tasks.append(task)

    def add_task(self, task):
        # Add the task to the list and insert it into the collection
        self.tasks.append(task)
        tasks_collection.insert_one(task)

    def remove_task(self, index):
        # Remove the task from the list and delete it from the collection
        task = self.tasks[index]
        self.tasks.remove(task)
        tasks_collection.delete_one(task)

    def complete_task(self, index):
        # Mark the task as completed in the list and update it in the collection
        task = self.tasks[index]
        self.tasks[index]["completed"] = True
        tasks_collection.update_one(task, {"$set": {"completed": True}})
