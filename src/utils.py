from datetime import datetime
from faker import Faker
import random
import string

import sys
sys.path.append('./src')

from db import get_student_asistance

# Obtener la fecha y hora actual
def get_formatted_date():
    return datetime.now().date().strftime("%Y%m%d")

# Función para convertir formato YYYYMMDD a DD/MM/YYYY
def transform_to_date(date):
    # Convierte la fecha de formato YYYYMMDD a un objeto datetime
    new_date = datetime.strptime(str(date), "%Y%m%d")
    # Formatea la fecha en el formato DD/MM/YYYY
    new_date = new_date.strftime("%d/%m/%Y")
    return new_date

# Generador de contrasenias
def generate_password(length=8):
    """Genera una contraseña aleatoria."""
    characters = string.ascii_letters + string.digits
    password = ''.join(random.choice(characters) for i in range(length))
    return password

# Genero un alumno aleatorio
def new_user():
    fake = Faker()

    # Generar un nombre aleatorio
    user_first_name = fake.first_name()

    # Generar un apellido aleatorio
    user_last_name = fake.last_name()
    
    # Genero el email
    user_email = '{}.{}@school.com'.format(user_first_name.lower(), user_last_name.lower())
    
    # Fuerzo la nacionalidad argentina
    user_nationalilty = 'arg'
    
    # Generar un número aleatorio para el DNI
    user_dni = random.randint(10000000, 90000000)
    
    # Genero una contrasenia
    user_password = generate_password()

    # Muestro los datos del estudiante
    print("Nombre:", user_first_name)
    print("Apellido:", user_last_name)
    print("Email:", user_email)
    print('Nacionalidad:', user_nationalilty)
    print("DNI:", user_dni)
    print("Contrasenia:", user_password)
    
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
    data = get_student_asistance(student)
    absent_dates = [transform_to_date(row['date']) for row in data if row['present'] == 0]
    n_absent = len(absent_dates)
    n_prensent = len(data) - n_absent
    present_rate = n_prensent / len(data) * 100.0
    return n_prensent, n_absent, present_rate, absent_dates

if __name__ == "__main__":
    new_user()