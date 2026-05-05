# Summary: This module contains the user interface and logic for a console-based version of the stock manager program.

from datetime import datetime
from stock_class import Stock, DailyData
from utilities import clear_screen, display_stock_chart
from os import path
import stock_data


# Main Menu
def main_menu(stock_list):
    option = ""
    while option != "0":
        clear_screen()
        print("Stock Analyzer ---")
        print("1 - Manage Stocks (Add, Update, Delete, List)")
        print("2 - Add Daily Stock Data (Date, Price, Volume)")
        print("3 - Show Report")
        print("4 - Show Chart")
        print("5 - Manage Data (Save, Load, Retrieve, Import)")
        print("0 - Exit Program")
        option = input("Enter Menu Option: ")
        while option not in ["1","2","3","4","5","0"]:
            clear_screen()
            print("*** Invalid Option - Try again ***")
            print("Stock Analyzer ---")
            print("1 - Manage Stocks (Add, Update, Delete, List)")
            print("2 - Add Daily Stock Data (Date, Price, Volume)")
            print("3 - Show Report")
            print("4 - Show Chart")
            print("5 - Manage Data (Save, Load, Retrieve, Import)")
            print("0 - Exit Program")
            option = input("Enter Menu Option: ")
        if option == "1":
            manage_stocks(stock_list)
        elif option == "2":
            add_stock_data(stock_list)
        elif option == "3":
            display_report(stock_list)
        elif option == "4":
            display_chart(stock_list)
        elif option == "5":
            manage_data(stock_list)
        else:
            clear_screen()
            print("Goodbye")

# Manage Stocks
def manage_stocks(stock_list):
    option = ""
    while option != "0":
        clear_screen()
        print("Manage Stocks ---")
        print("1 - Add Stock")
        print("2 - Update Shares")
        print("3 - Delete Stock")
        print("4 - List Stocks")
        print("0 - Exit Manage Stocks")
        option = input("Enter Menu Option: ")
        while option not in ["1","2","3","4","0"]:
            clear_screen()
            print("*** Invalid Option - Try again ***")
            print("1 - Add Stock")
            print("2 - Update Shares")
            print("3 - Delete Stock")
            print("4 - List Stocks")
            print("0 - Exit Manage Stocks")
            option = input("Enter Menu Option: ")
        if option == "1":
            add_stock(stock_list)
        elif option == "2":
            update_shares(stock_list)
        elif option == "3":
            delete_stock(stock_list)
        elif option == "4":
            list_stocks(stock_list)
        else:
            print("Returning to Main Menu")

# Add new stock to track
def add_stock(stock_list):
    clear_screen()
    print("Add Stock ---")
    symbol = input("Enter stock symbol: ").upper()
    name = input("Enter company name: ")
    shares = float(input("Enter shares: "))

    new_stock = Stock(symbol, name, shares)
    stock_list.append(new_stock)

    print(symbol + " added.")
    input("Press Enter to continue")
        
# Buy or Sell Shares Menu
def update_shares(stock_list):
    option = ""
    while option != "0":
        clear_screen()
        print("Update Shares ---")
        print("1 - Buy Shares")
        print("2 - Sell Shares")
        print("0 - Return to Main Menu")
        option = input("Enter Menu Option: ")

        if option == "1":
            buy_stock(stock_list)
        elif option == "2":
            sell_stock(stock_list)
        elif option != "0":
            print("Invalid option.")
            input("Press Enter to Continue")


# Buy Stocks (add to shares)
def buy_stock(stock_list):
    clear_screen()
    print("Buy Shares ---")
    print("Stock List: [",end="")

    for stock in stock_list:
        print(stock.symbol + " ", end="")

    print("]")

    symbol = input("Enter Stock Symbol: ").upper()
    shares = float(input("Enter Shares to Buy: "))

    for stock in stock_list:
        if stock.symbol == symbol:
            stock.buy(shares)
            print("Shares purchased.")
            input("Press Enter to Continue")
            return

    print("Stock not found.")
    input("Press Enter to Continue")

# Sell Stocks (subtract from shares)
def sell_stock(stock_list):
    clear_screen()
    for stock in stock_list:
        print(stock.symbol + " ", end="")

    print("]")

    symbol = input("Enter Stock Symbol: ").upper()
    shares = float(input("Enter Shares to Sell: "))

    for stock in stock_list:
        if stock.symbol == symbol:
            stock.sell(shares)
            print("Shares sold.")
            input("Press Enter to Continue")
            return

    print("Stock not found.")
    input("Press Enter to Continue")


# Remove stock and all daily data
def delete_stock(stock_list):
    clear_screen()
    print("Delete Stock ---")
    print("Stock List: [", end="")

    for stock in stock_list:
        print(stock.symbol + " ", end="")

    print("]")

    symbol = input("Enter Stock Symbol to Delete: ").upper()

    for stock in stock_list:
        if stock.symbol == symbol:
            stock_list.remove(stock)
            print(symbol + " deleted.")
            input("Press Enter to Continue")
            return

    print("Stock not found.")
    input("Press Enter to Continue")


