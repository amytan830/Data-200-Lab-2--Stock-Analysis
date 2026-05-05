# Summary: This module contains the user interface and logic for a graphical user interface version of the stock manager program.

from datetime import datetime
from os import path
from tkinter import *
from tkinter import ttk
from tkinter import messagebox, simpledialog, filedialog
import csv
import stock_data
from stock_class import Stock, DailyData
from utilities import clear_screen, display_stock_chart, sortStocks, sortDailyData

class StockApp:
    def __init__(self):
        self.stock_list = []
        #check for database, create if not exists
        if path.exists("stocks.db") == False:
            stock_data.create_database()

 # This section creates the user interface

        # Create Window
        self.root = Tk()
        self.root.title("(myname) Stock Manager") #Replace with a suitable name for your program


        # Add Menubar
        self.menubar = Menu(self.root)

        # Add File Menu
        self.filemenu = Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Load Data", command=self.load)
        self.filemenu.add_command(label="Save Data", command=self.save)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=self.root.quit)


        # Add Web Menu 
        self.webmenu = Menu(self.menubar, tearoff=0)
        self.webmenu.add_command(label="Scrape Data from Yahoo! Finance...", command=self.scrape_web_data)
        self.webmenu.add_command(label="Import CSV From Yahoo! Finance...", command=self.importCSV_web_data)

        # Add Chart Menu
        self.chartmenu = Menu(self.menubar, tearoff=0)
        self.chartmenu.add_command(label="Display Chart", command=self.display_chart)

        # Add menus to window       
        self.menubar.add_cascade(label="File", menu=self.filemenu)
        self.menubar.add_cascade(label="Web", menu=self.webmenu)
        self.menubar.add_cascade(label="Chart", menu=self.chartmenu)
        self.root.config(menu=self.menubar)

        # Add heading information
        self.headingLabel = Label(self.root, text="Stock Manager")
        self.headingLabel.pack()

        # Add stock list
        self.stockList = Listbox(self.root)
        self.stockList.pack()
        self.stockList.bind("<<ListboxSelect>>", self.update_data)


        # Add Tabs
        self.tabControl = ttk.Notebook(self.root)
        self.mainTab = ttk.Frame(self.tabControl)
        self.historyTab = ttk.Frame(self.tabControl)
        self.reportTab = ttk.Frame(self.tabControl)

        self.tabControl.add(self.mainTab, text="Main")
        self.tabControl.add(self.historyTab, text="History")
        self.tabControl.add(self.reportTab, text="Report")
        self.tabControl.pack(expand=1, fill="both")
        
        # Set Up Main Tab
        Label(self.mainTab, text="Symbol").pack()
        self.addSymbolEntry = Entry(self.mainTab)
        self.addSymbolEntry.pack()

        Label(self.mainTab, text="Name").pack()
        self.addNameEntry = Entry(self.mainTab)
        self.addNameEntry.pack()

        Label(self.mainTab, text="Shares").pack()
        self.addSharesEntry = Entry(self.mainTab)
        self.addSharesEntry.pack()

        Button(self.mainTab, text="Add Stock", command=self.add_stock).pack()
        Button(self.mainTab, text="Delete Stock", command=self.delete_stock).pack()

        Label(self.mainTab, text="Update Shares").pack()
        self.updateSharesEntry = Entry(self.mainTab)
        self.updateSharesEntry.pack()

        Button(self.mainTab, text="Buy Shares", command=self.buy_shares).pack()
        Button(self.mainTab, text="Sell Shares", command=self.sell_shares).pack()

        # Setup History Tab
        self.dailyDataList = Text(self.historyTab)
        self.dailyDataList.pack(expand=1, fill="both")
 
        # Setup Report Tab
        self.stockReport = Text(self.reportTab)
        self.stockReport.pack(expand=1, fill="both")


        ## Call MainLoop
        self.root.mainloop()

