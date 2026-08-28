from basic_pitch.inference import predict


AUDIO_FILE = r"tone-test.mp3"


print("Loading audio...")
print("Running Basic Pitch...")
print()


model_output, midi_data, note_events = predict(
    AUDIO_FILE
)


print("========== BASIC PITCH ==========")

print(
    "Model output type:",
    type(model_output),
)

print(
    "MIDI type:",
    type(midi_data),
)

print(
    "Note events:",
    len(note_events),
)

print()

print("First 10 note events:")

for index, event in enumerate(
    note_events[:10]
):
    print(
        "EVENT",
        index,
        "TYPE:",
        type(event),
    )

    print(
        "VALUE:",
        event,
    )

    try:
        print(
            "LENGTH:",
            len(event),
        )
    except TypeError:
        print(
            "LENGTH: not iterable"
        )

    print(
        "--------------------------------"
    )