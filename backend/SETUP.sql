-- Drop existing tables if they exist (for dev/testing)
DROP TABLE IF EXISTS user_inventory;
DROP TABLE IF EXISTS recipe_ingredients;
DROP TABLE IF EXISTS recipes;
DROP TABLE IF EXISTS ingredients;
DROP TABLE IF EXISTS units;

-- Ingredients table
CREATE TABLE ingredients (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE NOT NULL
);

-- Units table
CREATE TABLE units (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE NOT NULL -- e.g. 'oz', 'ml', 'tsp', 'dash'
);

-- Recipes table
CREATE TABLE recipes (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    instructions TEXT
);

-- Recipe Ingredients bridge table (many-to-many)
CREATE TABLE recipe_ingredients (
    recipe_id INTEGER NOT NULL REFERENCES recipes(id) ON DELETE CASCADE,
    ingredient_id INTEGER NOT NULL REFERENCES ingredients(id) ON DELETE CASCADE,
    quantity NUMERIC NOT NULL,
    unit_id INTEGER NOT NULL REFERENCES units(id),
    PRIMARY KEY (recipe_id, ingredient_id)
);

-- User inventory (simple list of available ingredients)
CREATE TABLE user_inventory (
    ingredient_id INTEGER PRIMARY KEY REFERENCES ingredients(id) ON DELETE CASCADE
);
