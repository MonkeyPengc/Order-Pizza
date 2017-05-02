
import sys
from modules.tk import *
from modules.calendar import Calendar
from database.sales_database import SqlHelper
from database.admin_database import adminDB
import calendar

LARGE_FONT= ("Verdana", 20)


class QueryInterface(Tk):
    """ 
    Query interface dynamiclly loads frames and creates
    shared methods and attributes.
    """
    
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)  ## inherit Tk class, create a Tk() window.
        container = Frame(self, width=40, height=120)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        
        for f in (StartPage, PageOne):
            frame = f(container, self)
            self.frames[f] = frame     ## pass all frame instances to dict
            frame.grid(row=0, column=0, sticky="nsew")
    
        self.showFrame(StartPage)

    def showFrame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()    ## render the backend frame up to front, tkraise() inherit from Tk

    def quit(self):
        self.destroy()


class StartPage(Frame):
    """ a login page that allows valid users to continue """
    
    fieldnames = ['Username', 'Password']
    
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        label = Label(self, text="Database Management System", font=LARGE_FONT)
        label.pack(pady=40, padx=40)

        self.entries = {}
        
        for fn in self.fieldnames:
            lab = Label(self, text=fn)
            ent = Entry(self, width=30)
            lab.pack()
            ent.pack()
            self.entries[fn] = ent

        button0 = Button(self, text="Login", command=lambda:self.login(controller))
        button0.pack()
    
        button1 = Button(self, text="Quit", command=lambda:controller.quit())
        button1.pack()

    def login(self, controller):
        """ require a valid username and password to login """
        
        username = self.entries[self.fieldnames[0]].get()
        
        if not username:
            showinfo(title="Pop-up", message="Please enter a username.")
            return

        password = self.entries[self.fieldnames[1]].get()
        
        if not password:
            showinfo(title="Pop-up", message="Please enter the password.")
            return

        if not self.verifyUser(username, password):
            showinfo(title="Pop-up", message="Invalid username or password.")
            return

        controller.showFrame(PageOne)

    def verifyUser(self, name, pw):
        """ connect to admin database and verify the user input """
        
        db = adminDB()
        
        user = db.queryByName(name)
        if not user or not db.login(name, pw, user[1]):
            return False

        return True


