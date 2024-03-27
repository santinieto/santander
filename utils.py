from datetime import datetime
from faker import Faker
import random
import string

# Obtener la fecha y hora actual
def get_formatted_date():
    return datetime.now().date().strftime("%Y%m%d")

# Generador de contrasenias
def generate_password(length=8):
    """Genera una contraseña aleatoria."""
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for i in range(length))
    return password

# Genero un alumno aleatorio
def create_student():
    fake = Faker()

    # Generar un nombre aleatorio
    student_first_name = fake.first_name()

    # Generar un apellido aleatorio
    student_last_name = fake.last_name()
    
    # Genero el email
    student_email = '{}.{}@school.com'.format(student_first_name.lower(), student_last_name.lower())
    
    # Fuerzo la nacionalidad argentina
    student_nationalilty = 'arg'
    
    # Generar un número aleatorio para el DNI
    student_dni = random.randint(10000000, 90000000)
    
    # Genero una contrasenia
    student_password = generate_password()

    # Muestro los datos del estudiante
    print("Nombre:", student_first_name)
    print("Apellido:", student_last_name)
    print("Email:", student_email)
    print('Nacionalidad:', student_nationalilty)
    print("DNI:", student_dni)
    print("Contrasenia:", student_password)
    
    # Datos del estudiante
    student_data = {
        "username": student_dni,
        "password": student_password,
        "first_name": student_first_name,
        "last_name": student_last_name,
        "nationality": student_nationalilty,
        "email": student_email
    }
    
    return student_data
    
if __name__ == "__main__":
    create_student()