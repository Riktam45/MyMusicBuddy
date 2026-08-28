from pathlib import Path
import tempfile

from fastapi import FastAPI, File, UploadFile

from basic_pitch.inference import (
    predict_and_save,
    ICASSP_2022_MODEL_PATH,
)

from ml.schema import (
    MLNoteEvent,
    MLTranscriptionResult,
)


app = FastAPI(
    title="MyMusic Buddy ML Service",
    version="1.0.0",
)


def _read_midi_notes(
    midi_path: Path,
) -> list[MLNoteEvent]:

    import mido

    midi = mido.MidiFile(
        str(midi_path)
    )

    notes = []

    for track in midi.tracks:

        current_time = 0.0
        active_notes = {}

        tempo = 500000

        for message in track:

            if message.type == "set_tempo":
                tempo = message.tempo

            current_time += (
                mido.tick2second(
                    message.time,
                    midi.ticks_per_beat,
                    tempo,
                )
            )

            if message.type == "note_on":

                if message.velocity > 0:

                    active_notes[
                        message.note
                    ] = (
                        current_time,
                        message.velocity,
                    )

                elif message.note in active_notes:

                    start, velocity = (
                        active_notes.pop(
                            message.note
                        )
                    )

                    notes.append(
                        MLNoteEvent(
                            pitch=int(
                                message.note
                            ),
                            start=float(start),
                            end=float(
                                current_time
                            ),
                            velocity=int(
                                velocity
                            ),
                        )
                    )

            elif message.type == "note_off":

                if message.note in active_notes:

                    start, velocity = (
                        active_notes.pop(
                            message.note
                        )
                    )

                    notes.append(
                        MLNoteEvent(
                            pitch=int(
                                message.note
                            ),
                            start=float(start),
                            end=float(
                                current_time
                            ),
                            velocity=int(
                                velocity
                            ),
                        )
                    )

    notes.sort(
        key=lambda note: (
            note.start,
            note.pitch,
        )
    )

    return notes


def transcribe_file(
    audio_path: str,
) -> MLTranscriptionResult:

    audio_file = Path(audio_path)

    if not audio_file.exists():
        raise FileNotFoundError(
            audio_path
        )

    with tempfile.TemporaryDirectory() as temp:

        output_dir = Path(temp)

        predict_and_save(
            [str(audio_file)],
            str(output_dir),
            save_midi=True,
            sonify_midi=False,
            save_model_outputs=False,
            save_notes=False,
            model_or_model_path=(
                ICASSP_2022_MODEL_PATH
            ),
        )

        midi_files = list(
            output_dir.glob("*.mid")
        )

        if not midi_files:
            raise RuntimeError(
                "Basic Pitch did not produce MIDI."
            )

        notes = _read_midi_notes(
            midi_files[0]
        )

    return MLTranscriptionResult(
        notes=notes,
        model="basic_pitch",
        confidence=None,
    )


@app.get("/health")
def health():
    return {
        "status": "ok",
        "model": "basic_pitch",
    }


@app.post(
    "/transcribe",
    response_model=MLTranscriptionResult,
)
async def transcribe(
    audio: UploadFile = File(...),
):

    suffix = (
        Path(
            audio.filename or "audio.wav"
        ).suffix
        or ".wav"
    )

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=suffix,
    ) as temp:

        temp.write(
            await audio.read()
        )

        temp_path = temp.name

    try:

        return transcribe_file(
            temp_path
        )

    finally:

        Path(temp_path).unlink(
            missing_ok=True
        )