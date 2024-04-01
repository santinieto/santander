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
        """
        CREATE TABLE IF NOT EXISTS students (
            username INTEGER PRIMARY KEY,
            password TEXT,
            first_name TEXT,
            last_name TEXT,
            nationality TEXT,
            email TEXT
            )
        """
    )
    conn.commit()
    conn.close()

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
            email TEXT
            )
        """
    )
    conn.commit()
    conn.close()

# Función para crear la tabla de preceptores si no existe
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
            email TEXT
            )
        """
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
                INSERT INTO students (username, password, first_name, last_name, nationality, email)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (username, password, first_name, last_name, nationality, email)
            )
            # Guardar los cambios y cerrar la conexión
            conn.commit()
            # Indicar que no hubo errores
            return {'message': 'El estudiante se ha creado correctamente'}
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
    conn = db_open()
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS asistance (date INTEGER, username INTEGER, present BOOL, justification TEXT)
        """
    )
    conn.commit()
    conn.close()
    
def register_student_asistance(date, username, present, justification):
    # Abro la conexión con la base de datos
    conn = db_open()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT OR REPLACE INTO asistance (date, username, present, justification)
            VALUES (?, ?, ?, ?)
            """,
            (date, username, present, justification)
        )
        # Guardo los cambios y cierro la conexión
        conn.commit()
    except Exception as e:
        print("Error al agregar el registro de asistencia:", e)
    finally:
        conn.close()

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
        print("Error al ejecutar la consulta:", e)
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
            "UPDATE asistance SET justification = ? WHERE username = ? and date = ?", (justification, username, date)
        )
    except Exception as e:
        print("Error al ejecutar la consulta:", e)
        return False
    finally:
        # Cierro la conexión con la base de datos
        conn.commit()
        conn.close()
        return True

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
        
def is_valid_date(date):
    # Abro la conexión con la base de datos
    conn = db_open()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT * FROM asistance WHERE date = ?", (date)
        )
        # Compruebo si hay alguna fila coincidente
        if cursor.fetchall():
            return True
        else:
            return False
    except Exception as e:
        print("Error al ejecutar la consulta:", e)
        return False
    finally:
        # Cierro la conexión con la base de datos
        conn.close()