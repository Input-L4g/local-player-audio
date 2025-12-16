"""
Esse módulo contém as tipagens estáticas usadas
em todo a aplicação.
"""
from typing import TypedDict, Literal, Optional, TypeAlias, Union
from pathlib import Path

VolumeType: TypeAlias = int
MuteType: TypeAlias = bool
SpeedRateType: TypeAlias = float
AudioOutputType: TypeAlias = Optional[str]
AudioChannelType: TypeAlias = Literal["stereo", "mono", "auto"]
AudioPathType: TypeAlias = Union[str, Path]
AudioSourceType = Literal["local"]

class PlayerOptions(TypedDict):
    """
    Representa um dicionário tipa com
    as configurações de uma instância de Player.
    - volume: int -> Volume do áudio, mímimo 0, máximo 100, default 75.
    - mute: bool -> Muta o áudio reproduzido.
    - speed_rate: float -> Velocidade de reprodução, mínimo 0.01, máximo 100.0, default 1.0.
    - audio_device: str -> Dispositivo de saída de som, decidido pelo sistema ou manualmente.
    - audio_channels: str -> Canal de áudio, só pode ser "mono", "stereo", "auto", default "auto".
    """
    volume: VolumeType
    mute: MuteType
    speed_rate: SpeedRateType
    audio_output: AudioOutputType
    audio_channel: AudioChannelType

class InitialPlayerOptions(TypedDict, total=False):
    """
    Representa um dicionário tipado com
    as configurações iniciais aplicadas
    ao criar uma instância de Player.
    """
    volume: VolumeType
    mute: MuteType
    speed_rate: SpeedRateType
    audio_output: AudioOutputType
    audio_channel: AudioChannelType
    debug: bool # Modo debug

class PlayerProperties(TypedDict, total=True):
    """Um dicionário tipado representando as propriedades internas do Player"""
    volume: VolumeType
    mute: MuteType
    speed_rate: SpeedRateType
    audio_output: AudioOutputType
    audio_channel: AudioChannelType
    debug: bool # Modo debug

PlaylistModes = Literal[
    "loop", # Loop infinito
    "one_repeat" # Loop em apenas uma trilha
]
