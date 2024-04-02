import sqlite3
from src.utils import *
import csv

# Variables globables
# Se supone que esto se ejecuta desde el main.py
DB_NAME = './database/escuela.db'

# Función para conectar a la base de datos SQLite
def db_open():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

# Borrar datos anteriores
def clean_database():
    try:
        conn = db_open()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM students")
        cursor.execute("DELETE FROM teachers")
        cursor.execute("DELETE FROM tutors")
        cursor.execute("DELETE FROM asistance")
        conn.commit()
        conn.close()
    except:
        pass

# Función para crear la tabla de estudiantes si no existe
def fetch_students_table():
    try:
        conn = db_open()
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS students (
                username INTEGER PRIMARY KEY,
                password TEXT,
                first_name TEXT,
                last_name TEXT,
                nationality TEXT,
                email TEXT,
                active BOOLEAN,
                updated_by TEXT,
                updated_at DATE,
                created_at DATE
                )
            """
        )
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        return False

# Función para crear la tabla de maestros si no existe
def fetch_teachers_table():
    conn = db_open()
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS teachers (
            username INTEGER PRIMARY KEY,
            password TEXT,
            first_name TEXT, 
            last_name TEXT,
            nationality TEXT,
            email TEXT,
            updated_by TEXT,
            updated_at DATE,
            created_at DATE
            )
        """
    )
    conn.commit()
    conn.close()

# Función para crear la tabla de maestros si no existe
def fetch_tutors_table():
    conn = db_open()
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS tutors (
            username INTEGER PRIMARY KEY,
            password TEXT,
            first_name TEXT, 
            last_name TEXT,
            nationality TEXT,
            email TEXT,
            updated_by TEXT,
            updated_at DATE,
            created_at DATE
            )
        """
    )
    conn.commit()
    conn.close()
    
def get_all_students():
    try:
        conn = db_open()
        cursor = conn.cursor()
        cursor.execute("SELECT username, first_name, last_name, nationality, email FROM students where active = 1")
        students = cursor.fetchall()
        conn.close()
        if len(students) > 0:
            return students
        else:
            return {'message': 'No hay alumnos para mostrar'}
    except Exception as e:
        return {'message': f'Se produjo un error al obtener la lista de alumnos. {e}'}
    
# Funcion para obtener los datos de un studiante
def get_student(username):
    conn = db_open()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT * FROM students WHERE username = {}".format(username)
        )
        student = cursor.fetchall()[0]
    except:
        student = None
    conn.close()
    return student
    
# Funcion para obtener los datos de un profesor
def get_teacher(username):
    conn = db_open()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT * FROM teachers WHERE username = {}".format(username)
        )
        teacher = cursor.fetchall()[0]
    except:
        teacher = None
    conn.close()
    return teacher
    
# Funcion para obtener los datos de un preceptor
def get_tutor(username):
    conn = db_open()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT * FROM tutors WHERE username = {}".format(username)
        )
        tutor = cursor.fetchall()[0]
    except:
        tutor = None
    conn.close()
    return tutor

# Agregar un estudiante
def add_student(username, password, first_name, last_name, nationality, email, active):
    try:
        # Abro la conexión con la base de datos
        conn = db_open()
        cursor = conn.cursor()
        
        # Verificar si el estudiante ya existe
        cursor.execute(
            """
            SELECT * FROM students WHERE username = ?
            """,
            (username,)
        )
        existing_student = cursor.fetchone()
        
        if existing_student:
            # Si el estudiante ya existe, devolver sus datos
            return {
                "username": existing_student[0],
                "password": existing_student[1],
                "first_name": existing_student[2],
                "last_name": existing_student[3],
                "nationality": existing_student[4],
                "email": existing_student[5],
                "message": "El estudiante ya existe"
            }
        else:
            # Insertar el nuevo estudiante en la base de datos
            cursor.execute(
                """
                INSERT INTO students (
                    username,
                    password,
                    first_name,
                    last_name,
                    nationality,
                    email,
                    active,
                    updated_by,
                    updated_at,
                    created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (username, password, first_name, last_name, nationality, email, active, get_user_name(), get_db_format_time(), get_db_format_time())
            )
            # Guardar los cambios y cerrar la conexión
            conn.commit()
            # Indicar que no hubo errores
            return {
                "username": username,
                "password": password,
                "first_name": first_name,
                "last_name": last_name,
                "nationality": nationality,
                "email": email,
                "active": active,
                "message": "El estudiante se ha creado correctamente"
            }
    except Exception as e:
        # Manejar cualquier error que ocurra durante la ejecución
        return {"error": f"Error al agregar/actualizar estudiante estudiante: {e}"}
    finally:
        # Cierro la conexion con la base de datos
        if conn:
            conn.close()

