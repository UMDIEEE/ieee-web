from IEEETestbankApp import app
from IEEETestbankApp.models.auth import Config
from IEEETestbankApp.models.db import db
from flask import Flask, render_template, request, redirect, url_for, jsonify
import hmac
import hashlib
import subprocess
import os

def pythonanywhere_touch(fname, mode=0o666, dir_fd=None, **kwargs):
    flags = os.O_CREAT | os.O_APPEND
    with os.fdopen(os.open(fname, flags=flags, mode=mode, dir_fd=dir_fd)) as f:
        os.utime(f.fileno() if os.utime in os.supports_fd else fname,
            dir_fd=None if os.supports_fd else dir_fd, **kwargs)

# Compare the HMAC hash signature
def verify_hmac_hash(data, signature):
    gh_secret = bytes(app.config['GITHUB_SECRET'], 'UTF-8')
    mac = hmac.new(gh_secret, msg=data, digestmod=hashlib.sha1)
    return hmac.compare_digest('sha1=' + mac.hexdigest(), signature)

def update_latest_github_commit(commit_hash):
    config_github_commit = Config.query.filter_by(name='github_commit').first()
    if config_github_commit != None:
        config_github_commit.value = commit_hash
        db.session.commit()
    else:
        config_github_commit = Config(name = 'github_commit',
                        value = commit_hash,
                        description = "Latest GitHub Commit Hash")
        db.session.add(config_github_commit)
        db.session.commit()

def get_latest_github_commit():
    config_github_commit = Config.query.filter_by(name='github_commit').first()
    if config_github_commit != None:
        return config_github_commit.value
    return None

# Flask route that will process the payload
@app.route("/api/github_payload", methods=['POST'])
def ghpayload():
    signature = request.headers.get('X-Hub-Signature')
    data = request.data
    if verify_hmac_hash(data, signature):
        if request.headers.get('X-GitHub-Event') == "ping":
            return jsonify({'msg': 'Ok'})
        if request.headers.get('X-GitHub-Event') == "push":
            payload = request.get_json()
            if payload['commits'][0]['distinct'] == True:
                update_latest_github_commit(payload['commits'][0]['id'])
                proc = subprocess.Popen(
                    ['git', 'pull', 'origin', 'master'],
                    cwd=os.path.dirname(os.path.realpath(__file__)),
                    stdout=subprocess.PIPE)
                cmd_output, err = p.communicate()
                pythonanywhere_touch(app.config['WSGI_CONFIG_FILE'])
                return jsonify({'msg': str(cmd_output)})
    else:
        return jsonify({'msg': 'invalid hash'})
        
