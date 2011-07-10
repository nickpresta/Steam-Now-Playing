#!/usr/bin/env python

import os
import logging

from utils.getnowplaying import SteamUserDataFetcher

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

from gaesessions import get_current_session

# This controller handles the
# generation of the front page.

class SteamLoginHandler(webapp.RequestHandler):
  """Handles the logging in through Steam. Extracts the SteamID64 field."""
  def get(self):
    session = get_current_session()

    fetcher = SteamUserDataFetcher()
    user_id = self.request.get('openid.claimed_id').split("/")[-1]
    if fetcher.isValidId64(user_id):
      session['profile_id'] = user_id
    else:
      logging.warning("Steam ID: %s" % user_id)

    self.redirect('/')
