import datetime
import os
import re
from typing import List, Tuple

from fpdf import FPDF

from util.logger import logger


class PDF(FPDF):
    """Classe personalizada que estende FPDF para adicionar cabeçalho e rodapé."""

    def __init__(self, title=""):
        super().__init__()
        self.set_margins(15, 15, 15)
        self.title = title
        self.set_auto_page_break(auto=True, margin=15)

    def header(self):
        self.set_font("Arial", "B", 12)
        self.set_fill_color(230, 230, 230)
        width = self.w - 30
        self.cell(width, 10, self.title, 0, 1, "C", 1)
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Página {self.page_no()}", 0, 0, "C")


class PdfService:
    def __init__(self):
        self.path = os.path.join(os.path.dirname(__file__), "..", "..", "..", "pdfs")
        os.makedirs(self.path, exist_ok=True)
        logger.debug(f"PDF output directory: {self.path}")

    def _extract_title_and_topics(self, text: str) -> Tuple[str, List[str]]:
        """Extrai o título e tópicos principais do texto."""
        lines = text.split("\n")

        title = "Resumo do Vídeo"
        for line in lines:
            if line.strip():
                title = line.strip()
                break

        if len(title) > 60:
            title = title[:57] + "..."

        topics = []
        topic_pattern = r"^(\d+\.\s|\-\s|\*\s|[A-Za-z]\)\s|[A-Za-z]\.\s)"

        for line in lines:
            line = line.strip()
            if re.match(topic_pattern, line):
                topics.append(line)
            elif line and len(line) < 100 and line.endswith(":"):
                topics.append(line)

        return title, topics

    def _add_metadata(self, pdf: PDF, video_url: str = ""):
        """Adiciona metadados ao PDF."""
        pdf.set_title("Resumo de Vídeo")
        pdf.set_author("LLM Estudy")
        pdf.set_creator("LLM Estudy PDF Generator")
        pdf.set_keywords("resumo, vídeo, IA, aprendizado")
        if video_url:
            pdf.set_subject(f"Resumo do vídeo: {video_url}")

    def _safe_text(self, text: str) -> str:
        """Torna o texto seguro para o PDF, removendo caracteres problemáticos."""
        text = text.replace("•", "-")
        text = text.replace("✓", "v")
        text = text.replace("✗", "x")
        text = text.replace("→", "->")
        text = text.replace("⇒", "=>")
        text = "".join(c for c in text if ord(c) < 128)
        return text

    def create_pdf(self, text: str, video_url: str = "") -> str:
        logger.info("Criando documento PDF aprimorado...")

        try:
            title, topics = self._extract_title_and_topics(text)
            title = self._safe_text(title)

            pdf = PDF(title)
            self._add_metadata(pdf, video_url)

            pdf.add_page()

            pdf.set_font("Arial", "B", size=14)
            pdf.cell(0, 10, title, ln=1, align="C")

            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            pdf.set_font("Arial", "I", size=8)
            pdf.cell(0, 5, f"Gerado em: {timestamp}", ln=1, align="R")

            if video_url:
                if len(video_url) > 70:
                    display_url = video_url[:67] + "..."
                else:
                    display_url = video_url

                pdf.set_font("Arial", "I", size=8)
                pdf.cell(0, 5, f"Fonte: {display_url}", ln=1, align="L")

            pdf.line(20, pdf.get_y() + 3, pdf.w - 20, pdf.get_y() + 3)
            pdf.ln(8)

            if len(topics) >= 3:
                pdf.set_font("Arial", "B", size=11)
                pdf.cell(0, 8, "Principais Tópicos:", ln=1)
                pdf.set_font("Arial", size=9)

                for i, topic in enumerate(topics):
                    short_topic = topic[:60] + "..." if len(topic) > 60 else topic
                    short_topic = self._safe_text(short_topic)
                    pdf.cell(0, 6, f"- {short_topic}", ln=1)

                pdf.ln(3)
                pdf.line(20, pdf.get_y(), pdf.w - 20, pdf.get_y())
                pdf.ln(8)

            pdf.set_font("Arial", "B", size=11)
            pdf.cell(0, 8, "Resumo Completo:", ln=1)
            pdf.set_font("Arial", size=10)

            paragraphs = text.split("\n")
            for paragraph in paragraphs:
                paragraph = paragraph.strip()
                if not paragraph:
                    pdf.ln(2)
                    continue

                paragraph = self._safe_text(paragraph)

                if len(paragraph) < 100 and (
                    paragraph.isupper() or paragraph.endswith(":")
                ):
                    pdf.ln(3)
                    pdf.set_font("Arial", "B", size=10)
                    pdf.write(5, paragraph)
                    pdf.ln(5)
                    pdf.set_font("Arial", size=10)
                elif re.match(
                    r"^(\d+\.\s|\-\s|\*\s|[A-Za-z]\)\s|[A-Za-z]\.\s)", paragraph
                ):
                    pdf.set_font("Arial", "B", size=10)
                    pdf.write(5, paragraph)
                    pdf.ln(5)
                    pdf.set_font("Arial", size=10)
                else:
                    pdf.write(5, paragraph)
                    pdf.ln(5)

            pdf.ln(8)
            pdf.set_font("Arial", "I", size=8)
            pdf.cell(
                0,
                5,
                "Este resumo foi gerado automaticamente por inteligência artificial.",
                ln=1,
                align="C",
            )

            timestamp_filename = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = os.path.join(self.path, f"resumo_{timestamp_filename}.pdf")
            pdf.output(output_path)

            logger.success(f"PDF criado com sucesso em: {output_path}")
            return output_path

        except Exception as e:
            logger.error(f"Falha ao criar PDF: {str(e)}")
            raise
