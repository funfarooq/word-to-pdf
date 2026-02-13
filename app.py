from flask import Flask, render_template, request, send_file
from docx import Document
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os
import uuid

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
PDF_FOLDER = "pdfs"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PDF_FOLDER, exist_ok=True)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/convert", methods=["POST"])
def convert():
    if "file" not in request.files:
        return "No file uploaded", 400

    file = request.files["file"]

    if file.filename == "":
        return "No selected file", 400

    if not file.filename.endswith(".docx"):
        return "Only .docx files are supported", 400

    # Unique filename
    unique_id = str(uuid.uuid4())
    docx_path = os.path.join(UPLOAD_FOLDER, unique_id + ".docx")
    pdf_path = os.path.join(PDF_FOLDER, unique_id + ".pdf")

    file.save(docx_path)

    # Extract text from Word
    document = Document(docx_path)
    full_text = []
    for para in document.paragraphs:
        full_text.append(para.text)

    # Create PDF
    c = canvas.Canvas(pdf_path, pagesize=letter)
    width, height = letter
    y = height - 40

    for line in full_text:
        c.drawString(40, y, line)
        y -= 20
        if y < 40:
            c.showPage()
            y = height - 40

    c.save()

    return send_file(pdf_path, as_attachment=True)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
