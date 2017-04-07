
import sys
from client.tk import *
from client.customer import Customer
from client.order import Order
from modules.jsonsocket import JsonSocket


LARGE_FONT= ("Verdana", 20)


class JsonClient(JsonSocket):
    """
    Inherit Json Socket class, and enable connect operation.
    """
    
    def __init__(self, hostname='127.0.0.1', port=1617):
        super(JsonClient, self).__init__(hostname, port)
    
    def connect(self):
        try:
            self.socket.connect((self.get_host(), self.get_port()))
        
        except OSError as e:
            self.logger.error(e)
            return

        else:
            self.logger.info("Socket connected.")

class AppInterface(Tk):
    """
    Client interface dynamiclly loads 4 frames, and creates shared 
    method and attributes. Each frame has access to other frames.
    """
    
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)  ## inherit Tk class, create a Tk() window.
        container = Frame(self, width=40, height=120)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.frames = {}
        self.customer = None
        
        for f in (StartPage, PageOne, PageTwo, PageThree):
            frame = f(container, self)
            self.frames[f] = frame     ## pass all frame instances to dict
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()    ## render the backend frame up to front, tkraise() inherit from Tk

    def transmit(self, package):
        """
        Establish socket communication, send/receive packages.
        """
        
        self.client = JsonClient()
        self.client.connect()
        self.client.sendPackage(package)
        msg = self.client.readPackage()
        
        return msg


class StartPage(Frame):
    """
    Instantiates a cusomter object by requesting user input, and 
    only allows customer to access to the following page.
    """
    
    fieldnames = ['User Name', 'Address']
    
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        label = Label(self, text="WELCOME TO PIZZA HUB", font=LARGE_FONT)
        label.pack(pady=40, padx=40)
        self.entries = {}
        self.connected = False
        
        for (i, fn) in enumerate(self.fieldnames):
            lab = Label(self, text=fn)
            ent = Entry(self, width=30)
            lab.pack()
            ent.pack()
            self.entries[fn] = ent
        
        button = Button(self, text="CUSTOMIZE", command=lambda: self.handle(controller))
        button.pack()
    
    def handle(self, controller):
        """
        Initialize a customer with username, address, and a customer id.
        Clients send request to the server and get the id.
        """
        
        username = self.entries[self.fieldnames[0]].get()
        
        if not username: ## set user name to be a required field
            showinfo(title="Pop-up", message="Please Enter Your Name.")
            return
        
        address = self.entries[self.fieldnames[1]].get()
        
        if not self.connected:
            package = {'customer_id':-1, 'customer_name':username, 'customer_address':address}
            msg = controller.transmit(package)  ## receive a new customer id
            controller.customer = Customer(username, address, msg['customer_id'])
            self.connected = not self.connected

        controller.show_frame(PageOne)


