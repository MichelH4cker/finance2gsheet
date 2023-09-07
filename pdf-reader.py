from PyPDF2 import PdfReader
import csv
import re

text = ""
parts = []

# jump header
def visitor_body(text, cm, tm, font_dict, font_size):
    y = tm[5]
    if y > 50:
        parts.append(text)

# simply read the pdf
try:
    reader = PdfReader("extrato.pdf")
    for page in reader.pages:
        text += page.extract_text(visitor_text = visitor_body)
        text_body = "".join(parts)
    print("[+] pdf read with success!\n")
except Exception as exc:
    print(f"[-] Error: {exc}")

# break the text into lines in a array
lines = text_body.split('\n')

# delete unnecessary data
cleaner_lines = []
for line in lines:
    if "Informações Adicionais" in line:  
        break
    cleaner_lines.append(line)
    #print(line)
lines = cleaner_lines

# create filters 
#  DD/MM/AAAA ou DD-MM-AAAA
date_pattern = r'\d{2}/\d{2}/\d{4}'
time_pattern = r'\d{2}:\d{2}'
money_pattern = r'\d{1},\d{2}|\d{2},\d{2}|\d{3},\d{2}|\d{1}.\d{3},\d{2}'
transaction_pattern = r'\(\+\)|\(\-\)'

description_line = False

csv_data = []
csv_filename = "extrato.csv"
with open(csv_filename, mode='w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)

    # csv header
    header = ["Data", "Valor", "Tipo de Transação", "Descrição", "Tipo de Serviço"]
    csv_writer.writerow(header)

    # read the entire data text
    for line in range(0, len(lines)):
        if description_line:
            time_matches = ''.join(re.findall(time_pattern, lines[line])).strip()

            # find the time position
            time_start = lines[line].find(time_matches)
            # take text after time
            service_type = lines[line][time_start + len(time_matches):].strip()

            row.append(service_type)
            csv_writer.writerow(row)

            description_line = False

        date_matches = ''.join(re.findall(date_pattern, lines[line])).strip()
        if (date_matches == ''):
            continue

        money_matches = ''.join(re.findall(money_pattern, lines[line])).strip()

        transaction_type_matches = ''.join(re.findall(transaction_pattern, lines[line])).strip()

        # find the date position
        date_start = lines[line].find(date_matches)
        # take text after date
        transaction_description = lines[line][date_start + len(date_matches):].strip()

        # create a matrix of datas
        row = [date_matches, money_matches, transaction_type_matches, transaction_description]

        # if transaction_description is some of these cases, the program will work differently in the next iteration, that's because the pdf data lines are poorly formulated
        if "Estorno de Débito" in transaction_description or "Saldo Anterior" in transaction_description:  
            row.append("- - -")
            csv_writer.writerow(row)
            continue
        else: 
            description_line = True

print("[+] csv file created")