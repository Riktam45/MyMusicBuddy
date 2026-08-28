from pathlib import Path

from basic_pitch.inference import predict

from app.music.notes import pitch_class_to_note

from .schema import MLNoteEvent


def midi_to_note_name(
    midi: int,
) -> str:
    """
    Convert a MIDI number into a note name.
    """

    pitch_class = midi % 12

    return pitch_class_to_note(
        pitch_class
    )


def midi_to_octave(
    midi: int,
) -> int:
    """
    Convert a MIDI number into an octave.
    """

    return (
        midi // 12
    ) - 1


def transcribe_with_basic_pitch(
    audio_path: str,
) -> list[MLNoteEvent]:
    """
    Run Basic Pitch and convert its
    predictions into MyMusic Buddy
    ML note events.
    """

    audio_file = Path(
        audio_path
    )

    if not audio_file.exists():
        raise FileNotFoundError(
            f"Audio file not found: {audio_path}"
        )

    (
        model_output,
        midi_data,
        note_events,
    ) = predict(
        str(audio_file)
    )

    results = []

    for event in note_events:

        start = float(
            event[0]
        )

        end = float(
            event[1]
        )

        midi = int(
            event[2]
        )

        confidence = float(
            event[3]
        )

        duration = max(
            0.0,
            end - start,
        )

        note = midi_to_note_name(
            midi
        )

        octave = midi_to_octave(
            midi
        )

        results.append(
            MLNoteEvent(
                note=note,
                octave=octave,
                midi=midi,
                start=round(
                    start,
                    3,
                ),
                end=round(
                    end,
                    3,
                ),
                duration=round(
                    duration,
                    3,
                ),
                confidence=round(
                    confidence,
                    3,
                ),
            )
        )

    return results