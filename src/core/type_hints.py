"""
Esse módulo contém as tipagens estáticas usadas
em todo a aplicação.
"""
from typing import TypedDict, Literal, Optional



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
    volume: int
    mute: bool
    speed_rate: float
    audio_device: Optional[str]
    audio_channels: Literal["stereo", "mono", "auto"]

class InitialPlayerOptions(PlayerOptions, total=False):
    """
    Representa um dicionário tipado com
    as configurações iniciais aplicadas
    ao criar uma instância de Player.
    """
