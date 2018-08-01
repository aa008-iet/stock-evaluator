from Alphav import Alphav

ticker = input("Enter the ticker: ")
comp = Alphav(ticker, 10)
# time.sleep(40)
comp.assemble().to_csv("alpha_%s.csv"%ticker, encoding="utf-8")
