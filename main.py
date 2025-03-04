from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
def index():
    return {"Mountblue_emp":{"id":1,"name":"faiz"}}


@app.get("/blog/parameter")
def blog_parameter():
    return {"this is blog parameter"}

@app.get("/about")
def about():
    return {"data":"This is about page"}

@app.get("/blog/{id}")
def blog_id(id:int):
    return {"blog" : {"this is ",id," blog"}}

@app.get("/blog/desc/{id}")
def blog_desc(id):
    return {"blog":"description of blog number"+id}



# query parameters
@app.get("/greet")
def greet(name:str = "unknown",age:int = 20):
    return {"message":f"his name is {name} and age is {age}"}


#request body
class User(BaseModel):
    name :str
    email: str
    phone_no : int
    age : int

@app.post("/adduser")
def add_user(request:User):
    return {"message":f"user {request.name} add successfully","date":request}



