import os
import ast
import gspread
import time
from dotenv import load_dotenv, find_dotenv
from get_price import get_price_history
from gspread_dataframe import  set_with_dataframe
from google.oauth2.service_account import Credentials
from get_com import get_all_com
from datetime import date


#load environment variables
load_dotenv(find_dotenv())

SHEET_KEY = os.getenv('SHEET_KEY')
COOKIES = os.getenv('COOKIES')

header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36 Edg/95.0.1020.40'}

scopes = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]
today = date.today().strftime("%m-%d-%Y")
start_date = '01-01-2000'


service_account_info = ast.literal_eval(SHEET_KEY)
credentials = Credentials.from_service_account_info(
    service_account_info,
    scopes=scopes
)
cookie = ast.literal_eval(COOKIES)
com_list = get_all_com('hose',cookie,header)
gc = gspread.authorize(credentials)
HSX_SHEET_ID ='1kKnFR1qmFuEN7YNtxjWYJI0xee2uVdXcHdLHsiSTosA'
sh = gc.open_by_key(HSX_SHEET_ID)

for com in com_list:
    df = get_price_history(com,start_date,today)
    worksheet = sh.add_worksheet(title=com, rows="5000", cols="10")
    worksheet = sh.worksheet(com)
    set_with_dataframe(worksheet, df, include_index=True)
    time.sleep(3)
    






if __name__ == "__main__":
    pass
    # print(get_all_com("hose",cookie,header))
