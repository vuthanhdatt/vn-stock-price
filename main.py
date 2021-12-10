import ast
import logging
import os
from datetime import date
import asyncio
import gspread_asyncio

from dotenv import find_dotenv, load_dotenv
from google.oauth2.service_account import Credentials

from get_com import get_all_com
from get_price import get_price_history

# load environment variables
load_dotenv(find_dotenv())

SHEET_KEY = os.getenv('SHEET_KEY')
service_account_info = ast.literal_eval(SHEET_KEY)
start_date = '2000-01-01'
today = date.today().strftime("%Y-%m-%d")

########### FOR LOGGING ##############
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s","%d-%m-%y %H:%M:%S")
ch.setFormatter(formatter)
logger.addHandler(ch)

########### FOR AUTHENTIC #############
scopes = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

credentials = Credentials.from_service_account_info(
    service_account_info,
    scopes=scopes
)
########### SYNCHRONOUS FUNCTION ############
#REMOVE

# gc = gspread.authorize(credentials)

# def auto(list_com, exchange, sheet_id):
#     sh = gc.open_by_key(sheet_id)
#     i = -4
#     e = 2.718281
#     for com in list_com:
#         df = get_price_history(com, start_date, today)
#         worksheet = sh.add_worksheet(title=com, rows="100", cols="4")
#         worksheet = sh.worksheet(com)
#         set_with_dataframe(worksheet, df, include_index=True)
#         df.to_csv(f'{exchange}/{com}.csv')
#         i += 0.01
#         t = 1.8 - e**i
#         if t>0:
#             time.sleep(t)
#         logger.info(f"{com} DONE!")


def get_credendital():
    credentials = Credentials.from_service_account_info(
    service_account_info,
    scopes=scopes
)
    return credentials

############# FOR USING UPDATE ON GITHUB ############
async def github(exchange, com_list):
    '''
    Async requests to data source to upload to Github, return dict of DataFrame
    to use in gsheet requests
    '''
    df_dict = {}
    semaphore = asyncio.Semaphore(10)
    async def single_file(com):
        async with semaphore:
            logger.info(f'{com, exchange} DONE!')
            result = await get_price_history(com,start_date,today)
            result.to_csv(f'{exchange}/{com}.csv')
            df_dict[com] = result

    coros = [single_file(com) for com in com_list]
    await asyncio.gather(*coros)
    return df_dict

######### FOR USING BATCH_UPDATE #############   
#CURRENTLY NOT USING
# def value(df):
#     row = df.shape[0] +1
#     l = []
#     for i in range(1,row,1):
#         d = {}
#         d['range'] = f'A{i}:G{i}'
#         d['values'] = [df.values.tolist()[i-1]]
#         l.append(d)
#     return l

######## FOR UPDATING ON GOOGLE SHEET #######
async def sheet(agcm, sheet_id,com_list,df_dict,entire=False):
    agc = await agcm.authorize()
    ss = await agc.open_by_key(sheet_id)

    async def entire_single_sheet(com):
        df = df_dict[com]
        # value_update = value(df)
        row = df.shape[0] +1
        try:
            ws = await ss.worksheet(com)
            logger.info(f'SHEET AWAIT {com}')
        except:
            ws = await ss.add_worksheet(title=com, rows="1000", cols="7")
            logger.info(f'SHEET ADD {com}')

        await ws.update(f'A1:H{row}',[df.columns.values.tolist()] + df.values.tolist())
        logger.info(f"UPDATE {com} SHEET DONE!")

    async def one_row_single_sheet(com):
        df= df_dict[com]
        row = df.shape[0] +1
        try:
            ws = await ss.worksheet(com)
            logger.info(f'SHEET AWAIT {com}')
        except:
            ws = await ss.add_worksheet(title=com, rows="1000", cols="7")
            logger.info(f'SHEET ADD {com}')
        await ws.batch_update([{'range':f'A{row}:H{row}','values':[df.values.tolist()[-1]]}])
        logger.info(f"UPDATE {com} SHEET DONE!")


    if entire:
        coros = [entire_single_sheet(com) for com in com_list]
    else:
        coros = [one_row_single_sheet(com) for com in com_list]
    await asyncio.gather(*coros)

