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

# PythonAnywhere also requires this, since they limit MySQL connections
# to 3 at max. We leave two open just in case we need to service things
# early.
SQLALCHEMY_POOL_SIZE = 2

# Prevent overflowing (e.g. adding extra connections):
SQLALCHEMY_MAX_OVERFLOW = 0

# Disable query tracking (not needed, wasteful):
SQLALCHEMY_TRACK_MODIFICATIONS = False

# CAS Configuration
CAS_SERVER = "https://login.umd.edu"
CAS_AFTER_LOGIN = "route_root"
