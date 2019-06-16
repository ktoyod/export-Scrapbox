import os
from urllib.parse import urljoin


class Config(object):
    CONNECT_SID = os.getenv('CONNECT_SID', '')

    API_BASE_URL = 'https://scrapbox.io/api/pages/'
    PROJECT_NAME = os.getenv('PROJECT_NAME', '')
    PROJECT_URL = urljoin(API_BASE_URL, PROJECT_NAME)
