"""
Esse módulo contem exceções referentes à
classe Player, em player.py.
"""
from typing import Sequence
from src.core.type_hints import AudioChannelType

class InvalidAudioChannelError(Exception):
    """Representa uma exceção ao definir um canal de áudio inválido."""
    def __init__(self, entry: str, expected: Sequence[AudioChannelType]) -> None:
        self.message = f"Canal de áudio inválido: {entry}. Era esperado: {expected}"
        super().__init__(self.message)
