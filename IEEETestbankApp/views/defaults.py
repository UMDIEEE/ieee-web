from flask.ext.security import current_user
from IEEETestbankApp.views.github import get_latest_github_commit

def get_default_template_kwargs():
    return {
        'user' : current_user,
        'sha'  : get_latest_github_commit(),
    }
