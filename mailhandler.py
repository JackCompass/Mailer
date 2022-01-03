# from __future__ import print_function
# from os import path
# from google.auth.transport.requests import Request
# from google.oauth2.credentials import Credentials
# import google_auth_oauthlib.flow
# from starlette.responses import RedirectResponse
#
#
# class Email:
#     def __init__(self):
#         self.scope = 'https://mail.google.com/'
#         self.creds = None
#         self.setup()
#
#     def setup(self):
#         """This function is going to do the basic setup for the email object"""
#         if path.exists('token.json'):
#             # If the path exists then we just use the token.json file and use to verify credentials
#             self.creds = Credentials.from_authorized_user_file('token.json', self.scope)
#
#         if not self.creds or not self.creds.valid:
#             if self.creds and self.creds.expired and self.creds.refresh_token:
#                 self.creds.refresh(Request())
#             else:
#                 flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
#                     'credentials.json', self.scope
#                 )
#                 flow.redirect_uri = 'https://mailcleaner.herokuapp.com/authenticated/'
#                 authorization_url, state = flow.authorization_url(
#                     access_type='offline',
#                     include_granted_scopes='true')
#                 return RedirectResponse(authorization_url)
#
#             # with open('token.json', 'w') as token:
#             #     token.write(self.creds.to_json())
#
#     def fetch_email(self):
#         # TODO: write a function which is going to fetch a number of emails
#         pass
#
#     def search_email(self):
#         # TODO: Write a function which is going to search and return emails with the search keyword
#         pass
#
#     def trash_email(self):
#         # TODO: Write a function which move selected emails to trash
#         pass
