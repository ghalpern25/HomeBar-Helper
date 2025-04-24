from flask import Flask, request, jsonify
from flask_cors import CORS 
import psycopg2

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# DB config (update these as needed)
DB_CONFIG = {
    'dbname': 'homebar_helper',
    'user': 'homebar_agent',
    'password': 'admin',  # Uncomment if needed
    'host': 'localhost',
    'port': 5432
}

### Returns a list of recipes, each containing a name and a list of ingredients, and the id
def get_makeable_recipes():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    # Get ingredient IDs from user inventory
    cur.execute("SELECT ingredient_id FROM user_inventory;")
    inventory = set(row[0] for row in cur.fetchall())

    # Get all recipes and their required ingredients
    cur.execute("""
        SELECT r.id, r.name, ri.ingredient_id
        FROM recipes r
        JOIN recipe_ingredients ri ON r.id = ri.recipe_id
        ORDER BY r.id;
    """)

    recipe_map = {}
    for recipe_id, name, ingredient_id in cur.fetchall():
        if recipe_id not in recipe_map:
            recipe_map[recipe_id] = {'name': name, 'ingredients': set()}
        recipe_map[recipe_id]['ingredients'].add(ingredient_id)

    makeable = []
    for recipe_id, recipe_data in recipe_map.items():
        if recipe_data['ingredients'].issubset(inventory):
            makeable.append(recipe_data['name'])

    cur.close()
    conn.close()

    return makeable

@app.route('/check_recipes', methods=['GET'])
def check_recipes():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    # Get user inventory
    cur.execute("SELECT ingredient_id FROM user_inventory;")
    inventory = set(row[0] for row in cur.fetchall())

    # Get all recipes and required ingredients
    cur.execute("""
        SELECT
            r.id,
            r.name,
            r.instructions,
            ri.ingredient_id,
            i.name AS ingredient_name,
            ri.quantity,
            u.name AS unit_name
        FROM recipes r
        JOIN recipe_ingredients ri ON r.id = ri.recipe_id
        JOIN ingredients i ON ri.ingredient_id = i.id
        JOIN units u ON ri.unit_id = u.id
        ORDER BY r.id;
    """)

    recipe_map = {}

    for row in cur.fetchall():
        recipe_id = row[0]
        recipe_name = row[1]
        instructions = row[2]
        ingredient_id = row[3]
        ingredient_name = row[4]
        quantity = float(row[5])
        unit = row[6]

        if recipe_id not in recipe_map:
            recipe_map[recipe_id] = {
                "id": recipe_id,
                "name": recipe_name,
                "instructions": instructions,
                "ingredients": [],
                "required_ingredient_ids": set()
            }

        recipe_map[recipe_id]["ingredients"].append({
            "name": ingredient_name,
            "quantity": quantity,
            "unit": unit
        })
        recipe_map[recipe_id]["required_ingredient_ids"].add(ingredient_id)

    # Filter to only makeable recipes
    makeable = [
        {
            "id": r["id"],
            "name": r["name"],
            "instructions": r["instructions"],
            "ingredients": r["ingredients"]
        }
        for r in recipe_map.values()
        if r["required_ingredient_ids"].issubset(inventory)
    ]

    cur.close()
    conn.close()

    return jsonify(makeable)

@app.route('/add_ingredient', methods=['POST'])
def add_ingredient():
    data = request.get_json()
    print(f"Raw JSON data: {data}")
    ingredient_name = data.get('ingredient_name')
    print(f"ingredient name: {ingredient_name}")

    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    # add ingredient to canonical ingredients table
    cur.execute("INSERT INTO ingredients (name) VALUES (%s);", (ingredient_name,))

    # Get the ID of the newly inserted ingredient
    cur.execute("SELECT id FROM ingredients WHERE name = %s;", (ingredient_name,))
    ingredient_id = cur.fetchone()[0]
    # Add ingredient to user inventory
    cur.execute("INSERT INTO user_inventory (ingredient_id) VALUES (%s);", (ingredient_id,))
    conn.commit()

    cur.close()
    conn.close()

    return jsonify({"status": "success", "message": "Ingredient added to inventory."})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)