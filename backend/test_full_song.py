from app.ai.loaders import load_audio
from app.ai.full_song_analyzer import FullSongAnalyzer


# --------------------------------------------------
# TEST AUDIO FILE
# --------------------------------------------------

audio_path = "test_audio.mp3"


# --------------------------------------------------
# LOAD AUDIO
# --------------------------------------------------

print("\n" + "=" * 60)
print("MYMUSIC BUDDY - FULL SONG ANALYSIS TEST")
print("=" * 60)

print("\n[1/4] Loading audio...")

context = load_audio(audio_path)

print("✓ Audio loaded successfully")
print(f"  Sample rate: {context.sample_rate}")
print(f"  Samples: {len(context.audio)}")


# --------------------------------------------------
# RUN FULL ANALYSIS
# --------------------------------------------------

print("\n[2/4] Running music analysis...")

analyzer = FullSongAnalyzer()

result = analyzer.analyze(context)

print("✓ Analysis completed")


# --------------------------------------------------
# DISPLAY BASIC RESULTS
# --------------------------------------------------

print("\n[3/4] BASIC MUSIC INFORMATION")
print("-" * 60)

print(f"BPM : {result.bpm}")
print(f"Key : {result.key}")


# --------------------------------------------------
# DISPLAY NOTES
# --------------------------------------------------

print("\n[4/4] DETECTED NOTES")
print("-" * 60)

if result.notes:

    print(f"Total note events: {len(result.notes)}")

    for note in result.notes[:20]:

        print(
            f"Time: {note.time:.3f}s | "
            f"Note: {note.note_with_octave} | "
            f"Frequency: {note.frequency:.2f} Hz | "
            f"Confidence: {note.confidence:.3f}"
        )

    if len(result.notes) > 20:
        print(
            f"... and {len(result.notes) - 20} more notes"
        )

else:

    print("No notes detected.")


# --------------------------------------------------
# DISPLAY CHORD PROGRESSION
# --------------------------------------------------

print("\nCHORD PROGRESSION")
print("-" * 60)

if result.chords:

    print(
        f"Detected chord segments: "
        f"{len(result.chords)}"
    )

    for chord in result.chords:

        print(
            f"{chord.start:.2f}s → "
            f"{chord.end:.2f}s | "
            f"{chord.chord} | "
            f"Confidence: "
            f"{chord.confidence:.3f}"
        )

else:

    print("No chords detected.")


# --------------------------------------------------
# FINISHED
# --------------------------------------------------

print("\n" + "=" * 60)
print("FULL SONG ANALYSIS TEST FINISHED")
print("=" * 60)