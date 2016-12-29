
from ingredients import Ingredients

class Veggies(Ingredients):
    def __init__(self, name, amount=0):
        Ingredients.__init__(self, name, amount)

class VeggiesMenu:
    items = ["FRESH MUSHROOMS", "ROASTED SPINACH", "PERUVIAN CHERRY PEPPERS", "FRESH RED ONIONS", "MEDITERRANEAN BLACK OLIVES", "FRESH GREEN BELL PEPPERS", "SLICED BANANA PEPPERS", "SWEET PINEAPPLE", "SLICED JALAPEÑO PEPPERS", "DICED ROMA TOMATOES"]

