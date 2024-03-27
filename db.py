import sqlite3

# Variables globables
DB_NAME = 'escuela.db'

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
    
# Funcion para obtener los datos de un studiante
def get_student(username):
    conn = db_open()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM students WHERE username = {}".format(username)
    )
    student = cursor.fetchall()
    conn.close()
    return student