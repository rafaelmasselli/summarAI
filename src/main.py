import sys
from typing import Optional

from application.handlers.youtube_handler import YouTubeHandler


def processar_video(
    url: str, tipo: str = "summarize", instrucoes: Optional[str] = None
) -> None:
    """Processa um vídeo do YouTube"""
    handler = YouTubeHandler()
    resultado = handler.handle_video_processing(
        video_url=url, process_type=tipo, instructions=instrucoes
    )
    print("\nResultado do processamento:")
    print(resultado)


def mostrar_ajuda() -> None:
    """Mostra as opções disponíveis do programa"""
    print("\nOpções disponíveis:")
    print("1. Processar vídeo:")
    print("   python main.py processar <url> [tipo] [instrucoes]")
    print("\nTipos de processamento disponíveis:")
    print("- summarize: Gera um resumo detalhado do vídeo")
    print("- technical: Realiza uma análise técnica do conteúdo")
    print("- default: Processamento padrão do vídeo")
    print("\nExemplos:")
    print('python main.py processar "https://youtube.com/..." summarize')
    print(
        'python main.py processar "https://youtube.com/..." technical "Foque em padrões de código"'
    )


def main() -> None:
    if len(sys.argv) < 2:
        print("Por favor, escolha uma opção:")
        mostrar_ajuda()
        return

    comando = sys.argv[1].lower()

    if comando in ["processar", "p"]:
        if len(sys.argv) < 3:
            print("URL do vídeo é obrigatória!")
            mostrar_ajuda()
            return

        url = sys.argv[2]
        tipo = sys.argv[3] if len(sys.argv) > 3 else "summarize"
        instrucoes = sys.argv[4] if len(sys.argv) > 4 else None

        # Mapeia o tipo para o valor correto
        tipo_map = {
            "technical": "technical_analysis",
            "t": "technical_analysis",
            "summarize": "summarize",
            "s": "summarize",
            "default": "default",
            "d": "default",
        }
        tipo_processamento = tipo_map.get(tipo.lower(), "summarize")

        processar_video(url, tipo_processamento, instrucoes)

    elif comando in ["ajuda", "help", "h"]:
        mostrar_ajuda()
    else:
        print(f"Comando '{comando}' não reconhecido")
        mostrar_ajuda()


if __name__ == "__main__":
    main()
