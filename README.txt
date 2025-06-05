Recipt Scanner:
- A Python API that reads a photo of a recipt and extracts information from it

Requirements:
- Python
- Tesseract OCR (https://github.com/tesseract-ocr/tesseract)
- run pip install -r requirements.txt

Running the API:
- Start the server with: uvicorn main:app --reload

How to Use:
- Send a POST request to /extract-receipt/
- Upload an image of a receipt
- Program returns JSON like:

{
  "store": "Walmart",
  "total_amount": "32.50",
  "date": "2024-09-22"
}