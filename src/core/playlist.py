"""
Esse módulo contém a classe Playlist,
reponsável por controlar quando e de que
forma cada musica será tocada e salvada
localmente.
"""
from dataclasses import dataclass, field
from uuid import uuid4
from typing import Optional, List, Iterator, Tuple
from src.core.type_hints import (
    AudioPathType,
    AudioSourceType,
    PlaylistModes,
    LoggingLevel
)
from src.exceptions.playlist_exceptions import (
    TrackExistsError,
    TrackNotExistsError,
    PlaylistEmptyError
)
from src.utils.operations_utils import increment_index
from src.utils.logging_utils import log
from src.core.config import LOGGING_SCOPES

@dataclass(eq=False, slots=True)
class Track:
    """Representa uma trilha na playlist."""
    path: AudioPathType
    source: AudioSourceType = "local"
    title: Optional[str] = field(default=None, kw_only=True)
    duration: Optional[float] = field(default=None, kw_only=True)
    id: str = field(init=False, default_factory=lambda: uuid4().hex)

    def __eq__(self, other):
        if not isinstance(other, Track):
            return NotImplemented
        return (
            self.path == other.path and
            self.source == other.source
        )

    def __str__(self) -> str:
        return f"{self.path} - {self.source}"


class Playlist:
    """
    Representa uma playlist, com métodos para adicionar/removes trilhas, pegar
    a atual, limpar toda a playlist, modos, etc.
    """
    _tracks: List[Track]
    _tracks_ids: List[str]
    current_index: Optional[int]
    mode: PlaylistModes
    debug: bool

    def __init__(
        self, mode: PlaylistModes = "loop", *, debug: bool = False) -> None:
        """Inicializa a classe Playlist."""
        self._log_handler("Instânciando Playlist", "debug")
        self._tracks = []
        self._tracks_ids = []
        self.current_index = None
        self.mode = mode
        self.debug = debug

    def _log_handler(self, message: str, level: LoggingLevel) -> None:
        """Handler que gera logs somente em modo debug."""
        if self.debug:
            log(message, level, LOGGING_SCOPES["playlist"])

    def clear(self) -> None:
        """Limpa a playlist."""
        self._log_handler("Limpando a playlist", "info")
        self._tracks.clear()
        self._tracks_ids.clear()

    def has_track(self, track: Track, raises: Optional[Exception] = None) -> bool:
        """Verifica se tem uma trilha na playlist."""
        self._log_handler(f"Verificando a trilha ({track}) (raise: {raises})", "debug")
        result = track in self
        if raises is not None and result is False:
            raise raises
        return result

    def is_empty(self) -> bool:
        """Verifica se a playlist está vazia."""
        return len(self) == 0

    def get_current_track(self) -> Optional[Track]:
        """Retorna a trilha atual ou None."""
        if self.current_index is None:
            return None
        return self[self.current_index]

    def add(self, track: Track) -> None:
        """Adiciona uma trilha à playlist."""
        self._log_handler(f"Adicionando item na playlist: ({track})", "info")
        self.has_track(track, TrackExistsError(track.path))
        self._tracks.append(track)
        self._tracks_ids.append(track.id)

    def pop(self, track_index: int = -1) -> Optional[Track]:
        """
        Remove uma trilha da playlist pelo index.

        Retorna a trilha removida ou None, caso ela não exista.
        """
        self._log_handler(f"Removendo o index {track_index} da playlist.", "info")
        if not 0 <= track_index < len(self):
            raise IndexError(
                f"O index passado ({track_index}) está fora da playlist ({len(self)}).")
        removed_track = self._tracks.pop(track_index)
        self._tracks_ids.remove(removed_track.id)
        return removed_track

    def remove(self, track: Track) -> Optional[Track]:
        """
        Remove uma trilha da playlist.

        Retorna a trilha removida ou None.
        """
        self._log_handler(f"Removendo a trilha ({track}) da playlist.", "info")
        self.has_track(track, TrackNotExistsError(track.path))
        track_index = self._tracks.index(track)
        removed_track = self._tracks.pop(track_index)
        self._tracks_ids.remove(removed_track.id)
        return removed_track

    def get_next(self) -> Optional[Tuple[Track, int]]:
        """Retorna a próxima trilha e o seu index ou None."""
        if self.current_index is None:
            return None
        new_index = increment_index(self.current_index, len(self))
        return self[new_index], new_index

    def get_previous(self) -> Optional[Tuple[Track, int]]:
        """Retorna a trilha anterior e o seu index ou None."""
        if self.current_index is None:
            return None
        new_index = increment_index(self.current_index, len(self), -1)
        return self[new_index], new_index

    def next(self) -> Optional[Track]:
        """
        Passa para a próxima trilha na playlist.

        Retorna a trilha ou None.
        """
        self._log_handler("Indo para a próxima trilha da playlist.", "info")
        next_ = self.get_next()
        if self.current_index is None or next_ is None:
            return None
        _, new_index = next_
        if self.mode == "loop":  # Em 'loop', continua normalmente
            self.current_index = new_index
        # Sem 'loop', fica na mesma trilha
        self._log_handler(f"Trilha mudada: {self.get_current_track()}", "info")
        return self.get_current_track()

    def previous(self) -> Optional[Track]:
        """
        Passa para a trilha anterior da atual na playlist.

        Retorna a trilha ou None.
        """
        self._log_handler("Indo para a trilha anterior da playlist.", "info")
        next_ = self.get_previous()
        if self.current_index is None or next_ is None:
            return None
        _, new_index = next_
        if self.mode == "loop":  # Em 'loop', continua normalmente
            self.current_index = new_index
        # Sem 'loop', fica na mesma trilha
        self._log_handler(f"Trilha mudada: {self.get_current_track()}", "info")
        return self.get_current_track()

    def __getitem__(self, index: int) -> Track:
        self._log_handler(f"Pegando o index {index} da playlist", "debug")
        return self._tracks[index]

    def __contains__(self, other) -> bool:
        if not isinstance(other, Track):
            return False
        return other in self._tracks

    def __iter__(self) -> Iterator[Track]:
        self._log_handler("Iterando sob a playlist", "debug")
        return iter(self._tracks)

    def __len__(self) -> int:
        return len(self._tracks)
