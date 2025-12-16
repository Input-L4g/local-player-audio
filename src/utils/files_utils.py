"""
Esse módulo contém funções utilitárias para
manipulação de arquivos.
"""
from src.core.type_hints import PathType

def clear_file(file_path: PathType) -> None:
    """Limpa o contúdo de um arquivo."""
    with open(file_path, "w", encoding="utf-8") as _:
        pass
