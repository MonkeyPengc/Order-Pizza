
import sqlite3
import random
import hashlib

try:
    from string import ascii_letters as letters ## python 3

except ImportError:
    from string import letters  ## python 2


class adminDB:
    """ 
    Database that stores account records of users having access
    to the sales database. 
    """

    def __init__(self):
        self.openConn()
        self.createTable()

    def createTable(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS admins (adminID INTEGER PRIMARY KEY AUTOINCREMENT, UserName TEXT NOT NULL UNIQUE, PasswordHash TEXT NOT NULL)")
    
    def openConn(self):
        self.conn = sqlite3.connect('admin_account.db')
        self.cursor = self.conn.cursor()
    
    def closeConn(self):
        self.cursor.close()
        self.conn.close()

    def queryByName(self, name):
        """ 
        return a record if the username is already exists
        else return empty.
        """
        
        try:
            # avoid sql injection
            res = self.cursor.execute("SELECT UserName, PasswordHash FROM admins WHERE UserName = ?", (name,)).fetchone()
            return res
        
        except sqlite3.ProgrammingError:
            self.openConn()
            res = self.cursor.execute("SELECT UserName, PasswordHash FROM admins WHERE UserName = ?", (name,)).fetchone()
            return res

    def login(self, name, password, pw_hash):
        """ 
        check whether a user is valid by matching hash value of 
        the user record in database with a hash value generated
        by the inputs from current user.
        """
    
        salt = pw_hash.split(',')[0]
        return pw_hash == self.hashPassword(name, password, salt)

    def hashPassword(self, name, pw, salt=None):
        if not salt:
            salt = self.makeSalt()
        
        encoded_line = (name + pw + salt).encode('utf-8')
        h = hashlib.sha256(encoded_line).hexdigest()
        
        return "%s,%s" % (salt, h)
    
    def makeSalt(self):
        length=5
        return ''.join(random.choice(letters) for x in range(length))




