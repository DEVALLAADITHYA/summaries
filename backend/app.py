import os
from flask import Flask, request, jsonify, render_template, send_file
from werkzeug.utils import secure_filename
from services.pdf_service import extract_text_from_pdf
from services.ocr_service import extract_text_from_image
from services.ai_service import generate_summaries
from dotenv import load_dotenv

load_dotenv()

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')

BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'tiff', 'bmp'}

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "templates"),
    static_folder=os.path.join(BASE_DIR, "static"),
    static_url_path="/static"
    )
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024  # 20MB limit

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if not allowed_file(file.filename):
        return jsonify({'error': 'Unsupported file type'}), 400

    filename = secure_filename(file.filename)
    path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(path)

    try:
        ext = filename.rsplit('.',1)[1].lower()
        if ext == 'pdf':
            text = extract_text_from_pdf(path)
        else:
            text = extract_text_from_image(path)

        text = (text or '').strip()
        if not text:
            return jsonify({'error': 'No extractable text found'}), 400

        summaries = generate_summaries(text)
        return jsonify({'summaries': summaries})
    except Exception as e:
        return jsonify({'error': 'Processing error', 'details': str(e)}), 500
    finally:
        try:
            os.remove(path)
        except Exception:
            pass

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
