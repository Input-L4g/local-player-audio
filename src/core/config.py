"""
Esse módulo contém os valores globais da
aplicação, bem como as configurações
padrões do sistema.
"""
from src.core.type_hints import PlayerOptions

DEFAULT_MPV_CONFIG = {
    # Desativa completamente o vídeo
    "video": "no",
    "vid": "no",

    # Backend de áudio (ajuste conforme o sistema)
    # Exemplos válidos: pulse, pipewire, alsa, jack
    "ao": "pulse",

    # Canal de mixagem (auto geralmente é o ideal)
    "audio-channels": "auto",

    # Normalização (ReplayGain, se existir no arquivo)
    "replaygain": "track",

    # Volume inicial
    "volume": 100,
    "volume-max": 100,

    # Mantém o pitch ao alterar velocidade
    "audio-pitch-correction": "yes",

    # Evita inicialização de entrada de teclado
    "input-default-bindings": "no",
    "input-terminal": "no",

    # Cache de áudio (streaming ou arquivos grandes)
    "cache": "yes",
    "cache-secs": 10,

    # Comportamento ao finalizar a faixa
    "keep-open": "no",

    # Precisão de seek (útil para players)
    "hr-seek": "yes",

    # Força modo headless
    "force-window": "no",

    # Desativa OSC e OSD
    "osc": "no",
    "osd-level": 0,
}

DEFAULT_PLAYER_OPTIONS: PlayerOptions = {
    "volume": 75,
    "audio_channel": "auto",
    "speed_rate": 1.0,
    "mute": False,
    "audio_output": DEFAULT_MPV_CONFIG["ao"]
}

MPV_LOGLEVELS_ERRORS = ("error", "fatal")

LOGGING_SCOPES = {
    "playlist": "core.playlist",
    "player": "core.player",
    "controller": "core.controller"
}

LOGGING_PATH_OUTPUT= "./log"
