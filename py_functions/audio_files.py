from pathlib import Path


def safe_remove_audio_file(audio_path: str | Path | None, audio_dir: str | Path) -> bool:
    """Remove an audio file only when it resolves inside the configured audio directory."""
    if not audio_path:
        return False

    base_dir = Path(audio_dir).resolve()
    target_path = Path(audio_path)
    if not target_path.is_absolute():
        target_path = Path.cwd() / target_path
    resolved_target = target_path.resolve(strict=False)

    try:
        resolved_target.relative_to(base_dir)
    except ValueError as exc:
        raise ValueError("Refusing to delete a file outside the audio directory") from exc

    if not resolved_target.exists():
        return False
    if not resolved_target.is_file():
        raise ValueError("Audio path is not a file")

    resolved_target.unlink()
    return True
