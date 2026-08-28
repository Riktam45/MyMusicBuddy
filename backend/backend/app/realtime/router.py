import tempfile
import librosa
from pathlib import Path
from app.ai.pitch_service import analyze_pitch
from fastapi import APIRouter, File, Form, UploadFile
import numpy as np
from scipy.signal import find_peaks
from typing import Any

from app.music.chords import CHORDS
from app.music.scales import SCALES
from app.music.arpeggios import ARPEGGIOS

REALTIME_DIR = Path("storage/realtime")
REALTIME_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


router = APIRouter(
    prefix="/realtime",
    tags=["Realtime"],
)

async def analyze_realtime_pitch_data(
    audio_data: bytes,
):
    import tempfile
    from pathlib import Path

    import librosa

    from app.ai.pitch_service import analyze_pitch

    temp_path = None

    try:
        with tempfile.NamedTemporaryFile(
            suffix=".webm",
            delete=False,
        ) as temp_file:
            temp_file.write(audio_data)
            temp_path = temp_file.name

        audio_signal, sample_rate = (
            librosa.load(
                temp_path,
                sr=16000,
                mono=True,
            )
        )

        if len(audio_signal) == 0:
            return {
                "detected": False,
                "message": (
                    "No audio detected."
                ),
            }

        f0, voiced_flag, voiced_prob = (
            librosa.pyin(
                audio_signal,
                fmin=librosa.note_to_hz("C2"),
                fmax=librosa.note_to_hz("C7"),
                sr=sample_rate,
            )
        )

        valid_pitches = []

        for (
            frequency,
            voiced,
            probability,
        ) in zip(
            f0,
            voiced_flag,
            voiced_prob,
        ):
            if not voiced:
                continue

            if frequency is None:
                continue

            valid_pitches.append(
                (
                    float(frequency),
                    float(probability),
                )
            )

        if not valid_pitches:
            return {
                "detected": False,
                "message": (
                    "No clear pitch detected."
                ),
            }

        frequency, probability = max(
            valid_pitches,
            key=lambda item: item[1],
        )

        result = analyze_pitch(
            frequency
        )

        return {
            "detected": True,
            "frequency": result[
                "frequency"
            ],
            "midi": result["midi"],
            "note": result["note"],
            "octave": result["octave"],
            "note_with_octave": (
                result["note_with_octave"]
            ),
            "confidence": round(
                probability,
                3,
            ),
        }

    finally:
        if temp_path:
            try:
                Path(temp_path).unlink(
                    missing_ok=True
                )
            except Exception:
                pass

@router.post("/pitch")
async def analyze_realtime_pitch(
    audio: UploadFile = File(...),
):
    audio_data = await audio.read()

    if not audio_data:
        return {
            "success": False,
            "message": "Empty audio chunk.",
        }

    temp_path = None

    try:
        with tempfile.NamedTemporaryFile(
            suffix=".webm",
            delete=False,
        ) as temp_file:
            temp_file.write(audio_data)
            temp_path = temp_file.name

        audio_signal, sample_rate = librosa.load(
            temp_path,
            sr=16000,
            mono=True,
        )

        if len(audio_signal) == 0:
            return {
                "success": False,
                "message": "Audio chunk contains no data.",
            }

        f0, voiced_flag, voiced_prob = librosa.pyin(
            audio_signal,
            fmin=librosa.note_to_hz("C2"),
            fmax=librosa.note_to_hz("C7"),
            sr=sample_rate,
        )

        valid_pitches = []

        for frequency, voiced, probability in zip(
            f0,
            voiced_flag,
            voiced_prob,
        ):
            if not voiced:
                continue

            if frequency is None:
                continue

            if not isinstance(
                frequency,
                (float, int),
            ):
                continue

            valid_pitches.append(
                (
                    float(frequency),
                    float(probability),
                )
            )

        if not valid_pitches:
            return {
                "success": True,
                "detected": False,
                "message": "No clear pitch detected.",
            }

        frequency, probability = max(
            valid_pitches,
            key=lambda item: item[1],
        )

        pitch_result = analyze_pitch(
            frequency
        )

        return {
            "success": True,
            "detected": True,
            "frequency": pitch_result["frequency"],
            "midi": pitch_result["midi"],
            "note": pitch_result["note"],
            "octave": pitch_result["octave"],
            "note_with_octave": (
                pitch_result["note_with_octave"]
            ),
            "confidence": round(
                probability,
                3,
            ),
        }

    except Exception as error:
        print(
            f"Realtime pitch analysis failed: {error}"
        )

        return {
            "success": False,
            "message": "Pitch analysis failed.",
        }

    finally:
        if temp_path:
            try:
                Path(temp_path).unlink(
                    missing_ok=True
                )
            except Exception:
                pass

