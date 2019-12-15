from service_api.app import app
from service_api.api import load_api


def runserver(host, port, debug):
    app.run(host=host, port=port, debug=debug)


if __name__ == "__main__":
    try:
        load_api(app)
        runserver(host=app.config['APP_HOST'], port=app.config['APP_PORT'], debug=app.config['DEBUG'])
    except OSError as ex:
        print(ex)
    except Exception as ex:
        print(f'Unexpected error occurred: {str(ex)}')
