type ArpeggioResult = {
    name: string;
    root: string;
    notes: string[];
    intervals: string[];
};


type ArpeggioListProps = {
    arpeggios: ArpeggioResult[];
};


function ArpeggioList({
    arpeggios,
}: ArpeggioListProps) {
    if (!arpeggios?.length) {
        return (
            <p className="mt-4 text-slate-500">
                No arpeggios detected.
            </p>
        );
    }

    return (
        <div className="mt-6 grid gap-5 lg:grid-cols-2">

            {arpeggios.map(
                (
                    arpeggio,
                    index,
                ) => (
                    <div
                        key={`${arpeggio.name}-${arpeggio.root}-${index}`}
                        className="rounded-2xl border border-slate-800 bg-slate-950 p-6"
                    >

                        {/* Header */}
                        <div className="flex items-center justify-between">

                            <div>
                                <p className="text-xs font-semibold uppercase tracking-wide text-slate-500">
                                    Arpeggio
                                </p>

                                <h4 className="mt-1 text-xl font-bold capitalize text-white">
                                    {arpeggio.name}
                                </h4>
                            </div>


                            <div className="arpeggio-root-circle flex h-10 w-10 items-center justify-center rounded-full text-sm font-bold">
                                {arpeggio.root}
                            </div>

                        </div>


                        {/* Notes */}
                        <div className="mt-7">

                            <p className="text-sm font-medium text-slate-400">
                                Notes
                            </p>

                            <div className="mt-3 flex flex-wrap gap-2">

                                {arpeggio.notes.map(
                                    (
                                        note,
                                        noteIndex,
                                    ) => (
                                        <span
                                            key={`${note}-${noteIndex}`}
                                            className={`rounded-xl px-4 py-2 text-sm font-semibold ${
                                                note ===
                                                arpeggio.root
                                                    ? "arpeggio-root-note"
                                                    : "bg-slate-900 text-slate-300"
                                            }`}
                                        >
                                            {note}
                                        </span>
                                    )
                                )}

                            </div>

                        </div>


                        {/* Intervals */}
                        <div className="mt-7">

                            <p className="text-sm font-medium text-slate-400">
                                Intervals
                            </p>

                            <div className="mt-3 flex flex-wrap gap-2">

                                {arpeggio.intervals.map(
                                    (
                                        interval,
                                        intervalIndex,
                                    ) => (
                                        <span
                                            key={`${interval}-${intervalIndex}`}
                                            className="max-w-full break-words rounded-full bg-slate-900 px-3 py-1.5 text-xs text-slate-300"
                                        >
                                            {interval}
                                        </span>
                                    )
                                )}

                            </div>

                        </div>

                    </div>
                )
            )}

        </div>
    );
}


export default ArpeggioList;