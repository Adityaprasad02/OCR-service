from fastapi import FastAPI, UploadFile
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io

app = FastAPI()

@app.post("/ocr")
async def ocr_pdf(file: UploadFile):
    pdf_bytes = await file.read()
    pdf = fitz.open(stream=pdf_bytes, filetype="pdf")
    full_text = ""

    for page_index in range(len(pdf)):
        page = pdf[page_index]
        pix = page.get_pixmap(dpi=200)
        img_bytes = pix.tobytes("png")
        img = Image.open(io.BytesIO(img_bytes))
        text = pytesseract.image_to_string(img)
        full_text += f"\n\n--- PAGE {page_index+1} ---\n{text}"

    return {"text": full_text}
