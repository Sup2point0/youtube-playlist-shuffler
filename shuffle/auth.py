from config import SCRIPT

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


def authorise():
  flow = InstalledAppFlow.from_client_secrets_file(
    SCRIPT / "credentials.json",
    scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]
  )
  creds = flow.run_local_server(port = 0)

  return build("youtube", "v3", credentials = creds)
