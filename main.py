# Librerias necesarias
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
import sqlite3
import random
import os
from datetime import datetime
import src.db as db
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
os.environ["USER_LOG_TIME"] = ''

############################################################################
# Funciones de control
############################################################################
def is_authenticated():
    if os.environ["USER_AUTHENTICATED"] == 'True':
        return True
    return False

def set_user_authenticated(username, role):
    os.environ["USER_AUTHENTICATED"] = 'True'
    os.environ["USER_USERNAME"] = username
    os.environ["USER_ROLE"] = role
    os.environ["USER_LOG_TIME"] = datetime.now().strftime("%Y%m%dT%H:%M:%S")
    
def get_user_role():
    return os.environ["USER_ROLE"]

def get_user_name():
    return os.environ["USER_USERNAME"]

def get_log_time():
    return os.environ["USER_LOG_TIME"]

############################################################################
# Ruta de sanidad
############################################################################
@app.get("/")
def read_root():
    return {"message": "Bienvenido al sistema de asistencia de la escuela rural."}

@app.get("/my_profile/")
def my_profile():
    
    if is_authenticated() is False:
        return {"message": "Debe iniciar sesion para acceder a los datos."}
    
    return {
        'username': get_user_name(),
        'role': get_user_role(),
        'log_time': get_log_time(),
    }

############################################################################
# Rutas de logeo
############################################################################
@app.get("/login/")
def login(username: str, password: str):
    """
    Inicia sesión de un usuario con las credenciales proporcionadas.

    Args:
        username (str): Nombre de usuario.
        password (str): Contraseña del usuario.

    Returns:
        dict: Un mensaje de bienvenida si las credenciales son válidas,
        o un mensaje de error si las credenciales son incorrectas o ya hay una sesión iniciada.
        
    Uso:
        http://localhost:8000/login?username=<username>&password=<password>
    """
    
    # Verificar si ya hay una sesión iniciada
    if is_authenticated():
        return {'message': 'Ya hay una sesión iniciada. Debe cerrarla para poder iniciar sesión en otra cuenta'}
    
    # Checko de inicio de sesion como administrador
    if username == 'admin' and password == 'admin':
        set_user_authenticated(username, 'admin')
        return {'message': f'Se ha iniciado sesion como administrador'}
    
    # Verificar las credenciales del estudiante
    if db.is_valid_student(username, password):
        set_user_authenticated(username, 'student')
        return {'message': f'Bienvenido estudiante {username}'}
    
    # Verificar las credenciales del profesor
    if db.is_valid_teacher(username, password):
        set_user_authenticated(username, 'teacher')
        return {'message': f'Bienvenido profesor {username}'}
    
    # Si las credenciales no son válidas
    return {'message': 'Usuario o contraseña incorrectos'}

@app.get("/logoff/")
def logoff():
    """
    Cierra la sesión del usuario actual.

    Returns:
        dict: Un mensaje indicando que la sesión se ha cerrado correctamente,
        o un mensaje de error si no hay una sesión iniciada.
        
    Uso:
        http://localhost:8000/logoff/
    """
    if is_authenticated():
        os.environ["USER_AUTHENTICATED"] = ''
        os.environ["USER_USERNAME"] = ''
        os.environ["USER_ROLE"] = ''
        return {'message': 'Se ha cerrado la sesión'}
    return {'message': 'No se ha iniciado sesión'}

############################################################################
# Gestion de estudiantes
############################################################################
@app.post("/add_student/")
def create_student(student: Student):
    """
    Agrega un estudiante a la base de datos.

    Args:
        student (Student): Datos del estudiante a agregar.

    Returns:
        dict: Datos del estudiante agregado.
    """
        
    # Obtener los datos del estudiante del modelo Pydantic
    username = student.username
    password = student.password
    first_name = student.first_name
    last_name = student.last_name
    nationality = student.nationality
    email = student.email
    
    # Verificar si el usuario actual es profesor o administrador
    if get_user_role() not in ['teacher', 'admin']:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Solo los profesores o administradores pueden agregar estudiantes.")

    try:
        # Verificar que existe la tabla de estudiantes
        db.fetch_students_table()
        
        # Agregar el alumno
        response = db.add_student(username, password, first_name, last_name, nationality, email)
        
        # Devuelvo el JSON
        return response
    
    except Exception as e:
        return {'message': f'Se produjo un error al crear el estudiante. Error: {e}'}

