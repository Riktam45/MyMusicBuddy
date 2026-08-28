from app.ai.note_transcriber import transcribe_notes
from app.ai.note_converter import convert_note_events
from app.ai.chord_detector import detect_chord


AUDIO_PATH = "storage/processed/song.wav"


print("===================================")
print("MyMusic Buddy - Chord Engine Test")
print("===================================")


# STEP 1 — Basic Pitch transcription
print("\n[1] Transcribing notes...")

result = transcribe_notes(AUDIO_PATH)

print(
    "Detected note events:",
    len(result["note_events"])
)


# STEP 2 — Convert notes
print("\n[2] Converting note events...")

notes = convert_note_events(
    result["note_events"]
)

print("Converted notes:", len(notes))

print("\nFirst 5 notes:")

for note in notes[:5]:
    print(note)


# STEP 3 — Detect chord
print("\n[3] Detecting chord...")

chord = detect_chord(notes)

print("\nDetected chord:")

print(chord)


print("\n===================================")
print("Test completed")
print("===================================")