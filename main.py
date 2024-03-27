# Librerias necesarias
from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3
from db import *
from open_meteo import *
from utils import *
from models import *

# Creación de la aplicación FastAPI
app = FastAPI()

# Para ejecutar el servidor
# uvicorn main:app --reload

# Rutas de FastAPI
@app.get("/")
def read_root():
    return {"Hello": "World"}

# Agrego un estudiante
@app.post("/add_student/")
def create_student(student: Student):
    # Obtener los datos del estudiante del modelo Pydantic
    username = student.username
    password = student.password
    first_name = student.first_name
    last_name = student.last_name
    nationality = student.nationality
    email = student.email
    
    # Abro la conexion con la vase de datos
    conn = db_open()
    cursor = conn.cursor()
    
    # Verificar que existe la tabla de estudiantes
    fetch_students_table()
    
    # Agregar el alumno
    cursor.execute(
        "INSERT INTO students (username, password, first_name, last_name, nationality, email) VALUES (?, ?, ?, ?, ?, ?)",
        (username, password, first_name, last_name, nationality, email)
    )
    
    # Guardo los cambios y cierro la conexion
    conn.commit()
    conn.close()
    
    # Devuelvo el JSON
    return {"username": username, "password": password, "first_name": first_name, "last_name": last_name, "nationality": nationality, "email": email}

# Ver los datos de un estudiante
@app.get("/get_student/")
def get_student_data():
    student = get_student(39374486)
    return student

# Veo la lista de estudiantes
@app.get("/students/")
def get_all_students():
    conn = db_open()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    conn.close()
    return [dict(student) for student in students]

# Agrego la informacion de una fecha
@app.get('/add_date/')
def add_date():
    # Obtengo la fecha
    date = get_formatted_date()
    # Obtengo la informacion del clima
    temp = Temperature()
    temp.fetch_data()
    rain = temp.last_rain
    # Lista de alumnos presentes
    present_students = []
    # Lista de alumnos ausentes
    absent_students = []
    # Devuelvo los datos
    return {"date": date, "rain": rain, "present_students": present_students, "absent_students": absent_students}