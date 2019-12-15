# initial scripts for DB


def drop_all_tables():
    """Deletes all tables"""
    drop_user_category = """ DROP TABLE IF EXISTS user_category """
    drop_users = """ DROP TABLE IF EXISTS user"""
    drop_items = """ DROP TABLE IF EXISTS items """
    drop_categories = """ DROP TABLE IF EXISTS categories """

    queries = [drop_user_category, drop_users, drop_items, drop_categories]
    return queries


def set_up_tables():
    """Create all tables"""
    create_user_table = """ 
    CREATE TABLE IF NOT EXISTS users (
        id serial PRIMARY KEY,
        user_name VARCHAR(20) NOT NULL UNIQUE
    )
    """

    create_category_table = """
    CREATE TABLE IF NOT EXISTS categories (
        id serial PRIMARY KEY,
        category_name VARCHAR(30) NOT NULL UNIQUE
    )
    """

    create_user_category_table = """
    CREATE TABLE IF NOT EXISTS user_category (
        user_id integer NOT NULL,
        category_id integer NOT NULL,
        PRIMARY KEY (user_id, category_id),
        CONSTRAINT uc_user_id_fk FOREIGN KEY (user_id)
            REFERENCES users, 
        CONSTRAINT uc_category_id_fk FOREIGN KEY (category_id)
            REFERENCES categories
    )
    """

    create_item_table = """
    CREATE TABLE IF NOT EXISTS items (
        id serial PRIMARY KEY,
        item_name VARCHAR(30) NOT NULL UNIQUE,
        category_id integer NOT NULL,
        CONSTRAINT item_category_id_fk FOREIGN KEY (category_id)
            REFERENCES categories
    )
    """

    queries = [create_user_table, create_category_table,
               create_user_category_table, create_item_table]

    return queries

