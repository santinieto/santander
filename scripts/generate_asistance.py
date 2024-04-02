# Librerias estandar
from datetime import datetime, timedelta
import random
import os
import sys
sys.path.append('./')

# Librerias custom
import src.db as db

# Funcion principal
def generate_asistance(n_days=10):
    
    os.environ["USER_USERNAME"] = 'script'
    
    # Cuantos estudiantes voy a crear
    if n_days is None:
        n_days = int(input('Cantidad de dias a generar: '))
    print(f'Se van a crear {n_days} de asistencia')
    
    # Verifico que existe la tabla de asistencia
    if db.fetch_asistance_table() is False:
        print('Se produjo un error al crear la tabla de asistencia')
        
    # Obtengo la lista de estudiantes
    students = [row['username'] for row in db.get_all_students()]
    # print(f'Lista de estudiantes: {students}')
    
    # Obtener la fecha actual
    current_date = datetime.now()

    # Bucle para retroceder n_days días
    dates_list = []
    for kk in range(n_days):
        # Restar un día a la fecha actual
        current_date -= timedelta(days=1)
        # Formatear la fecha en YYYYMMDD y agregarla a la lista
        formatted_date = current_date.strftime("%Y%m%d")
        dates_list.append(formatted_date)

    # Imprimir las fechas
    for date in dates_list:
        
        print(f'Generando asistencias para la fecha {date}:')
        
        # El dia estuvo lluvioso con 30% de probabilidad
        rain = int(random.random() > 0.7)
        
        print(f'Lluvia: {rain}')
        
        for student in students:
            
            # El alumno tiene cerca del 80% de asistencia
            present = int(random.random() > 0.2)
            
            print(f'\t - Estudiante {student} - Presente: {present}')
            
            if present == 0:
                if rain:
                    justification = 'Dia lluvioso'
                else:
                    justification = 'Other reason'
            else:
                justification = '-'
            
            # Registro la asistencia
            message = db.register_student_asistance(date, student, present, justification, rain)
            print(message)

if __name__ == '__main__':
    generate_asistance(n_days=None)