##Not yet working for pdf uploads..some documents have issues
import io
import PyPDF2
import docx2txt

def extract_text_from_file(file):
    """
    Extract text from various file formats (PDF, DOCX, TXT)
    
    Args:
        file: The uploaded file object
        
    Returns:
        str: Extracted text from the file
    """
    file_type = file.type
    
    if file_type == "application/pdf":
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        return docx2txt.process(file)
    else:
        return io.StringIO(file.getvalue().decode("utf-8")).read()
    
if __name__=='__main__':
    print(extract_text_from_file('resume.pdf'))