@router.post("/chunk")
async def receive_audio_chunk(
    session_id: str = Form(...),
    audio: UploadFile = File(...),
):
    chunk_data = await audio.read()

    if not chunk_data:
        return {
            "success": False,
            "message": "Empty audio chunk.",
        }

    session_file = (
        REALTIME_DIR
        / f"{session_id}.webm"
    )

    with open(
        session_file,
        "ab",
    ) as file:
        file.write(chunk_data)

    current_size = session_file.stat().st_size

    return {
        "success": True,
        "session_id": session_id,
        "chunk_size": len(chunk_data),
        "total_size": current_size,
        "message": "Audio chunk stored.",
    }

@router.post("/analyze")
async def analyze_realtime_chunk(
    session_id: str = Form(...),
    audio: UploadFile = File(...),
):
    chunk_data = await audio.read()

    if not chunk_data:
        return {
            "success": False,
            "message": "Empty audio chunk.",
        }

    session_file = (
        REALTIME_DIR
        / f"{session_id}.webm"
    )

    try:
        # 1. Store the chunk
        with open(
            session_file,
            "ab",
        ) as file:
            file.write(chunk_data)

        # 2. Analyze this chunk
        pitch_result = await analyze_realtime_pitch_data(
            chunk_data
        )

        return {
            "success": True,
            "session_id": session_id,
            "chunk_size": len(chunk_data),
            "total_size": session_file.stat().st_size,
            "pitch": pitch_result,
        }

    except Exception as error:
        print(
            f"Realtime analysis failed: {error}"
        )

        return {
            "success": False,
            "message": "Realtime analysis failed.",
        }

# ============================================================
# REALTIME EVENT ENGINE ADDITION
# Paste this addition into app/realtime/router.py while keeping
# the existing /pitch and /chunk endpoints.
# ============================================================

# Add these imports near the top of router.py:
# import numpy as np
# from scipy.signal import find_peaks
# from typing import Any

from app.music.chords import CHORDS
from app.music.scales import SCALES
from app.music.arpeggios import ARPEGGIOS

NOTE_NAMES = [
    "C", "C#", "D", "D#", "E", "F",
    "F#", "G", "G#", "A", "A#", "B",
]

SILENCE_RMS = 0.008
SILENCE_WINDOWS_TO_FINISH = 2
MIN_EVENT_WINDOWS = 1

_sessions: dict[str, dict[str, Any]] = {}

def _session(session_id: str) -> dict[str, Any]:
    return _sessions.setdefault(
        session_id,
        {
            "event_id": 0,
            "active": False,
            "silence_windows": 0,
            "event_windows": 0,
            "last_notes": [],
            "last_chord": None,
            "last_confidence": 0.0,
            "last_suggestions": None,
        },
    )


