#!/usr/bin/env python

import os

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

from utils.getnowplaying import SteamUserDataFetcher
from gaesessions import get_current_session

class LogoutHandler(webapp.RequestHandler):
  """Cleans up all sessions before logging the user out"""
  def get(self):
    logout_url = users.create_logout_url('/')

    # Terminate existing session with profile ID
    session = get_current_session()
    if session.has_key('profile_id'):
      session.terminate()

    self.redirect(logout_url)

class MainHandler(webapp.RequestHandler):
  """Renders the main page, prompts for Steam ID"""
  def get(self):
    url = self.request.url
    user = users.get_current_user()
    session = get_current_session()

    fetcher = SteamUserDataFetcher()

    if session.has_key('profile_id'):
      details = fetcher.get_user_details(session['profile_id'])
    else:
      details = {}

    path = os.path.join(os.path.dirname(__file__), '../views', 'index.html')
    self.response.out.write(
        template.render(path, {
          'nickname': user.nickname(),
          'details': details,
          'url': url,
          })
        )
