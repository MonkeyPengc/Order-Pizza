
# Order Pizza Client

Refer to: https://www.pizzahut.com/#/pizza/create-your-own 


## Support

Client code for order pizza app can be implemented with command line version in the command folder, or with the new GUI version in the client folder.

Command line version has been removed for simplicity. The lastest code runs on user's local host.


## Major Updates

* 2016-12-29: Added major functions.

* 2016-12-31: Added function that changes the pizza quantity. 

* 2017-01-11: Added database(SQLite) feature that records pizza sales, and partial input error handles.

* 2017-03-19: Brand-new version with graphic interface(Tinkter) and database features on client. Added function that removes pizza from order.

* 2017-03-27: Improved database for recording customers and orders separately. 

* 2017-03-30: Set up server/client architecture based on socket connection. The client code and documentation has been updated, requiring users to run both server and client code. Removed command line implementation.

* 2017-03-31: Updated database implementation.

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