def _midi_to_note(midi: int) -> tuple[str, int]:
    octave = (midi // 12) - 1
    return NOTE_NAMES[midi % 12], octave


def _note_frequency(midi: int) -> float:
    return 440.0 * (2.0 ** ((midi - 69) / 12.0))


def _decode_audio(audio_data: bytes) -> tuple[np.ndarray, int]:
    """
    Decode browser WebM/Opus audio using FFmpeg.

    Returns:
        audio samples as float32 NumPy array
        sample rate = 16000 Hz
    """

    import subprocess
    import tempfile

    input_path = None

    try:
        # Save browser WebM temporarily
        with tempfile.NamedTemporaryFile(
            suffix=".webm",
            delete=False,
        ) as temp_file:
            temp_file.write(audio_data)
            input_path = temp_file.name

        # Ask FFmpeg to decode WebM/Opus -> 16 kHz mono float32 PCM
        command = [
            "ffmpeg",
            "-hide_banner",
            "-loglevel",
            "error",
            "-i",
            input_path,
            "-f",
            "f32le",
            "-acodec",
            "pcm_f32le",
            "-ac",
            "1",
            "-ar",
            "16000",
            "pipe:1",
        ]

        process = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )

        if process.returncode != 0:
            error_message = process.stderr.decode(
                "utf-8",
                errors="replace",
            )

            raise RuntimeError(
                f"FFmpeg failed to decode audio: "
                f"{error_message}"
            )

        if not process.stdout:
            raise RuntimeError(
                "FFmpeg returned no decoded audio."
            )

        # Convert raw PCM bytes -> NumPy float32 samples
        audio_signal = np.frombuffer(
            process.stdout,
            dtype=np.float32,
        )

        if audio_signal.size == 0:
            raise RuntimeError(
                "Decoded audio contains no samples."
            )

        return audio_signal, 16000

    finally:
        if input_path:
            try:
                Path(input_path).unlink(
                    missing_ok=True
                )
            except Exception:
                pass


def _pitch_candidates(y: np.ndarray, sr: int) -> list[dict[str, Any]]:
    """Fast polyphonic pitch estimate for a short live window."""
    if len(y) < int(sr * 0.08):
        return []

    y = y.astype(np.float32, copy=False)
    y = y - float(np.mean(y))

    window = np.hanning(len(y))
    spectrum = np.abs(np.fft.rfft(y * window))
    freqs = np.fft.rfftfreq(len(y), 1.0 / sr)

    # Ignore sub-bass noise and very high frequencies that are less useful
    # for the live beginner-note/chord detector.
    mask = (freqs >= 65.0) & (freqs <= 1400.0)
    spectrum = spectrum[mask]
    freqs = freqs[mask]

    if spectrum.size == 0 or float(np.max(spectrum)) <= 1e-9:
        return []

    # Light spectral floor removes tiny bins and makes the detector less
    # likely to report microphone noise as a note.
    spectrum = np.maximum(spectrum - np.percentile(spectrum, 35), 0.0)
    max_spec = float(np.max(spectrum))
    if max_spec <= 1e-9:
        return []
    spectrum /= max_spec

    peaks, properties = find_peaks(
        spectrum,
        height=0.10,
        distance=max(1, int(round(len(freqs) / sr * 15))),
    )

    if len(peaks) == 0:
        return []

    peak_heights = properties.get("peak_heights", spectrum[peaks])

    # Convert spectral peaks to MIDI candidates. The fundamental gets a
    # harmonic-consistency score so strong overtones are less likely to be
    # mistaken for separate musical notes.
    scores: list[tuple[int, float]] = []

    for midi in range(36, 97):
        fundamental = _note_frequency(midi)
        if fundamental > 1400:
            continue

        score = 0.0
        weight_sum = 0.0

        for harmonic in range(1, 7):
            target = fundamental * harmonic
            if target >= sr / 2:
                break

            # Find the closest spectral bin.
            idx = int(np.argmin(np.abs(freqs - target)))
            distance_hz = abs(float(freqs[idx]) - target)
            tolerance = max(3.0, target * 0.018)

            if distance_hz <= tolerance:
                weight = 1.0 / harmonic
                score += float(spectrum[idx]) * weight
                weight_sum += weight

        if weight_sum > 0:
            scores.append((midi, score / weight_sum))

    if not scores:
        return []

    scores.sort(key=lambda item: item[1], reverse=True)
    best = scores[0][1]

    if best < 0.16:
        return []

    # Keep musically distinct candidates only. Do not let adjacent FFT
    # candidates flood the chord with duplicates.
    selected: list[tuple[int, float]] = []
    for midi, score in scores:
        if score < max(0.22, best * 0.38):
            break
        # Keep one representative octave per pitch class. Harmonics and
        # octave copies should not be reported as separate chord notes.
        if all(midi % 12 != other_midi % 12 for other_midi, _ in selected):
            selected.append((midi, score))
        if len(selected) >= 5:
            break

    result = []
    for midi, score in selected:
        note, octave = _midi_to_note(midi)
        result.append(
            {
                "note": note,
                "octave": octave,
                "note_with_octave": f"{note}{octave}",
                "midi": midi,
                "frequency": round(_note_frequency(midi), 2),
                "confidence": round(min(1.0, float(score)), 3),
            }
        )

    return result


