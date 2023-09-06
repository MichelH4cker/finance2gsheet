from PyPDF2 import PdfReader

text = ""
try:
    reader = PdfReader("extrato.pdf")
    for page in reader.pages:
        text += page.extract_text()
    print("[+] pdf read with success!\n")
except Exception as exc:
    print(f"[-] Error: {exc}")


print(text)