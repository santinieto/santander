import unittest
import requests

class UnitTest(unittest.TestCase):

    def test_create_students(self, nstudents=1):
        # Se inicia sesion como administrador
        response = requests.get(
            "http://127.0.0.1:8000/login/",
            params={"username": "admin", "password": "admin"}
            )
        
        # Verificar que el login fue exitoso (código de estado 200)
        self.assertEqual(response.status_code, 200)
        
        # # Muestro la respuesta del servidor
        # print('HTTP response code: {}'.format( response.status_code ) )
        # print('HTTP response body: {}'.format( response.json() ) )
        
        for k in range(nstudents):
            # Datos del estudiante
            student_data = {
                "username": '123456789',
                "password": '123456789',
                "first_name": 'foo',
                "last_name": 'foo',
                "nationality": 'foo',
                "email": 'foo'
            }
            
            # Realizar la solicitud POST
            response = requests.post("http://127.0.0.1:8000/add_student/", json=student_data)
            
            # Muestro la respuesta del servidor
            print('HTTP response code: {}'.format( response.status_code ) )
            print('HTTP response body: {}'.format( response.json() ) )
            
            # Verificar que la solicitud fue exitosa (código de estado 200)
            self.assertEqual(response.status_code, 200)
            
            # Verificar que la respuesta contiene los datos del estudiante
            response_data = response.json()
            self.assertEqual(str(response_data["username"]), student_data["username"])
            self.assertEqual(str(response_data["password"]), student_data["password"])
            self.assertEqual(str(response_data["first_name"]), student_data["first_name"])
            self.assertEqual(str(response_data["last_name"]), student_data["last_name"])
            self.assertEqual(str(response_data["nationality"]), student_data["nationality"])
            self.assertEqual(str(response_data["email"]), student_data["email"])

        # Se cierra la sesion
        response = requests.get(
            "http://127.0.0.1:8000/logoff/",
            )

    def test_create_student_error(self):
        # Se inicia sesion como administrador
        response = requests.get(
            "http://127.0.0.1:8000/login/",
            params={"username": "admin", "password": "admin"}
            )
        
        # Datos de estudiante con datos faltantes (esto debería provocar un error)
        invalid_student_data = {
            "username": "foo",
            "password": "abc123",
            "first_name": "foo",
            "last_name": "foo"
        }

        # Llamada a la API para agregar el estudiante con datos faltantes
        response = requests.post("http://127.0.0.1:8000/add_student/", json=invalid_student_data)

        # Verificar el código de respuesta (debería ser un error 500)
        self.assertNotEqual(response.status_code, 200)
        
        # Muestro la respuesta del servidor
        print('HTTP response code: {}'.format( response.status_code ) )
        print('HTTP response body: {}'.format( response.json() ) )

        # Se cierra la sesion
        response = requests.get(
            "http://127.0.0.1:8000/logoff/",
            )
        
if __name__ == '__main__':
    unittest.main()