def _detect_chord(notes: list[dict[str, Any]]) -> tuple[str | None, float]:
    if len(notes) < 2:
        return None, 0.0

    pitch_classes = {int(note["midi"]) % 12 for note in notes}

    templates = {
        "major": {0, 4, 7},
        "minor": {0, 3, 7},
        "dim": {0, 3, 6},
        "sus2": {0, 2, 7},
        "sus4": {0, 5, 7},
    }

    best_name = None
    best_score = 0.0

    for root in range(12):
        for suffix, intervals in templates.items():
            template = {(root + interval) % 12 for interval in intervals}
            overlap = len(template & pitch_classes)
            coverage = overlap / len(template)
            extra = len(pitch_classes - template)
            score = coverage - (0.10 * extra)

            if overlap >= 2 and score > best_score:
                best_score = score
                root_name = NOTE_NAMES[root]
                suffix_text = {"major": "", "minor": "m", "dim": "dim", "sus2": "sus2", "sus4": "sus4"}[suffix]
                best_name = f"{root_name}{suffix_text}"

    if best_score < 0.70:
        return None, 0.0

    return best_name, min(1.0, best_score)


def _note_name_from_midi(midi: int) -> str:
    return NOTE_NAMES[midi % 12]


def _chord_name(root: str, chord_type: str) -> str:
    suffixes = {
        "major": "",
        "minor": "m",
        "diminished": "dim",
        "maj7": "maj7",
        "min7": "m7",
        "dom7": "7",
    }
    return f"{root}{suffixes[chord_type]}"


def _chord_note_names(root_midi: int, intervals: list[int]) -> list[str]:
    return [
        _note_name_from_midi(root_midi + interval)
        for interval in intervals
    ]