# List stocks being tracked
def list_stocks(stock_list):
    clear_screen()
    print("List Stocks ---")

    if len(stock_list) == 0:
        print("No stocks currently tracked.")
    else:
        for stock in stock_list:
            print(stock.symbol + " (" + stock.name + ")" + " - Shares: " + str(stock.shares))

    input("Press Enter to Continue")

# Add Daily Stock Data
def add_stock_data(stock_list):
    clear_screen()
    print("Add Daily Stock Data ---")
    print("Stock List: [", end="")

    for stock in stock_list:
        print(stock.symbol + " ", end="")

    print("]")

    symbol = input("Enter Stock Symbol: ").upper()

    for stock in stock_list:
        if stock.symbol == symbol:
            date = input("Enter Date (m/d/yy): ")
            price = float(input("Enter Closing Price: "))
            volume = float(input("Enter Volume: "))

            daily_data = DailyData(datetime.strptime(date, "%m/%d/%y"), price, volume)
            stock.add_data(daily_data)

            print("Daily data added.")
            input("Press Enter to Continue")
            return

    print("Stock not found.")
    input("Press Enter to Continue")

# Display Report for All Stocks
def display_report(stock_data):
    clear_screen()
    print("Stock Report ---")
    for stock in stock_data:
        print()
        print(stock.symbol + " - " + stock.name)
        print("Shares:", stock.shares)

        if len(stock.DataList) > 0:

            sorted_data = sorted(stock.DataList, key=lambda d: d.date)

            first = sorted_data[0].close
            latest = sorted_data[-1].close
            gain_loss = (latest - first) * stock.shares

            print("First Price:", "${:0,.2f}".format(first))
            print("Latest Price:", "${:0,.2f}".format(latest))
            print("Gain/Loss:", "${:0,.2f}".format(gain_loss))
        else:
            print("No daily data available.")

    input("Press Enter to Continue")



# Display Chart
def display_chart(stock_list):
    print("Stock List: [",end="")
    
    for stock in stock_list:
        print(stock.symbol + " ", end="")

    print("]")

    symbol = input("Enter Stock Symbol to Chart: ").upper()
    display_stock_chart(stock_list, symbol)
    input("Press Enter to Continue")

# Manage Data Menu
def manage_data(stock_list):
    option = ""
    while option != "0":
        print("\nManage Data ---")
        print("1 - Save Data")
        print("2 - Load Data")
        print("3 - Retrieve Data from Web")
        print("4 - Import from CSV File")
        print("0 - Exit Manage Data")

        option = input("Enter Menu Option: ")

        if option == "1":
            stock_data.save_stock_data(stock_list)
            print("Data Saved.")

        elif option == "2":
            stock_data.load_stock_data(stock_list)
            print("Data Loaded.")

        elif option == "3":
            retrieve_from_web(stock_list)
        
        elif option == "4":
            import_csv(stock_list)

        elif option == "0":
            print("Returning to Main Menu...")

        else:
            print("Invalid option.")

# Get stock price and volume history from Yahoo! Finance using Web Scraping
def retrieve_from_web(stock_list):
    print("Retrieving Stock Data from Yahoo! Finance ---")
    print("This will retrieve data from all stocks in your stock list.")

    dateFrom = input("Enter Starting Date (m/d/yy): ")
    dateTo = input("Enter Ending Date (m/d/yy): ")

    try:
        records = stock_data.retrieve_stock_web(dateFrom, dateTo, stock_list)
        print("Records Retrieved:", records)
    except:
        print("Error retrieving data. Check ChromeDriver.")
        return 
    input("Press Enter to Continue")
    #clear_screen()
    #pass

# Import stock price and volume history from Yahoo! Finance using CSV Import
def import_csv(stock_list):
    clear_screen()
    print("Import CSV from Yahoo! Finance ---")
    print("Stock List: [", end="")

    for stock in stock_list:
        print(stock.symbol + " ", end="")

    print("]")

    symbol = input("Enter Stock Symbol: ").upper()
    filename = input("Enter CSV filename with full path: ").strip()

    # Validation to make sure it's a valid filename
    if symbol == "" or filename == "":
        print("Error: Symbol and filename cannot be empty.")
        input("Press Enter to Continue")
        return
    # check if the stock we want to import data for exists 
    found = any(stock.symbol == symbol for stock in stock_list)
    if not found:
        print("Stock not found.")
        return
    try:
        records = stock_data.import_stock_web_csv(stock_list, symbol, filename)
        print("CSV Imported. Records Imported:", records)
    except Exception as e:
        print("Error importing CSV file:", e)

    input("Press Enter to Continue")

# Begin program
def main():
    #check for database, create if not exists
    if path.exists("stocks.db") == False:
        stock_data.create_database()
    stock_list = []
    main_menu(stock_list)

# Program Starts Here
if __name__ == "__main__":
    # execute only if run as a stand-alone script
    main()