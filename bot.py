import datetime
from textwrap import dedent
from typing import cast

import click
from pydantic import BaseSettings
from telegram import Update, Chat
from telegram.ext import Updater, CommandHandler, CallbackContext, JobQueue
from stocks import get_yesterday_trading_prices
from stocks import get_current_trading_prices
from watchfiles import run_process


class Settings(BaseSettings):
    TELEGRAM_BOT_TOKEN: str

    class Config:
        env_file = '.env'
        case_sensitive = True
        env_nested_delimiter = '__'


PORTFOLIO = {
    'MSFT': 20,
    'AMZN': 15,
    'GOOGL': 10,
    'TSLA': 100,
}


def start(update: Update, context: CallbackContext) -> None:
    chat_id = cast(Chat, update.effective_chat).id
    update.message.reply_text('Привет! Я твой биржевой помощник!')

    # This needed to exclude the situation when
    # user presses /start multiple times and gets multiple jobs
    job_title = f'yesterday-stocks#{chat_id}'
    job_queue = cast(JobQueue, context.job_queue)
    if job_title not in {job.name for job in job_queue.jobs()}:
        job_queue.run_daily(
            yesterday_stocks_job,
            time=datetime.time(hour=7),
            name=job_title,
            context={'chat_id': chat_id}
        )


def format_ticker_stats(ticker: str, amount: int, open_price: float, close_price: float) -> str:
    diff = close_price - open_price
    revenue = diff * amount

    if revenue < 0:
        result = 'потеряли'
    else:
        result = 'заработали'

    return dedent(f'''
        {ticker} ({amount})
        открылись по {open_price:,.1f}$
        закрылись по {close_price:,.1f}$
        выручка с акции: {diff:,.1f}$
        учитывая количество, {result} {revenue:,.1f}$
    ''')


def current_stocks(update: Update, context: CallbackContext) -> None:
    msg = 'Ваши фин. показатели на текущий момент:\n\n'

    day_revenue = 0.0

    for ticker, amount in PORTFOLIO.items():
        open_price, close_price = get_current_trading_prices(ticker)
        diff = close_price - open_price
        revenue = diff * amount
        day_revenue += revenue
        msg += format_ticker_stats(ticker, amount, open_price, close_price)
    msg += dedent(f'''
        Итоговая разница за день: {day_revenue:,.1f}$
    ''')
    update.message.reply_text(msg)


def yesterday_stocks_job(context: CallbackContext) -> None:
    msg = 'Ваши фин. показатели по итогу прошлого дня:\n\n'

    chat_id = context.job.context['chat_id']
    day_revenue = 0.0

    for ticker, amount in PORTFOLIO.items():
        open_price, close_price = get_yesterday_trading_prices(ticker)
        diff = close_price - open_price
        revenue = diff * amount
        day_revenue += revenue
        msg += format_ticker_stats(ticker, amount, open_price, close_price)
    msg += dedent(f'''
        Итоговая разница за день: {day_revenue:,.1f}$
    ''')
    context.bot.send_message(chat_id=chat_id, text=msg)


def run_bot() -> None:
    settings = Settings()
    updater = Updater(settings.TELEGRAM_BOT_TOKEN)

    dispatcher = updater.dispatcher   # type: ignore
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("current_stocks", current_stocks))

    updater.start_polling()
    updater.idle()


@click.command()
@click.option('--autoreload', default=False, is_flag=True)
def main(autoreload: bool) -> None:
    if autoreload:
        print('Autoreload is enabled.')
        run_process('.', target=run_bot)
    else:
        run_bot()


if __name__ == '__main__':
    main()
