# Project Description

The Tehran Stock Exchange Symbol Scraper is a Python script that allows you to retrieve symbols from the Tehran Stock Exchange website (http://tsetmc.com/) and store them in a CSV file. It provides a convenient way to access and utilize the stock symbols for further analysis, data processing, or integration into other financial applications.

## Features

- Web scraping: The script uses web scraping techniques to extract stock symbols from the Tehran Stock Exchange website.
- Symbol retrieval: It retrieves symbols for all listed stocks on the Tehran Stock Exchange.
- CSV file storage: The script saves the retrieved symbols in a CSV file for easy access and compatibility with various data processing tools.
- Customization: The script can be easily customized to retrieve additional information or data fields associated with the stock symbols, such as company names, sector classifications, or market indices.

## Prerequisites

To run the Tehran Stock Exchange Symbol Scraper, you need to have the following prerequisites installed:

- Python 3.x: Make sure you have Python 3.x installed on your system.


## csv sample

``` csv
en_symbol_12_digit_code,en_symbol_5_digit_code,company_en_name,company_4_digit_code,company_fa_name,fa_symbol_name,fa_symbol_30_digit_code,company_12_digit_code,market_flow,bord_code,industry_code,sub_industry_code,group_name,exchange_code,is_active,tsetmc_id
IRO3HORZ0001,HORZ1,Omid Taban Hoor,HORZ,مديريت انرژي اميد تابان هور,وهور   ,مديريت انرژي اميد  تابان هور,IRO3HORZ0003,بازار دوم فرابورس,3,40,4010,عرضه برق، گاز، بخاروآب گرم,3,1,25215182208950217
```