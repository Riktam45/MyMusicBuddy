# MyMusic Buddy — Frontend Redesign

This is a **separate frontend redesign** for MyMusic Buddy.

## Important

The original project frontend is intentionally untouched.

This folder is a standalone redesign that reuses the existing:
- authentication API
- music upload / URL API
- analysis API
- fretboard API
- existing analysis components
- realtime microphone functionality

## Design

The UI follows the supplied MyMusic Buddy screen recording:
- clean white layout
- black typography
- rounded pill buttons
- large editorial headings
- image feature cards
- About / Contact sections
- Social section without account URLs
- responsive phone/tablet/desktop layout

## Address

123 ABC street, Kolkata, West Bengal, 700049, India

## Run

```powershell
npm install
npm run dev
```

The API URLs currently point to the existing backend:

`http://127.0.0.1:8000/api/v1`

## Connection strategy

Keep this frontend separate until it has been fully verified. Then it can replace or be merged into the main frontend deliberately.
