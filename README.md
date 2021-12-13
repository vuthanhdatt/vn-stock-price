# Auto update Vietnam stock price daily

## Problem
After create my [vndata](https://github.com/vuthanhdatt/vnstock-data-python) package. I'm thinking of making data easy to access for everyone not only Python user. So I create this repo to automatically update trading data to google sheet so that user can easily access trading data for techincal analysis with another tool.

## Product
User can access daily price in 3 sperate google sheet. Each sheet contain data on one exchange. Data will be updated every day after 3pm with Github Action. Due to lots of companies on UPCOM exchange, I divide UPCOM into 2 sheet.
1. [HOSE](https://docs.google.com/spreadsheets/d/1Br0SphvPJH5PZ0JSFtZk24dHUsR17uxIM4s38GBCAA4/edit?usp=sharing)
2. [HNX](https://docs.google.com/spreadsheets/d/1wM8UK3UbDGQJk_TkF292vYSe2OC4chxLTHVmta9D16A/edit?usp=sharing)
3. [UPCOM - 1](https://docs.google.com/spreadsheets/d/11s4hdIR06O7-OFnAbENdWOo_TelKJLSTQVLurq6IGsY/edit?usp=sharing)
4. [UPCOM - 2](https://docs.google.com/spreadsheets/d/1M044GDXB380wYGG7JfmUNSGVSn4obfSera5pmUBybC8/edit?usp=sharing)

User can also access to each individual company in 3 folder [hose](https://github.com/vuthanhdatt/vn-stock-price/tree/main/hose), [hnx](https://github.com/vuthanhdatt/vn-stock-price/tree/main/hnx), [upcom](https://github.com/vuthanhdatt/vn-stock-price/tree/main/upcom) of this repository.

## Improvement
Currently, I'm calling to `google.apps.sheets.v4.SpreadsheetsService.UpdateValues` API to update value of entire sheet. 

![google-sheet-api](https://github.com/vuthanhdatt/vn-stock-price/blob/main/images/sheet-api.png)

This make requests have high latency and time to finish updating all over 1600 companies up to 3 hours although using asynchronous. 

![time-finish](https://github.com/vuthanhdatt/vn-stock-price/blob/main/images/time-finish.png)

In my calculation, with google sheet API limit 100 request/s, time can reduce to 1-1.5h to update all companies. This project is just finished and not yet optimize, in near future I will update my code.

## Update
After changing calling method, building time actually reduce.

![reduce-time](https://github.com/vuthanhdatt/vn-stock-price/blob/main/images/reduce-time.png)

