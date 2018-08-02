# Obtaining Financial Data

<h3>Purpose</h3>
Finding data used to feed into the neural network and preprocessing.

<h3>Overview</h3>
In `Alphav.py` and `Morningstar.py`, there are classes that go by the same name as the files.
Under each, they have functions that allow them to pull data from APIs. 
The website Alpha Vantage provides data on its own, but the python library `alpha_vantage` allows easier API calls with its built-in functions.

Morningstar provides financial data with a web API that returns csv files, which are processed using `pandas`.

<h3>Usage</h3>
To call data, instantiate the classes `Alphav` and `Morningstar`. 
Each class has a function that assembles different data per ticker.

For example, the following code writes a csv file of adjusted close, highs, lows and volume of shares traded per business day, as well as relevant indicators such as the stochastic oscillator and the exponential moving average. 

```python
import Alphav
apple = Alphav("AAPL", 5)
apple.assemble()
```
Below, calling data from Morningstar yields a csv file with 100 columns of data from GOOGL financial statements.
```python
import Morningstar
google = Morningstar("GOOGL")
google.assemble()
```

<h3>Citations</h3>

>The [alpha_vantage library](https://github.com/RomelTorres/alpha_vantage) by RomelTorres

>[Alpha Vantage API](https://alphavantage.co) 

>[Morningstar API](https://gist.github.com/hahnicity/45323026693cdde6a116)

