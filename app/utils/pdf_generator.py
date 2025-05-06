# utils/pdf_generator.py
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import io
import os
from django.conf import settings

def generate_user_predictions_pdf(predictions, username):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    y = height - 50

    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, y, f"{username}'s Prediction Report")
    y -= 30

    for prediction in predictions:
        if y < 150:
            p.showPage()
            y = height - 50

        # Image
        image_path = os.path.join(settings.MEDIA_ROOT, prediction.image.name)
        try:
            img = ImageReader(image_path)
            p.drawImage(img, 50, y - 100, width=100, height=100)
        except:
            p.setFont("Helvetica", 10)
            p.drawString(50, y - 20, "Image not available")

        # Text
        p.setFont("Helvetica", 12)
        p.drawString(160, y - 20, f"Prediction: {prediction.prediction}")
        p.drawString(160, y - 40, f"Date: {prediction.datetime.strftime('%Y-%m-%d %H:%M')}")
        y -= 130

    p.save()
    buffer.seek(0)
    return buffer
