
import sys

from customer import Customer
from order import Order

class PizzaHub:
    def __init__(self):
        from collections import deque
        self.orders = deque([])
        self.num_orders = 0
        self.sum_money = 0

    def CreateYourOwn(self, customer):
        while True:
            self.CustomizePizza(customer)

            choice = int(input("(START OVER:0, ADD TO ORDER:1, SHOPPING CART:2, QUIT:3)>> "))

            ## start over
            if choice == 0:
                continue

            ## add to order
            elif choice == 1:
                self.CreateOrder(customer)
                if not self.ViewShoppingCart(customer):
                    continue

            ## view shopping cart
            elif choice == 2:
                if not self.ViewShoppingCart(customer):
                    continue

            else:
                break

    def CustomizePizza(self, customer):
        ## initialized
        customer.CreatePizza()
        self.ShowCustomizedPizza(customer)

        ## customize options
        size = int(input("PICK A SIZE (PERSONAL PAN:0, MEDIUM:1, LARGE:2)>> "))
        customer.PickSize(size)
        self.ShowCustomizedPizza(customer)

        cheese_amount = int(input("CHEESE OR NO CHEESE (NO CHEESE:0, REGULAR:1, EXTRA:2)>> "))
        customer.SetCheeseAmount(cheese_amount)
        self.ShowCustomizedPizza(customer)

        recommended_amount, current_amount = 5, 0
        for id, ingredient in enumerate(customer.pizza.ingredients):
            amount = int(input("{0} AMOUNT (NONE:0, REG:1, EXTRA:2)>> ".format(ingredient.name)))
            if amount and current_amount + amount > recommended_amount:
                print("Our Pan Pizza bakes best with 5 or few ingredients.")
                add = int(input("(DON'T ADD:0, or ADD {} ANYWAY:1)".format(ingredient.name)))
                if not add:
                    continue
        
            current_amount += amount
            customer.SetIngredientsAmount(id, amount)

        self.ShowCustomizedPizza(customer)

    def ViewShoppingCart(self, customer):
        if not customer.my_order:
            self.NoItemsInOrder()

        while customer.my_order:
            self.ShowPayment(customer)
            choice = int(input("(REMOVE PIZZA FROM ORDER:0, CHECKOUT:1, ADD MORE PIZZA:2, CHANGE QTY:3)>> "))
             
            if not choice:
                self.RemovePizzaFromOrder(customer)
                if not customer.my_order.items:
                    self.DeleteOrder(customer)
                    self.NoItemsInOrder()
             
                continue
             
            if choice == 1:
                self.CheckOut(customer)
             
            if choice == 2:
                break
        
            if choice == 3:
                self.ChangePizzaQTY(customer)
                continue
             
        return False
             
    def CheckOut(self, customer):
        place_order = int(input("(PLACE ORDER:1, or BACK TO MY ORDER:0)>> "))
                               
        if place_order:
            self.ShowPayment(customer)
            customer.CheckOut(customer.my_order.total)
            self.orders.append(customer.my_order)
            self.num_orders += 1
            self.sum_money += customer.my_order.total
            self.DeleteOrder(customer)
            print("\n Your order is on its way...")
            print("         (Hooray!)          \n")
            self.AskToQuit()
                          
    def RemovePizzaFromOrder(self, customer):
        pizza_id = int(input("Enter a pizza id to be removed: "))
                                              
        customer.RemovePizzaFromOrder(pizza_id)
    
    def ChangePizzaQTY(self, customer):
        pizza_id = int(input("Enter a pizza id to be changed: "))
        pizza_qty = int(input("Enter a quantity(1-50): "))
    
        customer.ChangePizzaQTY(pizza_id, pizza_qty)
    
                                              
    def ShowOrder(self, customer):
        for id, item in enumerate(customer.my_order.items):
            print("CREATE YOUR OWN [{0}]  \n {1} ".format(id, item))
                                                    
    def CreateOrder(self, customer):
        if not customer.my_order:
            customer.my_order = Order(customer.name, customer.address, customer.id)
        
        customer.AddToOrder()
                                                    
    def DeleteOrder(self, customer):
        customer.RemoveOrder()
                                                    
    def GetOrderPrice(self, customer):
        customer.my_order.CalculateOrderPrice()
    
    def ShowPayment(self, customer):
        if not customer.my_order:
            print("        MY ORDER      \n")
            print("========================")
            print("Sub Total       ${} \n".format(0.0))
            print("Tax             ${} \n".format(0.0))
            print("Total           ${} \n".format(0.0))
        
        else:
            print("        MY ORDER      \n")
            print("========================")
            self.ShowOrder(customer)
            self.GetOrderPrice(customer)
            print("========================")
            print("Sub Total       ${} \n".format(customer.my_order.subtotal))
            print("Tax             ${} \n".format(customer.my_order.tax))
            print("Total           ${} \n".format(customer.my_order.total))
        
    def GetCustomerInfo(self):
        name = input("Please enter your name: ")
        address = input("Please enter your location: ")
        id = self.num_orders
                                                    
        customer = Customer(name, address, id)
                                                    
        return customer
                                                    
    def ShowCustomizedPizza(self, customer):
        print("-------------------------------")
        print("CREATE YOUR OWN PIZZA \n {}".format(customer.pizza))
        print("-------------------------------")

    def AskToQuit(self):
        quit = int(input("QUIT? (Y:1, N:0)>> "))
        if quit:
            sys.exit(1)

    def NoItemsInOrder(self):
        print("THERE ARE NO ITEMS IN YOUR ORDER.")
        self.ShowPayment(customer)
        self.AskToQuit()



if __name__ == "__main__":
    
        print("*******************************************************")
        print("*                Welcome to Pizza Hub!                *")
        print("*                  2017 Cheng Peng                    *")
        print("*******************************************************")
                  
        app = PizzaHub()

        ## initialize a customer
        customer = app.GetCustomerInfo()
        
        ## start order and pay conversation
        app.CreateYourOwn(customer)
                  
        sys.exit(1)

