# Application configuration
# Non-sensitive configuration can go here!

# Flask-Security configuration

# Enable user tracking
SECURITY_TRACKABLE = True

# Enable account confirmation
SECURITY_CONFIRMABLE = True

# PythonAnywhere requires this, since MySQL connections have been set
# to close in 300s (5m).
SQLALCHEMY_POOL_RECYCLE = 200

# CAS Configuration
CAS_SERVER = "https://login.umd.edu"
CAS_AFTER_LOGIN = "route_root"
