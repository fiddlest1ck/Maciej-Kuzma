import tornado.ioloop
import tornado.web

from utils import _execute, get_key_values, BaseWebHandler


class MainHandler(BaseWebHandler):
    def put(self, pk):
        pk = str(pk)
        self.assure_json()
        self.assure_length()
        query = """update key_value set value = '{}' where key = '{}';""".format(self.request.body.decode(), pk)
        if pk in get_key_values() and self.request.body:
            _execute(query)

    def get(self, pk):
        pk = str(pk)
        query = """select value from key_value where key='{}'""".format(pk)
        if pk in get_key_values():
            _execute(query)
        else:
            raise tornado.web.HTTPError(404)

    def delete(self, pk):
        pk = str(pk)
        query = """update key_value set value = NULL where key = '{}';""".format(pk)
        if pk in get_key_values():
            _execute(query)
        else:
            raise tornado.web.HTTPError(400)


class BasicList(tornado.web.RequestHandler):

    def get(self):
        print(list(get_key_values()))
        self.finish(str(sorted(list(get_key_values()))))


def initialize_and_run():
    app = tornado.web.Application([
        (r"/api/objects/([a-zA-Z0-9]+)", MainHandler),
        (r"/api/objects", BasicList),
    ])
    app.listen(8080)
    tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__": # pragma: no cover
    initialize_and_run()
