import fastapi
from fastapi import FastAPI, Response
from starlette.responses import RedirectResponse
from os import path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import google_auth_oauthlib.flow
import json
import os
from pydantic import BaseModel
from fastapi_sessions.frontends.implementations import SessionCookie, CookieParameters
from fastapi_sessions.session_verifier import SessionVerifier
from fastapi_sessions.backends.implementations import InMemoryBackend

from uuid import UUID, uuid4
from fastapi import HTTPException, Response, Depends

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://mail.google.com/']

cookie_params = CookieParameters()
cookie = SessionCookie(cookie_name='authentication_state', identifier='state', auto_error=True, secret_key='saviour',
                       cookie_params=cookie_params)


class SessionData(BaseModel):
    state: str


backend = InMemoryBackend[UUID, SessionData]()


class BasicVerifier(SessionVerifier[UUID, SessionData]):
    def __init__(
            self,
            *,
            identifier: str,
            auto_error: bool,
            backend: InMemoryBackend[UUID, SessionData],
            auth_http_exception: HTTPException,
    ):
        self._identifier = identifier
        self._auto_error = auto_error
        self._backend = backend
        self._auth_http_exception = auth_http_exception

    @property
    def identifier(self):
        return self._identifier

    @property
    def backend(self):
        return self._backend

    @property
    def auto_error(self):
        return self._auto_error

    @property
    def auth_http_exception(self):
        return self._auth_http_exception

    def verify_session(self, model: SessionData) -> bool:
        """If the session exists, it is valid"""
        return True


verifier = BasicVerifier(
    identifier="state",
    auto_error=True,
    backend=backend,
    auth_http_exception=HTTPException(status_code=403, detail="invalid session"),
)

app = FastAPI()


# Just a comment
@app.get("/")
async def root(response: Response, request: fastapi.Request):
    print(request.url)
    session = uuid4()
    data = SessionData(state='')
    await backend.create(session, data)
    cookie.attach_to_response(response, session)
    return 'Welcome to the application'


@app.get("/hello/", dependencies=[Depends(cookie)])
async def say_hello(session_data: SessionData = Depends(verifier)):
    print(session_data.username)
    return {"message": f"Hello"}


@app.get('/verify', dependencies=[Depends(cookie)])
async def verify_account(session_data: SessionData = Depends(verifier), session_id: UUID = Depends(cookie)):
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
            await backend.update(session_id, SessionData(state=state))
            return RedirectResponse(authorization_url)
    else:
        return {'message': 'failure again'}


@app.get('/authenticated/', dependencies=[Depends(cookie)])
def authenticate(session_data: SessionData = Depends(verifier)):
    state = session_data.state
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        'credentials.json', SCOPES, state=state)
    flow.redirect_uri = 'https://mailcleaner.herokuapp.com/authenticated/'
    authorization_response = str(fastapi.Request.url)
    flow.fetch_token(authorization_response=authorization_response)
    try:
        with open('token.json', 'w') as token:
            token.write(flow.credentials.to_json())
        message = 'successful'
    except:
        message = 'unsuccessful'
    return {'message': f'{message}'}
