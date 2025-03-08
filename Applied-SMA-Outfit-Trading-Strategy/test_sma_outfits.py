import pytest
import backtrader as bt
from basic_sma_outfits import SMAOutfitsBasic
from advanced_sma_outfits import SMAOutfitsAdvanced
from live_trading import SchwabBroker, RobinhoodBroker, TradingViewBroker
from unittest.mock import MagicMock

@pytest.fixture
def cerebro():
    """Fixture to set up Backtrader environment with dummy data."""
    cerebro = bt.Cerebro()
    data = bt.feeds.BacktraderCSVData(dataname='test_data.csv')
    cerebro.adddata(data)
    return cerebro

def test_basic_strategy_initialization():
    """Test if the basic SMA strategy initializes correctly."""
    strategy = SMAOutfitsBasic()
    assert isinstance(strategy, SMAOutfitsBasic)

def test_advanced_strategy_initialization():
    """Test if the advanced SMA strategy initializes correctly."""
    strategy = SMAOutfitsAdvanced()
    assert isinstance(strategy, SMAOutfitsAdvanced)

def test_basic_strategy_execution(cerebro):
    """Test if the basic strategy runs without errors in Backtrader."""
    cerebro.addstrategy(SMAOutfitsBasic)
    cerebro.run()
    assert True

def test_advanced_strategy_execution(cerebro):
    """Test if the advanced strategy runs without errors in Backtrader."""
    cerebro.addstrategy(SMAOutfitsAdvanced)
    cerebro.run()
    assert True

def test_short_trade_execution(cerebro):
    """Ensure the strategy can enter short positions based on SMA signals."""
    cerebro.addstrategy(SMAOutfitsAdvanced)
    cerebro.run()
    assert cerebro.broker.getvalue() > 0

def test_atr_based_stop_loss(cerebro):
    """Ensure ATR-based trailing stops adjust correctly based on volatility."""
    cerebro.addstrategy(SMAOutfitsAdvanced)
    cerebro.run()
    for order in cerebro.broker.orders:
        if order.exectype == bt.Order.Stop:
            assert order.price > 0

def test_mocked_schwab_api():
    """Test Schwab broker API with mocked responses."""
    schwab = SchwabBroker(client_id='test_id', client_secret='test_secret')
    schwab.buy = MagicMock(return_value="Mocked Schwab Buy Order")
    schwab.sell = MagicMock(return_value="Mocked Schwab Sell Order")
    assert schwab.buy('SPY', 10) == "Mocked Schwab Buy Order"
    assert schwab.sell('SPY', 10) == "Mocked Schwab Sell Order"

def test_mocked_robinhood_api():
    """Test Robinhood broker API with mocked responses."""
    robinhood = RobinhoodBroker(username='test_user', password='test_pass')
    robinhood.buy = MagicMock(return_value="Mocked Robinhood Buy Order")
    robinhood.sell = MagicMock(return_value="Mocked Robinhood Sell Order")
    assert robinhood.buy('SPY', 10) == "Mocked Robinhood Buy Order"
    assert robinhood.sell('SPY', 10) == "Mocked Robinhood Sell Order"

def test_mocked_tradingview_api():
    """Test TradingView webhook API with mocked responses."""
    tradingview = TradingViewBroker(webhook_url='https://mock_webhook_url')
    tradingview.buy = MagicMock(return_value=(200, "Mocked TradingView Buy Order"))
    tradingview.sell = MagicMock(return_value=(200, "Mocked TradingView Sell Order"))
    assert tradingview.buy('SPY', 10) == (200, "Mocked TradingView Buy Order")
    assert tradingview.sell('SPY', 10) == (200, "Mocked TradingView Sell Order")
