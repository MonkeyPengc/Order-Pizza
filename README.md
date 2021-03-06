
# Order Pizza Client

The client code simulates custom ordering pizza at [PizzaHut](https://www.pizzahut.com/#/pizza/create-your-own).

More references about JSON socket could be found at [github](https://github.com/chris-piekarski/python-json-socket). Thanks, Chris.


## Support

Client code for order pizza app can be implemented with command line version in the command folder, or with the new GUI version in the client folder.

Command line has been removed for simplicity. The current version could be tested using local host.


## Major Updates

* 2016-12-29: Added major functions.

* 2016-12-31: Added function that changes the pizza quantity. 

* 2017-01-11: Added database(SQLite) feature that records pizza sales, and partial input error handles.

* 2017-03-19: Brand-new version with graphic interface(Tinkter) and database features on client. Added function that removes pizza from order.

* 2017-03-27: Improved database for recording customers and orders separately. 

* 2017-03-30: Set up server/client architecture based on TCP communication. The client code and documentation has been updated, requiring users to run both server and client code. Removed command line implementation.

* 2017-03-31: Updated database implementation.

* 2017-04-29: Added a sales management system.

* 2017-05-02: Added login authentication, and account administration features to sales management system. 


## Software Architecture

The program is organized into a number of different components:

![swa_pic](screenshots/arch.png)

pizzahub_server.py is the program that runs the server. It receives requests from client end. Next, it responds to the requests by sending packages back to the client, and updating the database.

pizzahub_client.py essentially manages user interfaces, and connects to the server end.

sales_management.py runs a query interface, that is able to query sales database.

admin.py is a program that manages accounts information of users, who having access to the sales management system.


## Modules of AppInterface

### Entities(Sub Entities)

Order

Pizza

Ingredients(Meats, Veggies)

Customer

### Relation between Entities

Meats and Veggies are Ingredients.

One Pizza may contain none or multiple (allow to add more than recommended amount of) Ingredients.

An Order contains at least one Pizza.

Customer has an Order, if Pizza is added to.


### Behaviors of Entities

Interfaces serve the Customer, take Order, and render the payment detail.

Customer customizes Pizza w/o Ingredients, modifies or places Order, and checkout.


## Screenshot in Test

Client Interface:

![gui_pic](screenshots/gui.png)

Sales Query:

![dbm_pic](screenshots/dbm.png)

