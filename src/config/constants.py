from os import getenv


def get_env_constant(constant_name):
    env_value = getenv(constant_name)
    if env_value is None:
        raise ValueError(
            f"Переменная окружения {constant_name} не установлена")
    return env_value


MIREA_LOGIN = get_env_constant("LOGIN")
MIREA_PASSWORD = get_env_constant("PASSWORD")
TG_TOKEN = get_env_constant("TGTOKEN")
