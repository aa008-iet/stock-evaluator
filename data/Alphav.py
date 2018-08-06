# libraries - statistical tools and datetime helpers
import pandas as pd
import time as t
from datetime import datetime, time
from dateutil.relativedelta import relativedelta
import matplotlib.pyplot as plt
# libraries - call financial data using Alpha Vantage API
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators


# Alphav returns a ticker's historical data and technical indicators over a requested number of years
class Alphav(object):
    # constructor for the class; uses the desired ticker and number of years of data as parameters
    def __init__(self, ticker, years):
        self.ticker = ticker
        self.years = years

    # checks if the stock exchange is open on 'date'
    def is_business_day(self, date):
        return bool(len(pd.bdate_range(date, date)))

    # returns a pandas.DataFrame of the selected ticker's historical data
    def daily_data(self):
        # API call is below
        ts = TimeSeries(key="Q63YHW130JGQ7JPT", output_format="pandas", indexing_type="date")
        data, meta_data = ts.get_daily_adjusted(symbol=self.ticker, outputsize="full")

        # start date is defined by the number of years specified from the constructor
        # for example 10 years would make the start date in 2008 if the most recent date was in 2018
        start = (datetime.strptime(data.index.values[-1], "%Y-%m-%d") - relativedelta(years=self.years)).strftime(
            "%Y-%m-%d")

        # selects and returns adjusted close prices, daily highs and lows, and volume of trades
        target = data.loc[start:data.index.values[-1], ["5. adjusted close", "2. high", "3. low", "6. volume"]]
        target.columns = ["adj_close", "high", "low", "volume"]
        return target

    # general function used to find technical indicators
    def indics(self, output):
        # API call below
        ti = TechIndicators(key="Q63YHW130JGQ7JPT", output_format="pandas", indexing_type="date")
        # calls a function depending on the requested indicator
        # if the 'output' parameters is 'bbands,' then the function 'bbands' is called
        get = getattr(self, output, lambda: "Invalid indicator.")

        return get(ti)

    '''
    Below are helper functions called in the function 'indics.' Each one returns one or multiple columns
    of financial data in the form of a pandas data frame.
    The call `parse(data)` refers to the function 'process' which is found below all the helpers.
    Refer to https://www.investopedia.com/ for reference.
    '''

    # helper function for 'indics' to find Bollinger Bands®
    def bbands(self, ti):
        data, meta_data = ti.get_bbands(symbol=self.ticker)
        parse = getattr(self, "process", lambda: "An error occurred.")
        return parse(data)

    # helper function for 'indics' to find the exponential moving average of share prices
    def ema(self, ti):
        data, meta_data = ti.get_ema(symbol=self.ticker)
        parse = getattr(self, "process", lambda: "An error occurred.")
        return parse(data)

    # helper function for 'indics' to find the stochastic oscillator
    def stoch(self, ti):
        data, meta_data = ti.get_stoch(symbol=self.ticker)
        parse = getattr(self, "process", lambda: "An error occurred.")
        return parse(data)

    # helper function for 'indics' to find the relative strength index
    def rsi(self, ti):
        data, meta_data = ti.get_rsi(symbol=self.ticker, time_period=14)
        parse = getattr(self, "process", lambda: "An error occurred.")
        return parse(data)

    # helper function for 'indics' to find the Chaikin oscillator
    def chaikin(self, ti):
        data, meta_data = ti.get_ad(symbol=self.ticker)
        parse = getattr(self, "process", lambda: "An error occurred.")
        return parse(data)

    # helper function for 'indics' to find the on-balance volume
    def obv(self, ti):
        data, meta_data = ti.get_obv(symbol=self.ticker)
        parse = getattr(self, "process", lambda: "An error occurred.")
        return parse(data)

    # helper function for 'indics' to find the Aroon oscillator
    def aroon(self, ti):
        data, meta_data = ti.get_aroon(symbol=self.ticker, time_period=14)
        parse = getattr(self, "process", lambda: "An error occurred.")
        return parse(data)

    # helper function for all the 'indics' functions to process and return data
    def process(self, data):
        # checks if the markets have opened; if they have, they have a timestamp that needs to be removed
        if self.is_business_day(datetime.today()) and time(9, 30) < datetime.now().time() < time(16, 0):
            start = (datetime.strptime(data.index.values[-1], "%Y-%m-%d %H:%M:%S") - relativedelta(
                years=self.years)).strftime("%Y-%m-%d")
        else:
            start = (datetime.strptime(data.index.values[-1], "%Y-%m-%d") - relativedelta(
                years=self.years)).strftime("%Y-%m-%d")
        # selects data from the start date to the most recent date
        target = data.loc[start:data.index.values[-1]]
        return target

    # function that calls all the other functions and compiles all the data into one pandas data frame
    def assemble(self):
        # python list that defines the indicators we want to call
        indics = ["bbands", "ema", "stoch", "rsi", "chaikin", "obv", "aroon"]
        prices = self.daily_data()
        # resets the index so that concatenating the data frames will be less messy
        master = prices.reset_index(drop=True)
        print("Successfully parsed stock data.")

        # loops through the list indics and calls all the necessary functions
        for i in indics:
            # API calls are limited to 5 per minute; this is a safety to not go over that
            if indics.index(i) == 3:
                print("Waiting for 60 seconds")
                t.sleep(60)
            # combines the existing master data frame with the indicator's data frame
            master = pd.concat([master, self.indics(i).reset_index(drop=True)], axis=1, sort=False)
            print("Successfully parsed %s." % i)

        # sets the row index names to the dates
        master.set_index(prices.index.values, inplace=True)
        # plots all the data using matplotlib
        master.plot()
        plt.title("Stock Prices and Indicators for %s" % self.ticker)
        plt.show()
        return master
