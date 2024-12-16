import os
import json
import socket
import configparser
import tkinter as tk
from tkinter import messagebox, filedialog
import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker

# Definir las rutas de la base de datos y la carpeta de exportación
db_path = os.environ.get("DATABASE_PATH", "data/tasks.db")
export_folder = os.environ.get("EXPORT_FOLDER", "export")

# Aseguramos la creación de la carpeta "data" si no existe
if not os.path.exists("data"):
    os.makedirs("data")

# Configuración de la base de datos usando SQLAlchemy
Base = declarative_base()

class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    completed = Column(Boolean, default=False)

# Conexión a la base de datos SQLite
engine = create_engine(f'sqlite:///{db_path}')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

# Configuración de red usando configparser
config = configparser.ConfigParser()
config.read('config.ini')

if 'network' not in config:
    config['network'] = {'ipAddress': '127.0.0.1'}

with open('config.ini', 'w') as configfile:
    config.write(configfile)

ip = config.get('network', 'ipAddress')

TITLE_REQUIRED_MSG = "El título de la tarea es obligatorio."

# Función para obtener todas las tareas de la base de datos
def get_all_tasks():
    session = Session()
    tasks = session.query(Task).all()
    session.close()
    return tasks

# Función para mostrar todas las tareas en un formato tabular usando Pandas
def show_tasks():
    tasks = get_all_tasks()
    tasks_data = [{"ID": task.id, "Title": task.title, "Description": task.description, "Completed": task.completed} for task in tasks]
    df = pd.DataFrame(tasks_data)
    print(df)  # Mostrar el DataFrame en la consola
    return df

# Función para exportar las tareas a un archivo JSON
def export_tasks():
    if not os.path.exists(export_folder):
        os.makedirs(export_folder)
    
    file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")])
    if file_path:
        tasks = get_all_tasks()
        data = [{"id": t.id, "title": t.title, "description": t.description, "completed": t.completed} for t in tasks]
        try:
            with open(file_path, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4, ensure_ascii=False)
            messagebox.showinfo("Éxito", "Tareas exportadas con éxito.")
        except Exception as e:
            messagebox.showerror("Error", f"Error al exportar: {e}")

# Función para importar tareas desde un archivo JSON
def import_tasks():
    file_path = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
    if file_path:
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
                session = Session()
                for task_data in data:
                    new_task = Task(
                        id=task_data.get("id"),
                        title=task_data.get("title", "Sin título"),
                        description=task_data.get("description", ""),
                        completed=task_data.get("completed", False)
                    )
                    session.merge(new_task)
                session.commit()
                session.close()
                load_tasks()
                messagebox.showinfo("Éxito", "Tareas importadas con éxito.")
        except Exception as e:
            messagebox.showerror("Error", f"Error al importar archivo JSON: {e}")

# Interfaz gráfica de la aplicación
class TaskManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Manager App")
        self.session = Session()

        # Mostrar las tareas con Pandas
        tasks_df = show_tasks()
        messagebox.showinfo("Tareas", f"Tareas cargadas:\n{tasks_df}")

        header_frame = tk.Frame(root)
        header_frame.pack()

        tk.Label(header_frame, text="Descripción", width=50, borderwidth=2, relief="groove").grid(row=0, column=0)
        tk.Label(header_frame, text="Estado", width=50, borderwidth=2, relief="groove").grid(row=0, column=1)

        self.task_frame = tk.Frame(root)
        self.task_frame.pack()

        self.description_listbox = tk.Listbox(self.task_frame, width=50, height=20)
        self.description_listbox.grid(row=1, column=0)
        self.description_listbox.bind("<Double-1>", self.show_task_description)

        self.status_listbox = tk.Listbox(self.task_frame, width=50, height=20)
        self.status_listbox.grid(row=1, column=1)

        self.add_task_button = tk.Button(root, text="Agregar Tarea", command=self.add_task)
        self.add_task_button.pack()

        self.complete_task_button = tk.Button(root, text="Marcar como Completada", command=self.complete_task)
        self.complete_task_button.pack()

        self.delete_task_button = tk.Button(root, text="Eliminar Tarea", command=self.delete_task)
        self.delete_task_button.pack()

        self.export_button = tk.Button(root, text="Exportar Tareas", command=export_tasks)
        self.export_button.pack()

        self.import_button = tk.Button(root, text="Importar Tareas", command=import_tasks)
        self.import_button.pack()

        self.task_ids = []
        self.load_tasks()

    def load_tasks(self):
        tasks = get_all_tasks()  # Obtener todas las tareas desde la base de datos
        self.description_listbox.delete(0, tk.END)
        self.status_listbox.delete(0, tk.END)
        self.task_ids.clear()

        for task in tasks:
            status = "Completada" if task.completed else "Pendiente"
            self.description_listbox.insert(tk.END, task.description or "Sin descripción")
            self.status_listbox.insert(tk.END, status)
            self.task_ids.append(task.id)

    def add_task(self):
        add_window = tk.Toplevel(self.root)
        add_window.title("Agregar Tarea")

        title_label = tk.Label(add_window, text="Título de la tarea")
        title_label.pack()

        title_entry = tk.Entry(add_window)
        title_entry.pack()

        description_label = tk.Label(add_window, text="Descripción de la tarea")
        description_label.pack()

        description_entry = tk.Entry(add_window)
        description_entry.pack()

        add_button = tk.Button(add_window, text="Agregar", command=lambda: self.save_task(title_entry.get(), description_entry.get(), add_window))
        add_button.pack()

    def save_task(self, title, description, window):
        if not title.strip():
            messagebox.showerror("Error", TITLE_REQUIRED_MSG)
            return
        new_task = Task(title=title.strip(), description=description.strip())
        self.session.add(new_task)
        self.session.commit()
        window.destroy()
        self.load_tasks()

    def complete_task(self):
        selected_task = self.get_selected_task()
        if selected_task:
            selected_task.completed = True
            self.session.commit()
            self.load_tasks()

    def delete_task(self):
        selected_task = self.get_selected_task()
        if selected_task:
            response = messagebox.askyesno("Confirmar", "¿Estás seguro de que deseas eliminar esta tarea?")
            if response:
                self.session.delete(selected_task)
                self.session.commit()
                self.load_tasks()

    def get_selected_task(self):
        try:
            index = self.description_listbox.curselection()[0]
            task_id = self.task_ids[index]
            selected_task = self.session.query(Task).filter(Task.id == task_id).first()
            return selected_task
        except IndexError:
            messagebox.showerror("Error", "Por favor, selecciona una tarea.")
            return None

    def show_task_description(self, event):
        selected_task = self.get_selected_task()
        if selected_task:
            description_window = tk.Toplevel(self.root)
            description_window.title("Descripción de la Tarea")
            description_label = tk.Label(description_window, text=selected_task.description or "Sin descripción", wraplength=300)
            description_label.pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerApp(root)
    root.mainloop()
