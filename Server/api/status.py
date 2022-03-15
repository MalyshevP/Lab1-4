from .base import GetView

# api чтобы проверить работоспособность сервера
class StatusView(GetView):
    ENDPOINT = "/status"

    def compute(self):
        return {"status": "OK"}
