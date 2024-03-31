# Librerias necesarias
from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3
import random
from src.db import *
from src.open_meteo import *
from src.utils import *
from src.models import *

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
    
    # Verificar que existe la tabla de estudiantes
    fetch_students_table()
    
    # Agregar el alumno
    add_student(username, password, first_name, last_name, nationality, email)
    
    # Devuelvo el JSON
    return {"username": username, "password": password, "first_name": first_name, "last_name": last_name, "nationality": nationality, "email": email}

# Ver los datos de un estudiante
# http://localhost:8000/get_student?username=johndoe&password=123456
# http://localhost:8000/get_student?username=64606130&password=123456
# http://localhost:8000/get_student?username=64606130&password=%oFUHmJC
@app.get("/get_student/")
def get_student_data(username: str, password: str):
    
    # Verifico que el usuario existe en la base de datos
    student = get_student(username)
    
    # Verifico que la contraseña sea correcta
    if (student is None) or (student['password'] != password):
        return {"message": "Usuario o contraseña incorrectos"}
    
    else:
        return {
            "Usuario": student['username'],
            "Nombre": f"{student['first_name']} {student['last_name']}",
            "Nacionalidad": student['nationality'],
            "Correo electronico:": student['email'],
            }

# Veo la lista de estudiantes
@app.get("/view_students/")
def view_students():
    students = get_all_students()
    return [dict(student) for student in students]

# Registrar asistencia
@app.get("/register_asistance/")
def register_asistance():
    # Obtengo la fecha
    date = get_formatted_date()
    # Obtengo la informacion del clima
    temp = Temperature()
    temp.fetch_data()
    rain = temp.last_rain
    
    # Voy a suponer que los estudiantes de alguna forma
    # registraron su asistencia
    students_list = [row["username"] for row in get_all_students()]
    # Probabilidad de True (70%) y False (30%)
    probabilidades = [True, False]
    probabilidades_pesos = [0.7, 0.3]
    # Asignar True o False a cada nombre con las probabilidades dadas
    resultados = random.choices(probabilidades, weights=probabilidades_pesos, k=len(students_list))
    # Crear un diccionario con los nombres y sus valores asignados
    resultados_dict = dict(zip(students_list, resultados))
    
    # Verifico que existe la tabla de asistencia
    fetch_asistance_table()

    # Lista de alumnos presentes
    present_students = [nombre for nombre, valor in resultados_dict.items() if valor]
    # Registro la lista de presentes
    for username in present_students:
        register_student_asistance(date, username, 1)
    
    # Lista de alumnos ausentes
    absent_students = [nombre for nombre, valor in resultados_dict.items() if not valor]
    # Registro la lista de ausentes
    for username in present_students:
        register_student_asistance(date, username, 0)
    
    # Devuelvo los datos
    return {"date": date, "rain": rain, "present_students": present_students, "absent_students": absent_students}