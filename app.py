from flask import Flask, render_template, request, send_file
from docx2pdf import convert
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "pdfs"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/convert", methods=["POST"])
def convert_file():
    file = request.files["file"]
    word_path = os.path.join(UPLOAD_FOLDER, file.filename)
    pdf_path = os.path.join(
        OUTPUT_FOLDER,
        file.filename.rsplit(".", 1)[0] + ".pdf"
    )

    file.save(word_path)
    convert(word_path, pdf_path)

    return send_file(pdf_path, as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
