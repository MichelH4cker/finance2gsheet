import gspread 
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

# setting the apis configs
try:
    myscope = ['https://spreadsheets.google.com/feeds',
               'https://www.googleapis.com/auth/drive']
    mycreds = ServiceAccountCredentials.from_json_keyfile_name('finance2gsheet-086d22416d93.json', myscope)
    myclient = gspread.authorize(mycreds)
    print("[+] credentials api OK")
except Exception as exc:
    print(f"[-] Error {exc}")
    exit

# open the spreadsheet
print(" * Write your google spreadsheet's name: ")
spreadsheetname = input()
worksheet = myclient.open(spreadsheetname).sheet1
if worksheet == '':
    print("[-] error oppening the spreadsheet")
    exit
print("[+] spreasheet opened")

# open csv file
print(" * Write your csv file name: ")
csvname = input()
df = pd.read_csv(csvname + ".csv")

# df.columns.values.toollist() take the name of columns
# df.values.tolist() take the values of all rows

# header format
header_format = {
    "backgroundColor": {
        "red": 49.0 / 255.0,
        "green": 119.0 / 255.0,
        "blue": 115.0 / 255.0
    },
    "horizontalAlignment": "CENTER",
    "textFormat": {
        "foregroundColor": {
            "red": 1.0,
            "green": 1.0,
            "blue": 1.0
        },
        "fontSize": 14,
        "bold": True
    }
}

body_format = {
    "backgroundColor":{
        "red": 176.0 / 255.0,
        "green": 164.0 / 255.0,
        "blue": 217.0 / 255.0,
    },
    "horizontalAlignment": "CENTER",
    "textFormat": {
        "bold": False,
        "foregroundColor": {
            "red": 0.0,
            "green": 0.0,
            "blue": 0.0
        },
        "fontSize": 12
    }
}

# put all datas in the worksheet
worksheet.update([df.columns.values.tolist()] + df.values.tolist(), value_input_option='USER_ENTERED')
print("[+] data sended to spreadsheet")

# get number of columns
n_columns = df.columns.size
print(f' * number of columns is {n_columns}')
# geet number of rows
n_rows = df.shape[0]
print(f' * number of row is {n_rows}')

# set the header format
worksheet.format('A1:{}'.format(chr(65 + n_columns - 1) + '1'), header_format)
print("[+] header formatted")

# data range (excluding header row)
data_range = 'A2:{}{}'.format(chr(65 + n_columns - 1), n_rows + 1)

# set the body format
worksheet.format(data_range, body_format)
print("[+] body formatted")

print("[+] spreadsheet available in google drive")