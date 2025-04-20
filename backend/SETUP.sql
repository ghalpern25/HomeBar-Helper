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

INSERT INTO units (name) VALUES
('oz'),
('mL'),
('dash'),
('cup'),
('gal'),
('unit'),
('tsp'),
('splash'),
('barspoon'),
('leaf');

INSERT INTO ingredients (name) VALUES
('Triple Sec'),
('Maraschino Liqueur'),
('Applejack'),
('Kahlua'),
('Tequila'),
('Bourbon'),
('St Germain'),
('White Rum'),
('Peach Schnapps'),
('Baileys'),
('Gin'),
('Vodka'),
('Chambord'),
('Crown Apple'),
('Grenadine'),
('Club Soda'),
('Pineapple Juice'),
('Angosturra Bitters'),
('Orange Bitters'),
('Lemon Juice'),
('Lime Juice'),
('Sour Mix'),
('Grape Juice'),
('Cranberry Juice'),
('Milk'),
('Dry Vermouth'),
('Simple Syrup'),
('Egg Whites'),
('Tonic Water'),
('Ginger Beer'),
('Orange Juice');

-- Margarita
INSERT INTO user_inventory (ingredient_id) VALUES
(5),  -- Tequila
(1),  -- Triple Sec
(22); -- Lime Juice

-- White Russian
INSERT INTO user_inventory (ingredient_id) VALUES
(12), -- Vodka
(4),  -- Kahlua
(25); -- Milk

-- Whiskey Sour (missing egg whites)
INSERT INTO user_inventory (ingredient_id) VALUES
(6),  -- Bourbon
(20), -- Lemon Juice
(27); -- Simple Syrup

INSERT INTO recipes (name, instructions) VALUES
('Classic Margarita', 'Shake all ingredients with ice and strain into a salt-rimmed glass.'),
('White Russian', 'Build in glass over ice and stir.'),
('Whiskey Sour', 'Shake all ingredients with ice, strain into a rocks glass, and garnish with a cherry.');

INSERT INTO recipes (name, instructions) VALUES
('Classic Margarita', 'Shake all ingredients with ice and strain into a salt-rimmed glass.'),
('White Russian', 'Build in glass over ice and stir.'),
('Whiskey Sour', 'Shake all ingredients with ice, strain into a rocks glass, and garnish with a cherry.');
