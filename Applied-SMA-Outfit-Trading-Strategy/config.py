# config.py - Configuration for SMA Outfit Trading Strategy

"""
This configuration file contains settings for selecting brokers and API credentials.

Supported Brokers:
- "Schwab": Uses Charles Schwab API for trade execution (requires OAuth2 authentication).
- "Robinhood": Uses the unofficial Robinhood API via the `robin_stocks` library.
- "TradingView": Sends trading alerts via TradingView webhook integration.

Users should set their preferred broker and corresponding API credentials below.
"""

# Select Broker: Options are "Schwab", "Robinhood", "TradingView"
BROKER = "Robinhood"

# Charles Schwab API Credentials (if using Schwab)
SCHWAB_CLIENT_ID = "your_client_id"  # Replace with your Schwab API client ID
SCHWAB_SECRET = "your_client_secret"  # Replace with your Schwab API client secret

# Robinhood Credentials (if using Robinhood)
ROBINHOOD_USERNAME = "your_username"  # Replace with your Robinhood username
ROBINHOOD_PASSWORD = "your_password"  # Replace with your Robinhood password

# TradingView Webhook URL (if using TradingView)
TRADINGVIEW_WEBHOOK_URL = "your_webhook_url"  # Replace with your TradingView webhook URL
