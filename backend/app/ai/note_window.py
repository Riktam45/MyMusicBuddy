def notes_in_window(
    note_events,
    start: float,
    end: float,
):
    """
    Return notes whose detection time falls
    inside the requested time window.
    """

    return [
        note
        for note in note_events
        if start <= note.time < end
    ]