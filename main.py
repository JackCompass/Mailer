from fastapi import FastAPI, Request, Response
from starlette.responses import RedirectResponse
from mailhandler import Email

app = FastAPI()


# Just a comment
@app.get("/")
def root():
    return 'Welcome to the application'


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.get('/verify')
def verify_account():
    return Email()


@app.get('/authencticated/')
def authenticate():
    return {'message': 'You got authenticated'}
