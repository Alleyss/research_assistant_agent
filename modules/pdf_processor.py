from pdfminer.high_level import extract_text

def extract_text_from_pdf(pdf_path):
    text = extract_text(pdf_path)
    return text

# Test with a sample PDF
text = extract_text_from_pdf("ace.pdf")
#print(text[:1000])  # Print first 500 characters to verify

import re
import spacy
0
def clean_text(text):
    # Remove headers/footers (customize based on your PDF patterns)
    text = re.sub(r'Page \d+ of \d+', '', text)
    text = re.sub(r'\n\s*\n', '\n', text)  # Remove empty lines
    return text.strip()

# Example usage:
cleaned_text = clean_text(text)
# print(cleaned_text)