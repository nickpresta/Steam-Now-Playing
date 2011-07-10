#!/usr/bin/env python

import os

from utils.getnowplaying import SteamUserDataFetcher

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

# This controller handles the
# generation of the front page.

class SteamIdHandler(webapp.RequestHandler):
  """Fetches the Steam ID given the form input"""
  def post(self):
    user = users.get_current_user()

    text_input = self.request.get('steamid').strip()

    fetcher = SteamUserDataFetcher()
    details = fetcher.get_user_details(text_input)

    path = os.path.join(os.path.dirname(__file__), '../views', 'index.html')
    self.response.out.write(
        template.render(path, {
          'input': text_input,
          'nickname': user.nickname(),
          'details': details
          })
        )
