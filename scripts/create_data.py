# Librerias estandar
import os
import sys
sys.path.append('./')

# Librerias custom
import src.db as db

from create_students import create_students
from create_teachers import create_teachers
from create_tutors import create_tutors
from generate_asistance import generate_asistance

if __name__ == '__main__':
    
    # Me fijo que las tablas existan
    db.fetch_students_table()
    db.fetch_teachers_table()
    db.fetch_tutors_table()
    db.fetch_asistance_table()
    
    # Borro los datos si los hubiera
    db.clean_database()
    
    # Genero datos
    create_students(n_students=30)
    create_teachers(n_teachers = 10)
    create_tutors(n_tutors = 5)
    generate_asistance(n_days = 30)