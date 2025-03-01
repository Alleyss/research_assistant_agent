from unstructured.partition.pdf import partition_pdf


def get_pdf_elements(file_path: str):
    elements = partition_pdf(
        filename=file_path,  # mandatory
        languages=["eng"],
        chunking_strategy='by_title',
        strategy="fast",  # mandatory to use ``hi_res`` strategy
        extract_images_in_pdf=True,  # mandatory to set as ``True``
        extract_image_block_types=["Image", "Table"],  # optional
        extract_image_block_to_payload=False,  # optional
        extract_image_block_output_dir="cache_files/images",  # optional - only works when ``extract_image_block_to_payload=False``
    )
    return elements
