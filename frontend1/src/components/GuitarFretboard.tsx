import { useState } from "react";

type FretPosition = {
    string: number;
    fret: number;
    note: string;
};


type GuitarFretboardProps = {
    positions: FretPosition[];
    root: string;
};


const STRINGS = [6, 5, 4, 3, 2, 1];

const STRING_NAMES: Record<
    number,
    string
> = {
    6: "E",
    5: "A",
    4: "D",
    3: "G",
    2: "B",
    1: "e",
};

const FRETS = Array.from(
    { length: 25 },
    (_, index) => index,
);

const MARKER_FRETS = new Set([
    3,
    5,
    7,
    9,
    15,
    17,
    19,
    21,
]);

const DOUBLE_MARKER_FRETS = new Set([
    12,
    24,
]);


function GuitarFretboard({
    positions,
    root,
}: GuitarFretboardProps) {

    const [selectedNote, setSelectedNote] =
    useState<{
        string: number;
        fret: number;
        note: string;
    } | null>(null);

    const isHighlighted = (
        stringNumber: number,
        fretNumber: number,
    ) => {
        return positions.some(
            (position) =>
                position.string ===
                    stringNumber &&
                position.fret ===
                    fretNumber,
        );
    };

    const getNote = (
        stringNumber: number,
        fretNumber: number,
    ) => {
        const position =
            positions.find(
                (item) =>
                    item.string ===
                        stringNumber &&
                    item.fret ===
                        fretNumber,
            );

        return position?.note ?? "";
    };


    return (
        <div className="mt-8">

            {/* Legend */}
            <div className="mb-5 flex flex-wrap gap-5 text-sm">

                <div className="flex items-center gap-2">
                    <span className="h-4 w-4 rounded-full bg-violet-500" />

                    <span className="text-slate-400">
                        Root
                    </span>
                </div>


                <div className="flex items-center gap-2">
                    <span className="h-4 w-4 rounded-full bg-slate-700" />

                    <span className="text-slate-400">
                        Scale note
                    </span>
                </div>

            </div>


            {/* Horizontal scrolling container */}
            <div className="overflow-x-auto rounded-2xl border border-slate-800 bg-slate-950 p-5">

                <div className="min-w-[1250px]">

                    {/* Fret numbers */}
                    <div
                        className="ml-20 grid"
                        style={{
                            gridTemplateColumns:
                                "repeat(25, minmax(48px, 1fr))",
                        }}
                    >

                        {FRETS.map(
                            (fret) => (
                                <div
                                    key={fret}
                                    className="border-r border-slate-800 py-2 text-center text-xs text-slate-500"
                                >
                                    {fret}
                                </div>
                            ),
                        )}

                    </div>


                    {/* Guitar neck */}
                    <div className="mt-2">

                        {STRINGS.map(
                            (stringNumber) => (
                                <div
                                    key={stringNumber}
                                    className="flex h-16"
                                >

                                    {/* String name */}
                                    <div className="flex w-20 shrink-0 items-center justify-center">

                                        <div className="text-center">

                                            <div className="text-sm font-bold text-slate-300">
                                                {STRING_NAMES[
                                                    stringNumber
                                                ]}
                                            </div>

                                            <div className="text-[10px] text-slate-600">
                                                String{" "}
                                                {stringNumber}
                                            </div>

                                        </div>

                                    </div>


                                    {/* Frets */}
                                    <div
                                        className="grid flex-1"
                                        style={{
                                            gridTemplateColumns:
                                                "repeat(25, minmax(48px, 1fr))",
                                        }}
                                    >

                                        {FRETS.map(
                                            (fret) => {

                                                const highlighted =
                                                    isHighlighted(
                                                        stringNumber,
                                                        fret,
                                                    );

                                                const note =
                                                    getNote(
                                                        stringNumber,
                                                        fret,
                                                    );

                                                const isRoot =
                                                    highlighted &&
                                                    note === root;

                                                const isSelected =
                                                    selectedNote?.string ===
                                                        stringNumber &&
                                                    selectedNote?.fret ===
                                                        fret;    
                                                

                                                const isSingleMarker =
                                                    MARKER_FRETS.has(
                                                        fret,
                                                    );

                                                const isDoubleMarker =
                                                    DOUBLE_MARKER_FRETS.has(
                                                        fret,
                                                    );

                                                return (
                                                    <div
                                                        key={`${stringNumber}-${fret}`}
                                                        className="relative flex items-center justify-center border-r border-slate-700"
                                                    >

                                                        {/* Fret marker */}
                                                        {(
                                                            isSingleMarker ||
                                                            isDoubleMarker
                                                        ) && (
                                                            <div className="pointer-events-none absolute inset-0 flex items-center justify-center">

                                                                {isDoubleMarker ? (
                                                                    <div className="flex flex-col gap-3">
                                                                        <span className="h-2.5 w-2.5 rounded-full bg-slate-800" />
                                                                        <span className="h-2.5 w-2.5 rounded-full bg-slate-800" />
                                                                    </div>
                                                                ) : (
                                                                    <span className="h-2.5 w-2.5 rounded-full bg-slate-800" />
                                                                )}

                                                            </div>
                                                        )}


                                                        {/* Guitar string */}
                                                        <div
                                                            className="pointer-events-none absolute left-0 right-0 top-1/2 h-px bg-slate-600"
                                                        />


                                                        {/* Nut */}
                                                        {fret === 0 && (
                                                            <div className="pointer-events-none absolute right-0 top-0 h-full w-1 bg-slate-500" />
                                                        )}


                                                        {/* Note */}
                                                        {highlighted && (
                                                            <button
                                                                type="button"
                                                                onClick={() => {
                                                                    setSelectedNote({
                                                                        string: stringNumber,
                                                                        fret: fret,
                                                                        note: note,
                                                                    });
                                                                }}
                                                                className={`relative z-10 flex h-10 w-10 items-center justify-center rounded-full text-xs font-bold shadow-lg transition hover:scale-110 ${
                                                                    isSelected
                                                                        ? "bg-amber-400 text-slate-950 ring-2 ring-white/60"
                                                                        : isRoot
                                                                            ? "bg-violet-500 text-white ring-2 ring-violet-300/40"
                                                                            : "bg-slate-700 text-slate-100"
                                                                }`}
                                                                title={`${note} — String ${stringNumber}, Fret ${fret}`}
                                                            >
                                                                {note}
                                                            </button>
                                                        )}

                                                        {selectedNote && (
                                                            <div className="mt-5 rounded-xl border border-violet-500/30 bg-violet-500/10 p-5">

                                                                <p className="text-sm text-violet-300">
                                                                    Selected Note
                                                                </p>

                                                                <div className="mt-3 flex flex-wrap items-end gap-6">

                                                                    <div>
                                                                        <p className="text-xs text-slate-500">
                                                                            Note
                                                                        </p>

                                                                        <p className="text-3xl font-bold text-white">
                                                                            {selectedNote.note}
                                                                        </p>
                                                                    </div>

                                                                    <div>
                                                                        <p className="text-xs text-slate-500">
                                                                            String
                                                                        </p>

                                                                        <p className="text-lg font-semibold text-slate-200">
                                                                            {STRING_NAMES[
                                                                                selectedNote.string
                                                                            ]}{" "}
                                                                            ({selectedNote.string})
                                                                        </p>
                                                                    </div>

                                                                    <div>
                                                                        <p className="text-xs text-slate-500">
                                                                            Fret
                                                                        </p>

                                                                        <p className="text-lg font-semibold text-slate-200">
                                                                            {selectedNote.fret}
                                                                        </p>
                                                                    </div>

                                                                </div>

                                                                <button
                                                                    type="button"
                                                                    onClick={() =>
                                                                        setSelectedNote(null)
                                                                    }
                                                                    className="mt-4 text-sm text-slate-400 transition hover:text-white"
                                                                >
                                                                    Clear selection
                                                                </button>

                                                            </div>
                                                        )}

                                                    </div>
                                                );
                                            },
                                        )}

                                    </div>

                                </div>
                            ),
                        )}

                    </div>


                    {/* Fret markers under neck */}
                    <div className="ml-20 grid">
                        <div
                            className="grid"
                            style={{
                                gridTemplateColumns:
                                    "repeat(25, minmax(48px, 1fr))",
                            }}
                        >
                            {FRETS.map(
                                (fret) => (
                                    <div
                                        key={`marker-${fret}`}
                                        className="h-7 border-r border-transparent"
                                    />
                                ),
                            )}
                        </div>
                    </div>

                </div>

            </div>


            {/* Note summary */}
            <div className="mt-5 rounded-xl border border-slate-800 bg-slate-950 p-5">

                <p className="text-sm text-slate-500">
                    Selected scale notes
                </p>

                <div className="mt-3 flex flex-wrap gap-2">

                    {Array.from(
                        new Set(
                            positions.map(
                                (position) =>
                                    position.note,
                            ),
                        ),
                    ).map(
                        (note) => (
                            <span
                                key={note}
                                className={
                                    note === root
                                        ? "rounded-lg bg-violet-500 px-3 py-1.5 text-sm font-semibold text-white"
                                        : "rounded-lg bg-slate-800 px-3 py-1.5 text-sm font-medium text-slate-300"
                                }
                            >
                                {note}
                            </span>
                        ),
                    )}

                </div>

            </div>

        </div>
    );
}


export default GuitarFretboard;