from http import HTTPStatus

from flask import request, abort

from service_api.db.models import Category, Item
from service_api.app import pg_conn
from service_api.views.base_view import BaseView


class CategoriesView(BaseView):
    def get(self):
        """Get all categories"""
        category_model = Category(pg_conn)
        result, status = category_model.get_all_entities()

        if status != HTTPStatus.OK.value:
            abort(self._get_response({'error_message': result}, status))

        response = self._get_response({'categories': result}, status)
        return response, status

    def post(self):
        """Create a new category"""
        self._validate_request(request, required=['category_name'])
        category_name = request.json.get('category_name')

        category_model = Category(pg_conn)
        result, status = category_model.create_entity(category_name)

        if status != HTTPStatus.CREATED.value:
            abort(self._get_response({'error_message': result}, status))

        response = self._get_response(result, status)
        return response, status


class CategoryItemsView(BaseView):
    def get(self, category_id):
        """Get all items for given category"""
        category_model = Category(pg_conn)
        self._check_entity_exists(category_id, category_model)

        result, status = category_model.get_category_items(category_id)

        if status != HTTPStatus.OK.value:
            abort(self._get_response({'error_message': result}, status))

        response = self._get_response(
            {
                'category_id': category_id,
                'items': result
            },
            status
        )
        return response, status

    def post(self, category_id):
        """Create a new item for given category"""
        self._validate_request(request, required=['item_name'])
        self._check_entity_exists(category_id, Category(pg_conn))

        item_name = request.json.get('item_name')

        item_model = Item(pg_conn)
        result, status = item_model.create_entity(item_name, category_id)

        if status != HTTPStatus.CREATED.value:
            abort(self._get_response({'error_message': result}, status))

        response = self._get_response(result, status)

        return response, status
