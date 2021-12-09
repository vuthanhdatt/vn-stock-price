import pandas as pd
import aiohttp

def make_price_history_form(symbol, start, end):
    '''
    Making form to requests to market_price_url

    Paramaters
    ----------
    symbol: string, company symbol
    start: starting date
    end: ending date

    Retruns
    -------
    dict
    '''

    form = {'Code': symbol,
            'OrderBy': '',
            'OrderDirection': 'desc',
            'FromDate': start,
            'ToDate': end,
            'ExportType': 'excel',
            'Cols': 'MC,DC,CN,TN,GDC,TKLGD',
            'ExchangeID': 1}

    return form


def make_price_history_df(df):
    '''
    Formating price df 

    Paramaters
    ----------
    df: DataFrame, df reading from price_history_url

    Return
    ------
    DataFrame

    '''
    cols = ['Date', 'Volume', 'Open', 'Close', 'High',
           'Low', 'Adj Close']
    df.columns = cols
    # df = df.set_index('Date')
    df = df.reindex(['Date','High', 'Low', 'Open', 'Close', 'Volume',
                    'Adj Close',], axis='columns')
    df = df.reindex(index=df.index[::-1])
    df.reset_index(inplace=True, drop=True)
    df.fillna('-', inplace=True)
    return df
async def get_price_history(symbol,start,end):

    '''
    Take price history of specific company from start to end, coming with user cookies.

    Paramaters
    ----------
    symbol: string, company symbol, etc. 'fts', 'hpg'...
    start: string, starting date
    end: string, ending date
    cookies: dict, user cookies
    
    Return
    ------
    DataFrame
    '''
    url = 'https://finance.vietstock.vn/data/ExportTradingResult'
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36 Edg/95.0.1020.40'}
    form = make_price_history_form(symbol,start,end)
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, data=form) as response:
            html = await response.text()
            df = pd.read_html(html)[1]
            result = make_price_history_df(df)    
    return result
    # url = 'https://finance.vietstock.vn/data/ExportTradingResult'
    # headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36 Edg/95.0.1020.40'}
    # form = make_price_history_form(symbol,start,end)
    # r = requests.get(url, headers= headers, data=form)
    # df = pd.read_html(r.text)[1]
    # result = make_price_history_df(df)    
    # return result

if __name__ == '__main__':
    # loop = asyncio.get_event_loop()
    # a = loop.run_until_complete(get_price_history('VCB','2020-01-01','2021-01-01'))
    # print(a)
    # # print([a.values.tolist()[0]])
    # def value(df):
    #     row = df.shape[0] +1
    #     l = []
    #     for i in range(1,row,1):
    #         d = {}
    #         d['range'] = f'A{i}:G{i}'
    #         d['values'] = [df.values.tolist()[i-1]]
    #         l.append(d)
    #     return l
    # print(value(a))
    pass