import pandas_datareader.yahoo.fx
import datetime
import matplotlib.pyplot as plt
import calendar
import dateutil.relativedelta
import pandas

currency_exrate = "EURUSD"
moving_average_type = "SMA"

# step length for moving average for 15 and 40 days
step_length = [15, 40]
# make sure that every value is int and there are no negative values
step_length_map = map(int, step_length)
step_length = list(map(abs, step_length_map))

# Zakładam że "za ostatni miesiąc" oznacza poprzedni miesiąc od 1-go do ostatniego dnia miesiąca.
current_date = datetime.date.today()

# First day of the month - 1st day for plot
first_month_day = (current_date - dateutil.relativedelta.relativedelta(months=1)).replace(day=1)
last_day_of_previous_month = calendar.monthrange(first_month_day.year, first_month_day.month)[1]
# Last day of the month - last day of plot
last_month_day = first_month_day.replace(day=last_day_of_previous_month)

# Aby móc narysować wykres średnich kroczących potrzebujemy danych sprzed okresu który nas interesuje
max_prev_days = first_month_day - datetime.timedelta(days=max(step_length))

start_date = max_prev_days
end_date = last_month_day

# from: https://pandas-datareader.readthedocs.io/en/latest/readers/yahoo.html#pandas_datareader.yahoo.fx.YahooFXReader
eur_exrate_reader = pandas_datareader.yahoo.fx.YahooFXReader(symbols=currency_exrate,
                                                             start=start_date, end=end_date,
                                                             interval='d')
eur_exrate = eur_exrate_reader.read()
print(eur_exrate.info())
# We will work on single column for simplifying
eur_exrate = eur_exrate["Close"].to_frame()

# We need to fill lacking date values, on weekends are no currency exchange rate information - expand index in dataframe
# Create new date range
new_date_idx = pandas.date_range(start_date, end_date)
# Replace old index in dataframe with filled one
reindexed_eur_exrate = eur_exrate.reindex(new_date_idx, fill_value=None)
# Fill None values from expanding index, with previous values (method pad)
eur_exrate = reindexed_eur_exrate.fillna(method='pad')

# Calculating simple or exponential moving average for Close
for step in step_length:
    if moving_average_type == "SMA":
        eur_exrate[f"{moving_average_type}{step}"] = eur_exrate['Close'].rolling(step).mean()
    elif moving_average_type == "EMA":
        eur_exrate[f"{moving_average_type}{step}"] = eur_exrate['Close'].ewm(span=step).mean()
    else:
        print("You shall not pass! \U0001F9D9")
        break

# Change column name
eur_exrate.rename(columns={'Close': currency_exrate}, inplace=True)
# Limit plot range for full month
eur_exrate_previous_month = eur_exrate.loc[first_month_day:last_month_day]
# Draw the plot!
eur_exrate_previous_month.plot(marker='.')
plt.show()
