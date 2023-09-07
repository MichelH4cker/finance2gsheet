import gspread 
from oauth2client.service_account import ServiceAccountCredentials

myscope = ['https://spreadsheets.google.com/feeds',
           'https://www.googleapis.com/auth/drive']

mycreds = ServiceAccountCredentials.from_json_keyfile_name()