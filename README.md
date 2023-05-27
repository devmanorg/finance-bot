# Lebowski — менеджмент личных финансов

Основной бот — [Lebowski](https://t.me/lebowski_finance_bot).

Бот находится в активной разработке:
- [x] Ручная проверка портфеля акций
- [ ] Автоматическая загрузка акций в портфеле
- [ ] Торговые сигналы в случае резких изменений цены
- [ ] Покупка-продажа активов из интерфейса бота
- [ ] Интеграции с банковскими приложениями для подсчёта общей суммы активов

## Содержимое

1. [Как развернуть local-окружение](#local-setup)
2. [Как вести разработку](#development)
    1. [Как обновить local-окружение](#update-local-env)
    2. [Как закоммитить код](#how-to-commit)
    3. [Как запустить линтеры Python](#run-python-linters)
    4. [Как запустить тесты](#run-tests)


<a name="development"></a>
## Как вести разработку

<a name="update-local-env"></a>
#### Как развернуть local-окружение

Для запуска ПО вам понадобятся консольный Git и Python версий выше 3.10. Инструкции по их установке:

- [Install Git](https://git-scm.com/book/ru/v2/%D0%92%D0%B2%D0%B5%D0%B4%D0%B5%D0%BD%D0%B8%D0%B5-%D0%A3%D1%81%D1%82%D0%B0%D0%BD%D0%BE%D0%B2%D0%BA%D0%B0-Git)
- [Download Python](https://www.python.org/downloads/)

Скачайте репозиторий командой:
```sh
$ git clone https://github.com/devmanorg/finance-bot
$ cd finance-bot
```
Установите менеджер зависимостей [Poetry](https://python-poetry.org/docs/), если ещё не установлен. Cоберите зависимости:
```sh
poetry install
```

Затем, активируйте окружение:
```sh
poetry shell
```


Далее, создайте тестового бота у [@BotFather](https://t.me/BotFather), получите от него токен такого вида:
```sh
9387204215:QELDaGlFj-l9IUfB2rpk-CANFub4B8g3
```

Создайте файл `.env` и положите в него токен:
```sh
TELEGRAM_BOT_TOKEN=9387204215:QELDaGlFj-l9IUfB2rpk-CANFub4B8g3
```

Перейдите в созданного бота и нажмите кнопку `START` внизу, чтобы инициировать диалог.

Запустите бота:
```
python bot.py
```

В консоль ничего не выведется. Напишите боту в Telegram `/start`, он должен вам ответить.

<a name="how-to-commit"></a>
#### Как закоммитить код

В репозитории используются хуки pre-commit, чтобы автоматически запускать линтер и тесты. Перед началом разработки установите [pre-commit package manager](https://pre-commit.com/).

В корне репозитория запустите команду для настройки хуков:

```sh
$ pre-commit install
```

<a name="run-python-linters"></a>
#### Как запустить линтеры Python

#TODO


<a name="run-tests"></a>
#### Как запустить тесты

Для тестирования используется `pytest`, тесты запускаются просто:
```sh
pytest
```
