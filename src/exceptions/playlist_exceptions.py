"""
Esse módulo contém exceções referentes
a classe Playlist.
"""
from src.core.type_hints import AudioPathType
from src.core.config import PLAYLIST_MODES

class TrackExistsError(Exception):
    """Representa uma exceção quando uma trilha já existe na playlist."""
    def __init__(self, track_path: AudioPathType) -> None:
        self.type = "TrackExistsError"
        self.message: str = f"A trilha '{track_path}' já existe."
        super().__init__(self.message)

class TrackNotExistsError(Exception):
    """Representa uma exceção quando uma trilha não existe na playlist."""
    def __init__(self, track_path: AudioPathType) -> None:
        self.type = "TrackNotExistsError"
        self.message: str = f"A trilha '{track_path}' não existe."
        super().__init__(self.message)

class PlaylistEmptyError(Exception):
    """Representa uma exceção quando a playlist está vazia."""
    def __init__(self) -> None:
        self.type = "PlaylistEmptyError"
        self.message: str = "A playlist está vazia."
        super().__init__(self.message)
