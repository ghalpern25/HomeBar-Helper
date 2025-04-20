# HomeBar Helper



### ERD

  +----------------+        +---------------------+       +-----------------+
  |   ingredients  |        |   recipe_ingredients|       |     recipes     |
  +----------------+        +---------------------+       +-----------------+
  | id (PK)        |<------>| recipe_id (PK, FK)  |<----->| id (PK)         |
  | name           |        | ingredient_id (PK,FK)|       | name            |
  +----------------+        | quantity            |       | instructions    |
                            | unit_id (FK)        |       +-----------------+
                            +---------------------+
                                      |
                                      v
                             +----------------+
                             |     units      |
                             +----------------+
                             | id (PK)        |
                             | name           |
                             +----------------+

  +--------------------+
  |   user_inventory   |
  +--------------------+
  | ingredient_id (PK) |
  +--------------------+
