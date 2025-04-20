import psycopg2

def get_makeable_recipes():
    conn = psycopg2.connect(
        dbname="homebar_helper",
        user="homebar_agent",
        password="admin",  # Uncomment if needed
        host="localhost",
        port=5432
    )
    cur = conn.cursor()

    # Fetch user's ingredient_ids
    cur.execute("SELECT ingredient_id FROM user_inventory;")
    inventory = set(row[0] for row in cur.fetchall())

    # Fetch all recipes and their required ingredients
    cur.execute("""
        SELECT r.id, r.name, ri.ingredient_id
        FROM recipes r
        JOIN recipe_ingredients ri ON r.id = ri.recipe_id
        ORDER BY r.id;
    """)

    # Build a map of recipe_id -> (recipe_name, set of required ingredient_ids)
    recipe_map = {}
    for recipe_id, name, ingredient_id in cur.fetchall():
        if recipe_id not in recipe_map:
            recipe_map[recipe_id] = (name, set())
        recipe_map[recipe_id][1].add(ingredient_id)

    # Determine which recipes are makeable
    makeable = []
    for recipe_id, (name, required_ingredients) in recipe_map.items():
        if required_ingredients.issubset(inventory):
            makeable.append(name)

    # Output
    print("🍸 You can make the following recipes:\n")
    for recipe in makeable:
        print(f" - {recipe}")

    # Cleanup
    cur.close()
    conn.close()

if __name__ == "__main__":
    get_makeable_recipes()
