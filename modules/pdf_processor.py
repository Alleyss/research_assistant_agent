# from pdfminer.high_level import extract_text


# def extract_text_from_pdf(pdf_path):
#     text = extract_text(pdf_path)
#     return text


# # Test with a sample PDF
# text = extract_text_from_pdf("ace.pdf")
# # print(text[:1000])  # Print first 500 characters to verify

# import re

# # import spacy


# def clean_text(text):
#     # Remove headers/footers (customize based on your PDF patterns)
#     text = re.sub(r"Page \d+ of \d+", "", text)
#     text = re.sub(r"\n\s*\n", "\n", text)  # Remove empty lines
#     return text.strip()


# # Example usage:
# cleaned_text = clean_text(text)
# print(cleaned_text)


from unstructured.partition.pdf import partition_pdf


def get_pdf(file_path: str):
    elements = partition_pdf(
        filename=file_path,  # mandatory
        languages=["eng"],
        strategy="fast",  # mandatory to use ``hi_res`` strategy
        extract_images_in_pdf=True,  # mandatory to set as ``True``
        extract_image_block_types=["Image", "Table"],  # optional
        extract_image_block_to_payload=False,  # optional
        extract_image_block_output_dir="cache_files/images",  # optional - only works when ``extract_image_block_to_payload=False``
    )
    return elements
