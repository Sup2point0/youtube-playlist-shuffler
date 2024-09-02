import os.path

from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

from config import ROOT


SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]


def authorise():
  creds = None

  # if os.path.exists(ROOT / "data" / "token.json"):
  #   creds = Credentials.from_authorized_user_file(
  #     ROOT / "data" / "token.json",
  #     scopes = SCOPES
  #   ).run_local_server(port = 0)

  # if not creds or not creds.valid:
  #   if creds and creds.expired and creds.refresh_token:
  #     creds.refresh(Request())
      
  #   else:
  flow = InstalledAppFlow.from_client_secrets_file(
    ROOT / "data" / "credentials.json",
    scopes = SCOPES
  )
  creds = flow.run_local_server(port = 0)

  with open(ROOT / "data" / "token.json", "w") as dest:
    dest.write(creds.to_json())

  return build("youtube", "v3", credentials = creds)
