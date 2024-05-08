from . import api
class Handler:
    def __init__(self) -> None:
        self.api = api.Api()
    def setup(self,router):
        router.add_url_rule("/save","save",self.api.save_file, methods=["POST"],)
        router.add_url_rule("/ping","ping",self.api.ping, methods=["GET"], )
        return router
