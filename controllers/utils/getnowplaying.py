#!/usr/bin/python

# Author: Nick Presta 2011
# Email: nick@nickpresta.ca
# License: BSD

import sys
import urllib2
from xml.etree import ElementTree

"""Fetches the game you're currently playing on Steam"""

class SteamUserDataFetcher(object):
  """Fetches user data from Steam for a specific user"""

  PROFILE_CUSTOM_URI = 'http://steamcommunity.com/id/%s?xml=1'
  PROFILE_DEFAULT_URI = 'http://steamcommunity.com/profiles/%s?xml=1'

  def _choose_uri(self, user_id):
    """If a user ID is a 17 or 25 digit integer string, use the default URI
       otherwise, use the custom URI"""
    mapping = {True: SteamUserDataFetcher.PROFILE_DEFAULT_URI,
               False: SteamUserDataFetcher.PROFILE_CUSTOM_URI}
    self._profile_uri = mapping[self.isValidId64(user_id)] % user_id
    return self._profile_uri

  def isValidId64(self, user_id):
    """Determines if a numeric profile id is valid."""
    return (len(user_id) == 17 or len(user_id) == 25) and user_id.isdigit()

  def _is_valid_profile(self, error):
    if not error:
      return True
    else:
      if 'could not be found' in error:
        return False

  def _fetch_user_data(self, user_id):
    """Fetches the raw XML from the user's profile page
       and returns an XML document object"""
    page = urllib2.urlopen(self._choose_uri(user_id))
    data = page.read()
    page.close()
    return ElementTree.fromstring(data)

  def get_user_details(self, user_id):
    """ Fetches the user details and formats them in a dictionary """
    document = self._fetch_user_data(user_id)
    error_text = document.findtext('error')
    out_dict = {
        # Error string, if any
        'errorText': error_text,
        'isValidProfile': self._is_valid_profile(error_text),
        # Player details
        'steamID64': document.findtext('steamID64'),
        'steamID': document.findtext('steamID'),
        'customURL': document.findtext('customURL'),
        'privacyState': document.findtext('privacyState'),
        'visibilityState': document.findtext('visibilityState'),
        'onlineState': document.findtext('onlineState'),
        'stateMessage': document.findtext('stateMessage'),
        # Game details
        'inGameServerIP': document.findtext('inGameServerIP'),
        'gameName': document.findtext('inGameInfo/gameName'),
        'gameLink': document.findtext('inGameInfo/gameLink'),
        'gameIcon': document.findtext('inGameInfo/gameIcon'),
        'gameLogo': document.findtext('inGameInfo/gameLogo'),
        'gameLogoSmall': document.findtext('inGameInfo/gameLogoSmall')}

    out_dict['profileURL'] = self._profile_uri.replace('?xml=1', '')

    return out_dict

if __name__ == '__main__':
  if len(sys.argv) != 2:
    user_id = 'nickpresta'
  else:
    user_id = sys.argv[1]
    fetcher = SteamUserDataFetcher()
    print fetcher.get_user_details(user_id)
