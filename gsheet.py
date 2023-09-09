import gspread 
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

# month dictionary
months = {
    "01" : "Janeiro",
    "02" : "Fevereiro",
    "03" : "Março",
    "04" : "Abril",
    "05" : "Maio",
    "06" : "Junho",
    "07" : "Julho",
    "08" : "Agosto",
    "09" : "Setembro",
    "10": "Outubro",
    "11": "Novembro",
    "12": "Dezembro"
}


def numberToLetter(value):
    return chr(65 + value - 1)

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
spreadsheet = myclient.open(spreadsheetname)
if spreadsheet == '':
    print("[-] error oppening the spreadsheet")
    exit
print("[+] spreasheet opened")

# open csv file
print(" * Write your csv file name: ")
csvname = input()
df = pd.read_csv(csvname + ".csv")

# get the column "Data"
date_column = df['Data']

# get the first item
value = date_column.iloc[0]

# divide string by '/'
parts = value.split('/')

# the second parth is the month
csv_month = parts[1]
print(csv_month)

month_name = months.get(csv_month)
print(f" * the worksheet that will be updated is {month_name}")

# open or create new worksheet
try:
    worksheet = spreadsheet.worksheet(month_name)
except Exception as exc:
    print("[-] This worksheet doesn't exist. We'll create a new worksheet")
    worksheet = spreadsheet.add_worksheet(title=month_name, rows="100", cols="10")

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
# get number of rows
n_rows = df.shape[0]
print(f' * number of row is {n_rows}')

# set the header format
worksheet.format('A1:{}'.format(
    numberToLetter(n_columns) + '1'), header_format)
print("[+] header formatted")

# data range (excluding header row)
data_range = 'A2:{}{}'.format(
    numberToLetter(n_columns), n_rows + 1)

# set the body format
print(data_range)
worksheet.format(data_range, body_format)

# data range (excluding header row)
money_range = 'B2:B{}'.format(n_rows + 1)
print(money_range)

# format to money
money_format = {
    "numberFormat": {
        "type": "CURRENCY",
        "pattern": "\"R$\"#,##0.00"
    }
}

# set the value format
worksheet.format(money_range, money_format)

print("[+] body formatted")

print("[+] spreadsheet available in google drive")