def _build_note_suggestions(note: dict[str, Any]) -> dict[str, Any]:
    """Create useful musical suggestions when the detected event is only one note."""
    midi = int(note["midi"])
    root_pc = midi % 12
    root = NOTE_NAMES[root_pc]

    # Prefer common triads first, then seventh chords. Keep the detected
    # pitch class inside every suggested chord.
    chord_candidates: list[tuple[int, str, str, list[int]]] = []
    for root_candidate in range(12):
        distance = (root_pc - root_candidate) % 12
        for chord_type in ("major", "minor", "diminished", "maj7", "min7", "dom7"):
            intervals = CHORDS[chord_type]
            if distance in intervals:
                chord_candidates.append((
                    (0 if root_candidate == root_pc else 1),
                    _chord_name(NOTE_NAMES[root_candidate], chord_type),
                    chord_type,
                    intervals,
                ))

    chord_candidates.sort(key=lambda item: (item[0], item[1]))
    selected_chords = chord_candidates[:6]

    chord_suggestions = []
    arpeggio_suggestions = []
    for _, chord_name, chord_type, intervals in selected_chords:
        # Recover the root pitch from the chord candidate.
        root_name = chord_name
        for suffix in ("maj7", "m7", "dim", "m", "7"):
            if root_name.endswith(suffix):
                root_name = root_name[:-len(suffix)]
                break
        root_midi = root_pc
        for candidate_pc, candidate_name in enumerate(NOTE_NAMES):
            if candidate_name == root_name:
                root_midi = candidate_pc + 60
                break

        chord_notes = _chord_note_names(root_midi, intervals)
        chord_suggestions.append({
            "name": chord_name,
            "root": root_name,
            "notes": chord_notes,
            "intervals": intervals,
            "contains_note": note["note"],
        })

        arp_intervals = ARPEGGIOS.get(chord_type)
        if arp_intervals:
            arpeggio_suggestions.append({
                "name": f"{chord_name} Arpeggio",
                "root": root_name,
                "notes": _chord_note_names(root_midi, arp_intervals),
                "intervals": arp_intervals,
                "description": f"Arpeggiate {chord_name} from the detected note {note['note_with_octave'] }.",
            })

    scale_order = (
        "major",
        "natural_minor",
        "major_pentatonic",
        "minor_pentatonic",
        "blues",
    )
    scale_suggestions = []
    for scale_type in scale_order:
        intervals = SCALES[scale_type]
        scale_notes = _chord_note_names(midi, intervals)
        scale_suggestions.append({
            "name": f"{root} {scale_type.replace('_', ' ').title()}",
            "root": root,
            "notes": scale_notes,
            "intervals": intervals,
            "description": f"A {scale_type.replace('_', ' ')} scale starting from {root}.",
        })

    # A simple, musically familiar progression centered around the detected
    # note's pitch class. This is a suggestion, not a claim that the note
    # itself proves a key.
    progression_roots = [
        root_pc,
        (root_pc + 7) % 12,
        (root_pc + 2) % 12,
        (root_pc + 9) % 12,
    ]
    chord_progression = [NOTE_NAMES[pc] for pc in progression_roots]

    return {
        "chords": chord_suggestions,
        "chord_progression": chord_progression,
        "arpeggios": arpeggio_suggestions,
        "scales": scale_suggestions,
        "intervals": [],
    }


def _build_suggestions(state: dict[str, Any]) -> dict[str, Any] | None:
    notes = state.get("last_notes") or []
    if not notes:
        return None

    if len(notes) == 1:
        return _build_note_suggestions(notes[0])

    chord = state.get("last_chord")
    if not chord:
        return _build_note_suggestions(notes[0])

    # For an already detected chord, expose the same suggestion shape while
    # preserving the detected chord as the first chord suggestion.
    root = chord
    chord_type = "major"
    for suffix, candidate_type in (("maj7", "maj7"), ("m7", "min7"), ("7", "dom7"), ("dim", "diminished"), ("m", "minor")):
        if chord.endswith(suffix):
            root = chord[:-len(suffix)]
            chord_type = candidate_type
            break
    intervals = CHORDS.get(chord_type, CHORDS["major"])
    root_pc = NOTE_NAMES.index(root) if root in NOTE_NAMES else int(notes[0]["midi"]) % 12
    root_midi = root_pc + 60
    chord_notes = _chord_note_names(root_midi, intervals)
    arp_intervals = ARPEGGIOS.get(chord_type, intervals)

    return {
        "chords": [{
            "name": chord,
            "root": root,
            "notes": chord_notes,
            "intervals": intervals,
        }],
        "chord_progression": [chord, NOTE_NAMES[(root_pc + 7) % 12], NOTE_NAMES[(root_pc + 9) % 12], NOTE_NAMES[(root_pc + 5) % 12]],
        "arpeggios": [{
            "name": f"{chord} Arpeggio",
            "root": root,
            "notes": _chord_note_names(root_midi, arp_intervals),
            "intervals": arp_intervals,
            "description": f"Arpeggiate the detected {chord} chord.",
        }],
        "scales": [{
            "name": f"{root} Major",
            "root": root,
            "notes": _chord_note_names(root_midi, SCALES["major"]),
            "intervals": SCALES["major"],
            "description": f"Major scale built from {root}.",
        }, {
            "name": f"{root} Natural Minor",
            "root": root,
            "notes": _chord_note_names(root_midi, SCALES["natural_minor"]),
            "intervals": SCALES["natural_minor"],
            "description": f"Natural minor scale built from {root}.",
        }],
        "intervals": [],
    }


def _reset_session(session_id: str) -> None:
    _sessions.pop(session_id, None)


