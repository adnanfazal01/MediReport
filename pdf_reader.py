import PyPDF2


def extract_text_from_pdf(uploaded_file):
    """
    Extract readable text from an uploaded PDF file.
    """

    pdf_reader = PyPDF2.PdfReader(uploaded_file)

    extracted_text = ""

    for page in pdf_reader.pages:
        page_text = page.extract_text()

        if page_text:
            extracted_text += page_text + "\n"

    return extracted_text