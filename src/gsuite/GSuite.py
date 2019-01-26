import json

from httplib2                  import Http
from oauth2client              import file, client
from oauth2client.tools        import argparser
from oauth2client.tools        import run_flow

from googleapiclient.discovery import build

from utils.Dev import Dev
from utils.Files               import Files
from utils.aws.secrets         import Secrets


class GSuite:
    def __init__(self):
        self.gsuite_secret_id = 'gsuite_token'

    # this function will prompt the user if there isn't a local tmp file with a token for the requested scope
    # the main credentials are stored using AWS Secrets (in the id defined at self.gsuite_secret_id)
    def get_oauth_token(self, desired_scope):
        secret_data      = json.loads(Secrets(self.gsuite_secret_id).value())                       # load secret from AWS Secrets store
        credentials_file = '/tmp/gsuite_credentials.json'                                           # file to hold the credentials.json value
        Files.write(credentials_file, secret_data['credentials.json'])                              # save value received from AWS into file

        token_file    = '/tmp/gmail_credential_{0}.json'.format(desired_scope)                      # this is the tmp file with the token value for the desired scope
        if not Files.exists(token_file):                                                            # if the file does not exist

            store         = file.Storage(token_file)                                                # create a gsuite Storage object
            scopes        = 'https://www.googleapis.com/auth/{0}'.format(desired_scope)             # full qualified name for the desired scopes

            flow = client.flow_from_clientsecrets(credentials_file, scopes)                         # create a gsuite flow object
            flags = argparser.parse_args('--auth_host_name localhost --logging_level INFO'.split()) # configure the use of a localhost server to received the oauth response
            run_flow(flow, store, flags)                                                            # open browser and prompt user to follow the OAuth flow

            Files.delete(credentials_file)                                                          # delete main gsuite credentials file (since we don't want it hanging around)

        return token_file                                                                           # return file with token credentials

    # this creates the credentials object required to create the GSuite service object
    def get_oauth_creds(self, desired_scope):
        token_file = self.get_oauth_token(desired_scope)        # get the token file
        store       = file.Storage(token_file)                  # create Storage object from file
        creds       = store.get()                               # extract GSuite creds value
        return creds

    def create_service(self,serviceName, version, scope):
        return build(serviceName, version, http=self.get_oauth_creds(scope).authorize(Http()))

    # helper files to create individual GSuite service objects
    def admin_reports_v1(self):
        return self.create_service('admin', 'reports_v1','admin.reports.audit.readonly')

    def drive_v3(self):
        return self.create_service('drive', 'v3', 'drive.metadata.readonly')