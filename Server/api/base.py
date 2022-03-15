import asyncio
from abc import ABCMeta, abstractmethod, ABC

from aiohttp import web

# Базовый класс  для обработки http запросов
class BaseView(web.View, metaclass=ABCMeta):
    # api route
    ENDPOINT: str

    # обработка в отдельном потоке запроса
    async def handle_request(self):
        response = await asyncio.to_thread(self.compute)
        return response

    # извлечение параметров запроса
    def _from_query(self, parameter, is_optional=False):
        value = self.request.rel_url.query.get(parameter)
        if not value and not is_optional:
            raise web.HTTPBadRequest(reason=f"{value} is required")
        return value

    # ожидание скачивания body запроса
    async def _await_body(self):
        self.body = await self.request.json()

    # извлечение полей из body
    def _from_body(self, parameter, is_optional=False):
        value = self.body.get(parameter)
        if not value and not is_optional:
            raise web.HTTPBadRequest(reason=f"{value} is required")
        return value

    # виртуальная функция, которая перегружается кодом для обработки конкретного запроса
    @abstractmethod
    async def compute(self) -> dict:
        pass


# класс для обработки GET запросов
class GetView(BaseView, ABC):
    async def get(self):
        response = await self.handle_request()
        return web.json_response(response)

# класс для обработки POST запросов
class PostView(BaseView, ABC):
    async def post(self):
        await self._await_body()
        response = await self.handle_request()
        return web.json_response(response)

