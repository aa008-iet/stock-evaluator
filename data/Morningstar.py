# uses pandas to organize data
import pandas as pd


# Morningstar reads a csv of company data and spits it back as a pandas data frame
class Morningstar(object):
    # constructor of the class that takes the desired ticker as a parameter
    def __init__(self, ticker):
        self.ticker = ticker
    
    # returns a pandas data frame of data
    def readratios(self):
        # reads exported csv from Morningstar
        url = "http://financials.morningstar.com/ajax/exportKR2CSV.html?t=%s" % self.ticker
        print("Now reading %s" % url)
        # flips the rows and columns (rows are now sorted by year) and removes any columns with empty values
        response = pd.read_csv(url, skiprows=2).transpose().dropna(axis=1)
        # sets column names equal to the names of the company data (revenue, operating margin, etc)
        response.columns = response.iloc[0]
        # removes any misread columns that have the words 'TTM' or 'Latest Qtr' in them
        response = response.loc[:, response.iloc[-1].ne('TTM')]
        response = response.loc[:, response.iloc[-1].ne('Latest Qtr')]
        # skips the first row of data since they're the column names now
        return response[1:]

