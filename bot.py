import datetime
from textwrap import dedent

from telegram.ext import Updater, CommandHandler, Update, CallbackContext
from environs import Env

from stocks import get_yesterday_trading_prices
from stocks import get_current_trading_prices


env = Env()
env.read_env()

portfolio = {
    'MSFT': 20,
    'AMZN': 15,
    'GOOGL': 10,
    'TSLA': 100,
}


def start(update: Update, context: CallbackContext) -> None:
    chat_id = update.effective_chat.id
    update.message.reply_text('Привет! Я твой биржевой помощник!')

    # This needed to exclude the situation when
    # user presses /start multiple times and gets multiple jobs
    job_title = f'yesterday-stocks#{chat_id}'
    if job_title in [job.name for job in job_queue.jobs()]:
        return
    job_queue.run_daily(
        yesterday_stocks_job,
        time=datetime.time(hour=7),
        name=job_title,
    )


def format_ticker_stats(ticker: str, amount: int, open_price: float, close_price: float) -> str:
    diff = close_price - open_price
    revenue = diff * amount

    if revenue > 0:
        result = 'заработали'
    else:
        result = 'потеряли'

    return dedent(f'''
        {ticker} ({amount})
        открылись по {open_price:,.1f}$
        закрылись по {close_price:,.1f}$
        выручка с акции: {diff:,.1f}$
        учитывая количество, {result} {revenue:,.1f}$
    ''')


def current_stocks(update: Update, context: CallbackContext) -> None:
    msg = 'Ваши фин. показатели на текущий момент:\n\n'

    day_revenue = 0

    for ticker, amount in portfolio.items():
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

    day_revenue = 0

    for ticker, amount in portfolio.items():
        open_price, close_price = get_yesterday_trading_prices(ticker)
        diff = close_price - open_price
        revenue = diff * amount
        day_revenue += revenue
        msg += format_ticker_stats(ticker, amount, open_price, close_price)
    msg += dedent(f'''
        Итоговая разница за день: {day_revenue:,.1f}$
    ''')
    context.bot.message.reply_text(msg)


if __name__ == '__main__':
    token = env('TELEGRAM_BOT_TOKEN')
    updater = Updater(token)
    dispatcher = updater.dispatcher
    job_queue = updater.job_queue

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("current_stocks", current_stocks))

    updater.start_polling()
    updater.idle()
