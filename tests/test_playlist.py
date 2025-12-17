"""
Esse módulo contém funções de testes
de cada método/funcionalidade da class
Playlist, do módulo playlist.py
"""
from pathlib import Path
from src.core.playlist import Track, Playlist

TRACK1 = Track(Path("./src/resources/test_musics/music1.mp3"), "local", title="track1")
TRACK2 = Track(Path("./src/resources/test_musics/music2.mp3"), "local", title="track2")
TRACK3 = Track(Path("./src/resources/test_musics/music3.mp3"), "local", title="track3")

playlist = Playlist(debug=True, allowed_logging_levels=("debug",))

def set_up() -> None:
    """Função executada antes de qualquer teste."""
    playlist.add(TRACK1)
    playlist.add(TRACK2)
    playlist.add(TRACK3)

def tear_down() -> None:
    """Função executada após qualquer teste"""
    playlist.clear()

def test_add() -> None:
    """Testa o método `add`."""
    set_up()
    assert playlist[0] == TRACK1
    assert playlist[1] == TRACK2
    assert playlist[2] == TRACK3
    tear_down()

def test_remove() -> None:
    """Testa o método `remove`."""
    set_up()
    playlist.remove(TRACK2)
    assert TRACK2 not in playlist
    tear_down()

def test_next() -> None:
    """Testa o método `next`"""
    set_up()
    assert TRACK1 == playlist.get_current_track()
    playlist.next()
    assert TRACK2 == playlist.get_current_track()
    playlist.next()
    assert TRACK3 == playlist.get_current_track()
    playlist.next() # Recomeça de TRACK1
    assert TRACK1 == playlist.get_current_track()
    playlist.next()
    assert TRACK2 == playlist.get_current_track()
    playlist.next()
    assert TRACK3 == playlist.get_current_track()
    tear_down()

def test_previous() -> None:
    """Testa o método `previous`."""
    set_up()
    assert TRACK1 == playlist.get_current_track()
    playlist.previous()
    assert TRACK3 == playlist.get_current_track()
    playlist.previous()
    assert TRACK2 == playlist.get_current_track()
    playlist.previous() # Recomeça de TRACK1
    assert TRACK1 == playlist.get_current_track()
    playlist.previous()
    assert TRACK3 == playlist.get_current_track()
    playlist.previous()
    assert TRACK2 == playlist.get_current_track()
    tear_down()

def test_clear() -> None:
    """Testa o método `clear`."""
    set_up()
    assert len(playlist) == 3
    playlist.clear()
    assert playlist.is_empty() is True
    tear_down()

def test_iter() -> None:
    """Testa o dunder `__iter__`."""
    set_up()
    tracks = list(playlist)
    assert playlist == tracks
    playlist2 = Playlist()
    playlist2.add(TRACK1)
    playlist2.add(TRACK2)
    playlist2.add(TRACK3)
    assert playlist == playlist2
    tear_down()

def test_pop() -> None:
    """Testa o método `pop`;"""
    set_up()
    track = playlist.pop(0)
    assert track == TRACK1
    track = playlist.pop(1)
    assert track == TRACK3
    tear_down()

def test_mode() -> None:
    """Testa a propriedade `mode`."""
    set_up()
    assert playlist.mode == "loop"
    playlist.mode = "one_repeat"
    assert playlist.mode == "one_repeat"
    assert playlist.get_current_track() == TRACK1
    assert playlist.next() == TRACK1
    assert playlist.next(force_next=True) == TRACK2
    assert playlist.next() == TRACK2
    playlist.mode = "loop"
    assert playlist.next() == TRACK3
    assert playlist.next() == TRACK1
    assert playlist.next() == TRACK2
    tear_down()