class PageOne(Frame):
    """
    Instantiates a pizza object by requesting user input.
    Has accesses to previous and following pages. Customer 
    could customize own pizza, view price, and add to the order.
    Customizations involve size, cheese, and ingredients.
    """
    
    fieldnames = ['PICK A SIZE', 'CHEESE OR NO CHEESE', 'INGREDIENTS']
    size = ['PERSONAL', 'MEDIUM', 'LARGE']
    amount = ['NONE', 'REG', 'EXTRA']
    vars = {}  ## create a class dictionary to store customer input
    
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        label = Label(self, text="CREATE YOUR OWN PIZZA", font=LARGE_FONT)
        label.grid(row=0, column=1, padx=40, pady=40)
        
        button0 = Button(self, text="CUSTOMIZE", command=lambda:self.handle_create(controller))
        button0.grid(row=1, column=0)
        
        button1 = Button(self, text="BACK TO HOME", command=lambda:controller.show_frame(StartPage))
        button1.grid(row=2, column=0)
        
        button2 = Button(self, text="ADD TO ORDER", command=lambda:self.handle_add(controller))
        button2.grid(row=3, column=0)
    
    def handle_create(self, controller):
        """
        Handle event when customers start to create pizza.
        """

        controller.customer.CreatePizza()   ## initialize a pizza object
        
        button3 = Button(self, text="GET PRICE", command=lambda:self.onShowPrice(controller.customer))
        button3.grid(row=4, column=0)

        # create PICK A SIZE menu
        lab = Label(self, text=self.fieldnames[0])
        lab.grid(row=1, column=1)
        
        var = IntVar()
        self.vars[self.fieldnames[0]] = var
        
        for (j, size) in enumerate(self.size):
            rb = Radiobutton(self, text=size, command=lambda:self.onPress(controller.customer), variable=self.vars[self.fieldnames[0]], value=j)
            rb.grid(row=j+2, column=1)
        self.vars[self.fieldnames[0]].set(j)  ## set the default pizza size to LARGE
    
        # create CHEESE OR NO CHEESE menu
        lab = Label(self, text=self.fieldnames[1])
        lab.grid(row=j+3, column=1)
        
        var = IntVar()
        self.vars[self.fieldnames[1]] = var
        self.vars[self.fieldnames[1]].set(1)  ## set the default cheese amount to REGULAR
        
        for (j, amount) in enumerate(self.amount):
            rb = Radiobutton(self, text=amount, command=lambda:self.onPress(controller.customer), variable=self.vars[self.fieldnames[1]], value=j)
            rb.grid(row=j+6, column=1)
        
        # create INGREDIENTS menu
        lab = Label(self, text=self.fieldnames[2])
        lab.grid(row=1, column=2)
        
        ingredients = controller.customer.pizza.ingredients  ## make a reference to a list of ingredient objects
        for (i, fn) in enumerate(ingredients):
            lab = Label(self, text=fn.name)
            lab.grid(row=i+2, column=2)
            var = StringVar()
            self.vars[i] = var
            self.vars[i].set('NONE')  ## set the default ingredient amount to NONE
            cob = ttk.Combobox(self, textvariable=self.vars[i], state="readonly", values=self.amount, width='6')
            cob.grid(row=i+2, column=3)


    def handle_add(self, controller):
        """
        Handle event when customers add pizza to an order.
        """
        
        try:
            pizza = controller.customer.pizza   ## get a reference to pizza object of the customer
        
        except Exception:
            showinfo(title='Pop-up', message="No Pizza Created Yet.")
            return
        
        else:
        # create an order if not exist, and add pizza to order
            c = controller.customer
            self.onPress(c)  ## update requested data
            if not c.my_order:
                c.my_order = Order(c.name, c.address, c.id)
            
            c.AddToOrder()
            controller.show_frame(PageTwo)  ## go to my order page

    def onPress(self, customer):
        """
        Load the requested data from user input, and update the
        pizza object. Currently no max limit on ingredients amount.
        """
        
        for key in self.vars:
            if key == self.fieldnames[0]:
                size = self.vars[key].get()
                customer.PickSize(size)  ## set pizza size
            
            elif key == self.fieldnames[1]:
                cheese_amount = self.vars[key].get()
                customer.SetCheeseAmount(cheese_amount)   ## set cheese amount
            
            else:
                ingredient_amount = self.vars[key].get()
                if ingredient_amount != 'NONE':
                    str_to_int = self.amount.index(ingredient_amount)
                    customer.SetIngredientsAmount(key, str_to_int)  ## set ingredient amount

    def onShowPrice(self, customer):
        self.onPress(customer)
        price = customer.pizza.InitializePizzaPrice()  ## if not updated by the customer, return default price
        showinfo(title="Price", message="TOTAL ${}".format(str(price)))


