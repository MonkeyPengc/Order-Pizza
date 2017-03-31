
from .meats import Meats, MeatsMenu
from .veggies import Veggies, VeggiesMenu


class PizzaSize:
    Personal = 0
    Medium = 1
    Large = 2


class CheeseAmount:
    Zero = 0
    Regular = 1
    Extra = 2


class IngredientAmount:
    Zero = 0
    Regular = 1
    Extra = 2



class Pizza:
    def __init__(self, size=PizzaSize.Large, cheese_amount=CheeseAmount.Regular):
        self.size = size
        self.cheese_amount = cheese_amount
        self.meats_menu = MeatsMenu.items
        self.veggies_menu = VeggiesMenu.items
        self.ingredients = []
        self.space_used_by_ingredients = 0
        self.quantity = 1

        for item in self.meats_menu:
            self.ingredients.append(Meats(item))

        for item in self.veggies_menu:
            self.ingredients.append(Veggies(item))

        self.__price = self.InitializePizzaPrice()

    def InitializePizzaPrice(self):
        price = self.SetSizePrice() + self.SetCheesePrice() + self.SetIngredientsPrice()
        self.SetPrice = float("%.2f" % (price * self.quantity))
        return self.GetPrice
    
    @property
    def GetPrice(self):
        return self.__price
    
    @GetPrice.setter
    def SetPrice(self, price):
        self.__price = price

    def SetSizePrice(self):
        if self.size == PizzaSize.Large:
            return 16.49

        if self.size == PizzaSize.Medium:
            return 15.49

        if self.size == PizzaSize.Personal:
            return 6.49

    def SetCheesePrice(self):
        ## the price of adding extra cheese depends on the size of pizza

        if self.cheese_amount == CheeseAmount.Extra:
            if self.size == PizzaSize.Large:
                return 1.6

            elif self.size == PizzaSize.Medium:
                return 1.3

            else:
                return 0.5

        else:
            return 0

    def SetIngredientsPrice(self):
        ingredients_price = 0

        if self.size == PizzaSize.Large:
            for ingredient in self.ingredients:
                if ingredient.amount == IngredientAmount.Zero:
                    continue

                if ingredient.amount == IngredientAmount.Regular:
                    ingredients_price += 1.6

                else:
                    ingredients_price += 3.2

        elif self.size == PizzaSize.Medium:
            for ingredient in self.ingredients:
                if ingredient.amount == IngredientAmount.Zero:
                    continue

                if ingredient.amount == IngredientAmount.Regular:
                    ingredients_price += 1.3

                else:
                    ingredients_price += 2.6


        else:
            ## For personal size pizza, if the ingredient added makes the space used larger than 1,
            ## add $0.5 for each additional 1 space spend.
            ## otherwise, the ingredient added is free.

            space_used = 0

            for ingredient in self.ingredients:
                if ingredient.amount == IngredientAmount.Zero:
                    continue

                if ingredient.amount == IngredientAmount.Regular:
                    space_used += 1

                    if space_used <= 1:
                        continue

                    ingredients_price += 0.5

                else:
                    space_used += 2

                    if space_used - 1 <= 1:
                        ingredients_price += 0.5

                    else:
                        ingredients_price += 1

        return ingredients_price

    def IsSpaceAvailable(self, ingredient_to_add):
        ## check if there is any space to add ingredients
        
        return self.space_used_by_ingredients + ingredient_to_add.amount <= 5

    def __str__(self):
        size_mapper = {0:"PERSONAL PAN PIZZA", 1:"MEDIUM", 2:"LARGE"}
        amount_mapper = {0:"NONE", 1:"REGULAR", 2:"EXTRA"}
        ingredients_option = ""
        
        for i in self.ingredients:
            if not i.amount:
                continue
                
            ingredients_option += "\n   " + ": ".join([i.name, amount_mapper[i.amount]])
        
        return "{0}, {1} CHEESE, {2} \n ${3}".format(size_mapper[self.size], amount_mapper[self.cheese_amount], ingredients_option, str(self.InitializePizzaPrice()))


