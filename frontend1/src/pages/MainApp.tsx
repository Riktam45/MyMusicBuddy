import { useState, type ChangeEvent } from "react";
import { Link, useNavigate } from "react-router-dom";

import { analyzeSong } from "../api/analysis";
import { createSongFromUrl, uploadSong } from "../api/music";
import { logout } from "../api/authState";
import ChordTimeline from "../components/ChordTimeline";
import ScaleRecommendations from "../components/ScaleRecommendations";
import IntervalList from "../components/IntervalList";
import ArpeggioList from "../components/ArpeggioList";
import GuitarFretboard from "../components/GuitarFretboard";
import RealtimePanel from "../components/RealtimePanel";
import { getFretboard } from "../api/fretboard";

function MainApp() {
    const navigate = useNavigate();
    const [musicUrl, setMusicUrl] = useState("");
    const [selectedFile, setSelectedFile] = useState<File | null>(null);
    const [analyzing, setAnalyzing] = useState(false);
    const [error, setError] = useState("");
    const [song, setSong] = useState<any>(null);
    const [analysis, setAnalysis] = useState<any>(null);
    const [fretboard, setFretboard] = useState<any>(null);
    const [selectedScaleIndex, setSelectedScaleIndex] = useState(0);

    const handleLogout = () => {
        logout();
        navigate("/login", { replace: true });
    };

    const handleFileChange = (event: ChangeEvent<HTMLInputElement>) => {
        const file = event.target.files?.[0] ?? null;
        setSelectedFile(file);
        if (file) setMusicUrl("");
    };

    const handleScaleChange = async (index: number) => {
        const scale = analysis?.scale_recommendations?.[index];
        if (!scale) return;

        setSelectedScaleIndex(index);

        try {
            const result = await getFretboard({
                root: scale.root,
                scale: scale.name,
                notes: scale.notes,
            });
            setFretboard(result);
        } catch (requestError) {
            console.error("Fretboard loading failed:", requestError);
        }
    };

    const handleAnalyze = async () => {
        if (!musicUrl.trim() && !selectedFile) {
            setError("Please enter a music URL or select an audio file.");
            return;
        }

        setError("");
        setAnalyzing(true);
        setSong(null);
        setAnalysis(null);
        setFretboard(null);
        setSelectedScaleIndex(0);

        try {
            const songResult = selectedFile
                ? await uploadSong(selectedFile)
                : await createSongFromUrl(musicUrl.trim());

            setSong(songResult);

            if (!songResult?.id) {
                throw new Error("Song was created but no song ID was returned.");
            }

            const analysisResult = await analyzeSong(songResult.id);
            setAnalysis(analysisResult);

            const firstScale = analysisResult?.scale_recommendations?.[0];

            if (firstScale) {
                try {
                    const fretboardResult = await getFretboard({
                        root: firstScale.root,
                        scale: firstScale.name,
                        notes: firstScale.notes,
                    });
                    setFretboard(fretboardResult);
                } catch (requestError) {
                    console.error("Initial fretboard loading failed:", requestError);
                }
            }
        } catch (requestError: any) {
            console.error("Music analysis failed:", requestError);

            const message =
                requestError?.response?.data?.detail ||
                requestError?.message ||
                "Unable to analyze the music.";

            setError(message);
        } finally {
            setAnalyzing(false);
        }
    };

    return (
        <main className="mm-site mm-analysis min-h-screen bg-white text-neutral-950">
            <header className="sticky top-0 z-50 border-b border-neutral-200 bg-white/95 backdrop-blur">
                <div className="mx-auto flex min-h-[78px] max-w-[1650px] items-center justify-between px-5 sm:px-6">
                    <Link to="/" className="text-2xl font-black tracking-[-0.05em]">
                        MyMusicBuddy
                    </Link>

                    <nav className="hidden items-center gap-8 text-sm text-neutral-600 md:flex">
                        <Link to="/" className="hover:text-black">Home</Link>
                        <a href="/#about" className="hover:text-black">About</a>
                        <a href="/#contact" className="hover:text-black">Contact Us</a>
                    </nav>

                    <button
                        type="button"
                        onClick={handleLogout}
                        className="rounded-full border border-black px-5 py-2.5 text-sm font-bold transition hover:bg-black hover:text-white"
                    >
                        Logout
                    </button>
                </div>
            </header>

            <section className="border-b border-neutral-200 px-5 py-16 sm:px-6 sm:py-24">
                <div className="mx-auto max-w-[1100px]">
                    <p className="text-xs font-bold uppercase tracking-[0.28em] text-neutral-500">
                        Music intelligence
                    </p>
                    <h1 className="mt-5 max-w-4xl text-5xl font-black leading-[0.98] tracking-[-0.055em] sm:text-7xl">
                        Understand the song.
                        <br />
                        Play the idea.
                    </h1>
                    <p className="mt-7 max-w-2xl text-base leading-7 text-neutral-600 sm:text-lg">
                        Upload an audio file or paste a supported music URL.
                        MyMusic Buddy combines DSP analysis and Basic Pitch ML
                        to turn the recording into practical musical information.
                    </p>

                    <div className="mt-12 rounded-[28px] border border-neutral-200 bg-neutral-50 p-5 sm:p-8">
                        <label htmlFor="music-url" className="text-sm font-bold">
                            Music URL
                        </label>
                        <input
                            id="music-url"
                            type="url"
                            value={musicUrl}
                            onChange={(event) => setMusicUrl(event.target.value)}
                            placeholder="Paste a supported music URL..."
                            className="mt-3 w-full rounded-2xl border border-neutral-300 bg-white px-4 py-4 text-sm outline-none transition focus:border-black sm:text-base"
                        />

                        <div className="my-6 flex items-center gap-4 text-xs font-bold uppercase tracking-[0.2em] text-neutral-400">
                            <span className="h-px flex-1 bg-neutral-200" />
                            or
                            <span className="h-px flex-1 bg-neutral-200" />
                        </div>

                        <label
                            htmlFor="audio-file"
                            className="block cursor-pointer rounded-2xl border border-dashed border-neutral-300 bg-white px-5 py-9 text-center transition hover:border-black"
                        >
                            <span className="text-3xl">↑</span>
                            <span className="mt-3 block text-lg font-bold">
                                Upload Audio
                            </span>
                            <span className="mt-2 block text-sm text-neutral-500">
                                MP3, WAV and other supported audio files
                            </span>
                            {selectedFile && (
                                <span className="mt-4 block truncate text-sm font-semibold">
                                    Selected: {selectedFile.name}
                                </span>
                            )}
                        </label>

                        <input
                            id="audio-file"
                            type="file"
                            accept="audio/*"
                            onChange={handleFileChange}
                            className="hidden"
                        />

                        <button
                            type="button"
                            onClick={handleAnalyze}
                            disabled={analyzing || (!musicUrl.trim() && !selectedFile)}
                            className="mt-5 w-full rounded-full bg-black px-6 py-4 text-sm font-bold text-white transition hover:bg-neutral-800 disabled:cursor-not-allowed disabled:opacity-35"
                        >
                            {analyzing ? "Analyzing Music..." : "Analyze Music"}
                        </button>
                    </div>

                    {error && (
                        <div className="mt-6 rounded-2xl border border-red-200 bg-red-50 p-4 text-sm text-red-700">
                            {error}
                        </div>
                    )}
                </div>
            </section>

            {analysis ? (
                <section className="border-b border-neutral-200 px-5 py-16 sm:px-6 sm:py-24">
                    <div className="mx-auto max-w-[1250px]">
                        <div className="flex flex-col justify-between gap-5 border-b border-neutral-200 pb-8 sm:flex-row sm:items-end">
                            <div>
                                <p className="text-xs font-bold uppercase tracking-[0.28em] text-neutral-500">
                                    Analysis complete
                                </p>
                                <h2 className="mt-3 text-4xl font-black tracking-[-0.04em] sm:text-5xl">
                                    {song?.title || "Unknown Song"}
                                </h2>
                                <p className="mt-2 text-neutral-500">
                                    {song?.artist || "Unknown Artist"}
                                </p>
                            </div>
                            <div className="rounded-full border border-neutral-200 px-4 py-2 text-xs font-bold">
                                HYBRID DSP + ML
                            </div>
                        </div>

                        <div className="mt-10 grid gap-5 sm:grid-cols-2">
                            <StatCard label="BPM" value={analysis.bpm ?? "--"} />
                            <StatCard label="Key" value={analysis.key || "--"} />
                        </div>

                        <div className="mt-5 rounded-[28px] border border-neutral-200 bg-neutral-50 p-6 sm:p-8">
                            <SectionHeading
                                eyebrow="Machine learning"
                                title="Basic Pitch"
                                description="Automatic note events detected from the audio."
                            />
                            <div className="mt-7 grid gap-5 sm:grid-cols-3">
                                <StatCard label="Model" value={analysis.ml_model || "--"} compact />
                                <StatCard label="Detected Notes" value={analysis.ml_notes?.length ?? 0} compact />
                                <StatCard label="Pitch Classes" value={analysis.ml_pitch_classes?.length ?? 0} compact />
                            </div>

                            {analysis.ml_chord_candidates?.length > 0 && (
                                <div className="mt-7">
                                    <p className="text-xs font-bold uppercase tracking-[0.2em] text-neutral-500">
                                        ML chord candidates
                                    </p>
                                    <div className="mt-3 flex flex-wrap gap-2">
                                        {analysis.ml_chord_candidates.map((chord: string, index: number) => (
                                            <span
                                                key={`${chord}-${index}`}
                                                className="rounded-full border border-neutral-300 bg-white px-4 py-2 text-sm font-semibold"
                                            >
                                                {chord}
                                            </span>
                                        ))}
                                    </div>
                                </div>
                            )}
                        </div>

                        <ResultSection eyebrow="Harmony" title="Chord Timeline" description="Chord changes throughout the song.">
                            <ChordTimeline segments={analysis.chord_segments || []} />
                        </ResultSection>

                        <ResultSection eyebrow="Practice" title="Scale Recommendations" description="Scales that fit the detected musical key.">
                            <ScaleRecommendations scales={analysis.scale_recommendations || []} />
                        </ResultSection>

                        <ResultSection eyebrow="Theory" title="Intervals" description="Musical relationships between detected notes and the song's key.">
                            <IntervalList intervals={(analysis.intervals || []).slice(0, 50)} />
                            {analysis.intervals?.length > 50 && (
                                <p className="mt-4 text-sm text-neutral-500">
                                    Showing the first 50 interval events out of {analysis.intervals.length}.
                                </p>
                            )}
                        </ResultSection>

                        <ResultSection eyebrow="Technique" title="Arpeggios" description="Arpeggio patterns derived from detected chords.">
                            <ArpeggioList arpeggios={analysis.arpeggios || []} />
                        </ResultSection>

                        {analysis.scale_recommendations?.length > 0 && (
                            <ResultSection eyebrow="Guitar" title="Guitar Fretboard" description="Explore the selected scale across the guitar neck.">
                                <label
                                    htmlFor="fretboard-scale"
                                    className="text-sm font-bold"
                                >
                                    Choose Scale
                                </label>
                                <select
                                    id="fretboard-scale"
                                    value={selectedScaleIndex}
                                    onChange={(event) => handleScaleChange(Number(event.target.value))}
                                    className="mt-3 rounded-xl border border-neutral-300 bg-white px-4 py-3 text-sm font-semibold outline-none focus:border-black"
                                >
                                    {analysis.scale_recommendations.map((scale: any, index: number) => (
                                        <option key={`${scale.name}-${index}`} value={index}>
                                            {scale.root} {scale.name}
                                        </option>
                                    ))}
                                </select>

                                {fretboard && (
                                    <div className="mt-7">
                                        <GuitarFretboard
                                            positions={fretboard.positions || []}
                                            root={fretboard.root}
                                        />
                                    </div>
                                )}
                            </ResultSection>
                        )}
                    </div>
                </section>
            ) : (
                <section className="px-5 py-16 sm:px-6 sm:py-24">
                    <div className="mx-auto max-w-3xl rounded-[28px] border border-dashed border-neutral-300 p-10 text-center sm:p-16">
                        <p className="text-4xl">♪</p>
                        <h2 className="mt-5 text-2xl font-black">Your analysis workspace is ready.</h2>
                        <p className="mx-auto mt-3 max-w-xl text-sm leading-6 text-neutral-500">
                            Upload a song to reveal BPM, key, chords, scales,
                            intervals, arpeggios, fretboard positions and ML notes.
                        </p>
                    </div>
                </section>
            )}

            <section className="border-t border-neutral-200 bg-neutral-50 px-5 py-16 sm:px-6 sm:py-24">
                <div className="mx-auto max-w-[1250px]">
                    <SectionHeading
                        eyebrow="Live music"
                        title="Real-Time Mode"
                        description="Use your microphone to detect notes and pitch while you play or sing."
                    />
                    <div className="mm-realtime mt-8">
                        <RealtimePanel />
                    </div>
                </div>
            </section>

            <footer className="px-5 py-12 sm:px-6">
                <div className="mx-auto flex max-w-[1250px] flex-col gap-5 border-t border-neutral-200 pt-8 text-sm text-neutral-500 sm:flex-row sm:items-center sm:justify-between">
                    <span className="font-bold text-black">MyMusicBuddy</span>
                    <Link to="/" className="hover:text-black">Back to home ↑</Link>
                </div>
            </footer>
        </main>
    );
}

