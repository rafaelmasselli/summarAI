import datetime
import os

from fpdf import FPDF

from util.logger import logger


class PdfService:
    def __init__(self):
        self.path = os.path.join(os.path.dirname(__file__), "..", "..", "..", "pdfs")
        os.makedirs(self.path, exist_ok=True)
        logger.debug(f"PDF output directory: {self.path}")

    def create_pdf(self, text: str) -> str:
        logger.info("Creating PDF document...")

        try:
            pdf = FPDF()
            pdf.add_page()
            logger.debug("PDF page added")

            pdf.set_font("Arial", "B", size=16)
            pdf.cell(200, 10, "Video Summary", ln=1, align="C")

            pdf.set_font("Arial", "I", size=10)
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            pdf.cell(200, 10, f"Generated on: {timestamp}", ln=1, align="R")

            logger.debug("PDF header added")

            pdf.set_font("Arial", size=12)
            pdf.ln(10)

            paragraphs = text.split("\n")
            logger.debug(f"Processing {len(paragraphs)} paragraphs")

            for paragraph in paragraphs:
                pdf.multi_cell(0, 10, paragraph)
                pdf.ln(5)

            output_path = os.path.join(self.path, "summary.pdf")
            pdf.output(output_path)

            logger.success(f"PDF created successfully at: {output_path}")
            return output_path

        except Exception as e:
            logger.error(f"Failed to create PDF: {str(e)}")
            raise
