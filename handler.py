# from __future__ import print_function
# from os import path
# from google.auth.transport.requests import Request
# from google.oauth2.credentials import Credentials
# from google_auth_oauthlib.flow import InstalledAppFlow
# from googleapiclient.discovery import build
# from googleapiclient.errors import HttpError
#
#
# class Email:
#     def __init__(self):
#         self.scope = 'https://mail.googel.com/'
#         self.creds = None
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
#                 flow = InstalledAppFlow.from_client_secrets_file(
#                     'credentials.json', self.scope
#                 )
#                 self.creds = flow.run_local_server(port=0)
#
#             with open('token.json', 'w') as token:
#                 token.write(self.creds.to_json())
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
