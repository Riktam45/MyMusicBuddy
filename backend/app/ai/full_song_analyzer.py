from app.ai.full_song_schema import FullSongAnalysis

from app.ai.bpm import detect_bpm
from app.ai.key_detector import detect_key
from app.ai.note_transcriber import transcribe_notes

from app.ai.beat_tracker import detect_beats
from app.ai.segmentation import create_segments
from app.ai.chord_segmenter import detect_segment_chords
from app.ai.chord_smoothing import smooth_chords
from app.ai.key_scale_engine import recommend_song_scales
from app.ai.interval_analyzer import (
    calculate_interval,
    identify_interval,
)
from app.ai.chord_arpeggio_engine import analyze_chord_arpeggio



class FullSongAnalyzer:
    """
    Coordinates the complete music analysis pipeline.

    Current analysis:
    - BPM
    - Musical key
    - Note transcription
    - Beat detection
    - Chord segmentation
    - Chord progression
    """

    def analyze(self, context):
        """
        Run the complete analysis on an AnalysisContext.
        """

        result = FullSongAnalysis()

        # -----------------------------------------
        # BPM
        # -----------------------------------------

        result.bpm = self._analyze_bpm(
            context
        )

        # -----------------------------------------
        # KEY
        # -----------------------------------------

        result.key = self._analyze_key(
            context
        )

        # -----------------------------------------
        # NOTES
        # -----------------------------------------

        note_events = self._analyze_notes(
            context
        )

        result.notes = note_events

        # -----------------------------------------
        # CHORDS / PROGRESSION
        # -----------------------------------------

        result.chords = self._analyze_chords(
            context,
            note_events,
        )

        result.progression = result.chords

        # -----------------------------------------
        # SCALES
        # -----------------------------------------

        result.scales = self._analyze_scales(
            result.key
        )

        # -----------------------------------------
        # INTERVALS
        # -----------------------------------------

        result.intervals = self._analyze_intervals(
            result.key,
            result.notes,
        )

        # -----------------------------------------
        # ARPEGGIOS
        # -----------------------------------------

        result.arpeggios = self._analyze_arpeggios(
            result.chords
        )

        # -----------------------------------------
        # PITCH INFORMATION
        # -----------------------------------------

        result.pitch = self._analyze_pitch(
           result.notes
        )

        return result

    # =========================================================
    # SCALES
    # =========================================================

    def _analyze_scales(self, key):
        """
        Recommend scales based on the detected song key.
        """

        if not key:
            return []

        try:
            return recommend_song_scales(
                key
            )

        except Exception as error:
            print(
                f"Scale analysis failed: {error}"
            )

            return []

    # =========================================================
    # BPM
    # =========================================================

    def _analyze_bpm(self, context):
        """
        Detect the tempo of the song.
        """

        try:
            return detect_bpm(
                context
            )

        except Exception as error:
            print(
                f"BPM analysis failed: {error}"
            )

            return None

    # =========================================================
    # KEY
    # =========================================================

    def _analyze_key(self, context):
        """
        Detect the musical key of the song.
        """

        try:
            return detect_key(
                context
            )

        except Exception as error:
            print(
                f"Key analysis failed: {error}"
            )

            return None

    # =========================================================
    # NOTES
    # =========================================================

    def _analyze_notes(self, context):
        """
        Transcribe musical notes from the audio.
        """

        try:
            return transcribe_notes(
                context
            )

        except Exception as error:
            print(
                f"Note analysis failed: {error}"
            )

            return []

    # =========================================================
    # CHORD PROGRESSION
    # =========================================================

    def _analyze_chords(
        self,
        context,
        note_events,
    ):
        """
        Detect chords across musical time segments.
        """

        try:

            # -----------------------------------------
            # Make sure notes exist
            # -----------------------------------------

            if not note_events:
                return []

            # -----------------------------------------
            # Detect beats
            # -----------------------------------------

            beats = detect_beats(
                context
            )

            if not beats:
                return []

            # -----------------------------------------
            # Create musical segments
            # -----------------------------------------

            segments = create_segments(
                beats,
                beats_per_segment=4,
            )

            if not segments:
                return []

            # -----------------------------------------
            # Detect chord for each segment
            # -----------------------------------------

            chord_segments = detect_segment_chords(
                note_events,
                segments,
            )

            if not chord_segments:
                return []

            return smooth_chords(
                chord_segments
            )

        except Exception as error:

            print(
                f"Chord progression analysis failed: {error}"
            )

            return []

    # =========================================================
    # INTERVALS
    # =========================================================

    def _analyze_intervals(self, key, note_events):
        """
        Analyze intervals between the detected song key
        and the detected notes.
        """

        if not key or not note_events:
            return []

        results = []

        try:
            for note_event in note_events:
                semitones = calculate_interval(
                    key,
                    note_event.note,
                )

                name = identify_interval(
                    key,
                    note_event.note,
                )

                results.append(
                    {
                        "root": key,
                        "note": note_event.note,
                        "semitones": semitones,
                        "name": name,
                    }
                )

            return results

        except Exception as error:
            print(
                f"Interval analysis failed: {error}"
            )

            return []

    # =========================================================
    # ARPEGGIOS
    # =========================================================

    def _analyze_arpeggios(self, chord_segments):
        """
        Generate arpeggio information
        for detected chord segments.
        """

        if not chord_segments:
            return []

        results = []

        try:
            for segment in chord_segments:

                arpeggio = analyze_chord_arpeggio(
                    segment.root,
                    segment.type,
                )

                if not arpeggio:
                    continue

                results.append(
                    {
                        "chord": segment.chord,
                        "start": segment.start,
                        "end": segment.end,
                        "confidence": segment.confidence,
                        "arpeggio": arpeggio,
                    }
                )

            return results

        except Exception as error:
            print(
                f"Arpeggio analysis failed: {error}"
            )

            return []

    # =========================================================
    # PITCH INFORMATION 
    # =========================================================

    def _analyze_pitch(self, note_events):
        """
        Extract pitch and octave information
        from detected note events.
        """

        if not note_events:
            return []

        results = []

        for note_event in note_events:
            results.append(
                {
                    "time": note_event.time,
                    "frequency": note_event.frequency,
                    "midi": note_event.pitch,
                    "note": note_event.note,
                    "octave": note_event.octave,
                    "note_with_octave": (
                        f"{note_event.note}"
                        f"{note_event.octave}"
                    ),
                    "confidence": note_event.confidence,
                }
            )

        return results

