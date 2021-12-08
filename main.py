import ast
import logging
import os
import time
from datetime import date
import asyncio
import gspread_asyncio

import gspread
from dotenv import find_dotenv, load_dotenv
from google.oauth2.service_account import Credentials
from gspread_dataframe import set_with_dataframe

from get_com import get_all_com
from get_price import get_price_history

# load environment variables
load_dotenv(find_dotenv())

SHEET_KEY = os.getenv('SHEET_KEY')
service_account_info = ast.literal_eval(SHEET_KEY)
start_date = '2000-01-01'
today = date.today().strftime("%Y-%m-%d")

#logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s","%d-%m-%y %H:%M:%S")
ch.setFormatter(formatter)
logger.addHandler(ch)

scopes = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

credentials = Credentials.from_service_account_info(
    service_account_info,
    scopes=scopes
)

gc = gspread.authorize(credentials)

def auto(list_com, exchange, sheet_id):
    sh = gc.open_by_key(sheet_id)
    i = -4
    e = 2.718281
    for com in list_com:
        df = get_price_history(com, start_date, today)
        worksheet = sh.add_worksheet(title=com, rows="100", cols="4")
        worksheet = sh.worksheet(com)
        set_with_dataframe(worksheet, df, include_index=True)
        df.to_csv(f'{exchange}/{com}.csv')
        i += 0.01
        t = 1.8 - e**i
        if t>0:
            time.sleep(t)
        logger.info(f"{com} DONE!")


def get_credendital():
    credentials = Credentials.from_service_account_info(
    service_account_info,
    scopes=scopes
)
    return credentials


async def github(exchange, com_list):
    D = {}
    semaphore = asyncio.Semaphore(10)
    async def one_iteration(com):
        async with semaphore:
            logger.info(f'{com} DONE!')
            result = await get_price_history(com,'2020-10-10',today)
            result.to_csv(f'{exchange}/{com}.csv')
            D[com] = result

    coros = [one_iteration(com) for com in com_list]
    await asyncio.gather(*coros)
    return D

async def sheet(agcm, sheet_id,com_list,D):
    
    async def test(com):
        agc = await agcm.authorize()
        ss = await agc.open_by_key(sheet_id)
        # df = get_price_history(com, start_date, today)
        df = D[com]
        row = df.shape[0] +1
        # ws = await ss.add_worksheet(title=com, rows="100", cols="7")
        ws = await ss.worksheet(com)
        await ws.update(f'A1:H{row}',[df.columns.values.tolist()] + df.values.tolist())
        logger.info(f"{com} SHEET DONE!")
    coro = [test(com) for com in com_list]
    await asyncio.gather(*coro)

if __name__ == "__main__":
    cookie = ast.literal_eval(os.getenv('COOKIES'))
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36 Edg/95.0.1020.40'}

    hose_com = get_all_com('hose', cookie, header)
    hnx_com = get_all_com('hnx', cookie, header)
    upcom_com = get_all_com('upcom', cookie, header)

    HOSE_SHEET_ID = '1Br0SphvPJH5PZ0JSFtZk24dHUsR17uxIM4s38GBCAA4'
    # HNX_SHEET_ID = '1wM8UK3UbDGQJk_TkF292vYSe2OC4chxLTHVmta9D16A'
    # UPCOM_SHEET_ID = '1WAHZEe6Hgzua7izI9T3wFK7Rre1KSZVQKIG9sHGzYis'
    TEST_SHEET_ID = '1KykDw2GYpiCuJluz_TC06nECDuzHjEI5hGSmb7VSxW8'

    # auto(hose_com, 'hose', HOSE_SHEET_ID)
    # # # # auto(hnx_com, 'hnx', HNX_SHEET_ID)
    # # # # auto(upcom_com, 'upcom', UPCOM_SHEET_ID)
    # # # sh = gc.open_by_key(TEST_SHEET_ID)

    # # df = get_price_history('VCB', start_date, today)
    # # # worksheet = sh.add_worksheet(title='TEST', rows="100", cols="4")
    # # # worksheet = sh.worksheet('TEST')
    # # # worksheet.update([[42,43], [43,45]])
    # # # print([df.columns.values.tolist()])
    agcm = gspread_asyncio.AsyncioGspreadClientManager(get_credendital)
    # # for com in hose_com:
    # #     asyncio.run(test(agcm,TEST_SHEET_ID,com), debug=True)
    # # # print(df)
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(main(agcm,TEST_SHEET_ID,hose_com))
    
    # async def first():
    #     await asyncio.sleep(1)
    #     return "1"

    # async def second():
    #     await asyncio.sleep(1)
    #     return "2"
    # import pandas as pd
    # d = {'col1': [1, 2,3], 'col2': [3, 4,5]}
    # d2 = {'col1': [1, 2], 'col2': [3, 4]}
    # d3 = {'col1': [1, 2,3,4], 'col2': [3, 4,5,6]}
    
    # df = pd.DataFrame(data=d)
    # df2 = pd.DataFrame(data=d2)
    # df3 = pd.DataFrame(data=d3)
    # T = {'1':df,'2':df2,'3':df3}

    loop = asyncio.get_event_loop()
    hose = loop.run_until_complete(github('hose',hose_com))
    # hnx = loop.run_until_complete(github('hnx',hnx_com))
    # upcom = loop.run_until_complete(github('upcom',upcom_com))
    loop.run_until_complete(sheet(agcm,HOSE_SHEET_ID,hose_com,hose))
    # loop.run_until_complete(sheet(agcm,HNX_SHEET_ID,hose_com,hnx))
    # loop.run_until_complete(sheet(agcm,UPCOM_SHEET_ID,upcom_com,upcom))
    # file = open("sample2.txt", "w")
    # file.write(repr(T))
    # file.close()
    