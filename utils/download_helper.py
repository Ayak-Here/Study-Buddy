from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import tempfile


def generate_pdf(text):
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")

    doc = SimpleDocTemplate(temp_file.name)
    styles = getSampleStyleSheet()
    story = []

    for para in text.split("\n"):
        if para.strip():
            story.append(Paragraph(para, styles["Normal"]))

    doc.build(story)

    return temp_file.name