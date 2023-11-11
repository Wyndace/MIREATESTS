from httpx import Client

from ..web import parser
from ...config import constants
from icecream import ic


def print_dates_link_to_console():
    client = Client()
    login_token = parser.get_logintoken(client)
    parser.login(client, constants.MIREA_LOGIN,
                 constants.MIREA_PASSWORD, login_token)
    ic(parser.get_tests_url(client))


def print_unit_to_console():
    client = Client()
    login_token = parser.get_logintoken(client)
    parser.login(client, constants.MIREA_LOGIN,
                 constants.MIREA_PASSWORD, login_token)
    links = parser.get_tests_url(client)
    for link in links:
        ic(parser.get_unit(client, link))
