# Archivos
- main.py: Archivo base que aloja el servidor y sus rutas.
- README.md: Este archivo

- database/db.py: Archivo que contiene los metodos para operar con la base de datos.

- src/models.py: Archivo donde se definen los modelos que se utilizan dentro del proyeto.
- src/open_meteo.py: Archivo que consume la API de Open Meteo.
- src/utils.py: Archivo donde se definen todos los metodos que son de utilidad para el proyecto.
- src/escuela.db: Archivo que contiene la base de datos del proyecto.

- tests/unitary_tests.py: Archivo donde se definen los tests unitarios para los metodos.

# Ejecucion del servidor
1. El usuario de ubicarse en el path donde se encuentre el archivo main.py y ejecutar el siguiente comando:
$ uvicorn main:app --reload

2. Luego de esto se le asignara una IP al servidor local a la cual se podra acceder, por defecto la misma suele ser http://127.0.0.1:8000/ y se puede acceder desde cualquier navegador.

3. A modo de check de sanidad, el servidor devolvera un mensaje de Hola Mundo! en su pagina de inicio.

# Documentacion
Para llevar adelante este proyecto se utiliza el framework FastAPI el cual facilita la interaccion con desarrollos web. La herramienta gestiona de manera automatica la documentacion de las distintas URL del proyecto. Se puede acceder a la documentacion mediante la direccion http://127.0.0.1:8000/docs asumiendo que la direccion IP es la mencionada anteriormente.

# URLs del proyecto
- "/": Muestra el mensaje de sanidad del servidor.
- "/login/": URL para el inicio de sesion.
- "/logoff/": URL para cerrar la sesion.
- "/add_student/": Agrega estudiantes al curso en cuestion.
- "/get_student/": Obtiene la informacion de un estudiante en particular.
- "/view_students/": Obtiene la informacion de todos los estudiantes del curso.
- "/generate_daily_report/": Obtiene las estadisticas de asistencia para el dia en curso.
- "/register_asistance/": Registra la asistencia para el dia de la fecha.
- "/view_absents/": Muestra la lista historica de ausencias del curso para todos o algunos estudiantes.
- "":
- "":

# Variables de entorno y sistema de logeo
Para poder visualizar la informacion de la escuela lo primero que debe hacerse es logearse, existen a priori los siguientes roles:
1. student
2. tutor
3. teacher

La forma de logear es mediante la URL http://localhost:<port>/login/?username=<username>&password=<password>

Una vez iniciada la sesion, el usuario contara con determinados privilegios segun su rol. Dentro del sistema a la hora de iniciada la sesion se disponen de tres variables de entorno para la gestion de datos:
- USER_AUTHENTICATED: Registra el estado de inicio de sesion
- USER_USERNAME: Registra el numero de usuario en cuestion
- USER_ROLE: Registra el role del usuario en cuestion

Para deslogearse del sitio, simplemente se debe acceder a la URL http://localhost:<port>/lofoff/ borrando asi la informacion registrada en las variables de entorno.

# Informacion de estudiantes
Para visualizar la informacion de un estudiante es necesario estar logeado como se menciono anteriormente y ademas la informacion estara disponible con restricciones:
- Un estudiante solo puede ver sus datos
- Un profesor o un tutor pueden ver la informacion de todos los estudiantes

# Registro de asistencia
El registro de asistencia solo puede ser realizar por profesores o tutores registrados y logeados en el sistema. Al momento de registrar la asistencia, el sistema hara uso de la API de Open Meteo para obtener la informacion del clima, en el caso de que el dia sea lluvioso, automaticamente se establecera por defecto el mensaje "Dia lluvioso" para el caso de los alumnos ausentes.
Si el dia no presenta lluvias, el tutor debera expresar de manera manual los motivos o justificaciones de ausencias para cada alumno segun corresponda.
La URL basica para el registro de asistencia es http://localhost:/register_asistance/

Luego se puede obtener un reporte del estado curricular de cada alumno en la URL http://localhost:8000/view_students/. Cabe destacar que esto ultimo solo puede ser realizado por profesores o preceptores.

La justificacion de asistencia se puede realizar mediante la URL http://localhost:8000/justify_absent?username=<username>&date=<date>&justificacion=<justification-opton>

# Generacion de estudiantes y profesores
En la carpeta tests/ se encuentran algunos tests unitarios para las funcionalidades creadas. En el caso de no tener estudiantes ni profesores se pueden crear 5 profesores y 50 estudiantes de manera aleatoria para ejecutar pruebas. Para tal fin solo basta con ejecutar el test unitario con el comando

$ python tests/unitary_tests.py