# This section provides the functionality
       
    # Load stocks and history from database.
    def load(self):
        self.stockList.delete(0,END)
        stock_data.load_stock_data(self.stock_list)
        sortStocks(self.stock_list)
        for stock in self.stock_list:
            self.stockList.insert(END,stock.symbol)
        messagebox.showinfo("Load Data","Data Loaded")

    # Save stocks and history to database.
    def save(self):
        stock_data.save_stock_data(self.stock_list)
        messagebox.showinfo("Save Data","Data Saved")

    # Refresh history and report tabs
    def update_data(self, evt):
        self.display_stock_data()

    # Display stock price and volume history.
    def display_stock_data(self):
        if len(self.stockList.curselection()) == 0:
            return
        symbol = self.stockList.get(self.stockList.curselection())
        for stock in self.stock_list:
            if stock.symbol == symbol:
                self.headingLabel['text'] = stock.name + " - " + str(stock.shares) + " Shares"
                self.dailyDataList.delete("1.0",END)
                self.stockReport.delete("1.0",END)
                self.dailyDataList.insert(END,"- Date -   - Price -   - Volume -\n")
                self.dailyDataList.insert(END,"=================================\n")
                for daily_data in stock.DataList:
                    row = daily_data.date.strftime("%m/%d/%y") + "   " +  '${:0,.2f}'.format(daily_data.close) + "   " + str(daily_data.volume) + "\n"
                    self.dailyDataList.insert(END,row)

                # display report
                if len(stock.DataList) > 0:
                    sorted_data = sorted(stock.DataList, key=lambda d: d.date)

                    first_price = sorted_data[0].close
                    latest_price = sorted_data[-1].close

                    change_per_share = latest_price - first_price
                    total_gain_loss = change_per_share * stock.shares
                    percent_change = (change_per_share / first_price) * 100

                    self.stockReport.insert(END, "Profit/Loss Report\n")
                    self.stockReport.insert(END, "========================\n")
                    self.stockReport.insert(END, "Symbol: " + stock.symbol + "\n")
                    self.stockReport.insert(END, "Shares Owned: " + str(stock.shares) + "\n\n")
                    self.stockReport.insert(END, "First Price: " + '${:0,.2f}'.format(first_price) + "\n")
                    self.stockReport.insert(END, "Latest Price: " + '${:0,.2f}'.format(latest_price) + "\n")
                    self.stockReport.insert(END, "Change Per Share: " + '${:0,.2f}'.format(change_per_share) + "\n")
                    self.stockReport.insert(END, "Total Gain/Loss: " + '${:0,.2f}'.format(total_gain_loss) + "\n")
                    self.stockReport.insert(END, "Percent Change: " + "{:.2f}%".format(percent_change) + "\n")


    # Add new stock to track.
    def add_stock(self):
        try:
            shares = float(self.addSharesEntry.get())
        except:
            messagebox.showerror("Invalid Input", "Enter a valid number for shares.")
            return

        new_stock = Stock(
            self.addSymbolEntry.get(),
            self.addNameEntry.get(),
            shares)

        self.stock_list.append(new_stock)
        self.stockList.insert(END, self.addSymbolEntry.get())

        self.addSymbolEntry.delete(0,END)
        self.addNameEntry.delete(0,END)
        self.addSharesEntry.delete(0,END)

    # Buy shares of stock.
    def buy_shares(self):
        # make sure a stock is selected
        if len(self.stockList.curselection()) == 0:
            messagebox.showerror("No Selection", "Please select a stock first.")
            return
        symbol = self.stockList.get(self.stockList.curselection())
        try:
            shares = float(self.updateSharesEntry.get())
        except:
            messagebox.showerror("Invalid Input", "Enter a valid number for shares.")
            return
        for stock in self.stock_list:
            if stock.symbol == symbol:
                stock.buy(shares)
                self.headingLabel['text'] = stock.name + " - " + str(stock.shares) + " Shares"
        messagebox.showinfo("Buy Shares","Shares Purchased")
        self.updateSharesEntry.delete(0,END)

    # Sell shares of stock.
    def sell_shares(self):
        # make sure a stock is selected
        if len(self.stockList.curselection()) == 0:
            messagebox.showerror("No Selection", "Please select a stock first.")
            return
        symbol = self.stockList.get(self.stockList.curselection())
        try:
            shares = float(self.updateSharesEntry.get())
        except:
            messagebox.showerror("Invalid Input", "Enter a valid number for shares.")
            return
        for stock in self.stock_list:
            if stock.symbol == symbol:
                stock.sell(shares)
                self.headingLabel['text'] = stock.name + " - " + str(stock.shares) + " Shares"
        messagebox.showinfo("Sell Shares","Shares Sold")
        self.updateSharesEntry.delete(0,END)

    # Remove stock and all history from being tracked.
    def delete_stock(self):
        # make sure a stock is selected
        if len(self.stockList.curselection()) == 0:
            messagebox.showerror("No Selection", "Please select a stock first.")
            return

        # get selected symbol
        symbol = self.stockList.get(self.stockList.curselection())

        # remove from stock_list
        for stock in self.stock_list:
            if stock.symbol == symbol:
                self.stock_list.remove(stock)
                break

        # remove from listbox
        self.stockList.delete(self.stockList.curselection())

        # clear display areas
        self.headingLabel['text'] = ""
        self.dailyDataList.delete("1.0", END)
        self.stockReport.delete("1.0", END)

        messagebox.showinfo("Delete Stock", symbol + " deleted.")

    # Get data from web scraping.
    def scrape_web_data(self):
        dateFrom = simpledialog.askstring("Starting Date","Enter Starting Date (m/d/yy)")
        dateTo = simpledialog.askstring("Ending Date","Enter Ending Date (m/d/yy)")
        try:
            stock_data.retrieve_stock_web(dateFrom,dateTo,self.stock_list)
        except Exception as e:
            print("GUI ERROR:", e)
            messagebox.showerror("Cannot Get Data from Web","Check Path for Chrome Driver")
            return
        self.display_stock_data()
        messagebox.showinfo("Get Data From Web","Data Retrieved")

    # Import CSV stock history file.
    def importCSV_web_data(self):
        # make sure a stock is selected
        if len(self.stockList.curselection()) == 0:
            messagebox.showerror("No Selection", "Please select a stock first.")
            return
        symbol = self.stockList.get(self.stockList.curselection())
        filename = filedialog.askopenfilename(title="Select " + symbol + " File to Import",filetypes=[('Yahoo Finance! CSV','*.csv')])
        if filename != "":
            stock_data.import_stock_web_csv(self.stock_list,symbol,filename)
            self.display_stock_data()
            messagebox.showinfo("Import Complete",symbol + " Import Complete")   
    
    # Display stock price chart.
    def display_chart(self):
        if len(self.stockList.curselection()) == 0:
            messagebox.showerror("No Stock Selected", "Please select a stock first.")
            return

        symbol = self.stockList.get(self.stockList.curselection())
        display_stock_chart(self.stock_list, symbol)


def main():
        app = StockApp()
        

if __name__ == "__main__":
    # execute only if run as a script
    main()