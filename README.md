# Proyecto

### Descripcion
En una escuela rural se desea automatizar la gestión de asistencia diaria de los alumnos.
Para esto se propone una solución de arquitectura de software que cumpla con dicho propósito. Con tal fin se propone un software en Python que haga uso del framework FastAPI cuya documentacion se puede encontrar en el siguiente sitio:

> https://fastapi.tiangolo.com/

### Archivos y carpetas
* ./database/
    * `escuela.db`: Base de datos del proyecto.

* ./results/
    * ...

* ./scripts/
    * `create_data.py`: Genera datos aleatorios para inicializar el proyecto llamando al resto de los scripts de esta carpeta.
    * `create_students.py`: Genera estudiantes aleatorios.
    * `create_teachers.py`: Genera perfiles de profesores aleatorios.
    * `create_tutors.py`: Genera perfiles de preceptores aleatorios.
    * `generate_asistance.py`: Genera un registro de asistencia para los alumnos creados.

* ./src/
    * `db.py`: Funciones asociadas a la interaccion con la base de datos.
    * `models.py`: Descripcion de los modelos de roles del proyecto.
    * `open_meteo.py`: Funcionalidades relacionadas con la API de Open Meteo.
    * `scrap.py`: Funcionalidades para obtener la informacion del clima desde Google o cualquier otro sitio de internet.
    * `utils.py`: Funciones de utilidad compartidas por todo el proyecto.

* ./tests/
    * `create_student_test.py`: Tests unitarios sobre la creacion de perfiles de estudiantes.
    * `create_teacher_test.py`: Tests unitarios sobre la creacion de perfiles de profesores.
    * `create_tutor_test.py`: Tests unitarios sobre la creacion de perfiles de preceptores.
    * `unitary_tests.py`: Tests unitarios varios.

* `main.py`: Archivo principal del proyecto. Contiene las rutas o URLs asociadas al mismo.
* `README.md`: Archivo de descripcion del proyecto (este archivo).

Existen otros archivos auxiliares cuya funcion se limita a la vinculacion entre archivos, para tales casos no se requiere de una descripcion especifica. Ejemplos de esto son los archivos `__init__.py`.

Se hace una mencion especial para la carpeta `./results` que sera donde se guardaran todos los archivos generados por el sistema. Tablas de bases de datos, reportes diarios, logeos, etc (no todo esta implementado actualmente pero en general los archivos generados por el sistema deberian ir aqui o en una hipotetica carpeta llamada `./logs/` o `./errors/`).

### Clonado del repositorio
Para descargar el repositorio y comenzar a utilizarlo simplemente se debe abrir una consola y ejecutar el siguiente comando donde se quiera tener los archivos:

> $ git clone https://github.com/santinieto/santander.git

### Generacion de datos aleatorios
Dentro de la carpeta `./scripts/` existen diversos archivos para generar datos aleatorios con los cuales se comenzara a trabajar (esto se realiza simplemente para tener datos validos y poder corroborar la funcionalidad de todo el sistema). Cabe destacar que para este caso, no es necesario tener el servidor encendido ni logearse de ninguna forma ya que el objetivo de los scripts en esta carpeta se limita a la generacion de datos para comenzar a trabajar.

Ubicado en el directorio raiz del proyecto solo basta con ejecutar el comando:

>$ python scripts\create_data.py

Por defecto el sistema creara 30 alumnos, 10 profesores, 5 preceptores y registros de asistencia de los alumnos generados de los ultimos 30 dias.

El motor de bases de datos utilizado para este proyecto es SQLite pero en caso de no disponer del mismo los datos generados se guardaran en archivos ".csv" dentro de la carpeta `./results/`.

### Ejecucion del servidor
1. El usuario de ubicarse en el path, ruta o camino donde se encuentre el archivo `main.py` y ejecutar el siguiente comando:

> $ uvicorn main:app --reload

Si la ejecucion del servidor resulto exitosa, la consola quedara en modo escucha o espera con mensajes similares a estos:

