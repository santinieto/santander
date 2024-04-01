# Librerias estandar
import os
import sys
sys.path.append('./')

# Librerias custom
import src.db as db
import src.utils as u

# Variables globables
# Se supone que esto se ejecuta desde el main.py
DB_NAME = './database/escuela.db'

# Funcion principal
def create_students(n_students=30):
    
    os.environ["USER_USERNAME"] = 'script'
    
    # Cuantos estudiantes voy a crear
    if n_students is None:
        n_students = int(input('Cantidad de estudiantes a crear: '))
    print(f'Se van a crear {n_students} estudiantes')
    
    # Me conecto con la base de datos y verifico que existe la tabla de estudiantes
    if db.fetch_students_table() is False:
        print('Se produjo un error al crear la tabla de estudiantes')
        
    # Creo los estudiantes
    for kk in range(n_students):
        print(f'Estudiante {kk + 1}:')
        
        user = u.new_user(verbose=True)
        
        message = db.add_student(
            user['username'],
            user['password'],
            user['first_name'],
            user['last_name'],
            user['nationality'],
            user['email'],
            1
            )
        
        print(message)

if __name__ == '__main__':
    create_students(n_students=None)