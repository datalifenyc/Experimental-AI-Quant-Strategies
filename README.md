# Experimental AI Quant Strategies

Welcome to the **Experimental AI Quant Strategies** repository. This project serves as a collection of algorithmic trading strategies powered by AI, quantitative models, and technical analysis. Our goal is to explore, test, and refine cutting-edge trading strategies that can be used for backtesting, research, and live trading execution.

## 📂 Strategy Collection

This repository houses various trading strategies, each contained in its respective subdirectory. Every strategy includes:

- A README explaining its methodology.
- Python scripts for backtesting and live trading.
- Configuration files for broker integration.

### Example Strategy: **Applied SMA Outfit Trading Strategy**

The **Applied SMA Outfit Trading Strategy** is a technical analysis-based strategy that leverages **moving average crossovers** to generate trading signals. It includes:

- **Basic SMA Strategy** (10/50/200 crossovers on a 30-minute chart)
- **Advanced SMA Strategy** (multi-timeframe analysis, RSI filtering, ATR-based stop-loss, and machine learning enhancements)
- **Live Trading Integration** with brokers such as Schwab, Robinhood, and TradingView

📂 **Folder Structure:**

```text
Experimental-AI-Quant-Strategies/
│
├── Applied-SMA-Outfit-Trading-Strategy/
│   ├── README.md  # Documentation for this specific strategy
│   ├── basic_sma_outfits.py  # Basic SMA crossover strategy
│   ├── advanced_sma_outfits.py  # Advanced version with 
│   ├── live_trading.py  # Live trading script with broker API 
│   ├── test_sma_outfits.py # Test script for strategy
│   ├── config.py  # API keys & settings
│   ├── requirements.txt  # Dependencies
│
├── Other-Strategies/ (Coming Soon)
│   ├── AI-Trend-Following/
│   ├── Reinforcement-Learning-Trading/
│   ├── High-Frequency-Mean-Reversion/
│
└── README.md  # Parent repository overview
```

## 🚀 Future Strategies

This repository will continue to grow with more AI-powered trading models, such as:

- **AI-Powered Trend Following**: Using machine learning to identify market regimes.
- **Reinforcement Learning for Trading**: Agents that learn optimal trading actions over time.
- **High-Frequency Mean Reversion**: Exploiting short-term price inefficiencies.

## 🔧 Setup & Installation

Clone this repository and navigate to any strategy folder to get started:

```sh
git clone https://github.com/YOUR_USERNAME/Experimental-AI-Quant-Strategies.git
cd Experimental-AI-Quant-Strategies/Applied-SMA-Outfit-Trading-Strategy
pip install -r requirements.txt
```

## 📊 Contributing & Research

We welcome contributions from traders, quants, and developers who are interested in refining quantitative strategies. If you have a new strategy, submit a pull request or open an issue to discuss your ideas.

This repository is for **educational and research purposes only**. Algorithmic trading carries financial risk, and past performance does not guarantee future results. Please use caution when deploying strategies in live trading.

---

🔍 **Stay tuned for new strategies!**
