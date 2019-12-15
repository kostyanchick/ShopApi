class Singleton(type):
    _instance = None

    def __call__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super.__call__(*args, **kwargs)
        return cls._instance


class BaseModel:
    """Model is created at once and used until the end of session"""
    __metaclass__ = Singleton

    TABLE_NAME = None
    ENTITY_NAME_COL = None

    def __init__(self, pg_connection):
        self.pg_connection = pg_connection

    def get_entity_by_id(self, entity_id):
        """Get single entity by given id"""
        query = f"""
        SELECT id FROM {self.TABLE_NAME} WHERE id = {entity_id}
        """
        return self.pg_connection.fetch_one_row(query)

    def get_all_entities(self):
        """Get all entities for given class table"""
        query = f"""
        SELECT * FROM {self.TABLE_NAME}
        """

        return self.pg_connection.fetch_all(query)

    def create_entity(self, entity_name):
        """Create entity for given class table"""
        query = f"""
        INSERT INTO {self.TABLE_NAME} ({self.ENTITY_NAME_COL})
        VALUES ('{entity_name}')
        RETURNING * 
        
        """

        return self.pg_connection.save_income_data(query)


class User(BaseModel):
    TABLE_NAME = 'users'
    ENTITY_NAME_COL = 'user_name'

    def get_available_categories(self, user_id):
        """Gets all categories available for given user"""

        query = f"""
         SELECT
            c.category_name
        FROM
            user_category AS uc
        INNER JOIN users AS u
            ON uc.user_id = u.id
        INNER JOIN categories as c
            ON uc.category_id = c.id
        WHERE u.id = {user_id};
        """

        return self.pg_connection.fetch_all(query)

    def get_available_items(self, user_id):
        """Get items from categories available to user"""

        query = f"""
        SELECT
           i.item_name
        FROM
             items AS i
        INNER JOIN categories c
            ON i.category_id = c.id
        INNER JOIN user_category uc
            ON c.id = uc.category_id
        INNER JOIN users u
            ON uc.user_id = u.id
        WHERE u.id = {user_id};
        """

        return self.pg_connection.fetch_all(query)


class Category(BaseModel):
    TABLE_NAME = 'categories'
    ENTITY_NAME_COL = 'category_name'

    def get_category_items(self, category_id):
        """Get items for given category"""

        query = f"""
        SELECT
           i.item_name
        FROM
             items AS i
        INNER JOIN categories c
            ON i.category_id = c.id
        WHERE c.id = {category_id};
        """

        return self.pg_connection.fetch_all(query)


class Item(BaseModel):
    TABLE_NAME = 'items'
    ENTITY_NAME_COL = 'item_name'

    def create_entity(self, entity_name, category_id):
        """Create item for given category"""
        query = f"""
        INSERT INTO {self.TABLE_NAME} ({self.ENTITY_NAME_COL}, category_id)
        VALUES ('{entity_name}', {category_id})
        RETURNING *
        """
        return self.pg_connection.save_income_data(query)


class UserCategory(BaseModel):
    TABLE_NAME = 'user_category'

    def create_entity(self, user_id, category_id):
        """Append category available for given user"""
        query = f"""
        INSERT INTO {self.TABLE_NAME} (user_id, category_id)
        VALUES ({user_id}, {category_id})
        RETURNING *
        """
        return self.pg_connection.save_income_data(query)
