from PyPDF2 import PdfReader

text = ""
parts = []

# jump header
def visitor_body(text, cm, tm, font_dict, font_size):
    y = tm[5]
    if y > 50:
        parts.append(text)


try:
    reader = PdfReader("extrato.pdf")
    for page in reader.pages:
        text += page.extract_text(visitor_text=visitor_body)
        text_body = "".join(parts)
    print("[+] pdf read with success!\n")
except Exception as exc:
    print(f"[-] Error: {exc}")


print(text_body)