@app.get("/update_student/")
def update_student(username: str, password: str = None, first_name: str = None, last_name: str = None, nationality: str = None, email: str = None):
    """
    Actualiza los datos personales de un estudiante en la base de datos.

    Args:
        username (str): Nombre de usuario del estudiante.
        new_data (dict): Datos nuevos a actualizar.

    Returns:
        dict: Mensaje de éxito o error.
    """
    
    try:
    
        # Verificar si el usuario actual es profesor o administrador
        if is_authenticated() is False:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Debe iniciar sesion para modificar los datos.")
        if get_user_role() in ['teacher']:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Los profesores no tienen acceso para modificar los datos de alumnos.")
        
        # Obtener los datos actuales del alumno
        student = db.get_student(username)
        
        # Obtener los datos del estudiante del modelo Pydantic
        password = password if password is not None else student['password']
        first_name = first_name if first_name is not None else student['first_name']
        last_name = last_name if last_name is not None else student['last_name']
        nationality = nationality if nationality is not None else student['nationality']
        email = email if email is not None else student['email']
        
        db.update_student(username, password, first_name, last_name, nationality, email)
        return {"message": "Datos actualizados exitosamente"}

    except Exception as e:
        return {"message": f"Error al actualizar los datos: {e}"}

@app.get("/get_student/")
def get_student_data(username: str):
    """
    Obtiene los datos de un estudiante específico de la base de datos.

    Args:
        username (str): Nombre de usuario del estudiante.

    Returns:
        dict: Datos del estudiante si se encuentra en la base de datos.
        Mensaje de error si el estudiante no se encuentra o si el acceso está denegado.
        
    Uso:
        http://localhost:8000/get_student?username=<username>
    """
    
    # Verifico si el usuario puede ver la informacion
    if is_authenticated() is False:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Debe iniciar sesion para acceder a los datos.")
    if get_user_role() != 'admin' and get_user_role() == 'student' and get_user_name() != username:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acceso denegado.")

    try:
        # Obtener los datos del estudiante de la base de datos
        student = db.get_student(username)
        if student is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Estudiante no encontrado")
        
        # Obtener la asistencia del estudiante
        n_present, n_absent, present_rate, absent_dates = calc_student_asistance(username)

        # Presentar los datos del estudiante en el formato deseado
        return {
            "username": student['username'],
            "name": f"{student['first_name']} {student['last_name']}",
            "nationality": student['nationality'],
            "email": student['email'],
            "n_present" : n_present,
            "n_absent" : n_absent,
            "present_rate" : present_rate,
            "absent_dates" : absent_dates,
        }
    except Exception as e:
        return {"message": f"Error al obtener los datos del estudiante: {e}"}

@app.get("/view_students/")
def view_students():
    """
    Obtiene la lista de estudiantes y sus datos de asistencia.

    Returns:
        list: Lista de diccionarios que contienen los datos de los estudiantes y su asistencia.
    """
    # Verificar si el usuario está autenticado
    if not is_authenticated():
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Debe iniciar sesión para acceder a los datos.")
    
    students = db.get_all_students()
    
    students_list = []
    for student in students:
        student_data = dict(student)
        n_present, n_absent, present_rate, absent_dates = calc_student_asistance(student_data['username'])
        student_data['n_present'] = n_present
        student_data['n_absent'] = n_absent
        student_data['present_rate'] = present_rate
        student_data['absent_dates'] = absent_dates
        students_list.append(student_data)
        
    return students_list

@app.get("/register_asistance/")
def register_asistance(username: str, date: str = None):
    """
    Registra la asistencia de un estudiante en una fecha especificada.

    Args:
        username (str): Nombre de usuario del estudiante.
        date (str, optional): Fecha en formato YYYYMMDD. Si no se proporciona, se usa la fecha actual.

    Returns:
        dict: Respuesta con la fecha y el nombre de usuario del estudiante registrado.

    NOTA:
        Para este caso estoy suponiendo que el preceptor o profesor esta obteniendo el DNI del estudiante
        de alguna manera (QR, escanedo de DNI, dictado, etc.). Entiendo que la forma en la que se obtiene
        este dato escapa al contexto de esta actividad.
    """
    
    # Verificar si el usuario está autenticado
    if not is_authenticated():
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Debe iniciar sesión para acceder a los datos.")
    
    # Verificar si el usuario tiene permisos para registrar asistencia
    if get_user_role() == 'student':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="El registro de asistencia solo puede ser realizado por profesores o preceptores.")
    
    # Obtener la fecha de la base de datos
    date = fetch_date_in_db(date)
    
    # Registrar la asistencia del estudiante como presente
    db.register_student_asistance(date, username, 1, '-')
    
    return {"date": date, "username": username}

