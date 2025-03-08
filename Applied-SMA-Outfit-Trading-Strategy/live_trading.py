import requests
import yfinance as yf
import time
from config import BROKER, SCHWAB_CLIENT_ID, SCHWAB_SECRET, ROBINHOOD_USERNAME, ROBINHOOD_PASSWORD, TRADINGVIEW_WEBHOOK_URL

class BrokerBase:
    """
    Base class for broker integration.
    Each broker subclass must implement buy() and sell() methods.
    """
    def buy(self, symbol, quantity):
        raise NotImplementedError
    
    def sell(self, symbol, quantity):
        raise NotImplementedError

class SchwabBroker(BrokerBase):
    """
    Integration with Charles Schwab API.
    Placeholder for OAuth2 authentication and order execution.
    """
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.token = None  # OAuth2 authentication required
    
    def buy(self, symbol, quantity):
        print(f"Placing BUY order on Schwab for {quantity} shares of {symbol}")
        return "Order placed"
    
    def sell(self, symbol, quantity):
        print(f"Placing SELL order on Schwab for {quantity} shares of {symbol}")
        return "Order placed"

class RobinhoodBroker(BrokerBase):
    """
    Integration with Robinhood API.
    Uses the robin_stocks library for authentication and order execution.
    """
    def __init__(self, username, password):
        import robin_stocks as r
        self.r = r
        self.r.login(username, password)
    
    def buy(self, symbol, quantity):
        return self.r.orders.order_buy_market(symbol, quantity)
    
    def sell(self, symbol, quantity):
        return self.r.orders.order_sell_market(symbol, quantity)

class TradingViewBroker(BrokerBase):
    """
    Integration with TradingView webhook alerts.
    Sends buy and sell signals to TradingView for execution.
    """
    def __init__(self, webhook_url):
        self.webhook_url = webhook_url
    
    def buy(self, symbol, quantity):
        resp = requests.post(self.webhook_url, json={"symbol": symbol, "action": "BUY", "quantity": quantity})
        return resp.status_code, resp.text
    
    def sell(self, symbol, quantity):
        resp = requests.post(self.webhook_url, json={"symbol": symbol, "action": "SELL", "quantity": quantity})
        return resp.status_code, resp.text

# Initialize broker based on config
if BROKER == "Schwab":
    broker = SchwabBroker(SCHWAB_CLIENT_ID, SCHWAB_SECRET)
elif BROKER == "Robinhood":
    broker = RobinhoodBroker(ROBINHOOD_USERNAME, ROBINHOOD_PASSWORD)
elif BROKER == "TradingView":
    broker = TradingViewBroker(TRADINGVIEW_WEBHOOK_URL)
else:
    raise ValueError("Invalid broker specified in config.py")

# Live trading loop configuration
symbol = "SPY"
quantity = 10
in_position = False
prev_fast, prev_slow = None, None
closes = []

while True:
    """
    Fetches latest market data and checks for SMA crossover signals.
    Executes buy/sell trades accordingly.
    """
    data = yf.download(tickers=symbol, period="1d", interval="30m")
    last_bar = data.iloc[-1]
    close_price = last_bar['Close']
    closes.append(close_price)
    
    if len(closes) < 200:
        time.sleep(1800)
        continue
    
    fast_sma = sum(closes[-10:]) / 10
    slow_sma = sum(closes[-50:]) / 50
    trend_sma = sum(closes[-200:]) / 200
    
    if prev_fast is not None and prev_slow is not None:
        crossover_up = (fast_sma > slow_sma) and (prev_fast <= prev_slow)
        crossover_down = (fast_sma < slow_sma) and (prev_fast >= prev_slow)
    else:
        crossover_up, crossover_down = False, False
    
    if not in_position and crossover_up and close_price > trend_sma:
        resp = broker.buy(symbol, quantity)
        print(f"Buy order sent: {resp}")
        in_position = True
    elif in_position and (crossover_down or close_price < trend_sma):
        resp = broker.sell(symbol, quantity)
        print(f"Sell order sent: {resp}")
        in_position = False
    
    prev_fast, prev_slow = fast_sma, slow_sma
    time.sleep(1800)
