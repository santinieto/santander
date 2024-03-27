from pydantic import BaseModel

# Definir un modelo de datos Pydantic para los datos del estudiante
class Student(BaseModel):
    username: int
    password: str
    first_name: str
    last_name: str
    nationality: str
    email: str