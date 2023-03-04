import pandas_datareader.yahoo.fx
import datetime
import matplotlib.pyplot as plt

end_date = datetime.date.today()
# w notatkach mam zapisane "za ostatni miesiąc", zakładam że jest to ostatnie 30 dni.
start_date = end_date - datetime.timedelta(days=20)

# from: https://pandas-datareader.readthedocs.io/en/latest/readers/yahoo.html#pandas_datareader.yahoo.fx.YahooFXReader
eurusd_reader = pandas_datareader.yahoo.fx.YahooFXReader(symbols="EURUSD", start=start_date, end=end_date, interval='d')
eurusd = eurusd_reader.read()
print(eurusd)
print(eurusd.loc[datetime.date.today() - datetime.timedelta(days=2)])
print(eurusd.info())


# Calculating simple moving average
eurusd = eurusd["Close"].to_frame()
eurusd["SMA5"] = eurusd['Close'].rolling(5).mean()
print(eurusd)

# Draw the plot!
eurusd.plot()
plt.show()


