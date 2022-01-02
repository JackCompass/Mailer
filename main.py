from fastapi import FastAPI
from handler import Email

app = FastAPI()


# Just a comment
@app.get("/")
def root():
    mymail = Email()
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
