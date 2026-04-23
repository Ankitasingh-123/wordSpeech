import os

def read_file(filepath):
    try:
        ext = os.path.splitext(filepath)[1].lower()

        # TXT
        if ext == ".txt":
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    return f.read()
            except:
                with open(filepath, "r", encoding="latin-1") as f:
                    return f.read()

        # PDF
        elif ext == ".pdf":
            import PyPDF2
            text = ""
            with open(filepath, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    text += page.extract_text() or ""
            return text

        # DOCX
        elif ext == ".docx":
            import docx
            doc = docx.Document(filepath)
            return "\n".join([p.text for p in doc.paragraphs])

        else:
            return "Unsupported file type!"

    except Exception as e:
        return f"Error: {str(e)}"