from http import HTTPStatus
from datetime import datetime
import json

from flask.views import MethodView
from flask import Response
from flask import abort


class BaseView(MethodView):

    def _validate_request(self, request, required):
        """
            Method checking all required params are present in request body
            (can be extended to check also headers and query parameters)
        """
        for key in required:
            if key not in request.json:
                error_message = f'{key} parameter is needed'
                status = HTTPStatus.BAD_REQUEST.value
                abort(self._get_response({'message': error_message}, status))

    def _check_entity_exists(self, entity_id, model, status_failed=HTTPStatus.NOT_FOUND.value):
        """
            Method checking whether the entity related to new object exists in DB
            Returns 404 if entity is as part of path tree, 400 if got from json body
            Returns 503 if connection with database lost
        """
        result, status = model.get_entity_by_id(entity_id)
        if status != HTTPStatus.OK.value:
            error_message = result
            abort(self._get_response({'error_message': error_message}, status))
        elif not result:
            error_message = f'{model.TABLE_NAME} entity with id {entity_id} does not exist'
            abort(self._get_response({'error_message': error_message}, status_failed))

    @staticmethod
    def _get_response(data, status=HTTPStatus.OK.value):
        """Builds response object with data or error message, status and current timestamp"""
        resp_obj = {
            'data': data,
            'status': 'success'
            if (status == HTTPStatus.OK.value or status == HTTPStatus.CREATED.value)
            else 'failed',
            'timestamp': str(datetime.utcnow())
        }

        response = Response(json.dumps(resp_obj), status, content_type='application/json')

        return response


class HelloWorldView(BaseView):
    def get(self):
        result = {'hello': 'world'}
        status = HTTPStatus.OK.value
        response = self._get_response(result, status)
        return response, status
