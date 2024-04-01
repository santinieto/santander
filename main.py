# Librerias necesarias
from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3
import random
import os
from src.db import *
from src.open_meteo import *
from src.utils import *
from src.models import *

# Creación de la aplicación FastAPI
app = FastAPI()

# Para ejecutar el servidor
# uvicorn main:app --reload

# Variables globables
os.environ["USER_AUTHENTICATED"] = 'False'
os.environ["USER_USERNAME"] = ''
os.environ["USER_ROLE"] = ''

############################################################################
# Ruta de sanidad
############################################################################
@app.get("/")
def read_root():
    return {"Hello": "World"}

############################################################################
# Ruta de logeo
############################################################################
# http://localhost:8000/login?username=1234&password=1234
# http://localhost:8000/login?username=38846700&password=ARLhIkRd
# http://localhost:8000/login?username=15947788&password=HKwN5U1N
@app.get("/login/")
def login(username: str, password: str):
    
    # Si ya hay una sesion iniciada primero hay que cerrarla:
    if os.environ["USER_AUTHENTICATED"] == 'True':
        return {'message', 'Ya hay una sesion iniciada. Debe cerrarla para poder ingresar a otra cuenta'}
    
    # Verifico si es un estudiante
    if is_valid_student(username, password) is True:
        os.environ["USER_AUTHENTICATED"] = 'True'
        os.environ["USER_USERNAME"] = username
        os.environ["USER_ROLE"] = 'student'
        return{'message': f'Bienvenido estudiante {os.environ["USER_USERNAME"]}'}
        
    if is_valid_teacher(username, password) is True:
        os.environ["USER_AUTHENTICATED"] = 'True'
        os.environ["USER_USERNAME"] = username
        os.environ["USER_ROLE"] = 'teacher'
        return{'message': f'Bienvenido profesor {os.environ["USER_USERNAME"]}'}
        
    return{'message': 'Usuario o contraseña incorrectos'}

@app.get("/logoff/")
def login():
    if os.environ["USER_AUTHENTICATED"] == 'False':
        return {'message': 'No se ha iniciado sesion'}
    else:
        os.environ["USER_AUTHENTICATED"] = 'False'
        os.environ["USER_USERNAME"] = ''
        os.environ["USER_ROLE"] = ''
        return {'message': 'Se ha cerrado la sesion'}

############################################################################
# Gestion de estudiantes
############################################################################
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
# http://localhost:8000/get_student?username=38846700
@app.get("/get_student/")
def get_student_data(username: str):
    
    # Verifico si el usuario puede ver la informacion
    valid = False
    if os.environ["USER_AUTHENTICATED"] is False:
        return {"message": "Debe iniciar sesion para acceder a los datos"}
    if os.environ["USER_ROLE"] in ['teacher', 'tutor']:
        valid = True
    if os.environ["USER_ROLE"] == 'student' and os.environ["USER_USERNAME"] == username:
        valid = True
        
    if valid is False:
        return {"message": "Acceso denegado"}

    # Verifico que el usuario existe en la base de datos
    student = get_student(username)
    
    n_prensent, n_absent, present_rate, absent_dates = calc_student_asistance(username)
    
    # Verifico que la contraseña sea correcta
    if student is None:
        return {"message": "Estudiante no encontrado"}
    
    else:
        return {
            "Usuario": student['username'],
            "Nombre": f"{student['first_name']} {student['last_name']}",
            "Nacionalidad": student['nationality'],
            "Correo electronico:": student['email'],
            "Cantidad de dias presentes": n_prensent,
            "Cantidad de asusencias": n_absent,
            "Porcentaje de asistencias": present_rate,
            "Fechas de ausencias": absent_dates,
            }

# Veo la lista de estudiantes
@app.get("/view_students/")
def view_students():
    
    # Verifico si el usuario puede ver la informacion
    if os.environ["USER_AUTHENTICATED"] is False:
        return {"message": "Debe iniciar sesion para acceder a los datos"}
    
    students = get_all_students()
    
    students_list = []
    for student in students:
        student = dict(student)
        n_prensent, n_absent, present_rate, absent_dates = calc_student_asistance(student['username'])
        student['n_prensent'] = n_prensent
        student['n_absent'] = n_absent
        student['present_rate'] = present_rate
        student['absent_dates'] = absent_dates
        students_list.append( student )
        
    return students_list

# Registrar asistencia
@app.get("/register_asistance/")
def register_asistance():
    
    # Verifico si el usuario puede ver la informacion
    if os.environ["USER_AUTHENTICATED"] is False:
        return {"message": "Debe iniciar sesion para acceder a los datos"}
    if os.environ["USER_ROLE"] in ['student']:
        return {"message": "El registro de asistencia solo puede ser realizado por profesores o preceptores"}
    
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
        register_student_asistance(date, username, 1, '-')
    
    # Lista de alumnos ausentes
    absent_students = [nombre for nombre, valor in resultados_dict.items() if not valor]
    justificacion = '-'
    if rain:
        justificacion = 'Dia lluvioso'
    # Registro la lista de ausentes
    for username in present_students:
        register_student_asistance(date, username, 0, justificacion)
    
    # Devuelvo los datos
    return {"date": date, "rain": rain, "present_students": present_students, "absent_students": absent_students}

# Ver los datos de un estudiante
# http://localhost:8000/justify_absent?username=29186424&date=20240331&justificacion=1
# http://localhost:8000/justify_absent?username=29186424&date=20240331&justificacion=2
# http://localhost:8000/justify_absent?username=29186424&date=20240331&justificacion=3
# http://localhost:8000/justify_absent?username=29186424&date=20240331&justificacion=Other-reason
@app.get("/justify_absent/")
def justify_absent(username: str, date: str, justificacion: str):
    
    if justificacion == "1":
        just_txt = 'Enfermedad'
    elif justificacion == '2':
        just_txt = 'Tramite personal'
    elif justificacion == '3':
        just_txt = 'Consulta medica'
    else:
        just_txt = justificacion.replace('-',' ')
        
    result = set_abset_justification(username, date, just_txt)
    
    if result is True:
        return {"message": "Actualizacion exitosa"}
    else:
        return {"message": "Se produjo un error al actualizar los datos"}
    
############################################################################
# Gestion de profesores
############################################################################
# Agrego un estudiante
@app.post("/add_teacher/")
def create_teacher(student: Student):
    # Obtener los datos del estudiante del modelo Pydantic
    username = student.username
    password = student.password
    first_name = student.first_name
    last_name = student.last_name
    nationality = student.nationality
    email = student.email
    
    # Verificar que existe la tabla de estudiantes
    fetch_teachers_table()
    
    # Agregar el alumno
    add_teacher(username, password, first_name, last_name, nationality, email)
    
    # Devuelvo el JSON
    return {"username": username, "password": password, "first_name": first_name, "last_name": last_name, "nationality": nationality, "email": email}
