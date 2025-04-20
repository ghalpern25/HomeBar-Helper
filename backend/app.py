from flask import Flask, request, jsonify
from flask_cors import CORS 
import psycopg2

app = Flask(__name__)
CORS(app)

# DB config (update these as needed)
DB_CONFIG = {
    'dbname': 'homebar_helper',
    'user': 'homebar_agent',
    'password': 'admin',  # Uncomment if needed
    'host': 'localhost',
    'port': 5432
}

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
    recipes = get_makeable_recipes()
    return jsonify({"makeable_recipes": recipes})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)