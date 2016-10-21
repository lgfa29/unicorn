import os
import tornado.ioloop
import tornado.web
import tornado.websocket

from tornado.options import define, options

define("port", default=8888, help="run on the given port", type=int)

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/ws/color", ColorSocketHandler),
        ]

        settings = dict(
            cookie_secret="DoDULMxOdWedpoidH50S673aCkVnjCN40O5UaU3TvL2GIb4vswTrcsKxyvN4SVzJFTqRrexZQN328Uap3T3STVtb3CJtA0yMA347IyI8X9v3mDmLBBfHRKCwMWnYhT8B",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=True,
        )

        super(Application, self).__init__(handlers, **settings)

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html", last_color=ColorSocketHandler.last_color)

class ColorSocketHandler(tornado.websocket.WebSocketHandler):
    clients = set()
    last_color = '#000000'

    def open(self):
        ColorSocketHandler.clients.add(self)

    def on_close(self):
        ColorSocketHandler.clients.remove(self)

    def on_message(self, message):
        parsed = tornado.escape.json_decode(message)

        ColorSocketHandler.last_color = parsed["color"]

        for client in ColorSocketHandler.clients:
            try:
                client.write_message(parsed)
            except:
                print("failed to send message")

def main():
    tornado.options.parse_command_line()
    app = Application()
    app.listen(options.port)

    print("Listening on port %s" % options.port)

    tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    main()
