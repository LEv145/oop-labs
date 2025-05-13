import re

from logger import Logger
from filters import TextLogFilter, RegexLogFilter
from handlers import ConsoleHandler, FileHandler


def main() -> None:
    filters = [
        TextLogFilter("ERROR"),
        RegexLogFilter(re.compile("^[Ww][Aa][Rr][Nn]")),
    ]
    handlers = [
        ConsoleHandler(),
        FileHandler("logs/app.log"),
    ]
    logger = Logger(filters, handlers)

    logger.log("INFO Это сообщение будет отфильтровано")
    logger.log("WARN Что‑то подозрительное обнаружено")
    logger.log("ERROR Произошла ошибка!")
    logger.log("debug тест, не должно пройти")
    logger.log("warn в нижнем регистре тоже считается предупреждением")


if __name__ == "__main__":
    main()
