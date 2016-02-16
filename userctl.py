from IEEETestbankApp.security import user_datastore, security
from IEEETestbankApp.models.db import db, initDatabase
from IEEETestbankApp.models.auth import User, Role, Config
from IEEETestbankApp.forms.security.register import major_choices, \
                                             grad_semester_choices

import sys

def confirm():
    while 1:
        yn = input("Confirm? [y/n] ")
        if yn and len(yn) > 0:
            if yn.lower()[0] == "y":
                return True
            elif yn.lower()[0] == "n":
                return False
            else:
                print("Invalid option!")

def intinput(field):
    while 1:
        field_in = input("%s: " % field)
        
        if not field_in.isdigit():
            print("Invalid %s - you need to specify a number!")
        else:
            return int(field_in)

def select(field, options):
    while 1:
        print("For %s, select from the following:" % field)
        print("=============================================")
        cur = 1
        for opt in options:
            print(" %i) %s" % (cur, opt[1]))
            cur += 1
        choice = intinput(field)
        
        if (choice > 0) and (choice <= len(options)):
            print("You selected choice %i: %s." % (choice, options[choice - 1][1]))
            if confirm(): break
        else:
            print("Invalid choice!")
    
    return options[choice - 1]

def addUser(user):
    while 1:
        print("Creating a new user!")
        username = input("Username: ")
        first_name = input("First Name: ")
        last_name = input("Last Name: ")
        major_act, major_pretty = select("Major", major_choices)
        grad_sem_act, grad_sem_pretty = select("Graduation Semester", grad_semester_choices)
        grad_year = intinput("Graduation Year: ")
        
        print("Confirm the new user:")
        print("=====================")
        
        print("Username: %s" % username)
        print("First Name: %s" % first_name)
        print("Last Name: %s" % last_name)
        print("Major: %s" % major_pretty)
        print("Graduation: %s %i" % (grad_sem_pretty, grad_year))
        print("\n")
        
        if confirm(): break
    
    new_user = user_datastore.create_user(username = username,
                                    first_name = first_name,
                                    last_name = last_name,
                                    major = major_act,
                                    grad_semester = grad_sem_act,
                                    grad_year = grad_year
                                  )
    db.session.commit()

def addRole():
    while 1:
        print("Creating a new role!")
        new_name = input("Role name: ")
        new_description = input("Role description: ")
        
        print("Confirm the new role:")
        print("=====================")
        print("Name: %s" % new_name)
        print("Description:")
        print(new_description)
        print("\n")
        
        if confirm(): break
    
    user_datastore.create_role(name = new_name,
                                description = new_description)
    db.session.commit()

def addRoleToUser():
    users = User.query.all()
    roles = Role.query.all()
    
    # Preprocess
    user_opts = []
    for user in users:
        user_opts.append([user, "%s %s (%s)" % (user.first_name, user.last_name, user.username)])
    
    role_opts = []
    for role in roles:
        role_opts.append([role, "%s - %s" % (role.name, role.description)])
    
    while 1:
        user_select, user_select_str = select("User", user_opts)
        role_select, role_select_str = select("Role", role_opts)
        
        print("Confirm adding role to user:")
        print("============================")
        print("User: %s" % user_select_str)
        print("Role: %s" % role_select_str)
        print("\n")
        
        if confirm(): break
    
    user_datastore.add_role_to_user(user_select, role_select)
    db.session.commit()

def removeRoleFromUser():
    users = User.query.all()
    
    # Preprocess
    user_opts = []
    for user in users:
        users_opts.append([user, "%s %s (%s)" % (user.first_name, user.last_name, user.username)])
    
    while 1:
        user_select, user_select_str = select("User", user_opts)
        
        role_opts = []
        roles = user_select.roles
        for role in roles:
            role_opts.append([role, "%s - %s" % (role.name, role.description)])
        
        role_select, role_select_str = select("Role", role_opts)
        
        print("Confirm removing role from user:")
        print("================================")
        print("User: %s" % user_select_str)
        print("Role: %s" % role_select_str)
        print("\n")
        
        if confirm(): break
    
    user_datastore.remove_role_from_user(user_select, role_select)
    db.session.commit()

def deleteUser():
    users = User.query.all()
    
    # Preprocess
    users_opts = []
    for user in users:
        users_opts.append([user, "%s %s (%s)" % (user.first_name, user.last_name, user.username)])
    
    while 1:
        user_select, user_select_str = select("User", user_opts)
        
        print("Confirm deleting user:")
        print("======================")
        print("User: %s" % user_select_str)
        print("\n")
        
        if confirm(): break
    
    user_datastore.delete_user(user_select)
    db.session.commit()

def listUsers():
    users = User.query.all()
    
    print("Users:")
    print("======")
    for user in users:
        print(" * %s %s (%s)" % (user.first_name, user.last_name, user.username))
        print("     Major:      %s" % (user.major))
        print("     Graduation: %s %i" % (user.grad_semester, user.grad_year))
        print("     Roles:      %s" % ", ".join([r.name for r in user.roles]))
    print("")

def listRoles():
    roles = Role.query.all()
    
    print("Roles:")
    print("======")
    for role in roles:
        print(" * %s" % (role.name))
        print("   %s" % (role.description))
    print("")

def listConfig():
    configs = Config.query.all()
    
    print("Configuration:")
    print("==============")
    for config in configs:
        print(" * %s" % (config.name))
        print("   %s" % (config.description))
        print("   %s" % (config.value))
    print("")

def main():
    while 1:
        menu_opts = [
                        [addUser,            "Add User"],
                        [addRole,            "Add Role"],
                        [addRoleToUser,      "Add Role to User"],
                        [removeRoleFromUser, "Remove Role from User"],
                        [listUsers,          "List Users"],
                        [listRoles,          "List Roles"],
                        [listConfig,          "List Config"],
                        [deleteUser,         "Delete User"],
                        [sys.exit,           "Exit"],
                    ]
        menu_pick = select("Command", menu_opts)
        print("Selected: %s" % menu_pick[1])
        menu_pick[0]()

if __name__ == "__main__":
    main()
