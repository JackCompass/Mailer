from fastapi import FastAPI, Request, Response
from starlette.responses import RedirectResponse
from __future__ import print_function
from os import path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import google_auth_oauthlib.flow
import os

app = FastAPI()

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://mail.google.com/']


# Just a comment
@app.get("/")
def root():
    return 'Welcome to the application'


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.get('/verify')
def verify_account():
    """Shows basic usage of the Gmail API.
        Lists the user's Gmail labels.
        """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
                'credentials.json', SCOPES)
            flow.redirect_uri = 'https://mailcleaner.herokuapp.com/authenticated/'
            authorization_url, state = flow.authorization_url(access_type='offline', include_granted_scopes='true')
            return RedirectResponse(authorization_url)
    else:
        return {'message': 'failure again'}


@app.get('/authencticated/')
def authenticate():
    return {'message': 'You got authenticated'}
