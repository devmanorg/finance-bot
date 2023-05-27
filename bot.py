import datetime
from textwrap import dedent
from typing import cast

from pydantic import BaseSettings
from telegram import Update, Chat
from telegram.ext import Updater, CommandHandler, CallbackContext, JobQueue, Job
from stocks import get_yesterday_trading_prices
from stocks import get_current_trading_prices


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
            context={'chat_id': chat_id},
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

    job = cast(Job, context.job)
    job_context = cast(CallbackContext, job.context)
    job_context = dict(job_context)  # type: ignore
    chat_id = job_context['chat_id']  # type: ignore
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


def yesterday_stocks(update: Update, context: CallbackContext) -> None:
    chat_id = cast(Chat, update.effective_chat).id

    job_title = f'yesterday-stocks#{chat_id}'
    job_queue = cast(JobQueue, context.job_queue)

    job_queue.run_once(
        yesterday_stocks_job,
        0,
        name=job_title,
        context={'chat_id': chat_id},
    )


def main(settings: Settings) -> None:
    updater = Updater(settings.TELEGRAM_BOT_TOKEN)

    dispatcher = updater.dispatcher   # type: ignore
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("current_stocks", current_stocks))
    dispatcher.add_handler(CommandHandler("yesterday_stocks", yesterday_stocks))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main(Settings())
