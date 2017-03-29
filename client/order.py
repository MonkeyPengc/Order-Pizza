
class Order:
    def __init__(self, name, address, id, num_items=None):
        self.customer_name = name
        self.customer_address = address
        self.id = id
        self.subtotal = 0
        self.tax = 0
        self.total = 0
        if not num_items:
            self.items = [None] * 20
        else:
            self.items = [None] * nums_items

    def CalculateOrderPrice(self):
        self.subtotal = float("%.2f" % sum([p.GetPrice for p in self.items if p]))
        self.tax = float("%.2f" % (self.subtotal * 0.09))
        self.total = float("%.2f" % (self.subtotal + self.tax))

