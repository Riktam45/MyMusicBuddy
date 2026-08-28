import json
from pathlib import Path

from app.ai.full_song_analyzer import FullSongAnalyzer
from app.ai.loaders import load_audio


AUDIO_PATH = Path(
    "D:/mymusic-buddy/backend/marmixer-see-you-later-203103.wav"
)


def main():
    if not AUDIO_PATH.exists():
        raise FileNotFoundError(
            f"Audio file not found: {AUDIO_PATH}"
        )

    print("Loading audio...")

    context = load_audio(
        str(AUDIO_PATH)
    )

    print("Running full song analysis...")

    analyzer = FullSongAnalyzer()

    result = analyzer.analyze(
        context
    )

    report = result.model_dump()

    with open(
        "storage/analysis_result.json",
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            report,
            file,
            indent=2,
        )

    print("\n========== MYMUSIC BUDDY ==========")

    print(
        f"BPM: {result.bpm}"
    )

    print(
        f"Key: {result.key}"
    )

    print(
        f"Notes detected: {len(result.notes)}"
    )

    print(
        f"Chord segments: {len(result.chords)}"
    )

    print(
        f"Scale recommendations: "
        f"{len(result.scales)}"
    )

    print(
        f"Intervals detected: "
        f"{len(result.intervals)}"
    )

    print(
        f"Arpeggios detected: "
        f"{len(result.arpeggios)}"
    )

    print(
        f"Pitch events: {len(result.pitch)}"
    )

    print("===================================")


if __name__ == "__main__":
    main()