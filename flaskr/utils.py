import flask


def get_user_ip(request: flask.Request) -> str:
  return request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
