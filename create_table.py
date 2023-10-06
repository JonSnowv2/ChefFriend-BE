import sqlite3

def create_table():
    conn = sqlite3.connect('recipes.db')

    c = conn.cursor()

    c.execute("""CREATE TABLE IF NOT EXISTS recipe (
              title TEXT,
              description TEXT,
              ingredients TEXT,
              instructions TEXT,
              category TEXT,
              image TEXT
    )""")

    conn.commit()

    c.execute("INSERT INTO recipe (title, description, ingredients, instructions, category, image) VALUES (?, ?, ?, ?, ?, ?)",
            ("spaghetti", "this is the description", "ingredients", "instructions", "category", "image"))

    conn.commit()

    conn.close()
