type ScaleRecommendation = {
    name: string;
    root: string;
    notes: string[];
    score?: number;
    reason?: string;
};


type ScaleRecommendationsProps = {
    scales: ScaleRecommendation[];
};


function ScaleRecommendations({
    scales,
}: ScaleRecommendationsProps) {
    if (!scales?.length) {
        return (
            <p className="mt-4 text-slate-500">
                No scale recommendations available.
            </p>
        );
    }

    return (
        <div className="mt-6 grid gap-4 md:grid-cols-3">

            {scales.map(
                (scale, index) => (
                    <div
                        key={`${scale.name}-${index}`}
                        className="rounded-2xl border border-slate-800 bg-slate-950 p-5 transition hover:border-violet-500/40"
                    >

                        <div className="flex items-start justify-between gap-4">

                            <div>
                                <h4 className="text-lg font-semibold text-white">
                                    {scale.name}
                                </h4>

                                <p className="mt-1 text-sm text-slate-400">
                                    Root: {scale.root}
                                </p>
                            </div>

                            {scale.score !== undefined && (
                                <span className="rounded-full bg-violet-600/15 px-3 py-1 text-xs text-violet-300">
                                    {(
                                        scale.score * 100
                                    ).toFixed(0)}
                                    %
                                </span>
                            )}

                        </div>


                        <div className="mt-5 flex flex-wrap gap-2">

                            {scale.notes.map(
                                (note, noteIndex) => (
                                    <span
                                        key={`${note}-${noteIndex}`}
                                        className={`rounded-lg px-3 py-1.5 text-sm font-medium ${
                                            note === scale.root
                                                ? "scale-root-note"
                                                : "bg-slate-900 text-slate-300"
                                        }`}
                                    >
                                        {note}
                                    </span>
                                )
                            )}

                        </div>


                        {scale.reason && (
                            <p className="mt-5 text-sm leading-6 text-slate-500">
                                {scale.reason}
                            </p>
                        )}

                    </div>
                )
            )}

        </div>
    );
}


export default ScaleRecommendations;