# Función para actualizar los datos de un estudiante existente
def update_student(username, password, first_name, last_name, nationality, email):
    try:
        # Abro la conexión con la base de datos
        conn = db_open()
        cursor = conn.cursor()
        
        # Verificar si el estudiante ya existe
        cursor.execute(
            """
            SELECT * FROM students WHERE username = ?
            """,
            (username,)
        )
        existing_student = cursor.fetchone()
        
        if existing_student:
            # Si el estudiante ya existe, actualizar sus datos
            cursor.execute(
                """
                UPDATE students 
                SET password = ?, first_name = ?, last_name = ?, nationality = ?, email = ?
                WHERE username = ?
                """,
                (password, first_name, last_name, nationality, email, username)
            )
            # Guardar los cambios
            conn.commit()
            # Devolver los datos actualizados del estudiante
            return {
                "username": username,
                "password": password,
                "first_name": first_name,
                "last_name": last_name,
                "nationality": nationality,
                "email": email,
                "message": "Los datos del estudiante se han actualizado correctamente"
            }
        else:
            # Si el estudiante no existe, devolver un mensaje de error
            return {"error": "El estudiante no existe en la base de datos"}
    except Exception as e:
        # Manejar cualquier error que ocurra durante la ejecución
        return {"error": f"Error al actualizar estudiante: {e}"}
    finally:
        # Cierro la conexión con la base de datos
        if conn:
            conn.close()

# Función para crear la tabla de asistencias
def fetch_asistance_table():
    try:
        conn = db_open()
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS asistance (
                date INTEGER,
                rain INTEGER,
                username INTEGER,
                present BOOL,
                justification TEXT,
                updated_by TEXT,
                updated_at DATE
                )
            """
        )
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        return False
    
def register_student_asistance(date, username, present, justification, rain=0):
    # Abro la conexión con la base de datos
    conn = db_open()
    cursor = conn.cursor()
    try:
        # Verificar si ya existe un registro para la fecha y el usuario
        cursor.execute(
            """
            SELECT * FROM asistance WHERE date = ? AND username = ?
            """,
            (date, username)
        )
        existing_record = cursor.fetchone()

        if existing_record:
            # Si ya existe un registro, actualizarlo
            cursor.execute(
                """
                UPDATE asistance
                SET present = ?, justification = ?, updated_by = ?, updated_at = ?
                WHERE date = ? AND username = ?
                """,
                (present, justification, get_user_name(), get_db_format_time(), date, username)
            )
        else:
            # Si no existe un registro, insertarlo
            cursor.execute(
                """
                INSERT INTO asistance (date, username, present, justification, rain, updated_by, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (date, username, present, justification, rain, get_user_name(), get_db_format_time())
            )
        # Guardo los cambios y cierro la conexión
        conn.commit()
        message = f'Los datos de asistencia para el alumno {username} se cargaron correctamente.'
    except Exception as e:
        message = f'Error al agregar o actualizar el registro de asistencia del alumno {username}: {e}'
    finally:
        conn.close()
        return message
        
# Obtengo la lista de inasistencias de un estudiante
def get_student_asistance(username):
    # Abro la conexión con la base de datos
    conn = db_open()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT * FROM asistance WHERE username = ?", (username,)
        )
        return cursor.fetchall()
    except Exception as e:
        return False
    finally:
        # Cierro la conexión con la base de datos
        conn.close()
        
def set_abset_justification(username, date, justification):
    # Abro la conexión con la base de datos
    conn = db_open()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            UPDATE asistance 
            SET justification = ?,
                updated_at = ?,
                updated_by = ?
            WHERE username = ?
                and date = ?
            """,
            (justification, get_db_format_time(), get_user_name(), username, date)
        )
    except Exception as e:
        return False
    finally:
        # Cierro la conexión con la base de datos
        conn.commit()
        conn.close()
        return True

# Agregar un profesor
def add_teacher(username, password, first_name, last_name, nationality, email):
    try:
        # Abro la conexion con la vase de datos
        conn = db_open()
        cursor = conn.cursor()
        cursor.execute(
                """
                INSERT INTO teachers (
                    username,
                    password,
                    first_name,
                    last_name,
                    nationality,
                    email,
                    updated_by,
                    updated_at,
                    created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (username, password, first_name, last_name, nationality, email, get_user_name(), get_db_format_time(), get_db_format_time())
                
        )
        # Guardo los cambios y cierro la conexion
        conn.commit()
        conn.close()
        return {'message': 'El profesor se ha creado correctamente.'}
    except Exception as e:
        return {'message': f'Se ha producido un error al crear el profesor. {e}'}

