import pandas_datareader.yahoo.fx
import datetime
import pandas

end_date = datetime.date.today()
start_date = end_date - datetime.timedelta(days=30)

eurusd_reader = pandas_datareader.yahoo.fx.YahooFXReader(symbols="EURUSD", start=start_date, end=end_date, interval='d',chunksize=7)
eurusd = eurusd_reader.read()
print(eurusd)


