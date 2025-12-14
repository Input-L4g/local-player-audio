from pathlib import Path
from time import sleep
from src.core.player import Player

AUDIO_PATH = Path("./src/resources/test_musics/music1.mp3")
player = Player(debug=True, volume=50)

def test_play() -> None:
    """Testa a função `play`."""
    player.play(AUDIO_PATH)
    player.wait_for_playback()
    assert True

def test_pause() -> None:
    """Testa a função `pause`."""
    player.play(AUDIO_PATH)
    sleep(5)
    player.pause()
    player.wait_for_playback()
    assert True

def test_unpause() -> None:
    """Testa a função `unpause`."""
    player.play(AUDIO_PATH)
    sleep(2)
    player.pause()
    sleep(2)
    player.unpause()
    player.wait_for_playback()
    assert True

def test_volume() -> None:
    """Testa a propriedade `volume`."""
    player.play(AUDIO_PATH)
    sleep(2)
    player.volume = 60
    sleep(2)
    assert player.volume == 60
    player.volume = 70
    sleep(2)
    assert player.volume == 70
    player.volume = 50
    sleep(2)
    assert player.volume == 50

def test_speed_rate() -> None:
    """Testa a propriedade `speed_rate`."""
    player.play(AUDIO_PATH)
    sleep(2)
    player.speed_rate = 1.5
    sleep(2)
    assert player.speed_rate == 1.5
    player.speed_rate = 2.5
    sleep(2)
    assert player.speed_rate == 2.5
    player.speed_rate = 0.5
    sleep(2)
    assert player.speed_rate == 0.5
