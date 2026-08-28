import { useEffect, useRef, useState } from "react";

import {
    analyzeRealtimeWindow,
    getRealtimeSessionId,
    startAudioCapture,
    startMicrophone,
    stopMicrophone,
    stopRealtimeSession,
    type RealtimeAnalysis,
} from "../realtime/microphone";

type EventResult = RealtimeAnalysis;

type SuggestionItem = {
    name?: string;
    root?: string;
    notes?: string[];
    intervals?: number[];
    description?: string;
    contains_note?: string;
};

type Suggestions = {
    chords?: SuggestionItem[];
    chord_progression?: string[];
    arpeggios?: SuggestionItem[];
    scales?: SuggestionItem[];
    intervals?: SuggestionItem[];
};

function RealtimePanel() {
    const [activeSuggestion, setActiveSuggestion] = useState<
        "chord" | "progression" | "arpeggio" | "scale" | null
    >(null);
    const [listening, setListening] = useState(false);
    const [result, setResult] = useState<EventResult | null>(null);
    const [suggestions, setSuggestions] = useState<Suggestions | null>(null);
    const [error, setError] = useState("");
    const [analyzing, setAnalyzing] = useState(false);
    const [eventCount, setEventCount] = useState(0);

    const latestChunk = useRef<Blob | null>(null);
    const processingLoop = useRef(false);
    const listeningRef = useRef(false);
    const mounted = useRef(true);
    const activeRequest = useRef<Promise<void> | null>(null);

    useEffect(() => {
        // React StrictMode may run an effect cleanup and then run the effect
        // again during development. Reset this flag on every mount/effect
        // setup so a previous cleanup cannot permanently disable UI updates.
        mounted.current = true;

        return () => {
            mounted.current = false;
            stopMicrophone();
        };
    }, []);

    const processLatestWindow = async () => {
        if (processingLoop.current || !listeningRef.current) return;

        const chunk = latestChunk.current;
        if (!chunk) return;

        latestChunk.current = null;
        processingLoop.current = true;
        setAnalyzing(true);

        const request = (async () => {
            try {
                const analysis = await analyzeRealtimeWindow(chunk);

                // Keep the final backend result available even when Stop is
                // clicked immediately after a sound was detected.
                if (!mounted.current) return;

                if (analysis.active || analysis.event_complete) {
                    setResult(analysis);
                }

                if (analysis.event_complete) {
                    setEventCount((count) => count + 1);
                }
            } catch (requestError) {
                console.error("Realtime event analysis failed:", requestError);
                if (mounted.current && listeningRef.current) {
                    setError(
                        requestError instanceof Error
                            ? requestError.message
                            : "Realtime analysis failed.",
                    );
                }
            } finally {
                processingLoop.current = false;
                setAnalyzing(false);
                activeRequest.current = null;
            }
        })();

        activeRequest.current = request;
        await request;

        if (latestChunk.current && listeningRef.current) {
            window.setTimeout(() => void processLatestWindow(), 0);
        }
    };

    const handleStart = async () => {
        try {
            setError("");
            setResult(null);
            setSuggestions(null);
            setEventCount(0);
            setActiveSuggestion(null);
            latestChunk.current = null;
            processingLoop.current = false;

            await startMicrophone();

            if (!getRealtimeSessionId()) {
                throw new Error("Realtime session was not created.");
            }

            listeningRef.current = true;
            setListening(true);

            startAudioCapture((chunk) => {
                latestChunk.current = chunk;
                window.setTimeout(() => void processLatestWindow(), 0);
            });
        } catch (startError) {
            console.error("Realtime microphone error:", startError);
            stopMicrophone();
            listeningRef.current = false;
            setListening(false);
            setError(
                startError instanceof Error
                    ? startError.message
                    : "Unable to start microphone.",
            );
        }
    };

    const handleStop = async () => {
        const sessionId = getRealtimeSessionId();

        // Stop creating new audio windows first, but keep the last request
        // alive long enough for the backend state to receive its result.
        stopMicrophone();
        listeningRef.current = false;
        latestChunk.current = null;
        setListening(false);
        setAnalyzing(false);

        try {
            if (activeRequest.current) {
                await activeRequest.current;
            }

            if (!sessionId) return;

            const finalResult = await stopRealtimeSession(sessionId);

            if (!mounted.current) return;

            // Prefer the backend's final snapshot. If it has no detected
            // pitch (for example, the user clicked Stop during silence),
            // keep the last successful live result already shown on screen.
            if (finalResult.note_with_octave || finalResult.chord) {
                setResult(finalResult);
            }

            if (finalResult.suggestions_ready && finalResult.suggestions) {
                setSuggestions(finalResult.suggestions as Suggestions);
                setActiveSuggestion("chord");
            } else {
                setSuggestions(null);
                setActiveSuggestion(null);
            }
        } catch (stopError) {
            console.error("Realtime stop/suggestion error:", stopError);
            if (mounted.current) {
                setError(
                    stopError instanceof Error
                        ? stopError.message
                        : "Unable to finish realtime analysis.",
                );
            }
        }
    };

    const displayTitle = result?.chord
        ? "CURRENT CHORD"
        : result?.note_with_octave
            ? "CURRENT NOTE"
            : "CURRENT MUSIC";

    const currentSuggestions = suggestions;

    return (
        <div className="rounded-2xl border border-slate-800 bg-slate-900 p-8">
            <div className="flex flex-col gap-2">
                <p className="text-sm font-medium text-violet-400">REAL-TIME MODE</p>
                <h3 className="text-2xl font-bold">Listen With MyMusic Buddy</h3>
                <p className="text-sm leading-6 text-slate-400">
                    Play a note or chord. The current note/chord updates while you play.
                    Stop listening to freeze the final result and generate musical suggestions.
                </p>
            </div>

            <div className="mt-6">
                {!listening ? (
                    <button
                        type="button"
                        onClick={handleStart}
                        className="rounded-xl bg-violet-600 px-6 py-3 font-semibold transition hover:bg-violet-500"
                    >
                        🎤 Start Listening
                    </button>
                ) : (
                    <button
                        type="button"
                        onClick={() => void handleStop()}
                        className="rounded-xl border border-red-500/40 bg-red-500/10 px-6 py-3 font-semibold text-red-300 transition hover:bg-red-500/20"
                    >
                        ⏹ Stop Listening
                    </button>
                )}
            </div>

            <div className="mt-5 flex items-center gap-3">
                <span
                    className={`h-3 w-3 rounded-full ${
                        listening ? "animate-pulse bg-emerald-400" : "bg-slate-600"
                    }`}
                />
                <span className="text-sm text-slate-400">
                    {listening
                        ? analyzing
                            ? "Analyzing current sound..."
                            : "Listening for music..."
                        : suggestions
                            ? "Final result ready — suggestions generated"
                            : "Microphone stopped"}
                </span>
            </div>

            {error && (
                <div className="mt-5 rounded-xl border border-red-500/30 bg-red-500/10 p-4 text-sm text-red-300">
                    {error}
                </div>
            )}

            <div className="mt-8 rounded-2xl border border-slate-800 bg-slate-950 p-8 text-center">
                {result?.chord || result?.note_with_octave ? (
                    <>
                        <p className="text-sm text-slate-500">{displayTitle}</p>
                        <p className="mt-3 text-6xl font-black tracking-tight text-violet-400 sm:text-7xl">
                            {result.chord ?? result.note_with_octave}
                        </p>

                        {result.notes.length > 0 && (
                            <div className="mt-5 flex flex-wrap justify-center gap-2">
                                {result.notes.map((note) => (
                                    <span
                                        key={`${note.midi}-${note.note}-${note.octave}`}
                                        className="rounded-full bg-slate-900 px-4 py-2 text-sm text-slate-300"
                                    >
                                        {note.note}{note.octave}
                                    </span>
                                ))}
                            </div>
                        )}

                        <div className="mt-8 grid gap-4 sm:grid-cols-3">
                            <div className="rounded-xl bg-slate-900 p-4">
                                <p className="text-xs uppercase tracking-wide text-slate-500">Confidence</p>
                                <p className="mt-2 text-lg font-semibold">
                                    {((result.confidence ?? 0) * 100).toFixed(1)}%
                                </p>
                            </div>
                            <div className="rounded-xl bg-slate-900 p-4">
                                <p className="text-xs uppercase tracking-wide text-slate-500">Notes Detected</p>
                                <p className="mt-2 text-lg font-semibold">{result.notes.length}</p>
                            </div>
                            <div className="rounded-xl bg-slate-900 p-4">
                                <p className="text-xs uppercase tracking-wide text-slate-500">Events</p>
                                <p className="mt-2 text-lg font-semibold">{eventCount}</p>
                            </div>
                        </div>

                        {currentSuggestions && (
                            <div className="mt-8 border-t border-slate-800 pt-8 text-left">
                                <div className="flex flex-wrap justify-center gap-3">
                                    <button
                                        type="button"
                                        onClick={() => setActiveSuggestion("chord")}
                                        className={`rounded-xl px-4 py-2 text-sm font-semibold transition ${
                                            activeSuggestion === "chord"
                                                ? "bg-violet-600 text-white"
                                                : "bg-slate-900 text-slate-300 hover:bg-slate-800"
                                        }`}
                                    >
                                        Chord
                                    </button>
                                    <button
                                        type="button"
                                        onClick={() => setActiveSuggestion("progression")}
                                        className={`rounded-xl px-4 py-2 text-sm font-semibold transition ${
                                            activeSuggestion === "progression"
                                                ? "bg-violet-600 text-white"
                                                : "bg-slate-900 text-slate-300 hover:bg-slate-800"
                                        }`}
                                    >
                                        Chord Progression
                                    </button>
                                    <button
                                        type="button"
                                        onClick={() => setActiveSuggestion("arpeggio")}
                                        className={`rounded-xl px-4 py-2 text-sm font-semibold transition ${
                                            activeSuggestion === "arpeggio"
                                                ? "bg-violet-600 text-white"
                                                : "bg-slate-900 text-slate-300 hover:bg-slate-800"
                                        }`}
                                    >
                                        Arpeggio
                                    </button>
                                    <button
                                        type="button"
                                        onClick={() => setActiveSuggestion("scale")}
                                        className={`rounded-xl px-4 py-2 text-sm font-semibold transition ${
                                            activeSuggestion === "scale"
                                                ? "bg-violet-600 text-white"
                                                : "bg-slate-900 text-slate-300 hover:bg-slate-800"
                                        }`}
                                    >
                                        Scale
                                    </button>
                                </div>

                                {activeSuggestion === "chord" && (
                                    <div className="mt-6 rounded-2xl border border-slate-800 bg-slate-900 p-6">
                                        <p className="text-xs uppercase tracking-wide text-violet-400">
                                            Chord Suggestions
                                        </p>
                                        <div className="mt-4 grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
                                            {currentSuggestions.chords?.map((item, index) => (
                                                <div key={`${item.name}-${index}`} className="rounded-xl bg-slate-950 p-4">
                                                    <h4 className="text-xl font-bold">{item.name}</h4>
                                                    {item.notes && (
                                                        <div className="mt-3 flex flex-wrap gap-2">
                                                            {item.notes.map((note) => (
                                                                <span key={note} className="rounded-lg bg-slate-900 px-3 py-2 text-sm text-slate-300">
                                                                    {note}
                                                                </span>
                                                            ))}
                                                        </div>
                                                    )}
                                                    {item.contains_note && (
                                                        <p className="mt-3 text-xs text-slate-500">
                                                            Contains detected note {item.contains_note}
                                                        </p>
                                                    )}
                                                </div>
                                            ))}
                                        </div>
                                    </div>
                                )}

                                {activeSuggestion === "progression" && (
                                    <div className="mt-6 rounded-2xl border border-slate-800 bg-slate-900 p-6">
                                        <p className="text-xs uppercase tracking-wide text-violet-400">Suggested Chord Progression</p>
                                        <div className="mt-4 flex flex-wrap items-center gap-3">
                                            {currentSuggestions.chord_progression?.map((chord, index) => (
                                                <span key={`${chord}-${index}`} className="rounded-xl bg-white px-4 py-3 text-lg font-semibold text-black">
                                                    {chord}
                                                </span>
                                            ))}
                                        </div>
                                    </div>
                                )}

                                {activeSuggestion === "arpeggio" && (
                                    <div className="mt-6 rounded-2xl border border-slate-800 bg-slate-900 p-6">
                                        <p className="text-xs uppercase tracking-wide text-violet-400">Arpeggio Suggestions</p>
                                        {currentSuggestions.arpeggios?.map((item, index) => (
                                            <div key={`${item.name}-${index}`} className="mt-4">
                                                <h4 className="text-xl font-bold">{item.name}</h4>
                                                {item.notes && (
                                                    <div className="mt-3 flex flex-wrap gap-2">
                                                        {item.notes.map((note) => (
                                                            <span key={note} className="rounded-lg bg-slate-950 px-3 py-2 text-sm">{note}</span>
                                                        ))}
                                                    </div>
                                                )}
                                                {item.description && <p className="mt-3 text-sm text-slate-400">{item.description}</p>}
                                            </div>
                                        ))}
                                    </div>
                                )}

                                {activeSuggestion === "scale" && (
                                    <div className="mt-6 rounded-2xl border border-slate-800 bg-slate-900 p-6">
                                        <p className="text-xs uppercase tracking-wide text-violet-400">Related Scales</p>
                                        {currentSuggestions.scales?.map((item, index) => (
                                            <div key={`${item.name}-${index}`} className="mt-4">
                                                <h4 className="text-xl font-bold">{item.name}</h4>
                                                {item.notes && (
                                                    <div className="mt-3 flex flex-wrap gap-2">
                                                        {item.notes.map((note) => (
                                                            <span key={note} className="rounded-lg bg-slate-950 px-3 py-2 text-sm">{note}</span>
                                                        ))}
                                                    </div>
                                                )}
                                                {item.description && <p className="mt-3 text-sm text-slate-400">{item.description}</p>}
                                            </div>
                                        ))}
                                    </div>
                                )}
                            </div>
                        )}
                    </>
                ) : (
                    <div className="py-8">
                        <p className="text-5xl">🎵</p>
                        <p className="mt-4 text-lg font-semibold text-slate-300">
                            {listening ? "Listening for a note or chord..." : "Start listening to detect music"}
                        </p>
                        <p className="mt-2 text-sm text-slate-500">
                            Play one note, several notes together, or a chord progression.
                        </p>
                    </div>
                )}
            </div>
        </div>
    );
}

export default RealtimePanel;
