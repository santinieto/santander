# Librerias necesarias
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
import sqlite3
import random
from datetime import datetime
import json
import src.db as db
from src.open_meteo import *
from src.utils import *
from src.models import *
from src.scrap import *

# Creación de la aplicación FastAPI
app = FastAPI()

# Para ejecutar el servidor
# uvicorn main:app --reload

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
    
    if get_user_role() == "admin":
        dicc = {}
        dicc['username'] = get_user_name()
        dicc['role'] = get_user_role()
        dicc['log_time'] = get_log_time()
        return dicc
    
    if get_user_role() == "student":
        data = db.get_student(get_user_name())
        
        # Si el alumno se encuentra inahiliatdo no puede ver sus datos
        if str(data['active']) == '0':
            return {"message": "Alumno inhabilitado. No se pueden mostrar los datos. Contacte a su profesor."}
        
        dicc = {}
        dicc['username'] = get_user_name()
        dicc['role'] = get_user_role()
        dicc['log_time'] = get_log_time()
        dicc['first_name'] = data['first_name']
        dicc['last_name'] = data['last_name']
        dicc['email'] = data['email']
        dicc['nationality'] = data['nationality']
        dicc['active'] = data['active']
    
    if get_user_role() == "teacher":
        data = db.get_teacher(get_user_name())
        dicc = {}
        dicc['username'] = get_user_name()
        dicc['role'] = get_user_role()
        dicc['log_time'] = get_log_time()
        dicc['first_name'] = data['first_name']
        dicc['last_name'] = data['last_name']
        dicc['email'] = data['email']
        dicc['nationality'] = data['nationality']
    
    if get_user_role() == "tutor":
        data = db.get_tutor(get_user_name())
        dicc = {}
        dicc['username'] = get_user_name()
        dicc['role'] = get_user_role()
        dicc['log_time'] = get_log_time()
        dicc['first_name'] = data['first_name']
        dicc['last_name'] = data['last_name']
        dicc['email'] = data['email']
        dicc['nationality'] = data['nationality']

    return dicc

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
    
    # Verificar las credenciales del preceptor
    if db.is_valid_tutor(username, password):
        set_user_authenticated(username, 'tutor')
        return {'message': f'Bienvenido preceptor {username}'}
    
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
        close_session()
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
    active = student.active
    
    # Verificar si el usuario actual es profesor o administrador
    if get_user_role() not in ['tutor', 'admin']:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Solo los profesores o administradores pueden agregar estudiantes.")

    try:
        # Verificar que existe la tabla de estudiantes
        db.fetch_students_table()
        
        # Agregar el alumno
        response = db.add_student(username, password, first_name, last_name, nationality, email, active)
        
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
        if get_user_role() == 'student' and get_user_name() != username:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acceso denegado.")
        
        # Obtener los datos actuales del alumno
        student = db.get_student(username)
        
        if str(student['active']) == '0' and get_user_name() == username:
            return {"message": "Alumno inhabilitado. No se pueden modificar los datos. Contacte a su profesor."}
        
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

