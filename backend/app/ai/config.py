from pathlib import Path

AI_MODEL_PATH = Path("storage/models")

AI_MODEL_PATH.mkdir(
    parents=True,
    exist_ok=True,
)