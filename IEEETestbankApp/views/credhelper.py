from oauth2client import client
from IEEETestbankApp.models.auth import Config
from IEEETestbankApp.models.db import db

def fetch_latest_cred(val):
    credentials = client.OAuth2Credentials.from_json(val)
    if credentials.access_token_expired:
        print('[credhelper.py] Detected credential expiration, refreshing tokens.')
        credentials.refresh()
        store_cred(credentials)
    return credentials

def store_cred(credentials):
    config_gdrive_cred = Config.query.filter_by(name='gdrive_oauth2_credentials').first()
    if config_gdrive_cred != None:
        config_gdrive_cred.value = credentials.to_json()
    else:
        new_cred = Config(name = 'gdrive_oauth2_credentials',
                            value = credentials.to_json(),
                            description = "IEEE@UMD Testbank <-> Google Drive Credentials")
        db.session.add(new_cred)
    db.session.commit()
