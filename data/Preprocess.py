# import local classes
from data.Alphav import Alphav
from data.Morningstar import Morningstar

# import libraries for statistics
import pandas as pd
import numpy as np


def preprocess(ticker):

    # creates a pandas data frame for the ticker for historical stock data
    alpha = Alphav(ticker, 10).assemble()

    # creates a pandas data frame for the ticker for historical financial data
    ms = Morningstar(ticker).readratios()

    # creates two datetime indices for each data frame
    ad_index = pd.to_datetime(alpha.index.values).year
    md_index = pd.to_datetime(ms.index.values[:-1]).year

    '''
    The nested for loop below cycles through both the historical stock data and the historical financial data.
    The stock data is daily while the financial data is monthly. In the for loop, the financial data is matched
    with the appropriate stock data based on the year. If the year of the daily stock data matches the year
    of a row in the yearly financial data, that value is put into the generated column.
    Ex: If the loop is examining column "Revenue" and finds that the current row is in the year 2010, then
    it will assign 2010's "Revenue" value to that row in the column. 
    '''

    # iterates through all the columns in Morningstar (ms)
    for col in range(len(ms.columns)):
        # creates a new column based on the column name from Morningstar and fills it with "NA" values
        alpha[ms.columns.values[col]] = np.nan
        # iterates through the rows from alpha
        for row in range(len(alpha.index)):
            if ad_index[row] == 2018:
                # 2018 data is "TTM" in ms so the usual method of assignment by matching years doesn't work
                alpha.iloc[row, alpha.columns.get_loc(ms.columns.values[col])] = ms.iloc[ms.index.get_loc(ms.last_valid_index()), col]
            else:
                # assigns a value to the new column according to matching years, as determined by matching md_index and ad_index
                alpha.iloc[row, alpha.columns.get_loc(ms.columns.values[col])] = ms.iloc[md_index.get_loc(ad_index[row]), col]
        print("At col %s." % col)

    # new column named score
    alpha["Score"] = np.nan
    # assigns a 1 if tomorrow's price is higher and a 0 if it's lower
    # this is what the neural network will try to predict (binary classification)
    for row in range(0, len(alpha) - 1):
        if alpha.adj_close[row] < alpha.adj_close[row + 1]:
            alpha.iloc[row, alpha.columns.get_loc("Score")] = 1
        else:
            alpha.iloc[row, alpha.columns.get_loc("Score")] = 0

    return alpha[:-1]


# saves the data as a csv file
preprocess("AAPL").to_csv("test.csv")
