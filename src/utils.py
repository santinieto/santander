from datetime import datetime
from faker import Faker
import random
import string
import os

import sys
sys.path.append('./src')

from db import get_student_asistance

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

def get_db_format_time():
    return datetime.now().strftime("%Y%m%dT%H:%M:%S")

############################################################################
# Funciones auxiliares
############################################################################
def get_formatted_date():
    """
    Obtiene la fecha actual en formato YYYYMMDD.

    Returns:
        str: Fecha actual en formato YYYYMMDD.
    """
    return datetime.now().strftime("%Y%m%d")

def transform_to_date(date):
    """
    Convierte una fecha del formato YYYYMMDD a DD/MM/YYYY.

    Args:
        date (int or str): Fecha en formato YYYYMMDD.

    Returns:
        str: Fecha en formato DD/MM/YYYY si la conversión es exitosa.
        '01/01/1980' si ocurre un error durante la conversión.
    """
    try:
        # Convierte la fecha de formato YYYYMMDD a un objeto datetime
        new_date = datetime.strptime(str(date), "%Y%m%d")
        # Formatea la fecha en el formato DD/MM/YYYY
        return new_date.strftime("%d/%m/%Y")
    except ValueError:
        # Si hay un error de valor, devuelve la fecha por defecto '01/01/1980'
        return '01/01/1980'

def generate_password(length=8):
    """
    Genera una contraseña aleatoria.

    Args:
        length (int): Longitud de la contraseña. Por defecto, 8 caracteres.

    Returns:
        str: Contraseña generada.
    """
    characters = string.ascii_letters + string.digits
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

def new_user(verbose=False):
    """
    Genera datos aleatorios para un nuevo usuario.

    Args:
        verbose (bool): Si es True, muestra los datos generados.

    Returns:
        dict: Datos generados para el nuevo usuario.
    """
    fake = Faker()

    # Generar un nombre aleatorio
    user_first_name = fake.first_name()

    # Generar un apellido aleatorio
    user_last_name = fake.last_name()
    
    # Generar el email
    user_email = '{}.{}@school.com'.format(user_first_name.lower(), user_last_name.lower())
    
    # Fuerzo la nacionalidad argentina
    user_nationalilty = 'arg'
    
    # Generar un número aleatorio para el DNI
    user_dni = random.randint(10000000, 90000000)
    
    # Generar una contraseña
    user_password = generate_password()

    # Mostrar los datos del estudiante
    if verbose:
        print("\t - Nombre:       ", user_first_name)
        print("\t - Apellido:     ", user_last_name)
        print("\t - Email:        ", user_email)
        print("\t - Nacionalidad: ", user_nationalilty)
        print("\t - DNI:          ", user_dni)
        print("\t - Contraseña:   ", user_password)
    
    # Datos del estudiante
    user_data = {
        "username": user_dni,
        "password": user_password,
        "first_name": user_first_name,
        "last_name": user_last_name,
        "nationality": user_nationalilty,
        "email": user_email
    }
    
    return user_data

def calc_student_asistance(student):
    """
    Calcula la asistencia de un estudiante.

    Args:
        student (str): Nombre de usuario del estudiante.

    Returns:
        tuple: Una tupla que contiene el número de días presentes,
        el número de días ausentes, el porcentaje de asistencias y
        una lista de fechas de ausencias.
    """
    data = get_student_asistance(student)
    absent_dates = [transform_to_date(row['date']) for row in data if row['present'] == 0]
    n_absent = len(absent_dates)
    n_prensent = len(data) - n_absent
    try:
        present_rate = round(n_prensent / len(data) * 100.0, 2)
    except:
        present_rate = 0
    return n_prensent, n_absent, present_rate, absent_dates

if __name__ == "__main__":
    new_user()