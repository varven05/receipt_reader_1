from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from PIL import Image
import pytesseract
import re
import io
from datetime import datetime

app = FastAPI()

@app.post("/extract-receipt/")
async def extract_receipt(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        text = pytesseract.image_to_string(image)

        lines = [line.strip() for line in text.splitlines() if line.strip()]

        # Assume the first non-empty, non-numeric line is the store name
        store = "Unknown"
        for line in lines:
            if not line.isdigit():
                store = line
                break

        # Find all prices and assume the highest is the total
        prices = re.findall(r'\$?\s?(\d{1,3}(?:,\d{3})*\.\d{2})', text)
        total = max((float(p.replace(',', '')) for p in prices), default=None)
        total = f"{total:.2f}" if total is not None else "Unknown"

        # Try to extract a date MM/DD/YYYY
        date = "Unknown"
        pattern = r'\d{2}/\d{2}/\d{4}'  # matches dates like 09/22/2024
        match = re.search(pattern, text)
        if match:
            try:
                date_obj = datetime.strptime(match.group(), '%m/%d/%Y')
                date = str(date_obj.date())
            except ValueError:
                date = "Unknown"

        return {
            "store": store,
            "total_amount": total,
            "date": date
        }

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
