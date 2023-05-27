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
    2. [Как запустить линтеры Python](#run-python-linters)
    3. [Как установить npm-пакет](#add-npm-package)
    4. [Как установить python-пакет](#add-python-package)
    5. [Как перезалить тестовые данные](#recreate-db)
    6. [Как запустить тесты](#run-tests)
    7. [Как сдампить тестовую БД](#create-db-backup)
3. [Sandbox server](#sandbox)
4. [Рекомендации](#recommendations)
5. [Соглашения по Client-Side](#client-side-guidelines)
6. [More docs](#extra-docs)

<a name="local-setup"></a>
## Как развернуть local-окружение

Для запуска ПО вам понадобятся консольный Git и Python версий выше 3.7. Инструкции по их установке:

- [Install Git](https://git-scm.com/book/ru/v2/%D0%92%D0%B2%D0%B5%D0%B4%D0%B5%D0%BD%D0%B8%D0%B5-%D0%A3%D1%81%D1%82%D0%B0%D0%BD%D0%BE%D0%B2%D0%BA%D0%B0-Git)
- [Download Python](https://www.python.org/downloads/)

Скачайте репозиторий командой:
```sh
$ git clone https://github.com/devmanorg/finance-bot
$ cd finance-bot
```

В репозитории используются хуки pre-commit, чтобы автоматически запускать линтер и тесты. Перед началом разработки установите [pre-commit package manager](https://pre-commit.com/).

В корне репозитория запустите команду для настройки хуков:

```sh
$ pre-commit install
```
