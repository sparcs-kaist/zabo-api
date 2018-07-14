import requests
import hmac
import time
import os
import urllib


# SPARCS sso v2 Client Version 1.1
# VALID ONLY AFTER
# Made by SPARCS SSO Team

class Client:
    SERVER_DOMAIN = 'https://sparcs.sso.kaist.ac.kr/'
    BETA_DOMAIN = 'https://ssobeta.sparcs.org/'
    DOMAIN = None

    API_PREFIX = 'api/'
    VERSION_PREFIX = 'v2/'

    URLS = {
        'token_require': 'token/require/',
        'token_info': 'token/info/',
        'logout': 'logout/',
        'unregister': 'unregister/',
        'point': 'point/',
        'notice': 'notice/',
    }

    def __init__(self, client_id, secret_key, is_beta):
