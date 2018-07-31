def readRatios(self):
    url = "http://financials.morningstar.com/ajax/exportKR2CSV.html?t=%s" % (self)
    print("Now reading %s" % (url))
    response = pd.read_csv(url, skiprows=2)
    return response