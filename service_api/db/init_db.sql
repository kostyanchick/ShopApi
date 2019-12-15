/* create db */
CREATE DATABASE shop_dev;

/* connect to created db */
\c shop_dev


/* create tables */

CREATE TABLE IF NOT EXISTS users (
    id serial PRIMARY KEY,
    user_name VARCHAR(20) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS categories (
    id serial PRIMARY KEY,
    category_name VARCHAR(30) NOT NULL UNIQUE
);

/* association table */
CREATE TABLE IF NOT EXISTS user_category (
        user_id integer NOT NULL,
        category_id integer NOT NULL,
        PRIMARY KEY (user_id, category_id),
        CONSTRAINT uc_user_id_fk FOREIGN KEY (user_id)
            REFERENCES users,
        CONSTRAINT uc_category_id_fk FOREIGN KEY (category_id)
            REFERENCES categories
);

CREATE TABLE IF NOT EXISTS items (
    id serial PRIMARY KEY,
    item_name VARCHAR(30) NOT NULL UNIQUE,
    category_id integer NOT NULL,
    CONSTRAINT item_category_id_fk FOREIGN KEY (category_id)
        REFERENCES categories
);
