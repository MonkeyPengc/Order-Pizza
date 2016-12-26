
# Order Pizza Online

Refers to: https://www.pizzahut.com/#/pizza/create-your-own 

----------------------------------

# Design Principles

### Entities(Sub Entities)

PizzaHub

Order

Pizza

Ingredients(Meats, Veggies)

Customer

### Relation between Entities

Meats and Veggies are Ingredients.

Pizza may contain multiple Ingredients.

An Order contains at least one Pizza.

PizzaHub has Orders.

### Behaviors of Entities

PizzaHub serves Customer, calculates and stores the Orders.

Customer places Orders by creating their own Pizza w/o Ingredients, and pays.
