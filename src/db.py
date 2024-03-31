import sqlite3

# Variables globables
# Se supone que esto se ejecuta desde el main.py
DB_NAME = './database/escuela.db'

# Función para conectar a la base de datos SQLite
def db_open():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

# Función para crear la tabla de estudiantes si no existe
def fetch_students_table():
    conn = db_open()
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS students (username INTEGER PRIMARY KEY, password TEXT, first_name TEXT, last_name TEXT, nationality TEXT, email TEXT)"
    )
    conn.commit()
    conn.close()

# Función para crear la tabla de maestros si no existe
def fetch_teachers_table():
    conn = db_open()
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS teachers (username INTEGER PRIMARY KEY, password TEXT, first_name TEXT, last_name TEXT, nationality TEXT, email TEXT)"
    )
    conn.commit()
    conn.close()

# Función para crear la tabla de preceptores si no existe
def fetch_tutors_table():
    conn = db_open()
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS tutors (username INTEGER PRIMARY KEY, password TEXT, first_name TEXT, last_name TEXT, nationality TEXT, email TEXT)"
    )
    conn.commit()
    conn.close()
    
def get_all_students():
    conn = db_open()
    cursor = conn.cursor()
    cursor.execute("SELECT username, first_name, last_name, nationality, email FROM students")
    students = cursor.fetchall()
    conn.close()
    return students
    
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

# Agregar un estudiante
def add_student(username, password, first_name, last_name, nationality, email):
    # Abro la conexion con la vase de datos
    conn = db_open()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO students (username, password, first_name, last_name, nationality, email) VALUES (?, ?, ?, ?, ?, ?)",
        (username, password, first_name, last_name, nationality, email)
    )
    # Guardo los cambios y cierro la conexion
    conn.commit()
    conn.close()

# Función para crear la tabla de asistencias
def fetch_asistance_table():
    conn = db_open()
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS asistance (date INTEGER, username INTEGER, present BOOL)"
    )
    conn.commit()
    conn.close()
    
# Agregar un registro de asistencia
def register_student_asistance(date, username, present):
    # Abro la conexion con la vase de datos
    conn = db_open()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO asistance (date, username, present) VALUES (?, ?, ?)",
        (date, username, present)
    )
    # Guardo los cambios y cierro la conexion
    conn.commit()
    conn.close()
    
# Agregar un estudiante
def add_teacher(username, password, first_name, last_name, nationality, email):
    # Abro la conexion con la vase de datos
    conn = db_open()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO teachers (username, password, first_name, last_name, nationality, email) VALUES (?, ?, ?, ?, ?, ?)",
        (username, password, first_name, last_name, nationality, email)
    )
    # Guardo los cambios y cierro la conexion
    conn.commit()
    conn.close()
    
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
        print("Error al ejecutar la consulta:", e)
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
        print("Error al ejecutar la consulta:", e)
        return False
    finally:
        # Cierro la conexión con la base de datos
        conn.close()