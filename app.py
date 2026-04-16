from flask import Flask, render_template, request
import os
import PyPDF2
from docx import Document

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def extract_text(filepath):
    text = ""

    if filepath.endswith('.pdf'):
        with open(filepath, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                if page.extract_text():
                    text += page.extract_text()

    elif filepath.endswith('.docx'):
        doc = Document(filepath)
        for para in doc.paragraphs:
            text += para.text

    return text.lower()


@app.route('/')
def home():
    return render_template('index.html')   # ✅ FIXED


@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['resume']

    if file:
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

        text = extract_text(filepath)

        # Simple scoring logic
        keywords = ["python", "java", "html", "css", "sql"]
        score = sum(1 for word in keywords if word in text) * 20

        suggestions = []
        for word in keywords:
            if word not in text:
                suggestions.append(f"Add {word} skill")

        return render_template('result.html', score=score, suggestions=suggestions)

    return "File upload failed"


if __name__ == '__main__':
    app.run(debug=True)