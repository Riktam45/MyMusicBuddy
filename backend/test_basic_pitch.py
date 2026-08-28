from ml.basic_pitch.inference import (
    transcribe_with_basic_pitch,
)


AUDIO_FILE = r"tone-test.mp3"


print("Loading audio...")
print("Running Basic Pitch...")
print()


notes = transcribe_with_basic_pitch(
    AUDIO_FILE
)


print()
print("========== MYMUSIC BUDDY ML ==========")

print(
    "ML notes detected:",
    len(notes),
)

print()

for note in notes[:20]:
    print(
        f"{note.note}{note.octave}"
        f" | MIDI {note.midi}"
        f" | {note.start}s"
        f" → {note.end}s"
        f" | confidence {note.confidence}"
    )

print()
print("=======================================")