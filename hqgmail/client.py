import httplib2

from apiclient.discovery import build
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run

def get_authenticated_service():
    # Path to the client_secret.json file downloaded from the Developer Console
    CLIENT_SECRET_FILE = 'client_secret.json'

    # Check https://developers.google.com/gmail/api/auth/scopes for all available scopes
    OAUTH_SCOPE = 'https://www.googleapis.com/auth/gmail.readonly'

    # Location of the credentials storage file
    STORAGE = Storage('gmail.storage')

    # Start the OAuth flow to retrieve credentials
    flow = flow_from_clientsecrets(CLIENT_SECRET_FILE, scope=OAUTH_SCOPE)
    http = httplib2.Http()

    # Try to retrieve credentials from storage or run the flow to generate them
    credentials = STORAGE.get()
    if credentials is None or credentials.invalid:
        credentials = run(flow, STORAGE, http=http)

    # Authorize the httplib2.Http object with our credentials
    http = credentials.authorize(http)

    # Build the Gmail service from discovery
    return build('gmail', 'v1', http=http)


class GmailClient(object):

    def __init__(self, service):
        self.service = service

    def iter_messages(self, q, howmany):
        remaining = howmany
        next_page = None
        while remaining > 0:
            kwargs = {}
            if next_page is not None:
                kwargs['pageToken'] = next_page
            results = self.service.users().messages().list(userId='me', q=q, **kwargs).execute()
            next_page = results.get('nextPageToken')
            if results['messages']:
                for message in results['messages']:
                    yield self.service.users().messages().get(userId='me', id=message['id']).execute()
                    remaining -= 1
                    if remaining <= 0:
                        break
                if next_page is None:
                    break
            else:
                break
