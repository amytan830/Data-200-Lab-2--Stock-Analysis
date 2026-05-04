# Lab 2 - Stock Analysis Project

## Overview

This project is a Python-based stock analysis application that allows users to:

* Store stock information in a SQLite database
* Import historical stock data from CSV files or Yahoo Finance
* Analyze stock performance
* View data through both console and GUI interfaces
  
---
## Tools Used

* Python
* SQLite3
* Pandas
* BeautifulSoup (web scraping)
* Selenium (for web data retrieval)

---

## How to Run

### Console Version

```bash
python stock_console.py
```

### GUI Version

```bash
python stock_GUI.py
```

---

## Data Sources

* CSV files (e.g., TSLA.csv, WMT.csv)
* Yahoo Finance (via web scraping or CSV export)

---

## Notes

* The database (`stocks.db`) is created automatically when the program runs.
* Duplicate records are prevented using a primary key (`symbol`, `date`).
* CSV files must follow the Yahoo Finance format.

---

## Author

Amy Tan
