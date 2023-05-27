import yfinance


def get_yesterday_trading_prices(ticker: str) -> tuple[float, float]: 
    yahoo_ticker_handler = yfinance.Ticker(ticker)
    history = yahoo_ticker_handler.history(period="1mo")
    open_price = float(history['Open'][-2])
    close_price = float(history['Close'][-2])
    return open_price, close_price


def get_current_trading_prices(ticker: str) -> tuple[float, float]:
    yahoo_ticker_handler = yfinance.Ticker(ticker)
    history = yahoo_ticker_handler.history(period="1d")
    open_price = float(history['Open'][-1])
    close_price = float(history['Close'][-1])
    return open_price, close_price
