import sqlite3
import datetime

class SalesDB:
    def __init__(self):
        self.conn = sqlite3.connect('order_inventory.db')
        self.cursor = self.conn.cursor()
        self.CreateTable()
    
    def CreateTable(self):
        self.cursor.execute('CREATE TABLE IF NOT EXISTS orderInventory (order_id INTEGER PRIMARY KEY AUTOINCREMENT, customer_id INT, datestamp TEXT, value REAL)')
    
    def InsertOrder(self, cid, order_value):
        date = datetime.datetime.today().strftime('%Y-%m-%d %H-%M-%S')
        
        try:
            self.cursor.execute('INSERT INTO orderInventory (customer_id, datestamp, value) VALUES(?, ?, ?)', (cid, date, order_value))
        
        except sqlite3.ProgrammingError:
            self.conn = sqlite3.connect('order_inventory.db')
            self.cursor = self.conn.cursor()
            self.cursor.execute('INSERT INTO orderInventory (customer_id, datestamp, value) VALUES(?, ?, ?)', (cid, date, order_value))
        
        finally:
            self.conn.commit()
            self.cursor.close()
            self.conn.close()

    def AllocateCustomerID(self):
        self.cursor.execute('SELECT MAX (customer_id) FROM orderInventory')
        
        try:
            return self.cursor.fetchone()[0] + 1
    
        except TypeError:
            return 1
