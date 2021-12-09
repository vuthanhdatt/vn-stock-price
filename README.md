# Auto update Vietnam stock price daily

## Problem
After long time looking for stock data, I realize it's not too easy to access Vietnam stock data, at least with Python. I create this project in order to centralize Vietnam stock data, which specific to only trading data([OCHLV](https://en.wikipedia.org/wiki/Open-high-low-close_chart)). For more hand-on package, visit my [vndata](https://github.com/vuthanhdatt/vnstock-data-python) package.

## Product
User can access daily price in 3 sperate google sheet. Each sheet contain data on one exchange. Data will be updated every day after 3pm with Github Action.
1. [HOSE](https://docs.google.com/spreadsheets/d/1Br0SphvPJH5PZ0JSFtZk24dHUsR17uxIM4s38GBCAA4/edit?usp=sharing)
2. [HNX](https://docs.google.com/spreadsheets/d/1wM8UK3UbDGQJk_TkF292vYSe2OC4chxLTHVmta9D16A/edit?usp=sharing)
3. [UPCOM](https://docs.google.com/spreadsheets/d/1WAHZEe6Hgzua7izI9T3wFK7Rre1KSZVQKIG9sHGzYis/edit?usp=sharing)

User can access to each individual company in 3 folder [hose](https://github.com/vuthanhdatt/vn-stock-price/tree/main/hose), [hnx](https://github.com/vuthanhdatt/vn-stock-price/tree/main/hnx), [upcom](https://github.com/vuthanhdatt/vn-stock-price/tree/main/upcom) of this repository.

## Improvement
Currently, I'm calling to `google.apps.sheets.v4.SpreadsheetsService.UpdateValues` API to update value of entire sheet. 
![google sheet api](https://github.com/vuthanhdatt/vn-stock-price/blob/main/images/sheet-api.png)
This make requests have high latency and time to finish updating all over 1600 companies up to 3 hours although using asynchronous. 
![time finish](https://github.com/vuthanhdatt/vn-stock-price/blob/main/images/time-finish.png)
In my calculation, with google sheet API limit 100 request/s, time can reduce to 1-1.5h to update all companies. This project is just finished and not yet optimize, in near future I will update my code.