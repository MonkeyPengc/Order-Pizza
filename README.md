
# Order Pizza Desktop App

Refer to: https://www.pizzahut.com/#/pizza/create-your-own 


## Support

Command version: Please run pizzahub.py through command line.

New GUI version: Please run client/pizzahub.py.

## Major Updates

* 2016-12-29: Added major functions.

* 2016-12-31: Added function that changes the pizza quantity. 

* 2017-01-11: Added database(SQLite) feature that records pizza sales, and partial input error handles.

* 2017-03-19: Brand-new version with graphic interface(Tinkter) and database features on client. Added function that removes pizza from order.

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



