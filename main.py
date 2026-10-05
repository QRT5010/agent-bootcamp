from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Course(BaseModel):
    name: str
    credit: float

@app.get("/")
def read_root():
    return {"msg": "hello"}

@app.get("/greet/{name}")
def greet(name: str):
    return {"msg": f"hello, {name}"}

@app.post("/courses")
def create_course(course: Course):
    return {"received": course, "msg": "收到课程"}
