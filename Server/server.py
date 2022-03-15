from aiohttp import web

from .api import VIEWS

# основной класс сервера обработки http запросов
class Server:
    def __init__(self, port=8000, host="localhost"):
        self.port = port
        self.host = host
        self.app = web.Application()

    def run(self):
        print(f"Run server")

        for view in VIEWS:
            self.app.router.add_route("*", view.ENDPOINT, view)

        web.run_app(self.app, host=self.host, port=self.port)
