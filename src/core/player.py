"""
Esse módulo contém a classe
Player, o motor de áudio da aplicação.
"""
from typing import Unpack
from rich import print as rprint
from src.core.type_hints import (
    # PlayerOptions,
    InitialPlayerOptions,
    AudioChannelType, VolumeType, SpeedRateType,
    AudioPathType, PlayerProperties
)
from src.mpv import mpv
from src.core.config import (
    DEFAULT_PLAYER_OPTIONS,
    DEFAULT_MPV_CONFIG,
    MPV_LOGLEVELS_ERRORS
)
from src.exceptions.player_exception import InvalidAudioChannelError


class Player:
    """
    Representa um player de áudio,
    podendo reproduzir, pausar/despausar e
    definir configurações básicas de reprodução.
    """

    def __init__(self, **options: Unpack[InitialPlayerOptions]) -> None:
        """
        Inicializa a classe Player.
        Seus argumentos estão tipados e documentados
        no módulo `type_hints.py`.
        """
        self.mpv_config = {
            **DEFAULT_MPV_CONFIG,
            **{"audio-device": options.get("audio_output", DEFAULT_PLAYER_OPTIONS["audio_output"])}
        }
        self._player = mpv.MPV(
            **self.mpv_config, log_handler=self._mpv_handler_log)
        self._player.volume = options.get(
            "volume", DEFAULT_PLAYER_OPTIONS["volume"])
        self._player.audio_channels = options.get(
            "audio_channel", DEFAULT_PLAYER_OPTIONS["audio_channel"])
        self._player.speed = options.get(
            "speed_rate", DEFAULT_PLAYER_OPTIONS["speed_rate"])
        self._player.mute = options.get("mute", DEFAULT_PLAYER_OPTIONS["mute"])

        self._properties: PlayerProperties = {
            **DEFAULT_PLAYER_OPTIONS, "debug": options.get("debug", False)}

    @property
    def debug(self) -> bool:
        """Ativa ou desativa o handler log."""
        return self._properties["debug"]

    @debug.setter
    def debug(self, value: bool) -> None:
        self._properties["debug"] = value

    @property
    def volume(self) -> VolumeType:
        """Volume aplicado à reprodução."""
        return self._properties["volume"]

    @volume.setter
    def volume(self, value: VolumeType) -> None:
        value = max(0, min(value, DEFAULT_MPV_CONFIG["volume-max"]))
        self._properties["volume"] = value
        self._player.volume = self._properties["volume"]

    @property
    def speed_rate(self) -> SpeedRateType:
        """Velocidade da reprodução. max: 100.0, min: 0.0, default: 1.0."""
        return self._properties["speed_rate"]

    @speed_rate.setter
    def speed_rate(self, rate: SpeedRateType) -> None:
        rate = max(0.0, min(rate, 100.0))
        self._properties["speed_rate"] = rate
        self._player.speed = self._properties["speed_rate"]

    @property
    def audio_channel(self) -> AudioChannelType:
        """Canal de áudio da reprodução. "mono", "stereo", "auto", default: "auto"."""
        return self._properties["audio_channel"]

    @audio_channel.setter
    def audio_channel(self, channel: AudioChannelType):
        raise NotImplementedError("property.setter não implementada")
        options = ("mono", "stereo", "auto")
        if channel not in options:
            raise InvalidAudioChannelError(channel, options)
        self._properties["audio_channel"] = channel
        self._player.audio_channel = self._properties["audio_channel"]

    def play(self, audio_path: AudioPathType) -> None:
        """Começa a reprodução de um áudio."""
        if not isinstance(audio_path, str):
            audio_path = str(audio_path)
        self._player.play(audio_path)

    def pause(self) -> None:
        """Pausa a reprodução atual."""
        self._player.pause = True

    def unpause(self) -> None:
        """Despausa a reprodução atual."""
        self._player.pause = False

    def wait_for_playback(self) -> None:
        """Não deixa o Python finalizar até a reprodução acabar."""
        self._player.wait_for_playback()

    def _mpv_handler_log(self, loglevel: str, component: str, message: str) -> None:
        """Handler que imprime um log do MPV em execução."""
        if self.debug:
            if self._is_log_error(loglevel):
                loglevel = loglevel.upper()
            print(f"[{loglevel}] {component}: {message}".strip())

    def _is_log_error(self, loglevel: str) -> bool:
        """Verifica se um `loglevel` do MPV indica um erro."""
        return loglevel in MPV_LOGLEVELS_ERRORS
