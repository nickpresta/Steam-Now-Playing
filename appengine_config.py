# Make webapp.template use django 1.2
webapp_django_version = '1.2'

from gaesessions import SessionMiddleware
def webapp_add_wsgi_middleware(app):
  app = SessionMiddleware(app, cookie_key="b34015c4940605c7d7f089a9b60feb159547427c")
  return app
