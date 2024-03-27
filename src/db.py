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