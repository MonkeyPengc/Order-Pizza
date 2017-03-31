
import sqlite3
import datetime


class Database:
    """
    Parent database class. Set check_same_thread to False, 
    because by default SQLite objects created in a thread
    can only be used in that same thread.
    """
    
    def __init__(self):
        self.conn = sqlite3.connect('customers_orders.db', check_same_thread=False)
        self.cursor = self.conn.cursor()
        
    def CreateTable(self):
        raise NotImplementedError


class Customers(Database):
    """
    A table for recording customers information.
    Attributes (CustomerID, CustomerName, Address)
    """
    
    def __init__(self):
        super().__init__()
        self.CreateTable()
    
    def CreateTable(self):
        self.cursor.execute('CREATE TABLE IF NOT EXISTS customers (CustomerID INTEGER PRIMARY KEY AUTOINCREMENT, CustomerName TEXT, Address TEXT)')

    def AllocateCustomerID(self, name, addr=None):
        # name is required, and address is optional.
        
        try:
            self.cursor.execute('SELECT MAX (CustomerID) FROM customers')
        
        except sqlite3.ProgrammingError:
            self.conn = sqlite3.connect('customers_orders.db', check_same_thread=False)
            self.cursor = self.conn.cursor()
            self.cursor.execute('SELECT MAX (CustomerID) FROM customers')
    
        try:
            cid = self.cursor.fetchone()[0] + 1
        
        except TypeError:
            cid = 1
        
        finally:
            self.cursor.execute('INSERT INTO customers (CustomerName, Address) VALUES(?, ?)', (name, addr))
            self.conn.commit()
            
        return cid


class OrderInventory(Database):
    """
    A table for recording order details.
    Attributes (OrderID, CustomerID, OrderDate, Price)
    """
    
    def __init__(self):
        super().__init__()
        self.CreateTable()
    
    def CreateTable(self):
        self.cursor.execute('CREATE TABLE IF NOT EXISTS orderInventory (OrderID INTEGER PRIMARY KEY AUTOINCREMENT, CustomerID INT, OrderDate TEXT, OrderPrice REAL)')
    
    def InsertOrder(self, cid, price):
        date = datetime.datetime.today().strftime('%Y-%m-%d %H-%M-%S')

        try:
            self.cursor.execute('INSERT INTO orderInventory (CustomerID, OrderDate, OrderPrice) VALUES(?, ?, ?)', (cid, date, price))
        
        except sqlite3.ProgrammingError:
            self.conn = sqlite3.connect('customers_orders.db', check_same_thread=False)
            self.cursor = self.conn.cursor()
            self.cursor.execute('INSERT INTO orderInventory (CustomerID, OrderDate, OrderPrice) VALUES(?, ?, ?)', (cid, date, price))
        
        finally:
            self.conn.commit()
            #self.cursor.close()
            #self.conn.close()


        



