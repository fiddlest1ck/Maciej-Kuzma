import json
from unittest.mock import Mock, patch
import pytest
import tornado.web
import tornado.ioloop
import tornado.testing
import sqlite3
from server import MainHandler, BasicList, BaseWebHandler, initialize_and_run
import utils


@patch.object(utils, 'db_path', 'test_key_value.db')
class MainHandlerTest(tornado.testing.AsyncHTTPTestCase):

    def get_app(self):
        app = tornado.web.Application([
            (r"/api/objects/([a-zA-Z0-9]+)", MainHandler),
            (r"/api/objects", BasicList),
        ])
        return app

    def test_put_data(self):
        put_data = 'dsadasdadasd'
        response = self.fetch(
            '/api/objects/key1', method='PUT', body=json.dumps(put_data), headers={'Content-Type': 'application/json'})
        assert response.code == 200

    def test_get_data(self):
        response = self.fetch(
            '/api/objects/key1', method='GET'
        )
        assert response.code == 200

    def test_failed_get_data(self):
        response = self.fetch(
            '/api/objects/nonexistkey', method='GET'
        )
        assert response.code == 404

    def test_delete_data(self):
        response = self.fetch(
            '/api/objects/key1', method='DELETE'
        )
        assert response.code == 200

    def test_failed_delete_data(self):
        response = self.fetch(
            '/api/objects/nonexistkey', method='DELETE'
        )
        assert response.code == 400

    def test_get_keys_list(self):
        response = self.fetch(
            '/api/objects', method='GET'
        )
        assert response.code == 200
        assert response.body == "['key1', 'key2', 'key3']".encode()


@patch('tornado.ioloop.IOLoop.instance')
def test_initialize_and_run(mock_ioloop_instance):
    initialize_and_run()
    mock_ioloop_instance.assert_called_with()

def test_base_web_handler_assure_json_bad():
    mock_request = Mock()
    mock_request.headers = {'Content-Type': 'text/plain'}
    with pytest.raises(tornado.web.HTTPError) as error:
        BaseWebHandler(MainHandlerTest.get_app(None), mock_request).assure_json()
    assert error.value.status_code == 400

def test_content_lenght_greater_than_1mb():
    mock_request = Mock()
    mock_request.headers = {'Content-Length': 9999999}
    with pytest.raises(tornado.web.HTTPError) as error:
        BaseWebHandler(MainHandlerTest.get_app(None), mock_request).assure_length()
    assert error.value.status_code == 413
