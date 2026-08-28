from pathlib import Path

import requests

from app.ai.ml_note_schema import (
    MLNoteEvent,
    MLTranscriptionResult,
)


ML_SERVICE_URL = (
    "http://127.0.0.1:8100"
)


def transcribe_audio(
    audio_path: str,
) -> MLTranscriptionResult:

    audio_file = Path(audio_path)

    if not audio_file.exists():
        raise FileNotFoundError(
            f"Audio file not found: {audio_path}"
        )

    with audio_file.open(
        "rb"
    ) as file:

        try:
            response = requests.post(
                f"{ML_SERVICE_URL}/transcribe",
                files={
                    "audio": (
                        audio_file.name,
                        file,
                        "application/octet-stream",
                    )
                },
                timeout=300,
            )

        except requests.RequestException as exc:
            raise RuntimeError(
                "ML service is unavailable."
            ) from exc

    if not response.ok:

        raise RuntimeError(
            "ML service failed: "
            f"{response.status_code} "
            f"{response.text}"
        )

    data = response.json()

    return MLTranscriptionResult(
        notes=[
            MLNoteEvent(**note)
            for note in data["notes"]
        ],
        model=data["model"],
        confidence=data.get(
            "confidence"
        ),
    )