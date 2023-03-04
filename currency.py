import pandas_datareader.yahoo.fx
import datetime
import pandas
import matplotlib.pyplot as plt

end_date = datetime.date.today()
start_date = end_date - datetime.timedelta(days=5)

# from: https://pandas-datareader.readthedocs.io/en/latest/readers/yahoo.html#pandas_datareader.yahoo.fx.YahooFXReader
eurusd_reader = pandas_datareader.yahoo.fx.YahooFXReader(symbols="EURUSD", start=start_date, end=end_date, interval='d')
eurusd = eurusd_reader.read()
print(eurusd)
print(eurusd.loc[datetime.date.today() - datetime.timedelta(days=2)])
print(eurusd.info())

eurusd.plot()
plt.show()


