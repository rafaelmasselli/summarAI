import datetime
import os

from fpdf import FPDF


class PdfService:
    def __init__(self):
        self.path = os.path.join(os.path.dirname(__file__), "..", "..", "..", "pdfs")
        # Create directory if it doesn't exist
        os.makedirs(self.path, exist_ok=True)

    def create_pdf(self, text: str) -> str:
        pdf = FPDF()
        pdf.add_page()

        # Add title
        pdf.set_font("Arial", "B", size=16)
        pdf.cell(200, 10, "Video Summary", ln=1, align="C")

        # Add timestamp
        pdf.set_font("Arial", "I", size=10)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        pdf.cell(200, 10, f"Generated on: {timestamp}", ln=1, align="R")

        # Add content
        pdf.set_font("Arial", size=12)

        # Handle multi-line text by adding each paragraph
        pdf.ln(10)

        # Split text into paragraphs and add them to the PDF
        paragraphs = text.split("\n")
        for paragraph in paragraphs:
            # Handle long paragraphs by wrapping text
            pdf.multi_cell(0, 10, paragraph)
            pdf.ln(5)

        # Save the PDF
        output_path = os.path.join(self.path, "summary.pdf")
        pdf.output(output_path)

        print(f"PDF created successfully at: {output_path}")
        return output_path
