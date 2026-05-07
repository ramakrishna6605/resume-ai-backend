from PyPDF2 import PdfReader

def extract_text_from_pdf(file):
    try:
        reader = PdfReader(file)
        text = ""

        for page in reader.pages:
            text += page.extract_text() or ""

        return text

    except Exception as e:
        print("PDF ERROR:", str(e))
        return ""