
import sys
import re
import sqlite3
from database.admin_database import adminDB

class adminInterface(adminDB):
    """ 
    An interface for add/remove users in admin database,
    registered users have access to the sales management.
    """
    
    def __init__(self, username, password=None):
        super().__init__()
        self.name = username
        self.pw = password
        self.pw_hash = None
    
    def register(self):
        """ register a new user """
        
        if not self.validUsername():
            print("Invalid username!")
            return
        
        elif not self.validPassword():
            print("Invalid password!")
            return
        
        else:
            if self.queryByName(self.name):
                print("User already exists!")
                return
            
            self.pw_hash = self.hashPassword(self.name, self.pw)
            self.addAccount(self.name, self.pw_hash)

    def validUsername(self):
        USER_REGEX = re.compile(r"""^[a-zA-Z0-9_-]{3,20}$""")
        
        return self.name and USER_REGEX.match(self.name)
    
    def validPassword(self):
        PASS_REGEX = re.compile(r"""^.{3,20}$""")
        
        return self.pw and PASS_REGEX.match(self.pw)

    def addAccount(self, name, hash):
        """ add a new user to the admin database """
        
        try:
            # avoid sql injection
            self.cursor.execute("INSERT INTO admins (UserName, PasswordHash) VALUES (?, ?)", (name, hash))
        
        except sqlite3.ProgrammingError:
            self.openConn()
            self.cursor.execute("INSERT INTO admins (UserName, PasswordHash) VALUES (?, ?)", (name, hash))
            
        finally:
            self.conn.commit()
            self.closeConn()
    
    def cancel(self):
        """ cancel an existing user """
        
        if not self.validUsername():
            print("Invalid username!")
            return

        else:
            if not self.queryByName(self.name):
                print("Not an existing user!")
                return

            self.removeAccount(self.name)

    def removeAccount(self, name):
        """ remove a user from admin database """

        try:
            self.cursor.execute("DELETE FROM admins WHERE UserName = ?", (name,))

        except sqlite3.ProgrammingError:
            self.openConn()
            self.cursor.execute("DELETE FROM admins WHERE UserName = ?", (name,))
        
        finally:
            self.conn.commit()
            self.closeConn()


if __name__ == "__main__":
    
    try:
        ask = int(input("Add or Remove an account? (add:1, remove:0)"))
    
    except ValueError:
        print("Please type 1/0!")
        sys.exit(0)

    if ask == 1:
        try:
            username = input("Enter a user name: ")
            password = input("Enter a password: ")
            adm = adminInterface(username, password)
    
        except Exception as e:
            print(e)
            sys.exit(1)

        adm.register()

    elif ask == 0:
        try:
            username = input("Enter a user name: ")
            adm = adminInterface(username)
        
        except Exception as e:
            print(e)
            sys.exit(1)

        adm.cancel()


