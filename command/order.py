
class Order:
    def __init__(self, name, address, id):
        self.customer_name = name
        self.customer_address = address
        self.id = id
        self.subtotal = 0
        self.tax = 0
        self.total = 0
        self.items = []

    def CalculateOrderPrice(self):
        self.subtotal = float("%.2f" % sum([self.GetPizzaPrice(p) for p in self.items]))
        self.tax = float("%.2f" % (self.subtotal * 0.09))
        self.total = float("%.2f" % (self.subtotal + self.tax))

    def GetPizzaPrice(self, pizza):
        return pizza.price
