# 📝 **Task Manager App**

## 📚 **Descripción**
**Task Manager App** es una aplicación en Python para gestionar tareas. Permite a los usuarios **agregar**, **completar**, **eliminar** y **visualizar** tareas a través de una interfaz gráfica amigable creada con **Tkinter**. Los datos se almacenan en una base de datos **SQLite**. Además, cuenta con funcionalidades para **exportar** e **importar** tareas en formato **JSON**.

🔧 **Tecnologías utilizadas**:
- **Python** 🐍
- **Tkinter** (para la interfaz gráfica) 💻
- **SQLite** (para la base de datos) 🗄️
- **Pandas** (para la visualización tabular de tareas) 📊

## 📊 **Captura de pantalla**
Aquí se muestra una captura de la aplicación en funcionamiento.

![SonarQube Screenshot](https://github.com/kantok32/Proyecto-1-tarea-python/blob/master/scanner%20sonarqude/Captura%20de%20pantalla%202024-12-16%20191611.png)

## 📊 **Interfaz grafica**
![SonarQube Screenshot](https://github.com/kantok32/Proyecto-1-tarea-python/blob/master/scanner%20sonarqude/interfaz%20completa.png)

![SonarQube Screenshot](https://github.com/kantok32/Proyecto-1-tarea-python/blob/master/scanner%20sonarqude/agregar%20tarea.png)

![SonarQube Screenshot](https://github.com/kantok32/Proyecto-1-tarea-python/blob/master/scanner%20sonarqude/seleccion%20de%20tarea%20y%20cambio.png)

![SonarQube Screenshot](https://github.com/kantok32/Proyecto-1-tarea-python/blob/master/scanner%20sonarqude/importacion.png)

## 🎯 **Funcionalidades**
- **➕ Agregar tareas**: Crear nuevas tareas con título y descripción.
- **✔️ Marcar tareas como completadas**: Cambiar el estado de la tarea a "Completada".
- **❌ Eliminar tareas**: Eliminar tareas de la base de datos.
- **💾 Exportar tareas**: Exportar todas las tareas a un archivo **JSON**.
- **📥 Importar tareas**: Cargar tareas desde un archivo **JSON**.

## 📦 **Requisitos**
Para ejecutar este proyecto, necesitas tener instalados los siguientes requisitos:

- **Python 3.6+**.
- **Bibliotecas necesarias**:
  - **SQLAlchemy**: Para gestionar la base de datos.
  - **Pandas**: Para mostrar las tareas en formato tabular.
  - **Tkinter**: Para crear la interfaz gráfica de la aplicación.

Puedes instalar las bibliotecas necesarias utilizando **pip**.

```bash
pip install sqlalchemy pandas tk
