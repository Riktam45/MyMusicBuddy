# Realtime backend requirement

The frontend realtime engine now calls:

`POST /api/v1/realtime/event`

with `session_id` and the current short `audio` window.

The endpoint must return the realtime event shape used by `src/realtime/microphone.ts`:

- `success`
- `active`
- `event_complete`
- `event_id`
- `note`
- `note_with_octave`
- `notes[]` (`note`, `octave`, `midi`, `frequency`, `confidence`)
- `chord`
- `confidence`
- optional `suggestions`

Important behavior:

1. Analyze only the current short window; never replay the whole session audio.
2. Detect multiple simultaneous pitches when possible.
3. Return the current note/chord immediately while sound is active.
4. Treat consecutive low-energy windows as an event boundary.
5. Silence finalizes the current event but does **not** end the listening session.
6. A later sound starts a new event using the same session.
7. Do not create an audio-analysis backlog.

A proposed FastAPI router implementation was generated separately from this frontend archive because the uploaded project is the frontend-only project.
