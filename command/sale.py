
import sqlite3
import datetime

class SaleDB:
    def __init__(self):
        self.conn = sqlite3.connect('sales_record.db')
        self.cursor = self.conn.cursor()
        self.CreateTable()

    def CreateTable(self):
        self.cursor.execute('CREATE TABLE IF NOT EXISTS salesRecord (datestamp TEXT, value REAL)')

    def InsertOrder(self, order_value):
        date = datetime.datetime.today().strftime('%Y-%m-%d %H-%M-%S')
        self.cursor.execute('INSERT INTO salesRecord (datestamp, value) VALUES(?, ?)', (date, order_value))
        self.conn.commit()
        self.cursor.close()
        self.conn.close()
