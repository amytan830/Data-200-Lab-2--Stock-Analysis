#Helper Functions

import matplotlib.pyplot as plt

from os import system, name

# Function to Clear the Screen
def clear_screen():
    if name == "nt": # User is running Windows
        _ = system('cls')
    else: # User is running Linux or Mac
        _ = system('clear')

# Function to sort the stock list (alphabetical)
def sortStocks(stock_list):
    ## Sort the stock list
    pass


# Function to sort the daily stock data (oldest to newest) for all stocks
def sortDailyData(stock_list):
    pass

# Function to create stock chart
def display_stock_chart(stock_list, symbol):
    import matplotlib.pyplot as plt

    for stock in stock_list:
        if stock.symbol == symbol:
            sorted_data = sorted(stock.DataList, key=lambda d: d.date)

            # show only last 60 data points
            chart_data = sorted_data[-60:]

            dates = []
            prices = []

            for daily_data in chart_data:
                dates.append(daily_data.date)
                prices.append(daily_data.close)

            if len(dates) == 0:
                print("No data to chart.")
                return

            plt.figure()
            plt.plot(dates, prices)
            plt.title(symbol + " Stock Price History")
            plt.xlabel("Date")
            plt.ylabel("Closing Price")
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.show()
            return