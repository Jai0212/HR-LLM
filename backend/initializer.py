import os
import fitz

def extract_text_from_pdf(pdf_path):
    try:
        doc = fitz.open(pdf_path)
        text = ""
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            text += page.get_text()
        return text
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return ""

current_dir = os.path.dirname(__file__)
pdf_path = os.path.join(current_dir, 'data', 'file_two.pdf')
output_path = os.path.join(current_dir, 'extracted_data', 'Company_B.txt')

with open(output_path, 'w', encoding='utf-8') as text_file:
    text_file.write(extract_text_from_pdf(pdf_path))
