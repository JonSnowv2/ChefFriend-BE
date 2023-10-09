import sqlite3

def create_tables():
    db_file = 'database.db'
    print(f"Using database file: {db_file}")

    conn = sqlite3.connect(db_file) 

    c = conn.cursor()

    create_table_sql_user = '''
    CREATE TABLE IF NOT EXISTS user (
        username TEXT PRIMARY KEY,
        name TEXT,
        password TEXT,
        pfp TEXT
    )
    '''

    create_table_sql_recipe = '''
    CREATE TABLE IF NOT EXISTS recipe (
        id INTEGER PRIMARY KEY,
        title TEXT,
        description TEXT,
        ingredients TEXT,
        instructions TEXT,
        category TEXT,
        image TEXT,
        user_username TEXT,  
        FOREIGN KEY (user_username) REFERENCES user (username)
    )
    '''

    c.execute(create_table_sql_user)
    c.execute(create_table_sql_recipe)

    conn.commit()

    conn.close()


def drop_table():
    conn = sqlite3.connect('database.db')

    c = conn.cursor()

    c.execute('DROP TABLE IF EXISTS recipe')
    c.execute('DROP TABLE IF EXISTS user')
    
    conn.commit()

    conn.close()
