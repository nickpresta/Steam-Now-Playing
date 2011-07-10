#!/usr/bin/env python

import logging

# Import controllers
from controllers import main as mainHandler
from controllers import steamid
from controllers import steamlogin

# Importing some of Google's AppEngine modules:
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util

# This is the main method that maps the URLs
# of your application with controller classes.
# If a URL is requested that is not listed here,
# a 404 error is displayed.

def main():
  logging.getLogger().setLevel(logging.DEBUG)
  application = webapp.WSGIApplication([
      ('/', mainHandler.MainHandler),
      ('/logout', mainHandler.LogoutHandler),
      #('/steamid', steamid.SteamIdHandler),
      ('/steamlogin', steamlogin.SteamLoginHandler),
    ], debug=True)
  util.run_wsgi_app(application)


if __name__ == '__main__':
  main()