######### ADD ROWS ########
async def add_rows(agcm, sheet_id,com_list, num_rows):
    agc = await agcm.authorize()
    ss = await agc.open_by_key(sheet_id)

    async def single_sheet(com):
        try:
            ws = await ss.worksheet(com)
            logger.info(f'SHEET AWAIT {com}')
        except:
            ws = await ss.add_worksheet(title=com, rows="100", cols="7")
            logger.info(f'SHEET ADD {com}')

        await ws.add_rows(num_rows)
        logger.info(f"ADD {num_rows} ROWS {com} SHEET!")

    coros = [single_sheet(com) for com in com_list]
    await asyncio.gather(*coros)

########## REMOVE SHEET #############
async def remove_sheet(agcm, sheet_id,com_list):
    agc = await agcm.authorize()
    ss = await agc.open_by_key(sheet_id)

    async def single_sheet(com):
        try:
            ws = await ss.worksheet(com)
            logger.info(f'SHEET AWAIT {com}')
            await ss.del_worksheet(ws)
            logger.info(f"DELETE {com} SHEET!")
        except:
            pass

    coros = [single_sheet(com) for com in com_list]
    await asyncio.gather(*coros)

if __name__ == "__main__":
    cookie = ast.literal_eval(os.getenv('COOKIES'))
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36 Edg/95.0.1020.40'}

    hose_com = get_all_com('hose', cookie, header)
    logger.info('Load all com hose')
    hnx_com = get_all_com('hnx', cookie, header)
    logger.info('Load all com hnx')
    upcom_com = get_all_com('upcom', cookie, header)
    upcom_com_1 = upcom_com[:int(len(upcom_com)/2)]
    upcom_com_2 = upcom_com[int(len(upcom_com)/2):]
    logger.info('Load all com upcom')

    HOSE_SHEET_ID = '1Br0SphvPJH5PZ0JSFtZk24dHUsR17uxIM4s38GBCAA4'
    HNX_SHEET_ID = '1wM8UK3UbDGQJk_TkF292vYSe2OC4chxLTHVmta9D16A'
    UPCOM_SHEET_ID_1 = '11s4hdIR06O7-OFnAbENdWOo_TelKJLSTQVLurq6IGsY'
    UPCOM_SHEET_ID_2 = '1M044GDXB380wYGG7JfmUNSGVSn4obfSera5pmUBybC8'

    # TEST_SHEET_ID = '1KykDw2GYpiCuJluz_TC06nECDuzHjEI5hGSmb7VSxW8'

    agcm = gspread_asyncio.AsyncioGspreadClientManager(get_credendital, reauth_interval=20)
    loop = asyncio.get_event_loop()

    # test_com = ['AAA','AAM','AAT','ABS']
    # test_df_dict = loop.run_until_complete(github('hose',test_com))
    hose_df_dict = loop.run_until_complete(github('hose',hose_com))
    hnx_df_dict = loop.run_until_complete(github('hnx',hnx_com))
    upcom_df_dict = loop.run_until_complete(github('upcom',upcom_com))

    # loop.run_until_complete(sheet(agcm,TEST_SHEET_ID,test_com,test_df_dict))
    loop.run_until_complete(sheet(agcm,HOSE_SHEET_ID,hose_com,hose_df_dict))
    loop.run_until_complete(sheet(agcm,HNX_SHEET_ID,hnx_com,hnx_df_dict))
    loop.run_until_complete(sheet(agcm,UPCOM_SHEET_ID_1,upcom_com_1,upcom_df_dict))
    loop.run_until_complete(sheet(agcm,UPCOM_SHEET_ID_2,upcom_com_2,upcom_df_dict))

    # loop.run_until_complete(add_rows(agcm,HOSE_SHEET_ID,hose_com,500))
    # loop.run_until_complete(add_rows(agcm,HNX_SHEET_ID,hnx_com,500))
    # loop.run_until_complete(add_rows(agcm,UPCOM_SHEET_ID_1,upcom_com_1,500))
    # loop.run_until_complete(remove_sheet(agcm, UPCOM_SHEET_ID_1,upcom_com_2))
    # loop.run_until_complete(add_rows(agcm,UPCOM_SHEET_ID_2,upcom_com_2,500))


