import json

import firebase_admin
from envyaml import EnvYAML
from firebase_admin import credentials
from google.cloud import secretmanager

env = EnvYAML('app.yaml')

DB_URL = env['env_variables']['DB_URL']
CRED_PATH = env['env_variables']['CRED_PATH']

PROJECT_ID = env['env_variables']['PROJECT_ID']
SECRET_ID = env['env_variables']['SECRET_ID']


def get_secret_manager_credentials():
    client = secretmanager.SecretManagerServiceClient()
    request = {"name": f"projects/{PROJECT_ID}/secrets/{SECRET_ID}/versions/latest"}
    response = client.access_secret_version(request)
    secret_string = response.payload.data.decode("UTF-8")
    service_account_info = json.loads(secret_string)
    return service_account_info


def init_database():
    cred = credentials.Certificate(get_secret_manager_credentials())

    firebase_admin.initialize_app(cred, {
        'databaseURL': DB_URL
    })
