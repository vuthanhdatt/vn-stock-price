import os
import ast
import json
import gspread
from dotenv import load_dotenv, find_dotenv
from get_price import get_price_history
from gspread_dataframe import  set_with_dataframe
from google.oauth2.service_account import Credentials

#load environment variables
load_dotenv(find_dotenv())

SHEET_KEY = os.getenv('SHEET_KEY')

scopes = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

service_account_info = ast.literal_eval(SHEET_KEY)
credentials = Credentials.from_service_account_info(
    service_account_info,
    scopes=scopes
)


df = get_price_history('HPG','01-01-2019','01-01-2021')

gc = gspread.authorize(credentials)

HSX_SHEET_KEY ='1kKnFR1qmFuEN7YNtxjWYJI0xee2uVdXcHdLHsiSTosA'
sh = gc.open_by_key(HSX_SHEET_KEY)

worksheet = sh.get_worksheet(0)
worksheet.clear()
set_with_dataframe(worksheet, df, include_index=True)