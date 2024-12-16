# app/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.task_model import Base

# Definir la ruta de la base de datos (SQLite)
DATABASE_URL = "sqlite:///data/tasks.db"

# Crear la conexión a la base de datos SQLite
engine = create_engine(DATABASE_URL)

# Crear todas las tablas en la base de datos si no existen
Base.metadata.create_all(engine)

# Crear la sesión para interactuar con la base de datos
Session = sessionmaker(bind=engine)

# Función para obtener una sesión de base de datos
def get_session():
    return Session()
