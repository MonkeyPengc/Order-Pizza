
from ingredients import Ingredients

class Veggies(Ingredients):
    def __init__(self, name, amount=0):
        Ingredients.__init__(self, name, amount)

class VeggiesMenu:
    items = ["FRESH MUSHROOMS", "PERUVIAN CHERRY PEPPERS", "FRESH RED ONIONS", "MEDITERRANEAN BLACK OLIVES", "SWEET PINEAPPLE", "DICED ROMA TOMATOES"]

