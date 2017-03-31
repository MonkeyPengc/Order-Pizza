
from .pizza import Pizza


class Customer:
    def __init__(self, name, address, id, money=500):
        self.name = name
        self.address = address
        self.id = id
        self.money = money
        self.my_order = None

    def CreatePizza(self):
        self.pizza = Pizza()

    def PickSize(self, size):
        self.pizza.size = size

    def SetCheeseAmount(self, cheese_amount):
        self.pizza.cheese_amount = cheese_amount

    def SetIngredientsAmount(self, ingredient_id, ingredient_amount):
        self.pizza.ingredients[ingredient_id].amount = ingredient_amount

    def AddToOrder(self):
        size = len(self.my_order.items)
        cur = 0
        
        # search the first empty bucket to add pizza
        for item in self.my_order.items:
            if not item:
                break
            cur += 1
        
        if cur < size:
            self.my_order.items[cur] = self.pizza

    def CheckOut(self, total_price):
        self.money -= total_price

    def ChangePizzaQTY(self, id, qty):
        self.my_order.items[id].quantity = qty

    def RemovePizzaFromOrder(self, id):
        self.my_order.items[id] = None

    def Clear(self):
        self.my_order = None
