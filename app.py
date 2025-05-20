from flask import Flask, request, render_template_string, send_file
from io import BytesIO
from PyPDF2 import PdfReader
from fpdf import FPDF
from googletrans import Translator, LANGUAGES

app = Flask(__name__)

# HTML template with inline CSS
HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>PDF Translator</title>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');
    body {
      margin: 0;
      font-family: 'Poppins', sans-serif;
      background: linear-gradient(135deg, #5ee7df 0%, #b490ca 100%);
      min-height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 20px;
      color: #333;
    }
    .container {
      background: white;
      max-width: 480px;
      width: 100%;
      border-radius: 16px;
      box-shadow: 0 12px 24px rgba(0,0,0,0.15);
      padding: 40px;
      box-sizing: border-box;
      text-align: center;
    }
    h1 {
      margin-bottom: 24px;
      font-weight: 600;
      color: #6a3093;
    }
    label {
      display: block;
      text-align: left;
      margin-bottom: 8px;
      font-weight: 600;
      color: #6a3093;
    }
    input[type="file"] {
      width: 100%;
      margin-bottom: 24px;
      padding: 10px;
      border-radius: 8px;
      border: 1px solid #ccc;
      cursor: pointer;
    }
    select {
      width: 100%;
      padding: 12px;
      border-radius: 8px;
      border: 1px solid #ccc;
      margin-bottom: 24px;
      font-size: 1rem;
      color: #333;
    }
    button {
      padding: 12px 32px;
      font-weight: 600;
      font-size: 1rem;
      border: none;
      border-radius: 50px;
      background: #6a3093;
      color: white;
      cursor: pointer;
      transition: background-color 0.3s ease;
    }
    button:hover {
      background: #5b237a;
    }
    .footer {
      margin-top: 32px;
      font-size: 0.8rem;
      color: #999;
    }
    .error {
      color: transparent;
      margin-bottom: 10px;
      font-weight: 600;
    }
  </style>
</head>
<body>
  <div class="container">
    <h1>PDF Translator</h1>
    {% if error %}
      <p class="error" style="color: #e74c3c;">{{ error }}</p>
    {% endif %}
    <form action="/" method="POST" enctype="multipart/form-data">
      <label for="pdf-file">Select a PDF file to translate:</label>
      <input type="file" name="pdf_file" id="pdf-file" accept=".pdf" required />
      <label for="language">Select target language:</label>
      <select name="language" id="language" required>
        {% for code, lang in languages.items() %}
          <option value="{{ code }}" {% if code == default_lang %}selected{% endif %}>{{ lang }}</option>
        {% endfor %}
      </select>
      <button type="submit">Translate PDF</button>
    </form>
    <div class="footer">
      &copy; PDF Translator
    </div>
  </div>
</body>
</html>
"""

def extract_text_from_pdf(file_stream):
    reader = PdfReader(file_stream)
    pages_text = []
    for page in reader.pages:
        pages_text.append(page.extract_text() or "")
    return pages_text

def translate_texts(texts, target_lang):
    translator = Translator()
    translated_texts = []
    for text in texts:
        if text.strip():
            translated = translator.translate(text, dest=target_lang)
            translated_texts.append(translated.text)
        else:
            translated_texts.append("")
    return translated_texts

# def create_pdf_from_texts(texts):
#     pdf = FPDF()
#     pdf.set_auto_page_break(auto=True, margin=15)
#     pdf.set_font("Arial", size=12)
#     for text in texts:
#         pdf.add_page()
#         for line in text.split('\n'):
#             pdf.multi_cell(0, 10, line)
#     pdf_output = pdf.output(dest='S').encode('latin1')
#     return BytesIO(pdf_output)

from fpdf import FPDF
from io import BytesIO
import os

class PDF(FPDF):
    pass

def create_pdf_from_texts(texts):
    from fpdf import FPDF
from io import BytesIO
import os

def create_pdf_from_texts(texts):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_margins(10, 15, 10)
import logging

# Create a logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create a file handler and a stream handler
file_handler = logging.FileHandler('pdf_translator.log')
stream_handler = logging.StreamHandler()

# Create a formatter and set it for the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
stream_handler.setFormatter(formatter)

# Add the handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(stream_handler)

def extract_text_from_pdf(file_stream):
    try:
        reader = PdfReader(file_stream)
        pages_text = []
        for page in reader.pages:
            pages_text.append(page.extract_text() or "")
        logger.info('Text extracted from PDF')
        return pages_text
    except Exception as e:
        logger.error(f'Error extracting text from PDF: {str(e)}')
        return []

def translate_texts(texts, target_lang):
    try:
        translator = Translator()
        translated_texts = []
        for text in texts:
            if text.strip():
                translated = translator.translate(text, dest=target_lang)
                translated_texts.append(translated.text)
            else:
                translated_texts.append("")
        logger.info('Texts translated')
        return translated_texts
    except Exception as e:
        logger.error(f'Error translating texts: {str(e)}')
        return []

def create_pdf_from_texts(texts):
    try:
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.set_margins(10, 15, 10)

        font_path = "DejaVuSans.ttf"
        if not os.path.exists(font_path):
            raise RuntimeError("Font file 'DejaVuSans.ttf' not found. Please download it and place in the app directory.")

        pdf.add_font("DejaVu", "", font_path, uni=True)
        pdf.set_font("DejaVu", "", 12)

        for text in texts:
            pdf.add_page()
            for line in text.split('\n'):
                try:
                    pdf.multi_cell(190, 10, line)  # 190 width to avoid wrapping issue
                except RuntimeError as e:
                    # Fallback for very wide characters (like emojis)
                    safe_line = ''.join(c if ord(c) < 65535 else '?' for c in line)
                    pdf.multi_cell(190, 10, safe_line)

        output = pdf.output(dest='S').encode('latin1')
        logger.info('PDF created')
        return BytesIO(output)
    except Exception as e:
        logger.error(f'Error creating PDF: {str(e)}')
        return BytesIO()

@app.route('/', methods=['GET', 'POST'])
def index():
    error = None
    languages = LANGUAGES
    default_lang = 'en'
    if request.method == 'POST':
        if 'pdf_file' not in request.files:
            error = "No file part"
            logger.error('No file part')
            return render_template_string(HTML_PAGE, languages=languages, error=error, default_lang=default_lang)
        file = request.files['pdf_file']
        if file.filename == '':
            error = "No selected file"
            logger.error('No selected file')
            return render_template_string(HTML_PAGE, languages=languages, error=error, default_lang=default_lang)
        language = request.form.get('language', 'en')
        if language not in languages:
            error = "Invalid target language selected"
            logger.error('Invalid target language selected')
            return render_template_string(HTML_PAGE, languages=languages, error=error, default_lang=default_lang)
        try:
            file_stream = file.stream
            pages_text = extract_text_from_pdf(file_stream)
            if not any(pages_text):
                error = "Could not extract text from the PDF. Make sure it has selectable text."
                logger.error('Could not extract text from the PDF')
                return render_template_string(HTML_PAGE, languages=languages, error=error, default_lang=default_lang)
            translated_pages = translate_texts(pages_text, language)
            pdf_output = create_pdf_from_texts(translated_pages)
            original_filename = file.filename.rsplit('.', 1)[0]
            new_filename = f"{original_filename}_translated_{language}.pdf"
            logger.info('PDF translation successful')
            return send_file(pdf_output, as_attachment=True, download_name=new_filename, mimetype='application/pdf')
        except Exception as e:
            import traceback
            logger.error(f'Error translating PDF: {str(e)}')
            logger.error(traceback.format_exc())
            error = f"An error occurred: {str(e)}"
            return render_template_string(HTML_PAGE, languages=languages, error=error, default_lang=default_lang)
    logger.info('GET request successful')
    return render_template_string(HTML_PAGE, languages=languages, error=error, default_lang=default_lang)
    font_path = "DejaVuSans.ttf"
    if not os.path.exists(font_path):
        raise RuntimeError("Font file 'DejaVuSans.ttf' not found. Please download it and place in the app directory.")

    pdf.add_font("DejaVu", "", font_path, uni=True)
    pdf.set_font("DejaVu", "", 12)

    for text in texts:
        pdf.add_page()
        for line in text.split('\n'):
            try:
                pdf.multi_cell(190, 10, line)  # 190 width to avoid wrapping issue
            except RuntimeError as e:
                # Fallback for very wide characters (like emojis)
                safe_line = ''.join(c if ord(c) < 65535 else '?' for c in line)
                pdf.multi_cell(190, 10, safe_line)

    output = pdf.output(dest='S').encode('latin1')
    return BytesIO(output)

@app.route('/', methods=['GET', 'POST'])
def index():
    error = None
    languages = LANGUAGES
    default_lang = 'en'
    if request.method == 'POST':
        if 'pdf_file' not in request.files:
            error = "No file part"
            return render_template_string(HTML_PAGE, languages=languages, error=error, default_lang=default_lang)
        file = request.files['pdf_file']
        if file.filename == '':
            error = "No selected file"
            return render_template_string(HTML_PAGE, languages=languages, error=error, default_lang=default_lang)
        language = request.form.get('language', 'en')
        if language not in languages:
            error = "Invalid target language selected"
            return render_template_string(HTML_PAGE, languages=languages, error=error, default_lang=default_lang)
        try:
            file_stream = file.stream
            pages_text = extract_text_from_pdf(file_stream)
            if not any(pages_text):
                error = "Could not extract text from the PDF. Make sure it has selectable text."
                return render_template_string(HTML_PAGE, languages=languages, error=error, default_lang=default_lang)
            translated_pages = translate_texts(pages_text, language)
            pdf_output = create_pdf_from_texts(translated_pages)
            original_filename = file.filename.rsplit('.', 1)[0]
            new_filename = f"{original_filename}_translated_{language}.pdf"
            return send_file(pdf_output, as_attachment=True, download_name=new_filename, mimetype='application/pdf')
        except Exception as e:
            import traceback
            print(traceback.format_exc())
            error = f"An error occurred: {str(e)}"
            return render_template_string(HTML_PAGE, languages=languages, error=error, default_lang=default_lang)
    return render_template_string(HTML_PAGE, languages=languages, error=error, default_lang=default_lang)

if __name__ == '__main__':
    app.run(debug=True)