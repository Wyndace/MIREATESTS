
from httpx import Client

from ..database.utils.session import DBSession
from ..database.usecase import unit as UnitUsecases
from ..web import parser
from ...config import constants
from icecream import ic


def save_unit_to_db():
    client = Client()
    db_session = DBSession()
    login_token = parser.get_logintoken(client)
    parser.login(client, constants.MIREA_LOGIN,
                 constants.MIREA_PASSWORD, login_token)
    links = parser.get_tests_url(client)
    for link in links:
        unit = parser.get_unit(client, link)
        ic(unit)
        UnitUsecases.save_from_namedtuple(db_session, unit)
