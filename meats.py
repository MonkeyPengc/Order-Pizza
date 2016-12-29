
from ingredients import Ingredients

class Meats(Ingredients):
    def __init__(self, name, amount=0):
        Ingredients.__init__(self, name, amount)

class MeatsMenu:
    items = ["PEPPERONI", "ITALIAN SAUSAGE", "PREMIUM SALAMI", "CLASSICAL MEATBALL", "SLOW-ROASTED HAM", "APPLEWOOD SMOKED BACON", "GRILLED CHICKEN", "BEEF", "SEASONED PORK"]

