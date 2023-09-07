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

# df.columns.values.toollist() take the name of columns
# df.values.tolist() take the values of all rows

# header format
header_format = {
    "textFormat": {
        "bold": True
    }
}

body_format = {
    "textFormat": {
        "bold": False,
        "foregroundColor": {
            "red": 0.0,
            "green": 0.0,
            "blue": 1.0
        }
    }
}

worksheet.update([df.columns.values.tolist()] + df.values.tolist(), value_input_option='USER_ENTERED')

# get number of columns
n_columns = df.columns.size
print(f'number of columns is {n_columns}')
n_rows = df.shape[0]
print(f'number of row is {n_rows}')

# set the header formatting in sheet
worksheet.format('A1:{}'.format(chr(65 + n_columns - 1) + '1'), header_format)

    # Define o intervalo das células de dados (excluindo o cabeçalho)
data_range = 'A2:{}{}'.format(chr(65 + n_columns - 1), n_rows + 1)

# Formato para as células de dados (exceto o cabeçalho)
data_format = {
    "textFormat": {
        "bold": False,
        "foregroundColor": {
            "red": 1.0,
            "green": 0.0,
            "blue": 0.0
        }
    }
}

# Aplica o formato às células de dados
worksheet.format(data_range, data_format)