from datetime import date
from typing import Type

from ..models.unit import Unit as UnitModel
from ..utils import querries
from ..utils.session import DBSession
from ...web.parser import Unit as UnitTuple
from icecream import ic


def get_by_id(session: DBSession,
              model: Type[UnitModel], unit_id: int) -> UnitModel:
    unit = querries.get_object_by_value(session, model, "id", unit_id)
    return unit


def get_by_url(session: DBSession,
               model: Type[UnitModel], url: str) -> UnitModel:
    unit = querries.get_object_by_value(session, model, "url", url)
    return unit


def get_by_name(session: DBSession,
                model: Type[UnitModel], name: str) -> list[UnitModel]:
    units = querries.get_objects_by_value(
        session, model, "name", name)
    return units


def get_by_date(session: DBSession,
                model: Type[UnitModel], date: date) -> list[UnitModel]:
    units = Uquerries.get_objects_by_value(
        session, model, "date", date)
    return units


def save_from_namedtuple(session: DBSession, unit_tuple: UnitTuple) -> None:
    unit_dict = unit_tuple._asdict()
    ic(unit_dict)
    querries.save_dict_to_db(session, UnitModel, unit_dict)
