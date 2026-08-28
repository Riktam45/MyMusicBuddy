type ChordSegment = {
    chord: string;
    start: number;
    end: number;
    confidence: number;
};


type ChordTimelineProps = {
    segments: ChordSegment[];
};


function formatTime(seconds: number) {
    const minutes = Math.floor(
        seconds / 60
    );

    const remainingSeconds =
        Math.floor(seconds % 60);

    return `${minutes}:${remainingSeconds
        .toString()
        .padStart(2, "0")}`;
}


function ChordTimeline({
    segments,
}: ChordTimelineProps) {
    if (!segments?.length) {
        return (
            <p className="mt-4 text-slate-500">
                No chord timeline available.
            </p>
        );
    }

    const totalDuration =
        Math.max(
            ...segments.map(
                (segment) => segment.end
            ),
            1,
        );

    return (
        <div className="mt-6">

            {/* Time labels */}
            <div className="mb-2 flex justify-between text-xs text-slate-500">
                <span>0:00</span>

                <span>
                    {formatTime(
                        totalDuration
                    )}
                </span>
            </div>


            {/* Timeline */}
            <div className="flex min-h-24 overflow-hidden rounded-xl border border-slate-800 bg-slate-950">

                {segments.map(
                    (
                        segment,
                        index,
                    ) => {
                        const duration =
                            segment.end -
                            segment.start;

                        const width =
                            (
                                duration /
                                totalDuration
                            ) * 100;

                        return (
                            <div
                                key={`${segment.start}-${index}`}
                                style={{
                                    width: `${width}%`,
                                }}
                                className="flex min-w-[70px] flex-col items-center justify-center border-r border-slate-800 bg-violet-600/15 px-3 text-center transition hover:bg-violet-600/25"
                            >

                                <span className="text-lg font-bold text-violet-300">
                                    {segment.chord}
                                </span>

                                <span className="mt-1 text-xs text-slate-500">
                                    {formatTime(
                                        segment.start
                                    )}
                                </span>

                            </div>
                        );
                    }
                )}

            </div>


            {/* Segment details */}
            <div className="mt-4 grid gap-2">

                {segments.map(
                    (
                        segment,
                        index,
                    ) => (
                        <div
                            key={`${segment.start}-detail-${index}`}
                            className="flex items-center justify-between rounded-lg bg-slate-900 px-4 py-3 text-sm"
                        >

                            <span className="font-medium text-white">
                                {segment.chord}
                            </span>

                            <span className="text-slate-500">
                                {formatTime(
                                    segment.start
                                )}
                                {" → "}
                                {formatTime(
                                    segment.end
                                )}
                            </span>

                            <span className="text-slate-400">
                                {(
                                    segment.confidence *
                                    100
                                ).toFixed(0)}
                                %
                            </span>

                        </div>
                    )
                )}

            </div>

        </div>
    );
}


export default ChordTimeline;