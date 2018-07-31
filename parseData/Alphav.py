# call financial data
import pandas as pd
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
import time
from datetime import datetime
from dateutil.relativedelta import relativedelta
import matplotlib.pyplot as plt

# used for printing out pandas dataframes
from pprint import pprint

class Alphav(object):
    def __init__(self, ticker, years):
        self.ticker = ticker
        self.years = years

    def daily_data(self):
        ts = TimeSeries(key = "Q63YHW130JGQ7JPT", output_format = "pandas", indexing_type = "date")
        data, meta_data = ts.get_daily_adjusted(symbol = self.ticker, outputsize = "full")
        start = (datetime.strptime(data.index.values[-1], "%Y-%m-%d") - relativedelta(years=self.years)).strftime("%Y-%m-%d")

        target = data.loc[start:data.index.values[-1], ["5. adjusted close", "2. high", "3. low", "6. volume"]]
        target.columns = ["adj_close", "high", "low", "volume"]
        return(target)

    def indics(self, output):
        ti = TechIndicators(key = "Q63YHW130JGQ7JPT", output_format = "pandas", indexing_type = "date")
        getindic = getattr(self, output, lambda: "Invalid indicator.")

        return getindic(ti)

    def bbands(self, ti):
        data, meta_data = ti.get_bbands(symbol = self.ticker)
        parse = getattr(self, "process", lambda: "An error occurred.")
        return parse(data)

    def ema(self, ti):
        data, meta_data = ti.get_ema(symbol=self.ticker)
        parse = getattr(self, "process", lambda: "An error occurred.")
        return parse(data)

    def stoch(self, ti):
        data, meta_data = ti.get_stoch(symbol=self.ticker)
        parse = getattr(self, "process", lambda: "An error occurred.")
        return parse(data)

    def rsi(self, ti):
        data, meta_data = ti.get_rsi(symbol=self.ticker, time_period = 14)
        parse = getattr(self, "process", lambda: "An error occurred.")
        return parse(data)

    def chaikin(self, ti):
        data, meta_data = ti.get_ad(symbol = self.ticker)
        parse = getattr(self, "process", lambda: "An error occurred.")
        return parse(data)

    def obv(self, ti):
        data, meta_data = ti.get_obv(symbol=self.ticker)
        parse = getattr(self, "process", lambda: "An error occurred.")
        return parse(data)

    def aroon(self, ti):
        data, meta_data = ti.get_aroon(symbol = self.ticker, time_period = 14)
        parse = getattr(self, "process", lambda: "An error occurred.")
        return parse(data)

    def process(self, data):
        start = (datetime.strptime(data.index.values[-1], "%Y-%m-%d %H:%M:%S") - relativedelta(years=self.years)).strftime("%Y-%m-%d")
        target = data.loc[start:data.index.values[-1]]
        return(target)

    def assemble(self):
        indics = ["bbands", "ema", "stoch", "rsi", "chaikin", "obv", "aroon"]
        prices = self.daily_data()
        master = prices.reset_index(drop = True)
        print("Successfully parsed stock data.")

        for i in range(0,len(indics)):
            if (i == 3):
                print("Waiting for 60 seconds")
                time.sleep(60)
            master = pd.concat([master, self.indics(indics[i]).reset_index(drop = True)], axis = 1, sort = False)
            print("Successfully parsed %s."%(indics[i]))

        master.set_index(prices.index.values, inplace = True)
        master.plot()
        plt.title("Stock Prices and Indicators for %s"%(self.ticker))
        plt.show()
        return master