@router.post("/event")
async def analyze_realtime_event(
    session_id: str = Form(...),
    audio: UploadFile = File(...),
):
    audio_data = await audio.read()

    if not audio_data:
        return {
            "success": False,
            "active": False,
            "event_complete": False,
            "event_id": 0,
            "note": None,
            "note_with_octave": None,
            "notes": [],
            "chord": None,
            "confidence": 0.0,
            "message": "Empty audio window.",
        }

    state = _session(session_id)

    try:
        y, sr = _decode_audio(audio_data)
        rms = float(np.sqrt(np.mean(np.square(y)))) if len(y) else 0.0

        # Silence is a boundary between musical events. It does NOT stop the
        # listening session, so the next sound starts a fresh event.
        if rms < SILENCE_RMS:
            state["silence_windows"] += 1

            event_complete = bool(
                state["active"]
                and state["event_windows"] >= MIN_EVENT_WINDOWS
                and state["silence_windows"] >= SILENCE_WINDOWS_TO_FINISH
            )

            if event_complete:
                state["active"] = False
                state["event_windows"] = 0
                state["silence_windows"] = 0
                state["event_id"] += 1

            return {
                "success": True,
                "active": False,
                "event_complete": event_complete,
                "event_id": state["event_id"],
                "note": None,
                "note_with_octave": None,
                "notes": state["last_notes"] if event_complete else [],
                "chord": state["last_chord"] if event_complete else None,
                "confidence": state["last_confidence"] if event_complete else 0.0,
                "message": "Silence detected; waiting for the next musical event.",
            }

        state["active"] = True
        state["silence_windows"] = 0
        state["event_windows"] += 1

        notes = _pitch_candidates(y, sr)

        if not notes:
            return {
                "success": True,
                "active": True,
                "event_complete": False,
                "event_id": state["event_id"],
                "note": None,
                "note_with_octave": None,
                "notes": [],
                "chord": None,
                "confidence": 0.0,
                "message": "Sound detected; waiting for a clear pitch.",
            }

        state["last_notes"] = notes

        chord, chord_confidence = _detect_chord(notes)
        top = notes[0]
        confidence = chord_confidence if chord else float(top["confidence"])
        state["last_chord"] = chord
        state["last_confidence"] = round(confidence, 3)
        state["last_suggestions"] = None

        return {
            "success": True,
            "active": True,
            "event_complete": False,
            "event_id": state["event_id"],
            "note": top["note"],
            "note_with_octave": f"{top['note']}{top['octave']}",
            "notes": notes,
            "chord": chord,
            "confidence": round(confidence, 3),
            "message": "Current musical event detected.",
        }

    except Exception as error:
        import traceback

        print("========================================")
        print("REALTIME EVENT ENGINE ERROR")
        print("ERROR TYPE:", type(error).__name__)
        print("ERROR:", repr(error))
        traceback.print_exc()
        print("========================================")

        return {
            "success": False,
            "active": False,
            "event_complete": False,
            "event_id": state["event_id"],
            "note": None,
            "note_with_octave": None,
            "notes": [],
            "chord": None,
            "confidence": 0.0,
            "message": "Realtime event analysis failed.",
        }


@router.post("/stop")
async def stop_realtime_session(session_id: str = Form(...)):
    state = _sessions.get(session_id)
    suggestions = _build_suggestions(state) if state else None

    result = {
        "success": True,
        "event_complete": bool(state and state.get("active")),
        "event_id": int(state["event_id"]) if state else 0,
        "notes": state.get("last_notes", []) if state else [],
        "note": state.get("last_notes", [None])[0].get("note") if state and state.get("last_notes") else None,
        "note_with_octave": (
            f"{state['last_notes'][0]['note']}{state['last_notes'][0]['octave']}"
            if state and state.get("last_notes") else None
        ),
        "chord": state.get("last_chord") if state else None,
        "confidence": float(state.get("last_confidence", 0.0)) if state else 0.0,
        "suggestions_ready": bool(suggestions),
        "suggestions": suggestions,
    }
    _reset_session(session_id)
    return result
