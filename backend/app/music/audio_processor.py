from pathlib import Path

import ffmpeg


PROCESSED_DIR = Path("storage/processed")
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


def convert_to_wav(input_file: str):
    """
    Convert audio into AI-ready WAV format.
    """

    input_path = Path(input_file)

    output_path = PROCESSED_DIR / f"{input_path.stem}.wav"

    (
        ffmpeg
        .input(str(input_path))
        .output(
            str(output_path),
            ac=1,          # Mono
            ar=16000,      # 16kHz
            acodec="pcm_s16le",
        )
        .overwrite_output()
        .run(quiet=True)
    )

    return str(output_path)