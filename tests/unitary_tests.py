import unittest
import requests
import http.client
import json
from src.utils import create_student

class UnitTest(unittest.TestCase):

    def test_create_student(self):
        # Datos del estudiante
        student_data = create_student()
        
        # Realizar la solicitud POST
        response = requests.post("http://127.0.0.1:8000/add_student/", json=student_data)
        
        # Muestro la respuesta del servidor
        print('HTTP response code: {}'.format( response.status_code ) )
        print('HTTP response body: {}'.format( response.json() ) )
        
        # Verificar que la solicitud fue exitosa (código de estado 200)
        self.assertEqual(response.status_code, 200)
        
        # Verificar que la respuesta contiene los datos del estudiante
        response_data = response.json()
        self.assertEqual(response_data["username"], student_data["username"])
        self.assertEqual(response_data["password"], student_data["password"])
        self.assertEqual(response_data["first_name"], student_data["first_name"])
        self.assertEqual(response_data["last_name"], student_data["last_name"])
        self.assertEqual(response_data["nationality"], student_data["nationality"])
        self.assertEqual(response_data["email"], student_data["email"])

if __name__ == '__main__':
    unittest.main()