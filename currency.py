import pandas_datareader.yahoo.fx
import datetime
import matplotlib.pyplot as plt
import calendar
import dateutil.relativedelta

# Dane dla średniej kroczącej 15 i 40 dni
step_length = [15, 40]

# Zakładam że "za ostatni miesiąc" oznacza poprzedni miesiąc od 1-go do ostatniego dnia miesiąca.
current_date = datetime.date.today()

previous_month_1_day = (current_date - dateutil.relativedelta.relativedelta(months=1)).replace(day=1) # 1st day for plot
last_day_of_previous_month = calendar.monthrange(previous_month_1_day.year, previous_month_1_day.month)[1]
previous_month_last_day = previous_month_1_day.replace(day=last_day_of_previous_month) # last day for plot

# Aby móc narysować wykres średnich kroczących potrzebujemy danych sprzed okresu który nas interesuje
max_prev_days = previous_month_1_day - datetime.timedelta(days=max(step_length))

start_date = max_prev_days
end_date = previous_month_last_day

# from: https://pandas-datareader.readthedocs.io/en/latest/readers/yahoo.html#pandas_datareader.yahoo.fx.YahooFXReader
eurusd_reader = pandas_datareader.yahoo.fx.YahooFXReader(symbols="EURUSD", start=start_date, end=end_date, interval='d')
eurusd = eurusd_reader.read()
print(eurusd)
# date_minus_five = previous_month_last_day - datetime.timedelta(days=5)
# print(eurusd.loc[date_minus_five])
print(eurusd.info())


# Calculating simple moving average for Close
eurusd = eurusd["Close"].to_frame()

# SMA15
eurusd["SMA15"] = eurusd['Close'].rolling(15).mean()

# SMA40
eurusd["SMA40"] = eurusd['Close'].rolling(40).mean()

# Draw the plot!
eurusd_previous_month = eurusd.loc[start_date:previous_month_last_day]
eurusd_previous_month.plot()
plt.show()


