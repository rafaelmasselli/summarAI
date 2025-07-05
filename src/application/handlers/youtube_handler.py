from typing import Optional

from application.services.youtube import YoutubeService
from domain.interfaces.model import Model
from infrastructure.factories.model_factory import ModelFactory


class YouTubeHandler:
    def __init__(self, model: Optional[Model] = None):
        self.model = model

    def get_model(self, type_model: str) -> Model:
        match type_model:
            case "gemini":
                return ModelFactory.create_model("gemini", "gemini-2.0-flash")
            case _:
                raise ValueError("Model not found")

    def handle_video_processing(
        self,
        video_url: str,
        process_type: str = "summarize",
        instructions: str = None,
        context: str = None,
    ) -> str:
        try:
            if not video_url:
                raise ValueError("URL do vídeo é obrigatória")

            service = YoutubeService(video_url)

            default_instructions = {
                "summarize": "Faça um resumo detalhado do vídeo, destacando os pontos principais",
                "technical_analysis": "Analise os aspectos técnicos do conteúdo, identificando padrões e práticas",
                "default": "Analise o conteúdo do vídeo",
            }

            final_instructions = instructions or default_instructions.get(
                process_type, default_instructions["default"]
            )
            final_context = context or ""

            if process_type == "summarize":
                return service.summarize_video(
                    instructions=final_instructions, context=final_context
                )
            elif process_type == "technical_analysis":
                return service.analyze_technical_content(
                    instructions=final_instructions, context=final_context
                )
            else:
                return service.process_with_model(
                    model_type="gemini",
                    model_name="gemini-pro",
                    template_type="default",
                    instructions=final_instructions,
                    context=final_context,
                )

        except Exception as e:
            self.handle_error(e)
            return f"Erro ao processar vídeo: {str(e)}"

    def handle_error(self, error: Exception) -> None:
        """Trata erros ocorridos durante o processamento"""
        # TODO: Implementar logging adequado
        print(f"Erro: {str(error)}")
