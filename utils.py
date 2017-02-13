import tornado.web
import sqlite3

db_path = 'key_value.db'


class BaseWebHandler(tornado.web.RequestHandler):
    def assure_json(self):
        if not self.request.headers['Content-Type'].startswith('application/json'):
            raise tornado.web.HTTPError(400)

    def assure_length(self):
        if int(self.request.headers['Content-Length']) > 1000000:
            raise tornado.web.HTTPError(413)

def _execute(query):
    connection = sqlite3.connect(db_path)
    cursorobj = connection.cursor()
    cursorobj.execute(query)
    result = cursorobj.fetchall()
    connection.commit()
    connection.close()
    return result

def get_key_values():
    query = '''select * from key_value;'''
    result = _execute(query)
    return dict(result)