```
INFO:     Will watch for changes in these directories: > ['C:\\Users\\santi\\OneDrive\\Desktop\\santander']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL> +C to quit)
INFO:     Started reloader process [30332] using WatchFiles
INFO:     Started server process [33556]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

2. Luego de esto se le asignara una IP al servidor local a la cual se podra acceder, por defecto la misma suele ser http://127.0.0.1:8000/ (aunque es recomendable verificarlo en cada caso) y se puede acceder desde cualquier navegador.

3. A modo de check de sanidad, el servidor devolvera un mensaje de "Bienvenido al sistema de asistencia de la escuela rural." en su pagina de inicio ('./').

**NOTA**: Se puede prescindir del conocimiento de la IP asignada al servidor y acceder al mismo mediante la URL http://localhost:8000/

### Documentacion
Para llevar adelante este proyecto se utiliza el framework FastAPI el cual facilita la interaccion con desarrollos web. La herramienta gestiona de manera automatica la documentacion de las distintas URL del proyecto. Se puede acceder a la documentacion mediante la direccion http://127.0.0.1:8000/docs asumiendo que la direccion IP es la mencionada anteriormente.

Dentro de ese entorno pueden realizarse distintas pruebas si se considera necesario.

### URLs del proyecto

* `/`: Muestra el mensaje de sanidad del servidor.
* `/my_profile/`: Visualiza la informacion del usuario que ha iniciado sesion.
* `/login/`: URL para el inicio de sesion.
* `/logoff/`: URL para cerrar la sesion.
* `/add_student/`: Agrega un perfil de estudiante al curso.
* `/update_student/`: Actualiza los datos personales de un estudiante.
* `/set_student_status/`: Establece el estado de activo para un estudiante.
* `/get_student/`: Obtiene la informacion de un estudiante en particular.
* `/view_students/`: Obtiene la informacion de todos los estudiantes del curso.
* `/register_asistance/`: Registra la asistencia para el dia de la fecha (o algun dia en particular).
* `/view_daily_report/`: Obtiene las estadisticas para el dia en curso (o algun dia en particular).
* `/edit_asistance/`: Edita la asitencia de una determinada fecha para algun alumno.
* `/justify_absent/`: Establece justificaciones de ausencias para los alumnos.
* `/add_teacher/`: Agrega un perfil de profesor al curso.
* `/add_tutor/`: Agrega un perfil de preceptor al curso.

### Pagina de logeo y roles
Existen diversos roles dentro del proyecto y cada uno tendra accesos distintos a las funcionalidades del proyecto. A saber:

* Un alumno puede:
    * Consultar y Modificar sus datos personales
    * Consultar sus asistencias
* Un docente puede:
    * Consultar los datos personales de los alumnos
    * Consultar las asistencias del curso
    * Tomar la asistencia del curso
    * Editar una asistencia del curso
    * Borrar una asistencia del curso
* Un preceptor puede:
    * Consultar y Modificar los datos personales de los alumnos
    * Consultar las asistencias del curso
    * Tomar la asistencia del curso
    * Editar una asistencia del curso
    * Borrar una asistencia del curso
    * Dar de alta un nuevo alumno
    * Deshabilitar a un alumno
* Como adicional al proyecto se creo el perfil de administrador el cual tiene acceso total a todas las funcionalidades. Para este caso particular tanto el usuario como la contraseña del administrador son "admin".

La URL de logeo es:

> http://localhost:8000/login/?username=username&password=password

Los datos de usuario y contraseña puede ser obtenidos a traves de la inspeccion de las tablas ".csv" generadas en `./results/`.

**NOTA**: Cabe destacar que estos datos no deberian ser accesibles por los usuarios finales y como se vera mas adelante, no todos los datos son visibles ante peticiones realizadas al servidor.

Para deslogearse del sitio, simplemente se debe acceder a la URL

> http://localhost:port/logoff/


### Variables de entorno y sistema de logeo

Una vez iniciada la sesion, el usuario contara con determinados privilegios o restricciones segun su rol de acuerdo a lo mencionado en la seccion anterior. Dentro del sistema, a la hora de iniciada la sesion se disponen de tres variables de entorno para la gestion de datos:
- `USER_AUTHENTICATED`: Registra el estado de inicio de sesion.
- `USER_USERNAME`: Registra el numero de usuario que ha iniciado sesion.
- `USER_ROLE`: Registra el role del usuario que ha iniciado sesion.
- `USER_LOG_TIME`: Registra la hora de conexion del usuario que ha iniciado sesion.

Al utilizar la URL (cerrar la sesion actual):

> http://localhost:port/logoff/

Se borrara la informacion registrada en las variables de entorno.

### Informacion de usuario
Una vez autenticado un usuario se dispone de una URL para realizar una verificacion rapida de los datos cargados en el sistema. Sin importar el rol, se puede acceder a la URL:

> http://localhost:port/my_profile/

Para corroborar los datos cargados.
A modo de ejemplo se muestra el output del servidor para el caso del administrador:

```
{
  "username": "admin",
  "role": "admin",
  "log_time": "20240401T15:33:45"
}
```

Y de un estudiante:

```
{
  "username": "10282608",
  "role": "student",
  "log_time": "20240401T15:42:25",
  "first_name": "Cristian",
  "last_name": "Johnson",
  "email": "cristian.johnson@school.com",
  "nationality": "arg",
  "active": 1
}
```

### Estadisticas de un estudiante
Para cada estudiante se puede obtener estadisticas de asistencia. Algunas consideraciones a tener en cuenta son:
* Para ver esta informacion se necesita estar logeado en el sistema.
* Un estudiante solo puede ver las estadisticas asociadas a su propio perfil.
* Los profesores, preceptores y el administrador pueden ver las estadisticas de cualquier estudiante.

Siguiendo con el ejemplo anterior, si el alumno "Cristian Johnson" quiere ver sus estadisticas debera acceder a la URL:

> http://localhost:8000/get_student/?username=10282608

Para lo cual el servidor respondera con la siguiente informacion:

```
{
  "username": 10282608,
  "name": "Cristian Johnson",
  "nationality": "arg",
  "email": "cristian.johnson@school.com",
  "n_present": 21,
  "n_absent": 12,
  "present_rate": 63.64,
  "absent_dates": [
    "28/03/2024",
    "22/03/2024",
    "18/03/2024",
    "16/03/2024",
    "12/03/2024",
    "06/03/2024",
    "05/03/2024",
    "04/03/2024",
    "03/03/2024",
    "31/03/2024",
    "31/03/2024",
    "31/03/2024"
  ]
}
```

Para este caso particular, el alumno posee un 63.64% de asistencia y ademas tiene un registro de cuales son los dias en los que estuvo ausente.

En el caso que Cristian quiera obtener las estadistica de Amanda Wilson con DNI 11373488, el servidor le denegara el acceso.

> http://localhost:8000/get_student/?username=11373488

```
{
  "detail": "Acceso denegado."
}
```

Una vez mas, esta restriccion no existe para el administrador, los profesores y los preceptores.

Se hace una mencion especial que para el caso de los roles admitidos, se puede consultar las estadisticas de todos los alumnos simultaneamente mediante la URL:

> http://localhost:8000/view_students/

Para lo cual el servidor respondera con la informacion correspondiente de todos los alumnos:

```
  {
    "username": 10282608,
    "first_name": "Cristian",
    "last_name": "Johnson",
    "nationality": "arg",
    "email": "cristian.johnson@school.com",
    "n_present": 21,
    "n_absent": 12,
    "present_rate": 63.64,
    "absent_dates": [
      "28/03/2024",
      "22/03/2024",
     "18/03/2024",
     "16/03/2024",
     "12/03/2024",
     "06/03/2024",
     "05/03/2024",
     "04/03/2024",
     "03/03/2024",
     "31/03/2024",
     "31/03/2024",
     "31/03/2024"
   ]
 },
 {
   "username": 11373488,
   "first_name": "Amanda",
   "last_name": "Wilson",
   "nationality": "arg",
   "email": "amanda.wilson@school.com",
   "n_present": 28,
   "n_absent": 5,
   "present_rate": 84.85,
   "absent_dates": [
     "27/03/2024",
     "04/03/2024",
     "31/03/2024",
     "31/03/2024",
     "31/03/2024"
   ]
 },
 {
   "username": 13628540,
   "first_name": "Peter",
   "last_name": "Mcdonald",
   "nationality": "arg",
   "email": "peter.mcdonald@school.com",
   "n_present": 26,
   "n_absent": 7,
   "present_rate": 78.79,
   "absent_dates": [
     "20/03/2024",
     "18/03/2024",
     "12/03/2024",
     "02/03/2024",
  ...
```

**NOTA**: Los alumnos que no cuenten con un estado activo no seran considerados para las estadisticas.

### Modificacion de datos personales
Los datos personales de cada alumno pueden ser modificados. Las restricciones son:
* Un estudiante solo puede modificar sus datos personales.
* Un profesor puede modificar los datos personales de cualquier alumno.
* El administrador puede modificar los datos personales de cualquier alumno.

Siguiendo con el ejemplo anterior, supongamos que el alumno Cristian Johnson desea cambiar su correo electronico de "cristian.johnson@school.com" a "cjohnson@school.com". Lo primero que debe hacer es estar logeado:

> http://localhost:8000/login/?username=10282608&password=7T44S26f

Seguidamente, la peticion al servidor sera:

> http://localhost:8000/update_student/?username=10282608&email=cjohnson@school.com

Si la peticion se realizo correctamente el servidor lo informara:

```
{
  "message": "Datos actualizados exitosamente"
}
```

Y el cambio deberia verse reflejado desde su perfil:

> http://localhost:8000/my_profile/

```
{
  "username": "10282608",
  "role": "student",
  "log_time": "20240401T16:00:26",
  "first_name": "Cristian",
  "last_name": "Johnson",
  "email": "cjohnson@school.com",
  "nationality": "arg",
  "active": 1
}
```

Una vez mas, si Cristian quisiera cambiar datos en el perfil de Amanda, no se le permitiria debido a que los estudiantes no pueden modificar datos personales de otros estudiantes:

> http://localhost:8000/update_student/?username=11373488&email=amanda@school.com

```
{
  "message": "Error al actualizar los datos: 403: Acceso denegado."
}
```

### Registro de asistencia
La escuela rural desea automatizar el proceso de registro de asistencia. Esta funcion puede ser llevada a cabo por profesores y tutores (el administrador tambien puede realizarlo pero no deberia ocurrir en la practica).
Al momento de registrar la asistencia, el sistema hara uso de la API de *Open Meteo* (https://open-meteo.com/) para obtener la informacion del clima, en el caso de que el dia sea lluvioso, automaticamente se establecera por defecto el mensaje "Dia lluvioso" para el caso de los alumnos ausentes.
Si el dia no presenta lluvias, el tutor debera expresar de manera manual los motivos o justificaciones de ausencias para cada alumno segun corresponda.

La URL para registrar la asistencia de un alumno es:

> http://localhost:8000//register_asistance/

Esta URL consta de los siguientes parametros:
- `username (string, obligatorio)`: Nombre de usuario del estudiante.
- `date (string, opcional)`: Fecha en formato YYYYMMDD. Si no se proporciona, se usa la fecha actual.
- `present (string, opcional)`: Presente o ausente, por defecto presente.
- `justification (string, opcional)`: Justificacion de ausencia si fuera requerido.

Al momento de registrar la asistencia, lo primero que se hara es verificar si existen datos asociados a la fecha proporcionada en la base de datos, en el caso de que no existan, automaticamente se crearan registros para cada alumnos en el dia mencionado y ademas el valor por defecto sera ausente para todo el curso (si el dia es lluvioso ademas se autoagregara la justificacion correspondiente en cada registro).

Luego de que el sistema asegura tener al menos un registro para cada alumno por dia se procedera a cargar la asistencia del alumno en particular. Supongamos que el profesor "Jose Tomas" con DNI 13059989 desea registrar la asistencia del alumno Cristian Johson. El procedimiento que se debe seguir es el de estar logeado:

> http://localhost:8000/login/?username=13059989&password=UBFLjXxV

```
{
  "message": "Bienvenido profesor 13059989"
}
```

Ahora el profesor debe registrar la asistencia del alumno:

> http://localhost:8000/register_asistance/?username=10282608

```
{
  "message": "Se ha cargado la asistencia del alumno 10282608"
}
```

Si se observa la base de datos, en la tabla `asistance`, se vera que la asistencia fue cargada como presente para Cristian Johnson y para el resto de los alumnos fue ausente

```
date     | username | present | updated_by   | updated_at
20240401 | 10282608 | 1       | 13059989     | 20240401T16:15:30
20240401 | 11373488 | 0       | 13059989     | 20240401T16:15:30
20240401 | 13628540 | 0       | 13059989     | 20240401T16:15:30
20240401 | 15306578 | 0       | 13059989     | 20240401T16:15:30
20240401 | 15557107 | 0       | 13059989     | 20240401T16:15:30
20240401 | 16205080 | 0       | 13059989     | 20240401T16:15:30
20240401 | 16230090 | 0       | 13059989     | 20240401T16:15:30   
...
```

Si el profesor ahora quiere cargar la asistencia del alumno con DNI 13628540 debe seguir el mismo proceso.

> http://localhost:8000/register_asistance/?username=13628540 

```
{
  "message": "Se ha cargado la asistencia del alumno 13628540"
}
```
```
date     | username | present | updated_by | updated_at
20240401 | 10282608 | 1       | 13059989   | 20240401T16:15:30
20240401 | 11373488 | 0       | 13059989   | 20240401T16:15:30
20240401 | 13628540 | 1       | 13059989   | 20240401T16:20:23
20240401 | 15306578 | 0       | 13059989   | 20240401T16:15:30
20240401 | 15557107 | 0       | 13059989   | 20240401T16:15:30
20240401 | 16205080 | 0       | 13059989   | 20240401T16:15:30
20240401 | 16230090 | 0       | 13059989   | 20240401T16:15:30
```

Si este proceso quiere ser ejecutado por un estudiante, el acceso estaria denegado:

```
{
  "detail": "El registro de asistencia solo puede ser realizado por profesores o preceptores."
}
```

**NOTA**: En este caso estoy asumiendo que quien este cargando la asistencia esta obteniendo el DNI de cada alumno de manera automatica ya sea un QR, escaneo del DNI, codigo de barras, escaneo de huella digital, escaneo facial, etc. Entiendo que no deberia ser algo que el profesor o preceptor deberia realizar de manera manual. En mi mente el proceso seria (por ejemplo) que hubiera un escaner QR en la puerta del aula conectado a un sistema en el cual el profesor este logeado y cuando el alumno acerca su QR al escaner el registro de asistencia (llamado a la API) se realiza automaticamente.

### Reporte diario
Los profesores, preceptores y el administrador pueden ver el reporte diario de asistencia del curso mediante la URL:

> http://localhost:8000/view_daily_report/

Por defecto se creara un reporte para la el dia de la fecha, sin embargo, si se requiere un reporte para alguna fecha en particular, la misma puede ser especificada en la peticion GET.

> http://localhost:8000/view_daily_report/?date=20240325

```
{
  "date": "20240325",
  "rain": 1,
  "n_present": 20,
  "n_absent": 10,
  "asistance": 66.67
}
```

Si se ingresa una fecha incorrecta:

> http://localhost:8000/view_daily_report/?date=135434

```
{
  "date": "135434",
  "rain": "Error",
  "n_present": "Error",
  "n_absent": "Error",
  "asistance": "Error"
}
```

### Justificacion de inasistencias
Es comprensible que los alumnos presenten ausencias durante el periodo escolar y esto debe ser tenido en cuenta por el sistema. Para ello se provee a los profesores, preceptores y al administrador una herramienta de justificacion de ausencias mediante la URL:

> http://localhost:8000/justify_absent/

La misma requiere de algunos parametros:
* `username (string, obligatorio)`: Nombre de usuario del estudiante.
* `date (string, opcional)`: Fecha en formato YYYYMMDD.
* `justification (string, opcional)`: Código o descripción de la justificación.

Existe un codigo de justificacion de ausencias predeterminado para el parametro justification a saber:

* "1": "Enfermedad"
* "2": "Trámite personal"
* "3": "Consulta médica"

Se puede ingresar tambien cualquier otra cadena de caracteres a modo de justificacion siempre que la separacion entre palabras sea un guion medio (-). 

Supongamos que el preceptor Kurt Long con DNI 61995108 quiere justificar las ausencias del dia 01/04/2024 para los alumnos Dustin Perkins, DNI 15306578, motivo "Enfermedad" y Pamela Robinson, DNI 30083693, motivo "Viaje cultural".

Lo primero que debe hacer es estar logeado:

> http://localhost:8000/login/?username=61995108&password=uqU1viqr

```
{
  "message": "Bienvenido preceptor 61995108"
}
```

Seguidamente procede a justificar la ausencia para el alumno 15306578:

> http://localhost:8000/justify_absent/?username=15306578&date=20240401&justification=1

```
{
  "message": "Actualización exitosa. Se justifico la asistencia del dia 20240401 para el alumno 15306578 con motivo Enfermedad"
}
```

Base de datos:

> 20240401 | 15306578 | 0 | Enfermedad | 61995108 | 20240401T16:46:57

Por ultimo, procede a hacer lo propio con el alumno 30083693:

> http://localhost:8000/justify_absent/?username=30083693&date=20240401&justification=Viaje-cultural

```
{
  "message": "Actualización exitosa. Se justifico la asistencia del dia 20240401 para el alumno 30083693 con motivo Viaje cultural personal"
}
```

Base de datos:
> 20240401	30083693	0	Viaje cultural	61995108	20240401T16:47:00

Cabe destacar que la estudiante Pamela Robinson no puede justificar su asistencia por sus propios medios ni tampoco la de otro estudiante:

> http://localhost:8000/justify_absent/?username=30083693&date=20240401&justification=Viaje-cultural-personal


```
{
  "detail": "El registro de asistencia solo puede ser modificado por profesores o preceptores."
}
```

Por ultimo, cabe recordar que en el caso de los dias lluviosos todos los alumnos ausentes tendra su ausencia justificada automaticamente con el motivo "Dia lluvioso".

**NOTA**: En el caso de que no sea posible obtener la informacion del clima a traves de la API de Open Meteo, se propone obtener la misma a traves de un scrapping de la informacion que Google provee. Para tal fin se procedera de la siguiente forma (TBD).

### Correcion de asistencia
El sistema puede cometer errores o simplemente un alumno puede olvidar de registrar su asistencia al llegar a la escuela. Por este motivo los profesores, preceptores y al administrador pueden corregir estos errores mediante la URL:

> http://localhost:8000/edit_asistance/

Supongamos que el profesor Jeffrey Briggs con DNI 65387263 quiere corregir la asitencia del alumno 16205080 del dia 2024/03/11 ya que erroneamente se cargo como ausente. En este caso lo primero que debe hacer es logearse:

> http://localhost:8000/login/?username=65387263&password=L98PWtrP

```
{
  "message": "Bienvenido profesor 65387263"
}
```

Y ahora debe corregir la asistencia:

> http://localhost:8000/edit_asistance/?date=20240311&username=16205080&present=1&justification=Fixed

```
{
  "mesage": "Los datos de asistencia para el alumno 16205080 se cargaron correctamente."
}
```

En la base de datos:

> 20240311 | 16205080 | 1 | Fixed | 65387263 | 20240401T19:56:19

### Creacion de alumnos
En una escuela cada año ingresan alumnos nuevos y por este motivo se les provee a los profesores y al administrador la posibilidad de agregar nuevos ingresos mediante la URL.

> http://localhost:8000/add_student/

En este caso particular, la creacion de perfiles de estudiante se realiza a traves del verbo POST. Debido a esto, los datos del estudiante deben ser brindados al sistema en formato JSON. Para esto se proponen algunos tests unitarios alojados en la carpeta `./tests`. A modo de ejemplo se creara a un alumno de prueba:

```
student_data = {
                    "username": '123456789',
                    "password": '123456789',
                    "first_name": 'foo',
                    "last_name": 'foo',
                    "nationality": 'foo',
                    "email": 'foo',
                    "active": '1',
                }
```

Estos son los parametros por defecto en el test unitario pero pueden ser cambiados sin problema. En la carpeta `./utils/` se dispone de un script para generar un perfil aleatorio mediante el metodo `new_user()`.
Para correr el test unitario se debe ejecutar el comando:

> $ python tests\create_student_test.py

El resultado del test deberia ser similar a:

```
(base) C:\Users\santi\OneDrive\Desktop\santander>python tests\create_student_test.py
*************************************************
* test_create_student_error                     *
*************************************************
HTTP response code: 422
HTTP response body: {'detail': [{'type': 'int_parsing', 'loc': ['body', 'username'], 'msg': 'Input should be a valid integer, unable to parse string as an integer', 'input': 'foo', 'url': 'https://errors.pydantic.dev/2.6/v/int_parsing'}, {'type': 'missing', 'loc': ['body', 'nationality'], 'msg': 'Field required', 'input': {'username': 'foo', 'password': 'abc123', 'first_name': 'foo', 'last_name': 'foo'}, 'url': 'https://errors.pydantic.dev/2.6/v/missing'}, {'type': 'missing', 'loc': ['body', 'email'], 'msg': 'Field required', 'input': {'username': 'foo', 'password': 'abc123', 'first_name': 'foo', 'last_name': 'foo'}, 'url': 'https://errors.pydantic.dev/2.6/v/missing'}, {'type': 'missing', 'loc': ['body', 'active'], 'msg': 'Field required', 'input': {'username': 'foo', 'password': 'abc123', 'first_name': 'foo', 'last_name': 'foo'}, 'url': 'https://errors.pydantic.dev/2.6/v/missing'}]}
.*************************************************
* test_create_students                          *
*************************************************
HTTP response code: 200
HTTP response body: {'username': 123456789, 'password': '123456789', 'first_name': 'foo', 'last_name': 'foo', 'nationality': 'foo', 'email': 'foo', 'active': '1', 'message': 'El estudiante se ha creado correctamente'}
.
----------------------------------------------------------------------
Ran 2 tests in 0.058s

OK

(base) C:\Users\santi\OneDrive\Desktop\santander>
```

El test unitario ejecuta dos escenarios:
1. Intenta crear un usuario sin brindar toda la informacion necesaria
2. Crea un usuario de prueba

Si ambos tests unitarios fueron ejecutados correctamente, la herramienta deberia decir `OK` al final de los mismos.

**NOTA**: El servidor debe estar encendido para poder ejecutar este test.

### Creacion de profesores y preceptores
Dentro de la institución hay un equipo de trabajo el cual puede crecer con el tiempo segun se requiere. Por este motivo el administrador puede crear perfiles para profesores y preceptores. Las URLs para llevar a cabo esta acciones son:

> http://localhost:8000/add_teacher/
> http://localhost:8000/add_tutor/

De igual forma que con la creacion de alumnos se crean tests unitarios para probar estas funcionalidades.

Se puede ejecutar tanto el test unitario para crear profesores:

```
(base) C:\Users\santi\OneDrive\Desktop\santander>python tests\create_teacher_test.py
*************************************************
* test_create_teacher_error                     *
*************************************************
HTTP response code: 422
HTTP response body: {'detail': [{'type': 'int_parsing', 'loc': ['body', 'username'], 'msg': 'Input should be a valid integer, unable to parse string as an integer', 'input': 'foo', 'url': 'https://errors.pydantic.dev/2.6/v/int_parsing'}, {'type': 'missing', 'loc': ['body', 'nationality'], 'msg': 'Field required', 'input': {'username': 'foo', 'password': 'abc123', 'first_name': 'foo', 'last_name': 'foo'}, 'url': 'https://errors.pydantic.dev/2.6/v/missing'}, {'type': 'missing', 'loc': ['body', 'email'], 'msg': 'Field required', 'input': {'username': 'foo', 'password': 'abc123', 'first_name': 'foo', 'last_name': 'foo'}, 'url': 'https://errors.pydantic.dev/2.6/v/missing'}]}
.*************************************************
* test_create_teachers                          *
*************************************************
HTTP response code: 200
HTTP response body: {'username': 123456789, 'password': '123456789', 'first_name': 'foo', 'last_name': 'foo', 'nationality': 'foo', 'email': 'foo', 'message': 'El profesor 123456789 se ha creado correctamente.'}
.
----------------------------------------------------------------------
Ran 2 tests in 0.053s

OK

(base) C:\Users\santi\OneDrive\Desktop\santander>
```

Como para crear preceptores:

```
(base) C:\Users\santi\OneDrive\Desktop\santander>python tests\create_tutor_test.py
*************************************************
* test_create_tutor_error                       *
*************************************************
HTTP response code: 422
HTTP response body: {'detail': [{'type': 'int_parsing', 'loc': ['body', 'username'], 'msg': 'Input should be a valid integer, unable to parse string as an integer', 'input': 'foo', 'url': 'https://errors.pydantic.dev/2.6/v/int_parsing'}, {'type': 'missing', 'loc': ['body', 'nationality'], 'msg': 'Field required', 'input': {'username': 'foo', 'password': 'abc123', 'first_name': 'foo', 'last_name': 'foo'}, 'url': 'https://errors.pydantic.dev/2.6/v/missing'}, {'type': 'missing', 'loc': ['body', 'email'], 'msg': 'Field required', 'input': {'username': 'foo', 'password': 'abc123', 'first_name': 'foo', 'last_name': 'foo'}, 'url': 'https://errors.pydantic.dev/2.6/v/missing'}]}
.*************************************************
* test_create_tutors                            *
*************************************************
HTTP response code: 200
HTTP response body: {'username': 123456789, 'password': '123456789', 'first_name': 'foo', 'last_name': 'foo', 'nationality': 'foo', 'email': 'foo', 'message': 'El preceptor 123456789 se ha creado correctamente.'}
.
----------------------------------------------------------------------
Ran 2 tests in 0.057s

OK

(base) C:\Users\santi\OneDrive\Desktop\santander>
```

Si los tests unitarios fueron ejecutados correctamente, la herramienta deberia decir `OK` al final de los mismos.

**NOTA**: El servidor debe estar encendido para poder ejecutar estos tests.

### Habilitacion de alumnos
Un alumno puede encontrarse con estado activo (1) o pasivo (0).

> http://localhost:8000/set_student_status/

Supongamos que el preceptor Mike Barnett con DNI 76073275 quiere inhabilitar al alumno Peter Mcdonald con DNI 13628540. Lo primero que debe hacer es logearse:

> http://localhost:8000/login/?username=76073275&password=29cQDC3a

```
{
  "message": "Bienvenido preceptor 76073275"
}
```

Ahora debe inhabilitar al alumno 13628540:

> http://localhost:8000/set_student_status/?username=13628540&status=0

```
{
  "message": "El estado de activo para el estudiante 13628540 a sido cambiado a 0 satisfactoriamente."
}
```

Ahora el alumno se encuentra inahilitado. Un alumno deshabilitado no se considera para la asistencia del curso, y además queda inhabilitado para visualizar y/o modificar sus datos personales.

Si ahora el 13628540 quiere ver sus datos no podra:

> http://localhost:8000/login/?username=13628540&password=SzB7JUeG
> http://localhost:8000/my_profile/

```
{
  "message": "Alumno inhabilitado. No se pueden mostrar los datos. Contacte a su profesor."
}
```

Tampoco puede modificar sus datos:

> http://localhost:8000/update_student/?username=13628540&email=pmcdonald@school.com

```
{
  "message": "Alumno inhabilitado. No se pueden modificar los datos. Contacte a su profesor."
}
```