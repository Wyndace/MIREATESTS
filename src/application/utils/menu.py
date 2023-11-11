def chooser_menu(inp_text: str, count_items: int) -> int:
    choice = -1
    while 0 > choice > count_items:
        try:
            choice = int(input(inp_text))
        except KeyboardInterrupt:
            print("\n\nВыходим из данного блока...\n")
            return count_items+1
        except ValueError:
            print('\nВведёно неверное значение! Попробуйте ещё раз!\n')
            continue
        if int(choice) == count_items+1:
            print("\nВыходим из данного блока...\n")
            return count_items+1
        if 0 > choice > count_items:
            print('\nВведено неверное значение! Попробуйте ещё раз!\n')
    return choice


def multi_chooser_menu(inp_text: str, items: list | tuple) -> int:
    choice = ''
    while '' == choice:
        try:
            print(inp_text)
            for i, item in enumerate(items, start=1):
                print(f'\t{i}.) {item}')
            print(f'\t{len(items)+1}.) Выйти из блока')
            choice = int(input(inp_text))
        except KeyboardInterrupt:
            print("\n\nВыходим из данного блока...\n")
            return len(items)+1
        except ValueError:
            print('\nВведёно неверное значение! Попробуйте ещё раз!\n')
            continue
        if int(choice) == len(items)+1:
            print("\nВыходим из данного блока...\n")
            return len(items)+1
        if 0 > int(choice) > len(items):
            print('\nВведёно неверное значение! Попробуйте ещё раз!\n')
            choice = -1
            continue
    return int(choice)
