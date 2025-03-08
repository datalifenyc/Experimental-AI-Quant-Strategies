import backtrader as bt
import pickle  # For optional ML-based filtering

class SMAOutfitsAdvanced(bt.Strategy):
    """
    An advanced SMA crossover trading strategy incorporating:
    
    - Multi-timeframe analysis (30-minute and daily data)
    - Additional technical indicators (RSI, ATR for stop-loss placement)
    - Machine learning filtering (optional) to enhance signal quality
    - Dynamic trailing stop-loss using ATR to lock in profits
    - Short-selling capabilities based on SMA trends
    
    Strategy Logic:
    - A buy signal is generated when the fast SMA crosses above the slow SMA, price is above the daily trend SMA, and RSI is below 70.
    - A short signal is generated when the fast SMA crosses below the slow SMA, price is below the daily trend SMA, and RSI is above 30.
    - Exit conditions based on trend reversals and ATR-based trailing stops.
    """
    
    params = dict(fast=10, slow=50, trend=200, rsi_period=14, atr_period=14)
    
    def __init__(self):
        """Initialize moving averages, indicators, and machine learning model (if available)."""
        self.sma_fast = bt.indicators.SMA(self.data0.close, period=self.p.fast)
        self.sma_slow = bt.indicators.SMA(self.data0.close, period=self.p.slow)
        self.sma_trend = bt.indicators.SMA(self.data1.close, period=self.p.trend)  # Daily trend filter
        self.rsi = bt.indicators.RSI(self.data0.close, period=self.p.rsi_period)
        self.atr = bt.indicators.ATR(self.data0, period=self.p.atr_period)
        
        self.crossup = bt.indicators.CrossOver(self.sma_fast, self.sma_slow)
        
        try:
            self.ml_model = pickle.load(open('sma_outfits_model.pkl', 'rb'))
        except Exception:
            self.ml_model = None
    
    def next(self):
        """Define strategy logic executed on each new bar."""
        if self.order:
            return  # Avoid multiple open orders
        
        crossover_up = self.crossup > 0
        crossover_down = self.crossup < 0
        
        if not self.position:
            if crossover_up and self.data0.close[0] > self.sma_trend[0] and self.rsi[0] < 70:
                signal_quality = True
                if self.ml_model:
                    features = [(self.data0.close[0] / self.data0.close[-1]) - 1.0, self.rsi[0], (self.sma_fast[0]/self.sma_slow[0])]
                    pred = self.ml_model.predict([features])
                    signal_quality = bool(pred[0])
                if signal_quality:
                    self.order = self.buy()
                    stop_price = self.data0.close[0] - 2 * self.atr[0]
                    self.stop_order = self.sell(exectype=bt.Order.Stop, price=stop_price)
            elif crossover_down and self.data0.close[0] < self.sma_trend[0] and self.rsi[0] > 30:
                self.order = self.sell()
                stop_price = self.data0.close[0] + 2 * self.atr[0]
                self.stop_order = self.buy(exectype=bt.Order.Stop, price=stop_price)
        else:
            if crossover_down and self.position.size > 0 or self.rsi[0] > 80:
                self.close()
                if self.stop_order:
                    self.broker.cancel(self.stop_order)
            elif crossover_up and self.position.size < 0 or self.rsi[0] < 20:
                self.close()
                if self.stop_order:
                    self.broker.cancel(self.stop_order)
            else:
                if self.stop_order:
                    current_stop = self.stop_order.created.price
                    new_stop = self.data0.close[0] - 2 * self.atr[0] if self.position.size > 0 else self.data0.close[0] + 2 * self.atr[0]
                    if (self.position.size > 0 and new_stop > current_stop) or (self.position.size < 0 and new_stop < current_stop):
                        self.broker.cancel(self.stop_order)
                        self.stop_order = self.sell(exectype=bt.Order.Stop, price=new_stop) if self.position.size > 0 else self.buy(exectype=bt.Order.Stop, price=new_stop)

if __name__ == '__main__':
    import datetime
    cerebro = bt.Cerebro()
    
    data30 = bt.feeds.YahooFinanceData(dataname="SPY", timeframe=bt.TimeFrame.Minutes, compression=30,
                                       fromdate=datetime.datetime(2020,1,1), todate=datetime.datetime(2021,1,1))
    data1d = bt.feeds.YahooFinanceData(dataname="SPY", timeframe=bt.TimeFrame.Days,
                                       fromdate=datetime.datetime(2019,1,1), todate=datetime.datetime(2021,1,1))
    
    cerebro.adddata(data30)  # 30-min data
    cerebro.adddata(data1d)  # Daily data
    
    cerebro.addstrategy(SMAOutfitsAdvanced)
    cerebro.broker.setcash(100000)
    cerebro.broker.setcommission(commission=0.001)
    cerebro.run()
    print(f"Final Portfolio Value: ${cerebro.broker.getvalue():.2f}")