function StatCard({
    label,
    value,
    compact = false,
}: {
    label: string;
    value: string | number;
    compact?: boolean;
}) {
    return (
        <div className="rounded-[24px] border border-neutral-200 bg-white p-6">
            <p className="text-xs font-bold uppercase tracking-[0.2em] text-neutral-500">
                {label}
            </p>
            <p className={`mt-3 font-black tracking-[-0.04em] ${compact ? "text-2xl" : "text-5xl"}`}>
                {value}
            </p>
        </div>
    );
}

function SectionHeading({
    eyebrow,
    title,
    description,
}: {
    eyebrow: string;
    title: string;
    description: string;
}) {
    return (
        <div>
            <p className="text-xs font-bold uppercase tracking-[0.25em] text-neutral-500">
                {eyebrow}
            </p>
            <h3 className="mt-3 text-3xl font-black tracking-[-0.035em] sm:text-4xl">
                {title}
            </h3>
            <p className="mt-3 max-w-2xl text-sm leading-6 text-neutral-600">
                {description}
            </p>
        </div>
    );
}

function ResultSection({
    eyebrow,
    title,
    description,
    children,
}: {
    eyebrow: string;
    title: string;
    description: string;
    children: React.ReactNode;
}) {
    return (
        <section className="mm-result-section mt-5 rounded-[28px] border border-neutral-200 bg-white p-6 sm:p-8">
            <SectionHeading eyebrow={eyebrow} title={title} description={description} />
            <div className="mt-5">{children}</div>
        </section>
    );
}

export default MainApp;
