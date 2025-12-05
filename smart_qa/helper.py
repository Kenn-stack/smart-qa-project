import json
from pathlib import Path
from docx import Document
import PyPDF2
from smart_qa.custom_exceptions import FileNotFound, FolderNotFound, UnsupportedFileType


def read_file(path) -> str:
    """reads different types of files and returns the content"""
    path = Path(path)
    if path.exists():
        suffix = path.suffix.lower()
    else:
        raise FileNotFound(f"File not found at {path}")

    # --- Text / Markdown files ---
    if suffix in [".txt", ".md"]:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    # --- DOCX files ---
    elif suffix == ".docx":
        doc = Document(path)
        return "\n".join(para.text for para in doc.paragraphs)

    # --- PDF files ---
    elif suffix == ".pdf":
        with open(path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            text = ""
            for page in reader.pages:
                text += page.extract_text() or ""
            return text

    else:
        raise UnsupportedFileType(f"Unsupported file type: {suffix}")




def save_text_to_file(path, content: str, file_type) -> None:
    """saves content to a file"""
    path = Path(path)
    if path.exists():
        if file_type == "json":
            with open(path / "output.json", "w") as f:
                json.dump(content, f, indent=2)
        else:
            with open(path / "output.txt",  "w", encoding="utf-8") as f:
                f.write(content)
    else:
        raise FolderNotFound(f"Folder not found at {path}")

            
            