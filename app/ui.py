# app/ui.py
import tkinter as tk
from tkinter import messagebox
from app.task_manager_app import TaskManagerApp

class TaskManagerUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Manager")

        # Crear botones y entradas de la UI
        self.add_button = tk.Button(root, text="Agregar Tarea", command=self.add_task)
        self.add_button.pack()

        self.show_button = tk.Button(root, text="Mostrar Tareas", command=self.show_tasks)
        self.show_button.pack()

        self.complete_button = tk.Button(root, text="Marcar como Completada", command=self.complete_task)
        self.complete_button.pack()

        self.delete_button = tk.Button(root, text="Eliminar Tarea", command=self.delete_task)
        self.delete_button.pack()

    def add_task(self):
        # Lógica para agregar una tarea
        messagebox.showinfo("Agregar tarea", "Aquí puedes agregar una tarea.")

    def show_tasks(self):
        # Lógica para mostrar las tareas
        messagebox.showinfo("Mostrar tareas", "Aquí se mostrarán las tareas.")

    def complete_task(self):
        # Lógica para completar una tarea
        messagebox.showinfo("Completar tarea", "Aquí puedes marcar una tarea como completada.")

    def delete_task(self):
        # Lógica para eliminar una tarea
        messagebox.showinfo("Eliminar tarea", "Aquí puedes eliminar una tarea.")

# Función para iniciar la UI
def run_ui():
    root = tk.Tk()
    app = TaskManagerUI(root)
    root.mainloop()

if __name__ == "__main__":
    run_ui()