from flask import Flask, render_template, redirect, url_for, flash
from flask.ext.security import login_required, current_user
from flask_menu import register_menu
from IEEETestbankApp import app
from IEEETestbankApp.models.auth import Config

from apiclient import discovery, errors
from oauth2client import client
import httplib2
import copy

# Browse page

def retrieve_all_files(service, path, folder_id):
    """Retrieve a list of File resources.
    
    Args:
        service: Drive API service instance.
    Returns:
        List of File resources.
    """
    
    page_token = None
    
    path = [p for p in path.split("/") if p.strip() != ""]
    old_path_len = len(path)
    
    while len(path) > 0:
        result_folders = []
        result_files   = []
        
        print("[browse.py] Searching for: %s" % path[0])
        while True:
            try:
                param = {}
                if page_token:
                    param['pageToken'] = page_token
                
                files = service.files().list(q = ("'%s' in parents" % folder_id), **param).execute()
                
                #result.extend(files['items'])
                for f in files['items']:
                    print("ENTRY: %s" % str(f))
                    if f.get('mimeType') == "application/vnd.google-apps.folder":
                        if f.get('title') != None:
                            if f.get('title') == path[0]:
                                folder_id = f.get('id')
                                path = path[1:]
                                break
                            result_folders.append([f.get('title'), copy.deepcopy(f)])
                    else:
                        if f.get('title') != None:
                            result_files.append([f.get('title'), copy.deepcopy(f)])
                
                page_token = files.get('nextPageToken')
                
                if not page_token:
                    break
                if len(path) != old_path_len:
                    break
            except errors.HttpError:
                _, err, _ = sys.exc_info()
                print('An error occurred: %s' % err)
                break
        
        if len(path) != old_path_len:
            # Traverse again!
            pass
        else:
            print("[browse.py] Could not locate directory, bailing.")
            flash("Base directory not found!")
            results_folders = []
            results_files = []
    
    # Sort by name, case-insensitive
    result_folders = sorted(result_folders, key=(lambda t: t[0].lower()))
    result_files = sorted(result_files, key=(lambda t: t[0].lower()))
    
    return result_folders, result_files

# Views
@app.route('/browse')
@register_menu(app, 'main.browse', 'Browse', order = 1)
def browse():
    config_gdrive_cred = Config.query.filter_by(name='gdrive_oauth2_credentials').first()
    config_gdrive_folder = Config.query.filter_by(name='gdrive_folder').first()
    
    if not config_gdrive_cred:
        flash("Something went wrong with accessing the files. Oops!")
        return redirect(url_for('home'))
    
    if not config_gdrive_folder:
        flash("Someone forgot to set the right folder, at the right time... Oops!")
        return redirect(url_for('home'))
    
    credentials = client.OAuth2Credentials.from_json(config_gdrive_cred.value)
    http_auth = credentials.authorize(httplib2.Http())
    drive_service = discovery.build('drive', 'v2', http_auth)
    folders_list, files_list = retrieve_all_files(drive_service, config_gdrive_folder.value, "root")
    
    print(folders_list)
    print(files_list)
    
    return render_template('browse.html', user = current_user, files = files_list, folders = folders_list)

