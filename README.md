
# Order Pizza Online

Code workflow refers to: https://www.pizzahut.com/#/pizza/create-your-own 


## Support

Please run pizzahub.py through command line, and follow the instructions.

## Updates

* 2016-12-29: Added major functions.

* 2016-12-31: Added function that changes the pizza quantity. 

* 2017-01-11: Added database(SQLite) feature that records pizza sales, and partial input error handles.

# Design Principles

### Entities(Sub Entities)

PizzaHub

Order

Pizza

Ingredients(Meats, Veggies)

Customer

### Relation between Entities

Meats and Veggies are Ingredients.

One Pizza may contain none or multiple (allow to add more than recommended amount of) Ingredients.

An Order contains at least one Pizza.

Customer has an Order, if Pizza is added to.

PizzaHub creates and stores Orders.

### Behaviors of Entities

PizzaHub serves the Customer, takes Order, and creates the payment detail by dialogs.

Customer customizes Pizza w/o Ingredients, modifies or places Order, and checkout.