class PageTwo(Frame):
    """
    Has accesses to previous and following pages. Customer
    could view/update the order, add more pizza, or checkout.
    Update involves changing quantity, and removing a specified
    pizza from order. Price is adjusted as requests updated.
    """
    
    max_range = 50  ## define a maximum quantity for each pizza can be ordered
    vars = {}  ## create a class dictionary to store customer input
    
    def __init__(self, parent, controller):
        Frame.__init__(self,parent)
        label = Label(self, text="MY ORDER", font=LARGE_FONT)
        label.grid(row=0, column=1, padx=40, pady=40, columnspan=3)
        
        button0 = Button(self, text="BACK TO HOME", command=lambda:controller.show_frame(StartPage))
        button0.grid(row=1, column=0)
        
        button1 = Button(self, text="ADD MORE PIZZA", command=lambda:self.handle_add(controller))
        button1.grid(row=1, column=1)

        button2 = Button(self, text="VIEW/UPDATE ORDER", command=lambda:self.handle_view(controller))
        button2.grid(row=1, column=2, columnspan=2)
    
    
    def handle_add(self, controller):
        """
        Handle event when customers want to add more pizza,
        program should reinitialize a pizza object.
        """
        
        controller.customer.CreatePizza()
        controller.show_frame(PageOne)


    def handle_view(self, controller):
        """
        Handle event when customers want to view or update
        the order detail. Display the current pizzas info, 
        quantity, and total price of the order. Customers 
        could change/remove pizza, and go to checkout.
        """
        
        order = controller.customer.my_order  ## make a reference to the order of customer
        
        for i in range(len(order.items)):
            if not order.items[i]:
                continue
            
            label0 = Label(self, text=order.items[i])
            label0.grid(row=i+2, column=0, columnspan=2, padx=10)
            
            label1 = Label(self, text="QTY:")
            label1.grid(row=i+2, column=2)
        
            qty = order.items[i].quantity
            var = IntVar()
            self.vars[i] = var
            self.vars[i].set(qty)
            combobox0 = ttk.Combobox(self, textvariable=self.vars[i], state="readonly", values=[j+1 for j in range(self.max_range)], width='3')
            combobox0.bind("<<ComboboxSelected>>", lambda event, c=controller.customer, p=i:self.onChange(c, p))  ## change pizza quantity
            combobox0.focus_set()
            combobox0.grid(row=i+2, column=3)

            button3 = Button(self, text="Remove", command=lambda p=i:self.onRemove(controller, p))
            button3.grid(row=i+2, column=4)

        button4 = Button(self, text="CHECKOUT", command=lambda:self.onCheckout(controller))
        button4.grid(row=1, column=4, columnspan=2, sticky='e')
        
        self.showOrderPrice(order)

    def onChange(self, customer, pizza_id):
        """
        Load a pizza quantity, update, and recalculate the price.
        """
        
        pizza_qty = self.vars[pizza_id].get()
        customer.ChangePizzaQTY(pizza_id, pizza_qty)
        self.showOrderPrice(customer.my_order)

    def onRemove(self, controller, pizza_id):
        # label text overlapping issue need to be solved caused by this event
        
        c = controller.customer
        c.RemovePizzaFromOrder(pizza_id)

    def onCheckout(self, controller):
        """
        Call server to insert an order in the order inventory.
        """
        
        if askokcancel("Proceed", "Pay the order?"):
            c = controller.customer
            package = {'customer_id':c.id, 'order_price':c.my_order.GetTotalPrice}
            msg = controller.transmit(package)
            
            if msg['order_received']:
                c.CheckOut(c.my_order.GetTotalPrice)
                c.Clear()
                controller.show_frame(PageThree)

    def showOrderPrice(self, order):
        """
        Calculate and display the order price.
        """
        
        order.CalculateOrderPrice()
        label3 = Label(self, text="$:"+str(order.GetTotalPrice), font=LARGE_FONT)
        label3.grid(row=2, column=5)
        

class PageThree(Frame):
    """
    Order confirmation, customers could choose to quit or add more pizza.
    """
    
    cnfrm_msg = "Your order is on its way... \n          (Hooray!)          \n"
    
    def __init__(self, parent, controller):
        Frame.__init__(self,parent)
        label = Label(self, text=self.cnfrm_msg, font=LARGE_FONT)
        label.pack(pady=40,padx=40)
        
        button0 = Button(self, text="QUIT", command=lambda:self.quit(controller))
        button0.pack()
        
        button1 = Button(self, text="ADD MORE FOOD", command=lambda:controller.show_frame(PageOne))
        button1.pack()

    def quit(self, controller):
        controller.client.close()
        controller.destroy()


if __name__ == "__main__":

    app = AppInterface()
    app.mainloop()
    
    sys.exit(0)
