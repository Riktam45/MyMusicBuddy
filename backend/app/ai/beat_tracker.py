import librosa


def detect_beats(context):
    """
    Detect beat positions in the song.
    """

    tempo, beat_frames = librosa.beat.beat_track(
        y=context.audio,
        sr=context.sample_rate,
    )

    beat_times = librosa.frames_to_time(
        beat_frames,
        sr=context.sample_rate,
    )

    return beat_times.tolist()