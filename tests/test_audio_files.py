
import pytest

from py_functions.audio_files import safe_remove_audio_file


def test_safe_remove_audio_file_removes_files_inside_audio_directory(tmp_path):
    audio_dir = tmp_path / "audio"
    audio_dir.mkdir()
    audio_file = audio_dir / "clip.mp3"
    audio_file.write_text("audio", encoding="utf-8")

    assert safe_remove_audio_file(audio_file, audio_dir) is True
    assert not audio_file.exists()


def test_safe_remove_audio_file_ignores_missing_or_empty_paths(tmp_path):
    audio_dir = tmp_path / "audio"
    audio_dir.mkdir()

    assert safe_remove_audio_file(None, audio_dir) is False
    assert safe_remove_audio_file(audio_dir / "missing.mp3", audio_dir) is False


def test_safe_remove_audio_file_refuses_to_delete_outside_audio_directory(tmp_path):
    audio_dir = tmp_path / "audio"
    audio_dir.mkdir()
    outside_file = tmp_path / "outside.mp3"
    outside_file.write_text("do not delete", encoding="utf-8")

    with pytest.raises(ValueError, match="outside the audio directory"):
        safe_remove_audio_file(outside_file, audio_dir)

    assert outside_file.exists()
