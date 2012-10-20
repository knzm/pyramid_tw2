import tw2.core.middleware
from pyramid.response import Response


class Tw2TweenFactory(object):
    def __init__(self, handler, registry):
        self.handler = handler
        # self.registry = registry

        self.app = tw2.core.middleware.make_middleware(
            self.wrapper, config=registry.settings)

        self.reset()

    def reset(self, request=None):
        self._request = request
        self._response = None
        self._status = None
        self._headers = None

    def __call__(self, request):
        self.reset(request)
        res = self.app(request.environ, self.start_response)
        return Response(status=self._status, headerlist=self._headers,
                        app_iter=res)

    def wrapper(self, environ, start_response):
        response = self.handler(self._request)
        self._response = response
        start_response(response.status, response.headerlist)
        return response.body

    def start_response(self, status, headers):
        self._status = status
        self._headers = headers


def includeme(config):
    config.add_tween('pyramid_tw2.Tw2TweenFactory')
