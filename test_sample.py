import pytest
import pandas
import json

from stocks import get_yesterday_trading_prices
from stocks import get_current_trading_prices


@pytest.fixture
def abc_1mo_dataframe() -> pandas.DataFrame:
    with open('fixtures/abc_1mo.json') as file:
        abc_1mo = json.load(file)
    return pandas.DataFrame(abc_1mo)


@pytest.fixture
def abc_1d_dataframe() -> pandas.DataFrame:
    with open('fixtures/abc_1d.json') as file:
        abc_1d = json.load(file)
    return pandas.DataFrame(abc_1d)


def test_yesterday_trading_prices(mocker, abc_1mo_dataframe: pandas.DataFrame) -> None:
    mocker.patch("yfinance.Ticker.history", return_value=abc_1mo_dataframe)
    assert get_yesterday_trading_prices('ABC') == (171.5099945068, 171.0599975586)


def test_current_trading_prices(mocker, abc_1d_dataframe: pandas.DataFrame) -> None:
    mocker.patch("yfinance.Ticker.history", return_value=abc_1d_dataframe)
    assert get_current_trading_prices('ABC') == (170.0700073242, 169.8350067139)
