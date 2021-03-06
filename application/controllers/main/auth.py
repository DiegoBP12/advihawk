#!/usr/bin/env python
# -*- coding:utf-8 -*-

import web
import urllib
import urlparse
import json
import app

# Google API Token
app_id = app.app_id
app_secret = app.app_secret


parameters = {
  'google': {
    'app_id': app_id,
    'app_secret': app_secret,
    'scope': 'https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/userinfo.email'
  }
  
}

class handler:
  """Authentication and authorization of users by OAuth 2.0
  """

  SUPPORTED_PROVIDERS = ['google', 'facebook']

  # provider: (auth_type, auth_url, access_token_url, parser_type)
  PROVIDERS = {
    'google':   ('oauth2',
      'https://accounts.google.com/o/oauth2/auth',
      'https://accounts.google.com/o/oauth2/token',
      '_json_parser'),
    'facebook': ('oauth2',
      'https://www.facebook.com/dialog/oauth',
      'https://graph.facebook.com/oauth/access_token',
      '_query_string_parser'),
  }

  def auth_init(self, provider):
    print "auth_init(self, provider): 100"
    self._oauth2_init(provider)

  def auth_callback(self, provider):
    print "auth_callback(self, provider): 101"
    self._oauth2_callback(provider)

  def on_signin(self, provider, profile):
    """Callback when the user successfully signs in the account of the provider
    (e.g., Google account or Facebook account). Developers should overwrite this
    funciton.

    Arguments:
      provider: google or facebook
      profile: the user profile of Google or facebook account of the user who
               signs in.

    Possible implementation of this callback:

    1. Set unique user_id:
      ```
      user_id = '%s:%s' % (provider, profile['id'])
      ```

    2. check whether the user_id is in database

    3. create a new entry in the database if the user_id is not in the database.
       i.e., the user is a new user in our webapp, and add this user in our
       database.

    4. sign in the user in our webapp by setting user id and profile in session
       or cookie. For example,
      ```
      # sign in the user by session:
      session.id = user_id
      # Or sign in the user by cookie:
      web.setcookie('_id', user_id)
      ```

    5. Redirect the user to other page. For example,
      ```
      raise web.seeother('/profile')
      ```

    """
    print "on_signin(self, provider, profile): 102"
    raise web.seeother('/')
    # raise NotImplementedError

  def _http_get(self, url, args=None):
    if args == None:
      response = urllib.urlopen(url)
    else:
      query_string = urllib.urlencode(args)
      response = urllib.urlopen('%s?%s' % (url, query_string))
    print "_http_get(self, url, args=None): 103"
    return response

  def _http_post(self, url, args):
    data = urllib.urlencode(args)
    response = urllib.urlopen(url, data)
    print "_http_post(self, url, args): 104"
    return response

  def _check_provider(self, provider):
    print "_check_provider(self, provider): 105"
    # check if the provider is supported
    if provider not in self.SUPPORTED_PROVIDERS:
      raise Exception('unsupported provider: %s' % provider)

    # check if app_id is None
    if not parameters[provider]['app_id']:
      raise Exception('invalid %s app id: %s' %
                      (provider, parameters[provider]['app_id']))

    # check if app_secret is None
    if not parameters[provider]['app_secret']:
      raise Exception('invalid %s app secret: %s' %
                      (provider, parameters[provider]['app_secret']))


  def _oauth2_init(self, provider):
    '''
    Google o Facebook muestran su pagina de inicio de sesion para autenticar usuarios
    '''
    self._check_provider(provider)

    args = {
      'response_type': 'code',
      'client_id': parameters[provider]['app_id'], 
      'redirect_uri': self.callback_uri(provider),
      'scope': parameters[provider]['scope']
    }

    auth_url = self.PROVIDERS[provider][1] + '?' + urllib.urlencode(args)

    # redirect users to login page of the provider
    print " _oauth2_init(self, provider): 106"
    raise web.seeother(auth_url)

  def _oauth2_callback(self, provider):
    """Step 2 of oauth 2.0: Handling response from login page of providers.
    Case 1) If auth (authentication and authorization) not ok, raise Exception.
    Case 2) If auth ok, get access_token first, and then use the access_token to
            retrieve user profile.
    """
    
    self._check_provider(provider)

    # check whether auth is ok, if not ok, raise Exception.
    error = web.input().get('error')
    if error:
      raise Exception(error)

    # auth ok, get access_token
    code = web.input().get('code')

    args = {
      'code': code,
      'client_id': parameters[provider]['app_id'], 
      'client_secret': parameters[provider]['app_secret'], 
      'redirect_uri': self.callback_uri(provider),
      'grant_type': 'authorization_code'
    }

    _parser = getattr(self, '%s' % self.PROVIDERS[provider][3])
    response = _parser(
        self._http_post(self.PROVIDERS[provider][2], args).read() )
    if response.get('error'):
      raise Exception(response)

    # access_token is ready, get user profile.
    _fetcher = getattr(self, '_get_%s_user_data' % provider)
    profile = _fetcher(response['access_token'])

    # user profile ok. call on_signin function
    print "_oauth2_callback(self, provider): 107"
    self.on_signin(provider, profile)

  def callback_uri(self, provider):
    """Should overwrite this method in child class.
    Implementation example: 
      return 'http://localhost:8080/auth/%s/callback' % provider
    OR
      return 'https://' + web.ctx.host + '/auth/%s/callback' % provider
    """
    print "callback_uri(self, provider): 108"
    return 'https://' + web.ctx.host + '/auth/%s/callback' % provider
    # raise NotImplementedError

  def _get_facebook_user_data(self, access_token):
    """Facebook APIs › Graph API
      https://graph.facebook.com/me
    returns the active user's profile
    """
    print "_get_facebook_user_data(self, access_token): 109"
    return json.loads(
        self._http_get('https://graph.facebook.com/me',
                       dict(access_token=access_token)).read()
      )

  def _get_google_user_data(self, access_token):
    """Obtaining User Profile Information from Google API
    userinfo endpoint:
      https://www.googleapis.com/oauth2/v3/userinfo
    """
    profile = json.loads(
        self._http_get('https://www.googleapis.com/oauth2/v3/userinfo',
                       dict(access_token=access_token)).read()
      )

    if 'id' not in profile and 'sub' in profile:
      profile['id'] = profile['sub']
    print "_get_google_user_data(self, access_token): 110"
    return profile

  def _query_string_parser(self, string):
    """Parse query-string-format string, and return Python dict object
    """
    print "_query_string_parser(self, string): 111"
    return dict(urlparse.parse_qsl(string))

  def _json_parser(self, string):
    """Parse JSON format string, and return Python dict object
    """
    print "_json_parser(self, string): 112"
    return json.loads(string)
