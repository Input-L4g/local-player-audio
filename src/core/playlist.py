"""
Esse módulo contém a classe Playlist,
reponsável por controlar quando e de que
forma cada musica será tocada e salvada
localmente.
"""
from dataclasses import dataclass, field
from uuid import uuid4
from typing import Optional, List, Iterator, Tuple, Unpack, Union
from src.core.type_hints import (
    AudioPathType,
    AudioSourceType,
    PlaylistModes,
    LoggingLevel,
    PlaylistDebugOptions,
    PlaylistDebugConfig
)
from src.exceptions.playlist_exceptions import (
    TrackExistsError,
    TrackNotExistsError,
    InvalidPlaylistModeError
    # PlaylistEmptyError
)
from src.utils.operations_utils import increment_index
from src.utils.logging_utils import log
from src.core.config import LOGGING_SCOPES, PLAYLIST_MODES

_LOGGING_SCOPE = "playlist"


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
    _mode: PlaylistModes
    debug: bool
    debug_config: PlaylistDebugConfig

    def __init__(
        self,
        mode: PlaylistModes = "loop",
        *,
        debug: bool = False,
        **debug_options: Unpack[PlaylistDebugOptions]
    ) -> None:
        """Inicializa a classe Playlist."""
        self.debug = debug
        default_debug_config: PlaylistDebugConfig = {
                "log_in_file": True,
                "clear_old_log": True,
                "allowed_logging_levels": ("info", "debug", "warning", "error", "critical")
            }
        self.debug_config = {
            **default_debug_config,
            **debug_options # Configuração aplicada
        }
        self._log_handler("Instanciando Playlist", "debug")
        self._tracks = []
        self._tracks_ids = []
        self.current_index = None
        self._mode = mode

    def _log_handler(self, message: str, level: LoggingLevel) -> None:
        """Handler que gera logs somente em modo debug."""
        if self.debug and level in self.debug_config["allowed_logging_levels"]:
            log(
                message,
                level,
                LOGGING_SCOPES[_LOGGING_SCOPE],
                self.debug_config["log_in_file"],
                self.debug_config["clear_old_log"]
            )

    def clear(self) -> None:
        """Limpa a playlist."""
        self._log_handler("Limpando a playlist", "info")
        self._tracks.clear()
        self._tracks_ids.clear()

    def get_by_id(self, track_id: str) -> Optional[Track]:
        """
        Procura e pega uma trilha por id.

        Se não encontrada, retorna None
        """
        return next((track for track in self if track.id == track_id), None)

    def get_all(self, in_original_pos: bool = False) -> List[Track]:
        """Retorna todas as trilhas nas respectivas posições."""
        tracks = self._tracks[:]
        if in_original_pos:
            tracks_by_id = {track.id: track for track in self}
            return [tracks_by_id[id_] for id_ in self._tracks_ids]
        return tracks

    def has_track(
        self,
        track: Track,
        raises: Optional[Exception] = None,
        raises_if: bool = False
    ) -> bool:
        """Verifica se tem uma trilha na playlist."""
        self._log_handler(f"Verificando a trilha ({track}) (raise: {raises})", "debug")
        result = track in self
        if raises is not None and result is raises_if:
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
        self._log_handler(f"[add()] Adicionando item na playlist: ({track})", "info")
        self.has_track(track, TrackExistsError(track.path), True)
        if len(self) == 0:
            self.current_index = 0
        self._tracks.append(track)
        self._tracks_ids.append(track.id)
        self._log_handler(f"[add()] A trilha ({track}) foi adicionada na playlist", "debug")

    def pop(self, track_index: int = -1) -> Optional[Track]:
        """
        Remove uma trilha da playlist pelo index.

        Retorna a trilha removida ou None, caso ela não exista.
        """
        self._log_handler(f"[pop()] Removendo o index {track_index} da playlist.", "info")
        if not 0 <= track_index < len(self):
            raise IndexError(
                f"O index passado ({track_index}) está fora da playlist ({len(self)}).")
        removed_track = self._tracks.pop(track_index)
        self._tracks_ids.remove(removed_track.id)
        self._log_handler(f"[pop()] O index {track_index} foi removido da playlist.", "debug")
        return removed_track

    def remove(self, track: Track) -> Optional[Track]:
        """
        Remove uma trilha da playlist.

        Retorna a trilha removida ou None.
        """
        self._log_handler(f"[remove()] Removendo a trilha ({track}) da playlist.", "info")
        self.has_track(track, TrackNotExistsError(track.path))
        track_index = self._tracks.index(track)
        removed_track = self._tracks.pop(track_index)
        self._tracks_ids.remove(removed_track.id)
        self._log_handler(f"[remove()] A trilha ({track}) foi removida da playlist.", "debug")
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

        """
        Passa para a próxima trilha na playlist.

        Retorna a trilha ou None.
        """
        self._log_handler("[next()] Indo para a próxima trilha da playlist.", "info")
        next_ = self.get_next()
        if self.current_index is None or next_ is None:
            return None
        _, new_index = next_
        if self._mode == "loop" or force_next:  # Em 'loop', continua normalmente
            self.current_index = new_index
        # Sem 'loop', fica na mesma trilha
        self._log_handler(f"[next()] Trilha mudada para: {self.get_current_track()}", "debug")
        return self.get_current_track()

    def previous(self) -> Optional[Track]:
        """
        Passa para a trilha anterior da atual na playlist.

        Retorna a trilha ou None.
        """
        self._log_handler("[previous()] Indo para a trilha anterior da playlist.", "info")
        next_ = self.get_previous()
        if self.current_index is None or next_ is None:
            return None
        _, new_index = next_
            self.current_index = new_index
        # Sem 'loop', fica na mesma trilha
        self._log_handler(f"[previous()] Trilha mudada para: ({self.get_current_track()})", "debug")
        return self.get_current_track()

        self._log_handler(f"[mode.setter()] O modo foi alterado para {mode}", "debug")
    def __getitem__(self, index: int) -> Track:
        self._log_handler(f"[__getitem__] Pegando o index {index} da playlist", "debug")
        return self._tracks[index]

    def __contains__(self, other) -> bool:
        if not isinstance(other, Track):
            return False
        return other in self._tracks

    def __iter__(self) -> Iterator[Track]:
        self._log_handler("[__iter__()] Iterando sob a playlist", "debug")
        return iter(self._tracks)

    def __len__(self) -> int:
        return len(self._tracks)
