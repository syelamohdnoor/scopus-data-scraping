# Scopus-Data-Scraping

A scopus data extraction script to scrape publication number, total citations and h-index from Scopus Author Profile

Input:

1. An input file (Excel xlsx) must be prepared as shown in example.xlsx
2. A username and password for account in Scopus

# Prerequisite

Python 3, Pandas, Selenium, webdriver_manager.chrome

# Notes

1. There is more efficient way of doing this, by using Scopus API. For more detail, please visit https://dev.elsevier.com/.

2. The script is improvised from https://github.com/teonghan/Scopus-Extract-h-Index. 

3. You may go through some problems before succesfully scraping the data due to the connection problem to Scopus.com.

4. It is advisable to check your output after scraping the data to detect errors and missing values.
