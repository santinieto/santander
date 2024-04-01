import unittest
import requests
import http.client
import json

import sys
sys.path.append('./src')

from utils import new_user

class UnitTest(unittest.TestCase):

    def test_create_student(self, nstudents=50):
        
        for k in range(nstudents):
            # Datos del estudiante
            student_data = new_user()
            
            # Realizar la solicitud POST
            response = requests.post("http://127.0.0.1:8000/add_student/", json=student_data)
            
            # Muestro la respuesta del servidor
            # print('HTTP response code: {}'.format( response.status_code ) )
            # print('HTTP response body: {}'.format( response.json() ) )
            
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

    def test_create_teacher(self, nteachers = 5):
        
        for k in range(nteachers):
            # Datos del estudiante
            teacher_data = new_user()
            
            # Realizar la solicitud POST
            response = requests.post("http://127.0.0.1:8000/add_teacher/", json=teacher_data)
            
            # Muestro la respuesta del servidor
            # print('HTTP response code: {}'.format( response.status_code ) )
            # print('HTTP response body: {}'.format( response.json() ) )
            
            # Verificar que la solicitud fue exitosa (código de estado 200)
            self.assertEqual(response.status_code, 200)
            
            # Verificar que la respuesta contiene los datos del estudiante
            response_data = response.json()
            self.assertEqual(response_data["username"], teacher_data["username"])
            self.assertEqual(response_data["password"], teacher_data["password"])
            self.assertEqual(response_data["first_name"], teacher_data["first_name"])
            self.assertEqual(response_data["last_name"], teacher_data["last_name"])
            self.assertEqual(response_data["nationality"], teacher_data["nationality"])
            self.assertEqual(response_data["email"], teacher_data["email"])

if __name__ == '__main__':
    unittest.main()