import unittest
import requests

class UnitTest(unittest.TestCase):

    def test_create_tutors(self, ntutors=1):
        
        print("*************************************************")
        print("* test_create_tutors                            *")
        print("*************************************************")
        
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
        
        for k in range(ntutors):
            # Datos del estudiante
            tutor_data = {
                "username": '123456789',
                "password": '123456789',
                "first_name": 'foo',
                "last_name": 'foo',
                "nationality": 'foo',
                "email": 'foo'
            }
            
            # Realizar la solicitud POST
            response = requests.post("http://127.0.0.1:8000/add_tutor/", json=tutor_data)
            
            # Muestro la respuesta del servidor
            print('HTTP response code: {}'.format( response.status_code ) )
            print('HTTP response body: {}'.format( response.json() ) )
            
            # Verificar que la solicitud fue exitosa (código de estado 200)
            self.assertEqual(response.status_code, 200)
            
            # Verificar que la respuesta contiene los datos del estudiante
            response_data = response.json()
            self.assertEqual(str(response_data["username"]), tutor_data["username"])
            self.assertEqual(str(response_data["password"]), tutor_data["password"])
            self.assertEqual(str(response_data["first_name"]), tutor_data["first_name"])
            self.assertEqual(str(response_data["last_name"]), tutor_data["last_name"])
            self.assertEqual(str(response_data["nationality"]), tutor_data["nationality"])
            self.assertEqual(str(response_data["email"]), tutor_data["email"])

        # Se cierra la sesion
        response = requests.get(
            "http://127.0.0.1:8000/logoff/",
            )

    def test_create_tutor_error(self):
        
        print("*************************************************")
        print("* test_create_tutor_error                       *")
        print("*************************************************")
        
        # Se inicia sesion como administrador
        response = requests.get(
            "http://127.0.0.1:8000/login/",
            params={"username": "admin", "password": "admin"}
            )
        
        # Datos de estudiante con datos faltantes (esto debería provocar un error)
        invalid_tutor_data = {
            "username": "foo",
            "password": "abc123",
            "first_name": "foo",
            "last_name": "foo"
        }

        # Llamada a la API para agregar el estudiante con datos faltantes
        response = requests.post("http://127.0.0.1:8000/add_tutor/", json=invalid_tutor_data)

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