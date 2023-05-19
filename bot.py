from textwrap import dedent

import yfinance
from telegram.ext import Updater, CommandHandler
from environs import Env

env = Env()
env.read_env()

portfolio = {
    'MSFT': 20,
    'AMZN': 15,
    'GOOGL': 10,
    'TSLA': 100,
}


def start(update, context):
    update.message.reply_text('Привет! Я твой биржевой помощник!')


def yesterday_stocks(update, context):
    msg = f'Ваши фин. показатели по итогу прошлого дня:\n\n'

    day_revenue = 0

    for ticker, amount in portfolio.items():
        yahoo_ticker_handler = yfinance.Ticker(ticker)
        history = yahoo_ticker_handler.history(period="1mo")
        stock_open = float(history['Open'][-2])
        stock_close = float(history['Close'][-2])
        diff = stock_close - stock_open
        
        revenue = diff * amount

        day_revenue += revenue

        if revenue > 0:
            result = 'заработали'
        else:
            result = 'потеряли'

        msg += dedent(f'''
            {ticker} ({amount})
            открылись по {stock_open:,.1f}$
            закрылись по {stock_close:,.1f}$
            выручка с акции сегодня: {diff:,.1f}$
            учитывая количество, {result} {revenue:,.1f}$
        ''')
    msg += dedent(f'''
        Итоговая разница за день: {day_revenue:,.1f}$
    ''')
    update.message.reply_text(msg)


if __name__ == '__main__':
    token = env('TELEGRAM_BOT_TOKEN')
    updater = Updater(token)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("yesterday_stocks", yesterday_stocks))

    updater.start_polling()
    updater.idle()
