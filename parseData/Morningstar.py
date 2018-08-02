import pandas as pd


class Morningstar(object):
    def __init__(self, ticker):
        self.ticker = ticker

    def readratios(self):
        url = "http://financials.morningstar.com/ajax/exportKR2CSV.html?t=%s" % self.ticker
        print("Now reading %s" % url)
        response = pd.read_csv(url, skiprows=2).transpose().dropna(axis=1)
        response.columns = response.iloc[0]
        return response[1:]

