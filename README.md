Document Summary Assistant (Flask)

This project matches the client's requirements:
- Upload PDF or image files (file picker + drag & drop)
- Extract text from PDFs (pdfminer.six) and images (pytesseract)
- Generate smart summaries (short, medium, long) and key points using Gemini/OpenAI-compatible API
- Clean, production-quality code with error handling and loading states
- Simple responsive UI

Setup (local):
1. Install system dependency: Tesseract OCR (required for pytesseract)
   - Ubuntu: sudo apt-get install tesseract-ocr
   - macOS (Homebrew): brew install tesseract

2. Backend:
   cd backend
   python3 -m venv venv
   source venv/bin/activate   (Windows: venv\Scripts\activate)
   pip install -r requirements.txt
   copy .env.example to .env and set GEMINI_API_KEY
   python app.py

3. Open http://localhost:5000 in your browser.

Notes:
- The ai_service uses a placeholder endpoint compatible with OpenAI Chat Completions. Replace endpoint/model per your Gemini details.
- .env.example is provided in backend/.env.example
- The app removes uploaded files after processing.