@app.get("/set_student_status/")
def set_student_status(username: str, status: str):
    """
    """
    
    # Verifico si el usuario puede ver la informacion
    if is_authenticated() is False:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Debe iniciar sesion para acceder a los datos.")
    if get_user_role() in ['student', 'teacher']:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acceso denegado.")
    
    message = db.set_student_status(username, status)
    
    return {'message': message}

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
    if get_user_role() == 'student' and get_user_name() != username:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acceso denegado.")

    try:
        # Obtener los datos del estudiante de la base de datos
        student = db.get_student(username)
        if student is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Estudiante no encontrado")
        
        if str(student['active']) == '0' and get_user_name() == username:
            return {"message": "Alumno inhabilitado. No se pueden visualizar los datos. Contacte a su profesor."}
        
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
    if get_user_role() == 'student':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acceso denegado.")
    
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
def register_asistance(username: str, date: str = None, present: str = '1', justification: str = '-'):
    """
    Registra la asistencia de un estudiante en una fecha especificada.

    Args:
        username (str): Nombre de usuario del estudiante.
        date (str, optional): Fecha en formato YYYYMMDD. Si no se proporciona, se usa la fecha actual.
        present (str, optional): Presente o ausente, por defecto presente.
        justification (str, optional): Justificacion de ausencia si fuera requerido.

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
    date, rain = fetch_date_in_db(date)
    
    # Registrar la asistencia del estudiante como presente
    if rain is not None:
        db.register_student_asistance(date, username, present, justification, rain)
    else:
        db.register_student_asistance(date, username, present, justification)
    
    return {"message": f"Se ha cargado la asistencia del alumno {username}"}

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
        return target_date, None
        
    # Obtener datos meteorológicos si la fecha es la fecha actual
    if target_date == sys_date:
        temp = Temperature()
        temp.fetch_data()
        rain = temp.last_rain
    else:
        rain = False
        
    # Si la obtencion de temperatura falla, obtengo los datos desde Google
    try:
        page = getHTTPResponse("https://www.google.com/search?q=clima", responseType='page')
        temp_txt = page.find('span', class_='wob_t q8U8x').text
        weather_txt = page.find('div', class_='wob_dcp').text
    except:
        pass
    
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
        db.register_student_asistance(target_date, student, 0, justification, int(rain))

    return target_date, int(rain)

@app.get('/view_daily_report/')
def view_daily_report(date = None):
    
    # Verificar si el usuario está autenticado
    if not is_authenticated():
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Debe iniciar sesión para ver los datos de asistencia.")
    
    # Verificar si el usuario tiene permisos para registrar asistencia
    if get_user_role() == 'student':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="El registro de asistencia solo puede ser visualizado por profesores o preceptores.")
    
    # Utilizar la fecha actual si no se proporciona una fecha específica
    if date is None:
        date = get_formatted_date()
        
    # Obtengo los datos de los estudiantes:
    try:
        data = db.get_asistance_data(date)
        
        students_present = [row['username'] for row in data if row['present'] == 1]
        students_absent = [row['username'] for row in data if row['present'] == 0]
        
        n_present = len( students_present )
        n_absent = len( students_absent )
        
        try:
            asistance = round( n_present / len(data) * 100, 2)
        except:
            asistance = 0
            
        stats = {
                'date': date,
                'rain': data[0]['rain'],
                'n_present': n_present,
                'n_absent': n_absent,
                'students_present': students_present,
                'students_absent': students_absent,
                'asistance': asistance
            }
            
        #  Guardo el reporte diario en un archivo tipo JSON
        filename = f'./results/daily_report_{date}.json'
        with open(filename, "w") as archivo:
            # Escribe el diccionario en el archivo como JSON
            json.dump(stats, archivo)
        
        return stats
    except:
        
        return {
            'date': date,
            'rain': 'Error',
            'n_present': '0',
            'n_absent': '0',
            'students_present': [],
            'students_absent': [],
            'asistance': '0'
        }

@app.get("/edit_asistance/")
def edit_asistance(username: str, present: str, justification: str, date: str):
    
    # Verificar si el usuario está autenticado
    if not is_authenticated():
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Debe iniciar sesión para modificar la asistencia.")
    
    # Verificar si el usuario tiene permisos para registrar asistencia
    if get_user_role() == 'student':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="El registro de asistencia solo puede ser modificado por profesores o preceptores.")
    
    # Registrar la asistencia del estudiante como presente
    response = db.register_student_asistance(date, username, present, justification)

    return {'mesage': response}

@app.get("/justify_absent/")
def justify_absent(username: str, date: str = None, justification: str = 'Other-reason'):
    """
    Actualiza la justificación de una ausencia para un estudiante en una fecha específica.

    Args:
        username (str): Nombre de usuario del estudiante.
        date (str, opcional): Fecha en formato YYYYMMDD.
        justification (str, opcional): Código o descripción de la justificación.

    Returns:
        dict: Mensaje de éxito o error.
        
    Usos:
        http://localhost:8000/justify_absent?username=<username>&date=<date>&justification=1
        http://localhost:8000/justify_absent?username=<username>&date=<date>&justification=2
        http://localhost:8000/justify_absent?username=<username>&date=<date>&justification=3
        http://localhost:8000/justify_absent?username=<username>&date=<date>&justification=Other-reason
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
        just_txt = justification_map.get(justification, justification.replace('-', ' '))
        
        # Actualizar la justificación en la base de datos
        result = db.set_abset_justification(username, date, just_txt)
        
        if result:
            return {"message": f"Actualización exitosa. Se justifico la asistencia del dia {date} para el alumno {username} con motivo {just_txt}"}
        else:
            return {"message": "Se produjo un error al actualizar los datos"}
    except Exception as e:
        return {"message": f"Error al actualizar los datos: {e}"}
    
############################################################################
# Gestion de profesores
############################################################################
@app.post("/add_teacher/")
def create_teacher(teacher: Teacher):
    # Obtener los datos del estudiante del modelo Pydantic
    username = teacher.username
    password = teacher.password
    first_name = teacher.first_name
    last_name = teacher.last_name
    nationality = teacher.nationality
    email = teacher.email
    
    # Verificar si el usuario está autenticado
    if not is_authenticated():
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Debe iniciar sesión para crear profesores.")
    
    # Verificar si el usuario tiene permisos para registrar asistencia
    if get_user_role() != 'admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Solo el administrador puede crear profesores.")
    
    # Verificar que existe la tabla de estudiantes
    db.fetch_teachers_table()
    
    # Agregar el alumno
    response = db.add_teacher(username, password, first_name, last_name, nationality, email)
    
    # Devuelvo el JSON
    return response

############################################################################
# Gestion de preceptores
############################################################################
@app.post("/add_tutor/")
def create_teacher(tutor: Tutor):
    # Obtener los datos del estudiante del modelo Pydantic
    username = tutor.username
    password = tutor.password
    first_name = tutor.first_name
    last_name = tutor.last_name
    nationality = tutor.nationality
    email = tutor.email
    
    # Verificar si el usuario está autenticado
    if not is_authenticated():
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Debe iniciar sesión para crear preceptores.")
    
    # Verificar si el usuario tiene permisos para registrar asistencia
    if get_user_role() != 'admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Solo el administrador puede crear preceptores.")
    
    # Verificar que existe la tabla de estudiantes
    db.fetch_tutors_table()
    
    # Agregar el alumno
    response = db.add_tutor(username, password, first_name, last_name, nationality, email)
    
    # Devuelvo el JSON
    return response
