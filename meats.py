
from ingredients import Ingredients

class Meats(Ingredients):
    def __init__(self, name, amount=0):
        Ingredients.__init__(self, name, amount)

class MeatsMenu:
    items = ["PEPPERONI", "ITALIAN SAUSAGE", "CLASSICAL MEATBALL", "APPLEWOOD SMOKED BACON", "GRILLED CHICKEN", "BEEF"]

