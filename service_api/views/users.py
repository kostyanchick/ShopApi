from http import HTTPStatus

from flask import request, abort

from service_api.db.models import User, Category, UserCategory
from service_api.app import pg_conn
from service_api.views.base_view import BaseView


class UsersView(BaseView):
    def get(self):
        """Get all users"""
        user_model = User(pg_conn)
        result, status = user_model.get_all_entities()

        if status != HTTPStatus.OK.value:
            abort(self._get_response({'error_message': result}, status))

        response = self._get_response({'users': result}, status)
        return response, status

    def post(self):
        """Creates a new user with given user_name"""
        self._validate_request(request, required=['user_name'])
        user_name = request.json.get('user_name')

        user_model = User(pg_conn)
        result, status = user_model.create_entity(user_name)

        if status != HTTPStatus.CREATED.value:
            abort(self._get_response({'error_message': result}, status))

        response = self._get_response(result, status)
        return response, status


class UserCategoriesView(BaseView):
    def get(self, user_id):
        """Get all categories available for given user"""
        user_model = User(pg_conn)
        self._check_entity_exists(user_id, user_model)
        result, status = user_model.get_available_categories(user_id)

        if status != HTTPStatus.OK.value:
            abort(self._get_response({'error_message': result}, status))

        response = self._get_response(
            {
                'user_id': user_id,
                'categories': result
            },
            status
        )
        return response, status

    def post(self, user_id):
        """Make category available to given user"""
        self._validate_request(request, required=['category_id'])
        self._check_entity_exists(user_id, User(pg_conn))
        category_id = request.json.get('category_id')
        self._check_entity_exists(category_id, Category(pg_conn),
                                  status_failed=HTTPStatus.BAD_REQUEST.value)

        user_category_model = UserCategory(pg_conn)
        result, status = user_category_model.create_entity(user_id=user_id, category_id=category_id)

        if status != HTTPStatus.CREATED.value:
            abort(self._get_response({'error_message': result}, status))

        response = self._get_response(result, status)
        return response, status


class UserItemsView(BaseView):
    def get(self, user_id):
        """Get all items from categories available for given user"""
        user_model = User(pg_conn)
        self._check_entity_exists(user_id, user_model)

        result, status = user_model.get_available_items(user_id)

        if status != HTTPStatus.OK.value:
            abort(self._get_response({'error_message': result}, status))

        response = self._get_response(
            {
                'user_id': user_id,
                'items': result
            },
            status
        )
        return response, status
