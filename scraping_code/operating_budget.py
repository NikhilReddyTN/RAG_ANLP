import json
from pypdf import PdfReader


pdf_file_path = "/scraping_code/23255_2024_Operating_Budget.pdf"
reader = PdfReader(pdf_file_path)
pdf_text = {}
for i, page in enumerate(reader.pages):
    text = page.extract_text()
    pdf_text[f"page_{i+1}"] = text.strip() if text else ""
output_file = "operating_budget.json"
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(pdf_text, f, ensure_ascii=False, indent=4)
