
# *Document Summaries – AI-Powered Document Summarization Tool*

A web application that allows users to upload *PDF files or images* and automatically generates smart summaries using *Google Gemini AI*. The application supports PDF text extraction, image OCR, multiple summary lengths, and provides a clean, responsive UI.

🌐 *Live Application:*
👉 [https://document-summaries.onrender.com/](https://document-summaries.onrender.com/)

---

## *Features*

* 📄 *Upload PDF Documents*
* 🖼 *Upload Images (OCR Supported)*
* 🔍 *Accurate Text Extraction*
* 🤖 *Summarization using Google Gemini API*
* 📏 *Choose Summary Length* (Short, Medium, Long)
* 📱 *Mobile-Responsive Interface*
* ⚡ *Loading States & Error Handling*
* 🐳 *Dockerized Backend*
* ☁ *Deployed on Render*

---

## *Tech Stack*

### *Frontend*

* HTML, CSS, JavaScript
* Responsive UI

### *Backend*

* Flask (Python)
* pdfminer.six for PDF parsing
* Tesseract OCR for image text extraction
* Google Gemini API for summarization
* Docker for containerization

---

## *Local Setup Instructions*

### *1. Clone the repository*

sh
git clone https://github.com/DEVALLAADITHYA/summaries.git
cd Document_Summaries


### **2. Create and configure .env**

Create a file named .env in the backend folder:


GEMINI_API_KEY=your_api_key_here


### *3. Install dependencies*

sh
pip install -r backend/requirements.txt


### *4. Run the application*

sh
python backend/app.py


The app will be available at:


http://127.0.0.1:5000


---

## *Deployment on Render (Steps Used in This Project)*

### *1. Create a new Web Service*

* Go to [https://dashboard.render.com/](https://dashboard.render.com/)
* Click *New → Web Service*
* Connect your GitHub repo

### *2. Select the repository*

Choose *Document_Summaries*

### *3. Configure Render settings*

* *Environment:* Docker
* *Root Directory:* / (repository root)
* *Dockerfile Path:* backend/Dockerfile
* *Instance Type:* Free
* *Region:* Any
* *Branch:* main

### *4. Add Environment Variables*

Go to *Environment → Add Variable*:


GEMINI_API_KEY=your_api_key_here


### *5. Deploy*

Render will:

* Build the Docker image
* Install dependencies
* Expose the app on port 8080
* Host it at your live URL

---

## *Project Structure*


backend/
│── app.py
│── requirements.txt
│── Dockerfile
│── templates/
│    └── index.html
│── static/
     ├── styles.css
     └── app.js
│── services/
     ├── ocr_service.py
     └── pdf_service.py


---

## *Live Demo*

💻 Try the working deployed app here:
👉 **[https://document-summaries.onrender.com/](https://document-summaries.onrender.com/)**


<img width="1896" height="913" alt="image" src="https://github.com/user-attachments/assets/bb059491-31d1-4d11-b81e-2d99f4da1edd" />





---

## *Author*

*DEVALLA ADITHYA*

