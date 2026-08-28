type IntervalResult = {
    root: string;
    note: string;
    semitones: number;
    name: string;
};


type IntervalListProps = {
    intervals: IntervalResult[];
};


function IntervalList({
    intervals,
}: IntervalListProps) {
    if (!intervals?.length) {
        return (
            <p className="mt-4 text-slate-500">
                No interval data available.
            </p>
        );
    }

    return (
        <div className="mt-6 overflow-hidden rounded-2xl border border-slate-800">

            {/* Header */}
            <div className="hidden grid-cols-[120px_120px_120px_minmax(0,1fr)] bg-slate-950 px-5 py-4 text-xs font-semibold uppercase tracking-wide text-slate-500 md:grid">
                <span>Root</span>
                <span>Note</span>
                <span>Semitones</span>
                <span>Interval</span>
            </div>


            {/* Rows */}
            <div>
                {intervals.map(
                    (
                        interval,
                        index,
                    ) => (
                        <div
                            key={`${interval.root}-${interval.note}-${index}`}
                            className="border-t border-slate-800 px-5 py-4"
                        >

                            {/* Desktop */}
                            <div className="hidden grid-cols-[120px_120px_120px_minmax(0,1fr)] items-center gap-0 md:grid">

                                <span className="font-semibold text-white">
                                    {interval.root}
                                </span>

                                <span className="font-medium text-violet-300">
                                    {interval.note}
                                </span>

                                <span className="text-slate-400">
                                    {interval.semitones}
                                </span>

                                <span className="interval-name font-medium">
                                    {interval.name}
                                </span>

                            </div>


                            {/* Mobile */}
                            <div className="grid grid-cols-2 gap-x-6 gap-y-3 md:hidden">

                                <div>
                                    <p className="text-xs uppercase tracking-wide text-slate-500">
                                        Root
                                    </p>

                                    <p className="mt-1 font-semibold text-white">
                                        {interval.root}
                                    </p>
                                </div>


                                <div>
                                    <p className="text-xs uppercase tracking-wide text-slate-500">
                                        Note
                                    </p>

                                    <p className="mt-1 font-medium text-violet-300">
                                        {interval.note}
                                    </p>
                                </div>


                                <div>
                                    <p className="text-xs uppercase tracking-wide text-slate-500">
                                        Semitones
                                    </p>

                                    <p className="mt-1 text-slate-400">
                                        {interval.semitones}
                                    </p>
                                </div>


                                <div>
                                    <p className="text-xs uppercase tracking-wide text-slate-500">
                                        Interval
                                    </p>

                                    <p className="interval-name mt-1 break-words font-medium">
                                        {interval.name}
                                    </p>
                                </div>

                            </div>

                        </div>
                    )
                )}
            </div>

        </div>
    );
}


export default IntervalList;