# Agregar un preceptor
def add_tutor(username, password, first_name, last_name, nationality, email):
    try:
        # Abro la conexion con la vase de datos
        conn = db_open()
        cursor = conn.cursor()
        cursor.execute(
                """
                INSERT INTO tutors (
                    username,
                    password,
                    first_name,
                    last_name,
                    nationality,
                    email,
                    updated_by,
                    updated_at,
                    created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (username, password, first_name, last_name, nationality, email, get_user_name(), get_db_format_time(), get_db_format_time())
                
        )
        # Guardo los cambios y cierro la conexion
        conn.commit()
        conn.close()
        return {'message': 'El preceptor se ha creado correctamente.'}
    except Exception as e:
        return {'message': f'Se ha producido un error al crear el preceptor. {e}'}

def is_valid_student(username, password):
    # Abro la conexión con la base de datos
    conn = db_open()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT username FROM students WHERE username = ? AND password = ?", (username, password)
        )
        # Compruebo si hay alguna fila coincidente
        if cursor.fetchone():
            return True
        else:
            return False
    except Exception as e:
        return False
    finally:
        # Cierro la conexión con la base de datos
        conn.close()

def is_valid_teacher(username, password):
    # Abro la conexión con la base de datos
    conn = db_open()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT username FROM teachers WHERE username = ? AND password = ?", (username, password)
        )
        # Compruebo si hay alguna fila coincidente
        if cursor.fetchone():
            return True
        else:
            return False
    except Exception as e:
        return False
    finally:
        # Cierro la conexión con la base de datos
        conn.close()
        
def is_valid_tutor(username, password):
    # Abro la conexión con la base de datos
    conn = db_open()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT username FROM tutors WHERE username = ? AND password = ?", (username, password)
        )
        # Compruebo si hay alguna fila coincidente
        if cursor.fetchone():
            return True
        else:
            return False
    except Exception as e:
        return False
    finally:
        # Cierro la conexión con la base de datos
        conn.close()

def is_valid_date(date):
    # Abro la conexión con la base de datos
    conn = db_open()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT * FROM asistance WHERE date = ?", (date,)
        )
        # Compruebo si hay alguna fila coincidente
        if cursor.fetchall():
            return True
        else:
            return False
    except Exception as e:
        return False
    finally:
        # Cierro la conexión con la base de datos
        conn.close()

def export_table_to_csv(table_name, csv_file):
    # Abro la conexión con la base de datos
    conn = db_open()
    cursor = conn.cursor()

    # Obtener todos los registros de la tabla
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()

    # Obtener los nombres de las columnas
    column_names = [description[0] for description in cursor.description]

    # Escribir los datos en el archivo CSV
    with open(csv_file, 'w', newline='') as file:
        writer = csv.writer(file)
        # Escribir los nombres de las columnas como la primera fila
        writer.writerow(column_names)
        # Escribir los datos de los registros
        writer.writerows(rows)

    # Cerrar la conexión con la base de datos
    conn.close()
    
def set_student_status(username, status):
    try:
        # Abro la conexión con la base de datos
        conn = db_open()
        cursor = conn.cursor()
        # Obtener todos los registros de la tabla
        cursor.execute(
            """UPDATE STUDENTS SET active = ?,
                updated_by = ?,
                updated_at = ?
                WHERE username = ?
            """,
            (status, get_user_name(), get_db_format_time(), username)
            )
        conn.commit()
        message = f"El estado de activo para el estudiante {username} a sido cambiado a {status} satisfactoriamente."
    except Exception as e:
        message = f"Error al actualizar el estado para el alumno {username}. {e}"
    finally:
        conn.close()
        return message

def get_asistance_data(date):
    try:
        # Abro la conexión con la base de datos
        conn = db_open()
        cursor = conn.cursor()
        # Obtener todos los registros de la tabla
        cursor.execute(
            """SELECT * FROM asistance
                WHERE date = ?
            """,
            (date,)
            )
        data = cursor.fetchall()
        conn.close()
        if len(data) > 0:
            return data
        else:
            return {'message': f'No hay datos para mostrar para la fecha {date}'} 
    except Exception as e:
        return {'message': f"Error al obtener datos de asistencia para la fecha {date}. {e}" }