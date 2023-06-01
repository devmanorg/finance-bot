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
3. [Как развернуть в production-режиме](#production)


<a name="development"></a>
## Как вести разработку

<a name="update-local-env"></a>
#### Как развернуть local-окружение

Для запуска ПО вам понадобятся консольный Git и Python версий 3.10 или выше. Инструкции по их установке:

- [Install Git](https://git-scm.com/book/ru/v2/%D0%92%D0%B2%D0%B5%D0%B4%D0%B5%D0%BD%D0%B8%D0%B5-%D0%A3%D1%81%D1%82%D0%B0%D0%BD%D0%BE%D0%B2%D0%BA%D0%B0-Git)
- [Download Python](https://www.python.org/downloads/)

Скачайте репозиторий командой:

```sh
$ git clone https://github.com/devmanorg/finance-bot
$ cd finance-bot
```

Установите менеджер зависимостей [Poetry](https://python-poetry.org/docs/), если ещё не установлен. Cоберите зависимости:

```sh
$ poetry install
```

Затем, активируйте окружение:

```sh
$ poetry shell
```

Далее, создайте тестового бота у [@BotFather](https://t.me/BotFather), получите от него токен такого вида:

```text
9387204215:QELDaGlFj-l9IUfB2rpk-CANFub4B8g3
```

Создайте файл `.env` и положите в него токен:

```env
TELEGRAM_BOT_TOKEN=9387204215:QELDaGlFj-l9IUfB2rpk-CANFub4B8g3
```

Запустите бота:

```sh
$ python bot.py --autoreload
```

Зайдите в чат к ранее созданному боту и отправьте ему команду `/start`, он должен вам ответить.

<a name="how-to-commit"></a>
#### Как закоммитить код

В репозитории используются хуки pre-commit, чтобы автоматически запускать линтер и тесты. Перед началом разработки установите [pre-commit package manager](https://pre-commit.com/).

В корне репозитория запустите команду для настройки хуков:

```sh
$ pre-commit install
```

Чтобы хуки сработали, работайте из виртуального окружения:
```sh
poetry shell
```


<a name="run-python-linters"></a>
#### Как запустить линтеры Python

Активируйте окружение:
```sh
poetry shell
```

Для тестирования используется `mypy`, линтер запускается такой командой::
```sh
mypy .
```

Если вы хотите проверить один конкретный файл, передайте аргументом название файла, пример:
```sh
pytest bot.py
```


<a name="run-tests"></a>
#### Как запустить тесты

Активируйте окружение:
```sh
poetry shell
```

Для тестирования используется `pytest`, тесты запускаются просто:

```sh
$ pytest
```

Если вы хотите запустить один конкретный тест, передайте аргументом "{название_файла}::{название_функции}", пример:

```sh
$ pytest test_sample.py::test_yesterday_trading_prices
```

<a name="production"></a>
#### Как развернуть в production-режиме


Для запуска ПО вам понадобятся консольный Git и Python версий 3.10 или выше. Инструкции по их установке:

- [Install Git](https://git-scm.com/book/ru/v2/%D0%92%D0%B2%D0%B5%D0%B4%D0%B5%D0%BD%D0%B8%D0%B5-%D0%A3%D1%81%D1%82%D0%B0%D0%BD%D0%BE%D0%B2%D0%BA%D0%B0-Git)
- [Download Python](https://www.python.org/downloads/)

Скачайте репозиторий командой:

```sh
$ git clone https://github.com/devmanorg/finance-bot
$ cd finance-bot
```

Установите менеджер зависимостей [Poetry](https://python-poetry.org/docs/), если ещё не установлен. Cоберите зависимости:

```sh
$ poetry install
```

Затем, активируйте окружение:

```sh
$ poetry shell
```

Создайте файл `.env` и положите в него токен (укажите настоящий, текущий для примера):

```env
TELEGRAM_BOT_TOKEN=9387204215:QELDaGlFj-l9IUfB2rpk-CANFub4B8g3
```

Запустите бота 

```sh
#TODO: systemd
```

Зайдите в чат к ранее созданному боту и отправьте ему команду `/start`, он должен вам ответить.

Проверьте, что запустился `job_queue` командой `/yesterday_stocks`. Он должен прислать сообщение с информацией по акциям.
