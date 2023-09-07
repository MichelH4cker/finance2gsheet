import gspread 
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

# setting the apis configs
myscope = ['https://spreadsheets.google.com/feeds',
           'https://www.googleapis.com/auth/drive']
mycreds = ServiceAccountCredentials.from_json_keyfile_name('finance2gsheet-086d22416d93.json', myscope)
myclient = gspread.authorize(mycreds)

# open the spreadsheet
worksheet = myclient.open("Finanças").sheet1

# open csv file
df = pd.read_csv("extrato.csv")

print([df.columns.values.tolist()])

# df.columns.values.toollist() take the name of columns
# df.values.tolist() take the values of all rows

# update the worksheet
worksheet.update([df.columns.values.tolist()] + df.values.tolist())