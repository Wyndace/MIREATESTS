from datetime import date, datetime
from time import time
from httpx import Client
from typing import Any, NamedTuple
from selectolax.parser import HTMLParser, Node
from re import search as regex_search
from icecream import ic
from .connector import Connector
from ...config import urls


class Unit(NamedTuple):
    url: str
    name: str
    subject: str
    date_start: date
    date_end: date
    time_end: int
    passed_points: float
    max_points: float
    eval_method: str
    attempts: int


months = {
    'Январь': 1,
    'Февраль': 2,
    'Март': 3,
    'Апрель': 4,
    'Май': 5,
    'Июнь': 6,
    'Июль': 7,
    'Август': 8,
    'Сентябрь': 9,
    'Октябрь': 10,
    'Ноябрь': 11,
    'Декабрь': 12
}


def get_item_text(block: Node | HTMLParser, selector: str = "",
                  deep: bool = True) -> str:
    try:
        if selector:
            return block.css_first(selector).text(deep=deep)\
                .replace('\xa0', ' ').strip()
        return block.text(deep=deep).replace('\xa0', '').strip()
    except AttributeError as e:
        ic(e)
        return ""


def get_item_attribute(block: Node | Any,
                       attribute: str, selector: str = "") -> str | None:
    try:
        if selector:
            return block.css_first(selector).attributes.get(attribute)
        return block.attributes.get(attribute)
    except AttributeError as e:
        ic(e)
        return ""


def get_value_from_regex(regex: str, string: str | None) -> str:
    if not string:
        return ""
    regex_result = regex_search(regex, string)
    if regex_result:
        return regex_result.group()
    else:
        return ""


def get_html(client: Client, url: str) -> str | None:
    r = Connector.get(client, url)
    if r:
        return r.text


def get_logintoken(client) -> str:
    raw_html = get_html(client, urls.HTTPS_ONLINE_EDU)
    login_token = ""
    if raw_html:
        html = HTMLParser(raw_html)
        login_token = get_item_attribute(
            html, "value", "input[name=logintoken]")
    if not login_token:
        login_token = ""
    return login_token


def login(client: Client, login: str, password: str, login_token: str) -> bool:
    r = Connector.post(client,
                       urls.HTTPS_ONLINE_EDU + "/login/index.php",
                       data={"username": login, "password": password,
                             "logintoken": login_token})
    if r:
        return True
    else:
        return False


def get_tests_url(client: Client) -> set[str]:
    html = get_html(client, urls.CALENDAR + "&time=" + str(int(time())))
    dates_url = set([])
    if html:
        links = HTMLParser(html).css("[data-event-component=mod_quiz] a")
        for link in links:
            dates_url.add(get_item_attribute(link, "href"))
    return dates_url


def get_unit(client: Client, url) -> Unit:
    name = ""
    subject = ""
    time_end = 0
    passed_points = 0.0
    max_points = 0.0
    eval_method = ""
    attempts = 0
    date_start = date.today()
    date_end = date.today()
    raw_html = get_html(client, url)
    if raw_html:
        html = HTMLParser(raw_html)
        content = html.css_first("[role=main]")

        name = get_item_text(content, "h2")
        subject = get_item_text(html, "h1")

        dates = html.css("[data-region=activity-dates] div")
        date_start = get_item_text(dates[0],
                                   deep=False).replace("Открыто: ", "")
        time = date_start.split(', ')[2]
        date_start = date_start.split(', ')[1]
        ic(date_start)
        day, month_name, year = date_start.split()
        month = months[month_name]
        date_time_str = f"{year}-{month:02d}-{int(day):02d} {time}"
        date_start = datetime.strptime(date_time_str, "%Y-%m-%d %H:%M")

        date_end = get_item_text(dates[1], deep=False).replace("Закрыто: ", "")
        time = date_end.split(', ')[2]
        date_end = date_end.split(', ')[1]
        day, month_name, year = date_end.split()
        month = months[month_name]
        date_time_str = f"{year}-{month:02d}-{int(day):02d} {time}"
        date_end = datetime.strptime(date_time_str, "%Y-%m-%d %H:%M")

        time_end = 0
        passed_points = 0.0
        max_points = 0.0
        eval_method = ""
        attempts = 0

        quizinfo = html.css(".quizinfo p")
        for info in quizinfo:
            text_info = get_item_text(info)
            if "Разрешено попыток: " in text_info:
                # TODO завершить блок с попытками, временем на тест,
                # мин. и макс баллом + методом оценивания и кол-во попыток
                text_info = text_info.replace("Разрешено попыток: ", "")
                attempts = int(text_info)
            if "Ограничение по времени: " in text_info:
                hours = 0
                minutes = 0
                seconds = 0
                parts = text_info.replace(
                    "Ограничение по времени: ", "").split()
                for i in range(len(parts)):
                    if parts[i] == 'ч.':
                        hours = int(parts[i - 1])
                    elif parts[i] == 'мин.':
                        minutes = int(parts[i - 1])
                    elif parts[i] == 'сек.':
                        seconds = int(parts[i - 1])
                    time_end = hours * 60 * 60 + minutes * 60 + seconds
            if "Метод оценивания: " in text_info:
                text_info = text_info.replace("Метод оценивания: ", "")
                eval_method = text_info
            if "Проходная оценка: " in text_info:
                text_info = text_info.replace(
                    "Проходная оценка: ", "").split(" из ")
                passed_points = float(text_info[0].replace(",", "."))
                max_points = float(text_info[1].replace(",", "."))
    unit = Unit(url, name, subject, date_start, date_end,
                time_end, passed_points, max_points, eval_method, attempts)
    return unit


def run():
    # test function
    ...


if __name__ == "__main__":
    run()
