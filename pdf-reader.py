from PyPDF2 import PdfReader
import csv

text = ""
parts = []

csv_data = []

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

lines = cleaner_lines

