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
def create_tutors(n_tutors=5):
    
    os.environ["USER_USERNAME"] = 'script'
    
    # Cuantos profesores voy a crear
    if n_tutors is None:
        n_tutors = int(input('Cantidad de profesores a crear: '))
    print(f'Se van a crear {n_tutors} profesores')
    
    # Me conecto con la base de datos y verifico que existe la tabla de profesores
    if db.fetch_tutors_table() is False:
        print('Se produjo un error al crear la tabla de profesores')
        
    # Creo los profesores
    for kk in range(n_tutors):
        print(f'Profesor {kk + 1}:')
        
        user = u.new_user(verbose=True)
        
        message = db.add_tutor(
            user['username'],
            user['password'],
            user['first_name'],
            user['last_name'],
            user['nationality'],
            user['email'],
            )
        
        print(message)

if __name__ == '__main__':
    create_tutors(n_tutors=None)