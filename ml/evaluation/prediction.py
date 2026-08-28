from pathlib import Path
import json
import mido


def midi_to_predictions(
    midi_path: str,
    output_path: str,
):
    midi = mido.MidiFile(midi_path)

    ticks_per_beat = midi.ticks_per_beat
    tempo = 500000

    notes = []

    for track in midi.tracks:

        current_time = 0.0
        active_notes = {}

        for message in track:

            if message.type == "set_tempo":
                tempo = message.tempo

            current_time += mido.tick2second(
                message.time,
                ticks_per_beat,
                tempo,
            )

            if message.type == "note_on":

                if message.velocity > 0:

                    active_notes[message.note] = (
                        current_time
                    )

                elif message.note in active_notes:

                    start_time = active_notes.pop(
                        message.note
                    )

                    notes.append(
                        {
                            "pitch": int(message.note),
                            "start": float(start_time),
                            "end": float(current_time),
                        }
                    )

            elif message.type == "note_off":

                if message.note in active_notes:

                    start_time = active_notes.pop(
                        message.note
                    )

                    notes.append(
                        {
                            "pitch": int(message.note),
                            "start": float(start_time),
                            "end": float(current_time),
                        }
                    )

    notes.sort(
        key=lambda note: (
            note["start"],
            note["pitch"],
        )
    )

    output = Path(output_path)
    output.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with output.open(
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            notes,
            file,
            indent=2,
        )

    print(
        f"Predictions created: {output}"
    )

    print(
        f"Predicted notes: {len(notes)}"
    )


if __name__ == "__main__":

    prediction_file = (
        r"D:\mymusic-buddy\ml\evaluation"
        r"\maps\prediction"
        r"\MAPS_MUS-alb_se3_AkPnBcht_basic_pitch.mid"
    )

    output_file = (
        r"D:\mymusic-buddy\ml\evaluation"
        r"\ground_truth"
        r"\maps_alb_se3_predictions.json"
    )

    midi_to_predictions(
        prediction_file,
        output_file,
    )