import backtrader as bt

class SMAOutfitsBasic(bt.Strategy):
    """
    A basic SMA crossover trading strategy with long and short entries.
    
    Strategy:
    - Uses a fast SMA (short-term), slow SMA (medium-term), and trend SMA (long-term).
    - A buy signal is generated when the fast SMA crosses above the slow SMA while price is above the trend SMA.
    - A short signal is generated when the fast SMA crosses below the slow SMA while price is below the trend SMA.
    - Exit positions when the opposite signal is generated or price violates the trend SMA.
    """
    
    params = dict(fast=10, slow=50, trend=200)
    
    def __init__(self):
        """Initialize moving averages and crossover indicators."""
        self.sma_fast = bt.indicators.SMA(self.data0.close, period=self.p.fast)
        self.sma_slow = bt.indicators.SMA(self.data0.close, period=self.p.slow)
        self.sma_trend = bt.indicators.SMA(self.data0.close, period=self.p.trend)
        self.crossup = bt.indicators.CrossOver(self.sma_fast, self.sma_slow)
    
    def next(self):
        """Define strategy logic executed on each new bar."""
        if not self.position:
            if self.crossup > 0 and self.data0.close[0] > self.sma_trend[0]:
                self.buy()
            elif self.crossup < 0 and self.data0.close[0] < self.sma_trend[0]:
                self.sell()
        else:
            if (self.crossup < 0 and self.position.size > 0) or self.data0.close[0] < self.sma_trend[0]:
                self.close()
            elif (self.crossup > 0 and self.position.size < 0) or self.data0.close[0] > self.sma_trend[0]:
                self.close()

if __name__ == '__main__':
    import datetime
    cerebro = bt.Cerebro()
    data = bt.feeds.YahooFinanceData(
        dataname="SPY", timeframe=bt.TimeFrame.Minutes, compression=30,
        fromdate=datetime.datetime(2020, 1, 1), todate=datetime.datetime(2021, 1, 1))
    
    cerebro.adddata(data)
    cerebro.addstrategy(SMAOutfitsBasic)
    cerebro.broker.setcash(100000.0)
    cerebro.broker.setcommission(commission=0.001)
    cerebro.run()
    print(f"Final Portfolio Value: ${cerebro.broker.getvalue():.2f}")
