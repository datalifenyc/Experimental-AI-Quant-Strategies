# Applied SMA Outfit Trading Strategy

This repository provides a complete implementation of the **[SMA Outfit Trading Strategy](https://github.com/raultrades/SMA-outfits)**, including both backtesting and live trading capabilities. The strategy is based on moving average (SMA) crossovers, using specific configurations that institutional traders are believed to use to influence market behavior.

## Features

- **Basic Strategy:** A simple SMA crossover approach (e.g., 10/50/200 SMAs on a 30-minute chart for SPY).
- **Advanced Strategy:** Multi-timeframe confirmation, additional indicators (RSI, Bollinger Bands), and machine learning-based filtering.
- **Backtesting:** Uses Backtrader to simulate strategy performance with historical data.
- **Live Trading:** API integration for Charles Schwab, Robinhood, and TradingView.
- **Risk Management:** Adaptive stop-loss, transaction cost modeling, and filtering to improve trade quality.

## Installation

Clone the repository and install dependencies:

```sh
git clone https://github.com/datalifenyc/Applied-SMA-Outfit-Trading-Strategy.git
cd Applied-SMA-Outfit-Trading-Strategy
pip install -r requirements.txt
```

## Usage

### Backtest the Basic Strategy

```sh
python basic_sma_outfits.py
```

### Backtest the Advanced Strategy

```sh
python advanced_sma_outfits.py
```

### Run Live Trading

Before running live trading, configure `config.py` with your broker API keys.

```sh
python live_trading.py
```

## Configuration

Edit `config.py` to set up API credentials for brokers:

```python
BROKER = "Robinhood"  # Options: "Schwab", "Robinhood", "TradingView"
SCHWAB_CLIENT_ID = "your_client_id"
SCHWAB_SECRET = "your_client_secret"
ROBINHOOD_USERNAME = "your_username"
ROBINHOOD_PASSWORD = "your_password"
TRADINGVIEW_WEBHOOK_URL = "your_webhook_url"
```

## Strategy Details

- **Entry:** Buy when the short SMA crosses above the long SMA while price is above the trend SMA.
- **Exit:** Sell when the short SMA crosses below the long SMA or price falls below the trend SMA.
- **Advanced Strategy Enhancements:**
  - Requires confirmation from daily timeframe trend.
  - Uses RSI to avoid overbought entries.
  - Integrates machine learning filtering (optional).
  - Implements ATR-based trailing stops.

## Broker Integration

- **Charles Schwab:** Uses OAuth2 authentication for API trading.
- **Robinhood:** Uses `robin_stocks` for order execution (unofficial API).
- **TradingView:** Sends webhook alerts for manual confirmation or auto-execution.

## Disclaimer

This code is for educational and research purposes only. Live trading involves risks; use a paper trading account before deploying with real money.

---

### Future Enhancements

- Optimize ML-based filtering with a trained classifier.
- Improve execution speed for high-frequency trading scenarios.
- Add dynamic position sizing based on market conditions.

---

Developed by: OpenAI ChatGPT 4o

For issues, feedback, or contributions, submit a pull request or open an issue in this repo.