class PageOne(Frame):
    """ allow interactions with the sales history """
    
    base_year = 2000
    year_range = 30
    month_range = 12
    day_range = 31
    
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        label = Label(self, text="Sales History", font=LARGE_FONT)
        label.grid(row=0, column=0, padx=40, pady=40)
        self.colNames = ("OrderID", "OrderPrice", "Date", "DeliverTo")
        self.createTable()
        self.loadData("SELECT o.OrderID, o.OrderPrice, o.OrderDate, c.Address FROM orderInventory AS o LEFT JOIN customers as c ON o.CustomerID=c.CustomerID ORDER BY o.OrderID")
        self.vars = {}
        label1 = Label(self, text="Year:")
        label1.grid(row=4, column=0, pady=10, sticky="e")

        var = StringVar()
        self.vars["YY"] = var
        self.vars["YY"].set('--')
        val = [self.base_year+j for j in range(self.year_range)]
        val.append('--')
        combobox0 = ttk.Combobox(self, textvariable=self.vars["YY"], state="readonly", values=val, width='4')
        combobox0.focus_set()
        combobox0.grid(row=4, column=1, pady=10, sticky="w")

        label2 = Label(self, text="Month:")
        label2.grid(row=4, column=2, pady=10, sticky="e")
        
        var = StringVar()
        self.vars["MM"] = var
        self.vars["MM"].set('--')
        val = [j+1 for j in range(self.month_range)]
        val.append('--')
        combobox1 = ttk.Combobox(self, textvariable=self.vars["MM"], state="readonly", values=val, width='3')
        combobox1.focus_set()
        combobox1.grid(row=4, column=3, pady=10, sticky="w")

        label3 = Label(self, text="Day:")
        label3.grid(row=4, column=4, pady=10, sticky="e")
        
        var = StringVar()
        self.vars["DD"] = var
        self.vars["DD"].set('--')
        val = [j+1 for j in range(self.day_range)]
        val.append('--')
        combobox2 = ttk.Combobox(self, textvariable=self.vars["DD"], state="readonly", values=val, width='3')
        combobox2.focus_set()
        combobox2.grid(row=4, column=5, pady=10, sticky="w")
        
        button0 = Button(self, text="Calendar", command=lambda:self.queryByCalendar())
        button0.grid(row=4, column=6, sticky="e")

        button1 = Button(self, text="Query", command=lambda:self.queryByComb())
        button1.grid(row=4, column=7, padx=10, pady=10)

        button2 = Button(self, text="Quit", command=lambda:controller.quit())
        button2.grid(row=5, column=7, padx=10, pady=10)


    def createTable(self):
        """ create a treeview table that displays sales history """
        
        self.tv = ttk.Treeview(self, columns=self.colNames, show="headings")
        vsb = Scrollbar(self, orient="vertical", command=self.tv.yview)
        hsb = Scrollbar(self, orient="horizontal", command=self.tv.xview)
        self.tv.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        self.tv.grid(row=1, column=0, sticky="nsew", columnspan=8)
        vsb.grid(row=1, column=8, sticky="ns")
        hsb.grid(row=2, column=0, sticky="ew", columnspan=8)

    def loadData(self, sql):
        """ load data from database by specified sql queries """
        
        for col in self.colNames:
            self.tv.heading(col, text=col)
            self.tv.column(col, width=110)
        
        try:
            sqlHelper = SqlHelper()
            res = sqlHelper.queryExecute(sql)
        
        except Exception as e:
            print(e)

        else:
            if res:
                num_order, sales_order = 0, 0
                for item in res:
                    self.tv.insert('', 'end', values=item)
                    num_order += 1
                    sales_order += item[1]

        self.label4 = Label(self, text="Total Orders:"+str(num_order))
        self.label4.grid(row=3, column=6, padx=10)
        
        self.label5 = Label(self, text="Total Sales:$"+"{0:.2f}".format(sales_order))
        self.label5.grid(row=3, column=7, padx=10)


    def queryByComb(self):
        """ query sales by fill year, month, and day info in comboboxes """
        
        yy, mm, dd = self.vars["YY"].get(), self.vars["MM"].get(), self.vars["DD"].get()
        stack = []
        
        if yy == '--':
            stack.append('*')
    
        else:
            stack.append(yy)
    
        if mm == '--':
            stack.append('*')
        
        else:
            if int(mm) < 10:
                stack.append('0' + mm)

            else:
                stack.append(mm)

        if dd == '--':
            stack.append('*')
        
        else:
            if int(dd) < 10:
                stack.append('0' + dd)

            else:
                stack.append(dd)

        date = '-'.join(stack) + '*'   ## generate a datetime pattern

        sql = "SELECT o.OrderID, o.OrderPrice, o.OrderDate, c.Address FROM orderInventory AS o LEFT JOIN customers as c ON o.CustomerID=c.CustomerID WHERE o.OrderDate GLOB '{}' ORDER BY o.OrderID".format(date)

        self.label4.grid_forget()  ## clear up the previous label for redisplay
        self.label5.grid_forget()

        self.createTable()  ## reload data
        self.loadData(sql)
        

    def queryByCalendar(self):
        """ query sales by pick a day from calendar """
        
        popwin = Toplevel()
        popwin.wm_title("Calendar")
        self.calendar = Calendar(master=popwin, firstweekday=calendar.SUNDAY)
        self.calendar.grid(row=3, column=1, columnspan=2)
        
        if 'win' not in sys.platform:
            style = ttk.Style()
            style.theme_use('clam')


class PageTwo(Frame):
    """ display delivery info by google map """
    pass



if __name__ == "__main__":
    
    app = QueryInterface()
    app.title("PizzaHub")
    app.mainloop()
    
    sys.exit(0)


