from http import HTTPStatus

from flask import abort

from service_api.db.models import Item
from service_api.app import pg_conn
from service_api.views.base_view import BaseView


class ItemsView(BaseView):
    def get(self):
        """Get all items"""
        item_model = Item(pg_conn)
        result, status = item_model.get_all_entities()
        if status != HTTPStatus.OK.value:
            abort(self._get_response({'error_message': result}, status))

        response = self._get_response({'categories': result}, status)
        return response, status
