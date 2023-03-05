import pandas_datareader.yahoo.fx
import datetime
import matplotlib.pyplot as plt
import calendar
import dateutil.relativedelta
import pandas

currency_exrate = "EURUSD"
moving_average_type = "EMA"

# Dane dla średniej kroczącej 15 i 40 dni
step_length = [15, 40]

# Zakładam że "za ostatni miesiąc" oznacza poprzedni miesiąc od 1-go do ostatniego dnia miesiąca.
current_date = datetime.date.today()

previous_month_1_day = (current_date - dateutil.relativedelta.relativedelta(months=1)).replace(day=1)  # 1st day for plot
last_day_of_previous_month = calendar.monthrange(previous_month_1_day.year, previous_month_1_day.month)[1]
previous_month_last_day = previous_month_1_day.replace(day=last_day_of_previous_month)  # last day for plot

# Aby móc narysować wykres średnich kroczących potrzebujemy danych sprzed okresu który nas interesuje
max_prev_days = previous_month_1_day - datetime.timedelta(days=max(step_length))

start_date = max_prev_days
end_date = previous_month_last_day

# from: https://pandas-datareader.readthedocs.io/en/latest/readers/yahoo.html#pandas_datareader.yahoo.fx.YahooFXReader
eur_exrate_reader = pandas_datareader.yahoo.fx.YahooFXReader(symbols=currency_exrate,
                                                             start=start_date, end=end_date,
                                                             interval='d')
eur_exrate = eur_exrate_reader.read()
print(eur_exrate.info())
# We will work on single column for simplifying
eur_exrate = eur_exrate["Close"].to_frame()

new_date_idx = pandas.date_range(start_date, end_date)
reindexed_eur_exrate = eur_exrate.reindex(new_date_idx, fill_value=None)
filled_eur_exrate = reindexed_eur_exrate.fillna(method='pad')

# Calculating simple or exponential moving average for Close
for step in step_length:
    if moving_average_type == "SMA":
        filled_eur_exrate[f"{moving_average_type}{step}"] = filled_eur_exrate['Close'].rolling(step).mean()
    elif moving_average_type == "EMA":
        filled_eur_exrate[f"{moving_average_type}{step}"] = filled_eur_exrate['Close'].ewm(span=step).mean()
    else:
        print("You shall not pass! \U0001F9D9")
        break

# Draw the plot!
eur_exrate_previous_month = filled_eur_exrate.loc[previous_month_1_day:previous_month_last_day]
eur_exrate_previous_month.plot()
plt.show()


