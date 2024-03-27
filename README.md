# Archivos
- main.py: Archivo base que aloja el servidor y sus rutas.
- db.py: Archivo que contiene los metodos para operar con la base de datos.
- models.py: Archivo donde se definen los modelos que se utilizan dentro del proyeto.
- open_meteo.py: Archivo que consume la API de Open Meteo.
- unitary_tests.py: Archivo donde se definen los tests unitarios para los metodos.
- utils.py: Archivo donde se definen todos los metodos que son de utilidad para el proyecto.
- escuela.db: Archivo que contiene la base de datos del proyecto.
- README.md: Este archivo

# Ejecucion del servidor
1. El usuario de ubicarse en el path donde se encuentre el archivo main.py y ejecutar el siguiente comando:
$ uvicorn main:app --reload

2. Luego de esto se le asignara una IP al servidor local a la cual se podra acceder, por defecto la misma suele ser http://127.0.0.1:8000/ y se puede acceder desde cualquier navegador.

3. A modo de check de sanidad, el servidor devolvera un mensaje de Hola Mundo! en su pagina de inicio.

# Documentacion
Para llevar adelante este proyecto se utiliza el framework FastAPI el cual facilita la interaccion con desarrollos web. La herramienta gestiona de manera automatica la documentacion de las distintas URL del proyecto. Se puede acceder a la documentacion mediante la direccion http://127.0.0.1:8000/docs asumiendo que la direccion IP es la mencionada anteriormente.

# URLs del proyecto
- "/": Muestra el mensaje de sanidad del servidor.
- "/add_student/": Agrega estudiantes al curso en cuestion.
- "/get_student/": Obtiene la informacion de un estudiante en particular.
- "/students/": Obtiene la informacion de todos los estudiantes del curso.
- "/add_date/": Obtiene la informacion del estado del clima para el dia de la fecha
- "/generate_daily_report/": Obtiene las estadisticas de asistencia para el dia en curso.
- "/register_asistance/": Registra la asistencia para el dia de la fecha.
- "/view_absents/": Muestra la lista historica de ausencias del curso para todos o algunos estudiantes.
- "":
- "":

# Pruebas unitarias