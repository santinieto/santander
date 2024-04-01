from pydantic import BaseModel

# Definir un modelo de datos Pydantic para los datos del estudiante
class Student(BaseModel):
    username: int
    password: str
    first_name: str
    last_name: str
    nationality: str
    email: str
    active: str

# Definir un modelo de datos Pydantic para los datos del profesor
class Teacher(BaseModel):
    username: int
    password: str
    first_name: str
    last_name: str
    nationality: str
    email: str

# Definir un modelo de datos Pydantic para los datos del preceptor
class Tutor(BaseModel):
    username: int
    password: str
    first_name: str
    last_name: str
    nationality: str
    email: str