def fetch_date_in_db(target_date=None):
    """
    Verifica si existe una fecha en la base de datos y la registra si no está presente.
    Se verifica el estado del clima para autojustificar la asistencia del estudiante.

    Args:
        target_date (str, optional): Fecha en formato YYYYMMDD. Si no se proporciona, se usa la fecha actual.

    Returns:
        str: Fecha registrada en la base de datos.
    """
    
    # Obtener la fecha del sistema
    sys_date = get_formatted_date()
    
    # Utilizar la fecha actual si no se proporciona una fecha específica
    if target_date is None:
        target_date = sys_date

    # Verificar si la fecha ya está en la base de datos
    is_date_loaded = db.is_valid_date(target_date)
    
    # Si la fecha ya está en la base de datos, no se hace nada más
    if is_date_loaded:
        return target_date
        
    # Obtener datos meteorológicos si la fecha es la fecha actual
    if target_date == sys_date:
        temp = Temperature()
        temp.fetch_data()
        rain = temp.last_rain
    else:
        rain = False
        
    # Establecer justificación en caso de lluvia
    if rain:
        justification = 'Dia lluvioso'
    else:
        justification = '-'
        
    # Obtener la lista de estudiantes
    students_list = [row["username"] for row in db.get_all_students()]
    
    # Verificar que existe la tabla de asistencia
    db.fetch_asistance_table()
    
    # Registrar la lista de estudiantes como ausentes
    for student in students_list:
        db.register_student_asistance(target_date, student, 0, justification)

    return target_date

@app.get("/justify_absent/")
def justify_absent(username: str, date: str = None, justificacion: str = 'Other-reason'):
    """
    Actualiza la justificación de una ausencia para un estudiante en una fecha específica.

    Args:
        username (str): Nombre de usuario del estudiante.
        date (str, opcional): Fecha en formato YYYYMMDD.
        justificacion (str, opcional): Código o descripción de la justificación.

    Returns:
        dict: Mensaje de éxito o error.
        
    Usos:
        http://localhost:8000/justify_absent?username=<username>&date=<date>&justificacion=1
        http://localhost:8000/justify_absent?username=<username>&date=<date>&justificacion=2
        http://localhost:8000/justify_absent?username=<username>&date=<date>&justificacion=3
        http://localhost:8000/justify_absent?username=<username>&date=<date>&justificacion=Other-reason
    """
    
    # Verificar si el usuario está autenticado
    if not is_authenticated():
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Debe iniciar sesión para modificar datos de asistencia.")
    
    # Verificar si el usuario tiene permisos para registrar asistencia
    if get_user_role() == 'student':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="El registro de asistencia solo puede ser modificado por profesores o preceptores.")
    
    try:
        justification_map = {
            "1": "Enfermedad",
            "2": "Trámite personal",
            "3": "Consulta médica"
        }
    
        # Utilizar la fecha actual si no se proporciona una fecha específica
        if date is None:
            date = get_formatted_date()
        
        # Obtener la justificación correspondiente
        just_txt = justification_map.get(justificacion, justificacion.replace('-', ' '))
        
        # Actualizar la justificación en la base de datos
        result = db.set_abset_justification(username, date, just_txt)
        
        if result:
            return {"message": "Actualización exitosa"}
        else:
            return {"message": "Se produjo un error al actualizar los datos"}
    except Exception as e:
        return {"message": f"Error al actualizar los datos: {e}"}
    
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
    db.fetch_teachers_table()
    
    # Agregar el alumno
    db.add_teacher(username, password, first_name, last_name, nationality, email)
    
    # Devuelvo el JSON
    return {"username": username, "password": password, "first_name": first_name, "last_name": last_name, "nationality": nationality, "email": email}
