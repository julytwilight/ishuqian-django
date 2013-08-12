# -*- coding: utf-8 -*-
from weibo import APIClient

APP_KEY      = '3120994132'                            # app key
APP_SECRET   = '6507333a8c1c432eab40723e9bef204c'      # app secret
CALLBACK_URL = 'http://ishuqian.com/callback/weibo'     # callback url

client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)

def get_authorize_url():
    return client.get_authorize_url()

def get_user_info(code):
    r = client.request_access_token(code)
    client.set_access_token(r.access_token, r.expires_in)
    return [client.users.show.get(uid=r.uid), r]