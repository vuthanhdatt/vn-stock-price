import os
import ast
import gspread
import time
from dotenv import load_dotenv, find_dotenv
from get_price import get_price_history
from gspread_dataframe import set_with_dataframe
from google.oauth2.service_account import Credentials
from get_com import get_all_com
from datetime import date


# load environment variables
load_dotenv(find_dotenv())

# SHEET_KEY = os.getenv('SHEET_KEY')
# service_account_info = ast.literal_eval(SHEET_KEY)
start_date = '2000-01-01'
today = date.today().strftime("%Y-%m-%d")

# scopes = [
#     'https://www.googleapis.com/auth/spreadsheets',
#     'https://www.googleapis.com/auth/drive'
# ]

# credentials = Credentials.from_service_account_info(
#     service_account_info,
#     scopes=scopes
# )

# gc = gspread.authorize(credentials)

def auto(list_com, exchange, sheet_id):
    # sh = gc.open_by_key(sheet_id)
    for com in list_com:
        df = get_price_history(com, start_date, today)
        # worksheet = sh.add_worksheet(title=com, rows="100", cols="4")
        # worksheet = sh.worksheet(com)
        # set_with_dataframe(worksheet, df, include_index=True)
        df.to_csv(f'{exchange}/{com}.csv')
        # time.sleep(1.8)


if __name__ == "__main__":
    cookie = ast.literal_eval(os.getenv('COOKIES'))
    header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36 Edg/95.0.1020.40'}

    hose_com = get_all_com('hose', cookie, header)
    hnx_com = get_all_com('hnx', cookie, header)
    upcom_com = get_all_com('upcom',cookie,header)

    HOSE_SHEET_ID = '12VgHndPoEwJzS0G1qvDeXbmspqvK7xyCDanuTmK_xx8'
    HNX_SHEET_ID = '189L98z5PEXTuHfeIeQV0C-ZX09joZcNmfoBtj1fF6xc'
    UPCOM_SHEET_ID = '1nKGCSeOFq36HHu-DK0YTFBX02wl2z6k2t1Hc5ApxNvA'

    auto(hose_com,'hose',HOSE_SHEET_ID)
    auto(hnx_com,'hnx',HNX_SHEET_ID)
    auto(upcom_com,'upcom',UPCOM_SHEET_ID)

    
    


