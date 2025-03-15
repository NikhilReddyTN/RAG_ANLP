import os
import json
from pypdf import PdfReader


pdf_dir = "/scraping_code/tax"  
output_file = "tax.json"

pdf_data = {}


for filename in os.listdir(pdf_dir):
    if filename.lower().endswith(".pdf"):
        pdf_path = os.path.join(pdf_dir, filename)
        print(f"Processing: {pdf_path}")
        try:
            reader = PdfReader(pdf_path)
        except Exception as e:
            print(f"Failed to read {filename}: {e}")
            continue

        pages_text = {}
        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            pages_text[f"page_{i+1}"] = text.strip() if text else ""
        pdf_data[filename] = pages_text


with open(output_file, "w", encoding="utf-8") as f:
    json.dump(pdf_data, f, ensure_ascii=False, indent=4)

print(f"All PDF content saved to {output_file}")
