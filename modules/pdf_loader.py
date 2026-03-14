from pypdf import PdfReader

def extract_text_from_pdf(state) :
    pdf = state["resume_file"]
    reader = PdfReader(pdf)
    text = ""

    for pages in reader.pages:
        text += pages.extract_text()
    
    return {"resume_text": text}