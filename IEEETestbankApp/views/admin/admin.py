from flask.ext.security import current_user

def check_admin():
    print("ADMIN CHECK")
    print("RESULT = %s" % str((current_user and current_user.has_role('Administrator'))))
    return (current_user and current_user.has_role('Administrator'))
