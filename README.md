# Stock Data Management Project

This repository contains a set of Python scripts that collectively form a project for managing stock data. The project involves creating a SQLite database, populating it with stock tickers and their corresponding information, and fetching and storing daily stock price data.

## Table of Contents

- [Introduction](#introduction)
- [Scripts](#scripts)
  - [1. Create_DB.py](#1-create_dbpy)
  - [2. Ticker_Load.py](#2-ticker_loadpy)
  - [3. Add_Stock_Info.py](#3-add_stock_infopy)
  - [4. Add_Daily_Values.py](#4-add_daily_valuespy)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Introduction

This project aims to streamline the process of collecting, managing, and analyzing stock data. The scripts provided help in creating a database structure, populating it with stock tickers, fetching stock information, and storing daily stock price values.

## Scripts

The project is divided into four main scripts, each serving a specific purpose:

### 1. Create_DB.py

This script creates an SQLite database named "Stocks.db" with two tables: "Stocks" and "Prices". The "Stocks" table stores information about different stocks, while the "Prices" table is designed to store historical price data for those stocks.

### 2. Ticker_Load.py

This script performs web scraping to extract stock tickers from a specified URL. The extracted tickers are processed and saved into a CSV file named "tickers.csv".

### 3. Add_Stock_Info.py

This script uses the `yfinance` library to fetch additional information about the stocks using the tickers from the "tickers.csv" file. It populates the "Stocks" table in the database with stock names and sectors.

### 4. Add_Daily_Values.py

This script fetches daily stock price data for the tickers provided in the "tickers.csv" file. It populates the "Prices" table in the database with the fetched data, making sure not to duplicate existing data.

## Usage

1. Clone this repository to your local machine.

2. Install the required dependencies by running the following commands:

   ```bash
   pip install requests
   pip install beautifulsoup4
   pip install pandas
   pip install yfinance
   ```

3. Execute the scripts in the following order:

   a. Run `Create_DB.py` to create the SQLite database and tables.

   b. Run `Ticker_Load.py` to extract and save stock tickers.

   c. Run `Add_Stock_Info.py` to fetch and store additional stock information.

   d. Run `Add_Daily_Values.py` to fetch and store daily stock price data.

4. Make sure to customize and modify the scripts according to your specific needs, such as adjusting batch sizes, date ranges, and data storage locations.

## Contributing

Contributions to this project are welcome! If you have suggestions, improvements, or bug fixes, feel free to open an issue or submit a pull request.

## Future Updates

We have exciting plans for future updates to enhance the functionality of this project:

- **Advanced Data Analysis:** I'm working on implementing advanced data analysis techniques to provide valuable insights from the collected stock data.

- **Interactive Visualization:** Expect interactive data visualization tools that will help you better understand stock trends and patterns.

- **User Customization:** I'm planning to add options for users to customize data collection parameters and analysis settings.

I'm committed to improving this project and making it even more useful for managing and analyzing stock data. Your feedback and contributions are always welcome!

## License

This project is licensed under the The MIT License (MIT)

Copyright (c) 2023 Piotr Siergiej
