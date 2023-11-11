from src.application.database.models.unit import Unit
from src.application.database.utils.session import DBSession
from src.application.utils import menu
from src.application.controllers import parserconsole, parserdatabase, databasetg


def main():
    items = (
        "Показать ссылки на тесты в этом месяце",
        "Показать тесты в этом месяце",
        "Сохранить тесты этого месяца в Б/Д",
    )
    choice = menu.multi_chooser_menu("Выберите пункт меню: ", items)
    if choice == 1:
        parserconsole.print_dates_link_to_console()
    if choice == 2:
        parserconsole.print_unit_to_console()
    if choice == 3:
        parserdatabase.save_unit_to_db()
    DBSession().close_session()


if __name__ == "__main__":
    main()
