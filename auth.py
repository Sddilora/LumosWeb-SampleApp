import re
from LumosWeb.middleware import Middleware
# Custom middlewares should inherit from the Middleware class.

STATIC_TOKEN = "ae4CMvqBe2"

class TokenMiddleware(Middleware):
    _regex = re.compile(r"^Token: (\w+)$")

    def process_request(self, req):
        header = req.headers.get("Authorization", "")
        match = self._regex.match(header)
        token = match and match.group(1) or None
        req.token = token

class InvalidTokenException(Exception):
    pass

def login_required(handler):
    def wrapped_view(req, resp, *args, **kwargs):
        token = getattr(req, "token", None)

        if token is None or token != STATIC_TOKEN:
            raise InvalidTokenException("Invalid token")
        
        return handler(req, resp, *args, **kwargs)
    
    return wrapped_view

def on_exception(req, resp, exc):
    if isinstance(exc, InvalidTokenException):
        resp.status_code = 401
        resp.text = "Invalid token. What are you trying to do stranger!."
    elif isinstance(exc, ValueError):
        resp.status_code = 400
        resp.text = "Bad request. Could not decode JSON."
    else:
        raise exc