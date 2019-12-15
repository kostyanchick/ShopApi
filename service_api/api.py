from flask.blueprints import Blueprint
from flask import Flask

from service_api.views.base_view import HelloWorldView
from service_api.views.users import UsersView, UserCategoriesView, UserItemsView
from service_api.views.categories import CategoriesView, CategoryItemsView
from service_api.views.items import ItemsView


def load_api(app: Flask):
    api_prefix = '/{service_name}/v1'.format(service_name=app.config.get("SERVICE_NAME"))
    api_v1 = Blueprint('v1', __name__, url_prefix=api_prefix)

    api_v1.add_url_rule('/', view_func=HelloWorldView.as_view('hello_world'))

    api_v1.add_url_rule('/users', view_func=UsersView.as_view('users'))
    api_v1.add_url_rule('/users/<user_id>/categories', view_func=UserCategoriesView.as_view('user_categories'))
    api_v1.add_url_rule('/users/<user_id>/items', view_func=UserItemsView.as_view('user_items'))

    api_v1.add_url_rule('/categories', view_func=CategoriesView.as_view('categories'))
    api_v1.add_url_rule('/categories/<category_id>/items', view_func=CategoryItemsView.as_view('category_items'))

    api_v1.add_url_rule('/items', view_func=ItemsView.as_view('items'))

    app.register_blueprint(api_v1)
