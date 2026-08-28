let audioContext: AudioContext | null = null;
let microphoneStream: MediaStream | null = null;
let mediaRecorder: MediaRecorder | null = null;
let realtimeSessionId: string | null = null;

const REALTIME_API = "http://127.0.0.1:8000/api/v1/realtime";

function getSupportedMimeType(): string {
    const mimeTypes = [
        "audio/webm;codecs=opus",
        "audio/webm",
        "audio/ogg;codecs=opus",
        "audio/ogg",
    ];

    for (const mimeType of mimeTypes) {
        if (MediaRecorder.isTypeSupported(mimeType)) {
            return mimeType;
        }
    }

    throw new Error(
        "No supported microphone recording format was found."
    );
}

function createSessionId(): string {
    if (typeof crypto !== "undefined" && crypto.randomUUID) {
        return crypto.randomUUID();
    }

    return `${Date.now()}-${Math.random()}`;
}

export async function startMicrophone() {
    if (!navigator.mediaDevices?.getUserMedia) {
        throw new Error(
            "Microphone access is not supported by this browser."
        );
    }

    realtimeSessionId = createSessionId();

    microphoneStream = await navigator.mediaDevices.getUserMedia({
        audio: {
            echoCancellation: false,
            noiseSuppression: false,
            autoGainControl: false,
            channelCount: 1,
        },
    });

    audioContext = new AudioContext();
    await audioContext.resume();

    const source = audioContext.createMediaStreamSource(
        microphoneStream
    );

    console.log("Realtime session:", realtimeSessionId);
    console.log("Microphone started.");

    return {
        audioContext,
        source,
        stream: microphoneStream,
    };
}

/**
 * Capture short rolling windows. The recorder emits every 200 ms,
 * but the callback receives a ~250 ms analysis window. The realtime
 * UI decides which window to analyze; it never builds a backlog.
 */
export function startAudioCapture(
    onChunk: (chunk: Blob) => void,
) {
    if (!microphoneStream) {
        throw new Error("Microphone is not started.");
    }

    const mimeType = getSupportedMimeType();

    mediaRecorder = new MediaRecorder(microphoneStream, {
        mimeType,
    });

    // IMPORTANT:
    // WebM/Opus MediaRecorder output is a container stream. A later
    // MediaRecorder data chunk may not contain the WebM initialization
    // segment by itself. Sending only the newest chunks can therefore make
    // FFmpeg reject the request even though the microphone is working.
    //
    // Keep the first chunk (which contains the stream initialization) and
    // combine it with only the newest media chunks. This gives us a fresh
    // rolling analysis window without building a stale backlog.
    const chunkBuffer: Blob[] = [];
    let initializationChunk: Blob | null = null;
    let bufferStartTime = 0;

    mediaRecorder.onstart = () => {
        bufferStartTime = performance.now();
        console.log("MediaRecorder started.");
    };

    mediaRecorder.ondataavailable = (event: BlobEvent) => {
        if (event.data.size === 0) {
            return;
        }

        if (!initializationChunk) {
            initializationChunk = event.data;
        }

        chunkBuffer.push(event.data);

        // Keep only a short rolling tail. The initialization chunk is
        // retained separately so every request remains independently
        // decodable by the backend.
        if (chunkBuffer.length > 4) {
            chunkBuffer.shift();
        }

        const elapsed = performance.now() - bufferStartTime;

        if (elapsed >= 250 && initializationChunk) {
            const newestChunks = chunkBuffer.filter(
                (chunk) => chunk !== initializationChunk,
            );

            const analysisWindow = new Blob(
                [initializationChunk, ...newestChunks],
                { type: mimeType },
            );

            bufferStartTime = performance.now();

            onChunk(analysisWindow);
        }
    };

    mediaRecorder.onerror = (event) => {
        console.error("MediaRecorder error:", event);
    };

    mediaRecorder.onstop = () => {
        chunkBuffer.length = 0;
        initializationChunk = null;
        console.log("MediaRecorder stopped.");
    };

    mediaRecorder.start(100);
}

export function stopAudioCapture() {
    if (!mediaRecorder) {
        return;
    }

    if (mediaRecorder.state !== "inactive") {
        mediaRecorder.stop();
    }

    mediaRecorder = null;
}

export function stopMicrophone() {
    stopAudioCapture();

    microphoneStream?.getTracks().forEach((track) => track.stop());
    microphoneStream = null;

    if (audioContext) {
        void audioContext.close();
        audioContext = null;
    }

    realtimeSessionId = null;
    console.log("Microphone completely stopped.");
}

export type RealtimeNote = {
    note: string;
    octave: number;
    midi: number;
    frequency: number;
    confidence: number;
};

export type RealtimeAnalysis = {
    success: boolean;
    active: boolean;
    event_complete: boolean;
    event_id: number;
    note: string | null;
    note_with_octave: string | null;
    notes: RealtimeNote[];
    chord: string | null;
    confidence: number;
    suggestions_ready?: boolean;
    suggestions?: {
        scales?: unknown[];
        intervals?: unknown[];
        arpeggios?: unknown[];
        chord_progression?: string[];
    };
    message?: string;
};

/**
 * Latest-only realtime request. The caller should not queue audio while
 * a request is running. The backend receives one current window at a time.
 */
export async function analyzeRealtimeWindow(
    chunk: Blob,
): Promise<RealtimeAnalysis> {
    const startTime = performance.now();
    const formData = new FormData();

    formData.append("session_id", realtimeSessionId ?? "");
    formData.append("audio", chunk, "realtime.webm");

    const response = await fetch(`${REALTIME_API}/event`, {
        method: "POST",
        body: formData,
    });

    if (!response.ok) {
        throw new Error(
            `Realtime event analysis failed: ${response.status}`
        );
    }

    const result = (await response.json()) as RealtimeAnalysis;

    console.log(
        "Realtime event latency:",
        `${(performance.now() - startTime).toFixed(1)} ms`,
        result,
    );

    return result;
}

export type RealtimeStopResult = RealtimeAnalysis & {
    suggestions_ready: boolean;
};

export async function stopRealtimeSession(
    sessionId: string,
): Promise<RealtimeStopResult> {
    const formData = new FormData();
    formData.append("session_id", sessionId);

    const response = await fetch(`${REALTIME_API}/stop`, {
        method: "POST",
        body: formData,
    });

    // Read the response body even for an HTTP error so the actual backend
    // detail is visible to the UI instead of becoming a generic fetch error.
    const rawBody = await response.text();
    let body: unknown = null;

    try {
        body = rawBody ? JSON.parse(rawBody) : null;
    } catch {
        body = null;
    }

    if (!response.ok) {
        const detail =
            typeof body === "object" &&
            body !== null &&
            "detail" in body
                ? String((body as { detail?: unknown }).detail)
                : rawBody;

        throw new Error(
            `Realtime session stop failed: ${response.status}${detail ? ` - ${detail}` : ""}`
        );
    }

    if (!body || typeof body !== "object") {
        throw new Error("Realtime stop returned an empty or invalid response.");
    }

    return body as RealtimeStopResult;
}

/** Backwards-compatible name for existing callers. */
export const analyzeAudioChunk = analyzeRealtimeWindow;

export function getRealtimeSessionId() {
    return realtimeSessionId;
}
