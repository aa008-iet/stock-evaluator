from data.Alphav import Alphav
from data.Morningstar import Morningstar
import pandas as pd
import numpy as np


def preprocess(ticker):

    alpha = Alphav(ticker, 10).assemble()

    ms = Morningstar(ticker).readratios()

    ad_index = pd.to_datetime(alpha.index.values).year
    md_index = pd.to_datetime(ms.index.values[:-1]).year

    for col in range(len(ms.columns)):
        alpha[ms.columns.values[col]] = np.nan
        for row in range(len(alpha.index)):
            if ad_index[row] == 2018:
                alpha.iloc[row, alpha.columns.get_loc(ms.columns.values[col])] = ms.iloc[ms.index.get_loc(ms.last_valid_index()), col]
            else:
                alpha.iloc[row, alpha.columns.get_loc(ms.columns.values[col])] = ms.iloc[md_index.get_loc(ad_index[row]), col]
        print("At col %s." % col)

    alpha["Score"] = np.nan
    for row in range(0, len(alpha) - 1):
        if alpha.adj_close[row] < alpha.adj_close[row + 1]:
            alpha.iloc[row, alpha.columns.get_loc("Score")] = 1
        else:
            alpha.iloc[row, alpha.columns.get_loc("Score")] = 0

    return alpha[:-1]


preprocess("AAPL").to_csv("test.csv")
