from Alphav import Alphav
from Morningstar import Morningstar
import time

ticker = input("Enter the ticker: ")
time.sleep(60)
comp = Alphav(ticker, 10)
comp.assemble().to_csv("alpha_%s.csv"%ticker, encoding="utf-8")

indic = Morningstar(ticker)
indic.readratios().to_csv("ms_%s.csv" % ticker, encoding="utf8")