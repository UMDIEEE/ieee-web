from IEEETestbankApp.models.db import db, initDatabase
from IEEETestbankApp.models.auth import User, Role

print("Confirm that you want to nuke tables by pressing ENTER 10 times.")

for i in range(0, 10):
    input()

db.drop_all()
#initDatabase()
