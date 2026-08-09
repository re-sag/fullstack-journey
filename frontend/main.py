from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from datetime import datetime
import json
import os

# File to save tasks
TASKS_FILE = "tasks.json"

class ToDoAppLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", padding=10, spacing=10, **kwargs)

        # Title
        self.add_widget(Label(text="📅 My Schedule & To‑Do List", font_size=20, size_hint_y=None, height=40))

        # Input fields
        self.task_input = TextInput(hint_text="Enter task...", multiline=False, size_hint_y=None, height=40)
        self.time_input = TextInput(hint_text="Enter time (HH:MM, e.g. 14:30)", multiline=False, size_hint_y=None, height=40)
        self.add_widget(self.task_input)
        self.add_widget(self.time_input)

        # Add button
        add_btn = Button(text="➕ Add Task", size_hint_y=None, height=45, background_color=(0.2, 0.6, 0.2, 1))
        add_btn.bind(on_press=self.add_task)
        self.add_widget(add_btn)

        # Scrollable task list
        self.scroll = ScrollView()
        self.task_list = GridLayout(cols=1, spacing=5, size_hint_y=None)
        self.task_list.bind(minimum_height=self.task_list.setter("height"))
        self.scroll.add_widget(self.task_list)
        self.add_widget(self.scroll)

        # Load saved tasks
        self.tasks = self.load_tasks()
        self.refresh_list()

    def add_task(self, instance):
        task_text = self.task_input.text.strip()
        task_time = self.time_input.text.strip()
        if task_text and task_time:
            try:
                # Validate time format
                datetime.strptime(task_time, "%H:%M")
                self.tasks.append({"task": task_text, "time": task_time, "done": False})
                self.save_tasks()
                self.refresh_list()
                self.task_input.text = ""
                self.time_input.text = ""
            except ValueError:
                self.task_input.text = "Invalid time! Use HH:MM"

    def refresh_list(self):
        self.task_list.clear_widgets()
        for idx, item in enumerate(self.tasks):
            row = BoxLayout(size_hint_y=None, height=50, spacing=5)
            status = "✅ " if item["done"] else "🔔 "
            text = f"{status}{item['time']} — {item['task']}"
            lbl = Label(text=text, halign="left", valign="middle")
            lbl.bind(size=lbl.setter("text_size"))
            row.add_widget(lbl)

            # Mark done button
            done_btn = Button(text="✓", size_hint_x=0.2, background_color=(0.2, 0.5, 1, 1))
            done_btn.bind(on_press=lambda b, i=idx: self.mark_done(i))
            row.add_widget(done_btn)

            # Delete button
            del_btn = Button(text="🗑️", size_hint_x=0.2, background_color=(0.9, 0.2, 0.2, 1))
            del_btn.bind(on_press=lambda b, i=idx: self.delete_task(i))
            row.add_widget(del_btn)

            self.task_list.add_widget(row)

    def mark_done(self, index):
        self.tasks[index]["done"] = not self.tasks[index]["done"]
        self.save_tasks()
        self.refresh_list()

    def delete_task(self, index):
        del self.tasks[index]
        self.save_tasks()
        self.refresh_list()

    def save_tasks(self):
        with open(TASKS_FILE, "w") as f:
            json.dump(self.tasks, f)

    def load_tasks(self):
        if os.path.exists(TASKS_FILE):
            with open(TASKS_FILE, "r") as f:
                return json.load(f)
        return []

class ScheduleApp(App):
    def build(self):
        return ToDoAppLayout()

if __name__ == "__main__":
    ScheduleApp().run()
