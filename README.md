# MyMusicBuddy 🎵

MyMusicBuddy is an AI-powered music analysis application designed to help musicians understand and explore music through automatic note detection, chord analysis, scales, arpeggios, intervals, fretboard visualization, and real-time audio analysis.

The project combines a React/Vite frontend with a Python/FastAPI backend and machine-learning-assisted music analysis.

---

## ✨ Features

### 🎧 Real-Time Music Detection
- Detect musical notes from microphone input
- Detect current pitch and octave
- Detect multiple simultaneous notes
- Detect chords from incoming audio
- Display confidence scores
- Real-time event processing

### 🎼 Music Analysis
- Note detection
- Chord detection
- Chord progression suggestions
- Scale recommendations
- Arpeggio suggestions
- Interval analysis
- Key/scale analysis
- BPM and beat-related analysis

### 🎸 Guitar Fretboard
- Visualize detected notes
- Display relevant fretboard positions
- Explore scales and musical relationships on the guitar

### 🤖 Machine Learning
MyMusicBuddy integrates **Spotify Basic Pitch** for automatic music transcription and pitch detection.

Basic Pitch is a lightweight neural-network-based Automatic Music Transcription (AMT) system developed by Spotify's Audio Intelligence Lab.

It can analyze audio and estimate:
- Musical notes
- Note onset and offset
- Pitch
- Multiple simultaneous notes
- Pitch bends

Basic Pitch is designed to work with polyphonic audio and is instrument-agnostic, although it performs best when the recording primarily contains one instrument.

---

# 🤖 Machine Learning Model

## Spotify Basic Pitch

**Model:** Basic Pitch

**Developer:** Spotify Audio Intelligence Lab

**Purpose:** Automatic Music Transcription (AMT)

**Primary task:** Audio → Musical Note / MIDI transcription

**Repository:**
https://github.com/spotify/basic-pitch

**Model / Package:**
https://huggingface.co/spotify/basic-pitch

**PyPI:**
https://pypi.org/project/basic-pitch/

**Research Paper:**
https://arxiv.org/abs/2203.09893

### What Basic Pitch Does

Basic Pitch takes an audio recording as input and estimates musical note events.

Conceptually:

Audio
   ↓
Audio preprocessing
   ↓
Basic Pitch neural network
   ↓
Pitch / note detection
   ↓
Note events
   ↓
MyMusicBuddy music-analysis pipeline
   ↓
Notes / Chords / Scales / Arpeggios / Intervals

The model can work with common audio formats such as:

- WAV
- MP3
- OGG
- FLAC
- M4A

Audio is internally processed at a 22050 Hz sample rate.

---

# 📥 Installing / Downloading the ML Model

You normally do **not** need to manually download a large model archive.

Install Basic Pitch through PyPI:

```bash
pip install basic-pitch
Official package:
https://pypi.org/project/basic-pitch/

Official source repository:
https://github.com/spotify/basic-pitch

The Basic Pitch package contains the supported model runtime and model files.
Depending on the operating system and installed runtime, Basic Pitch can use different model formats including:

TensorFlow

CoreML

TensorFlow Lite

ONNX

For Windows environments, the project documentation supports ONNX as a model runtime.

👨‍🔬 Basic Pitch Authors
The Basic Pitch research paper is:
"A Lightweight Instrument-Agnostic Model for Polyphonic Note Transcription and Multipitch Estimation"

Authors:

Rachel M. Bittner

Juan José Bosch

David Rubinstein

Gabriel Meseguer-Brocal

Sebastian Ewert

Published at:
IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP), 2022

Citation
Code snippet
@inproceedings{2022_BittnerBRME_LightweightNoteTranscription_ICASSP,
  author = {
    Bittner, Rachel M. and
    Bosch, Juan Jos\'e and
    Rubinstein, David and
    Meseguer-Brocal, Gabriel and
    Ewert, Sebastian
  },
  title = {
    A Lightweight Instrument-Agnostic Model for
    Polyphonic Note Transcription and Multipitch Estimation
  },
  booktitle = {
    Proceedings of the IEEE International Conference on
    Acoustics, Speech and Signal Processing (ICASSP)
  },
  address = {Singapore},
  year = {2022}
}
🧠 MyMusicBuddy ML Pipeline
MyMusicBuddy does not rely exclusively on the ML model.
The project uses a combination of machine-learning and music-signal-processing techniques.

A simplified pipeline is:

                 Audio Input
                     │
                     ▼
              Audio Processing
                     │
                     ▼
             ┌───────────────┐
             │ Basic Pitch   │
             │ ML Model      │
             └───────────────┘
                     │
                     ▼
               Note Events
                     │
          ┌──────────┼──────────┐
          ▼          ▼          ▼
       Pitch       Notes      Timing
          │          │          │
          └──────────┼──────────┘
                     ▼
              Music Analysis
                     │
       ┌─────────────┼─────────────┐
       ▼             ▼             ▼
     Chords        Scales       Intervals
       │             │             │
       ▼             ▼             ▼
   Progressions   Arpeggios    Fretboard
                     │
                     ▼
                User Interface
The ML transcription stage is integrated into the larger MyMusicBuddy analysis pipeline rather than being the entire application.

🗂️ Project Structure
MyMusicBuddy/
│
├── ai-engine/
│
├── backend/
│   ├── app/
│   │   ├── ai/
│   │   ├── analysis/
│   │   ├── api/
│   │   ├── auth/
│   │   ├── fretboard/
│   │   ├── music/
│   │   ├── playlists/
│   │   ├── realtime/
│   │   └── users/
│   │
│   ├── requirements.txt
│   └── ...
│
├── frontend1/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── realtime/
│   │   └── api/
│   ├── package.json
│   └── ...
│
├── ml/
│   ├── basic_pitch/
│   ├── hybrid/
│   ├── evaluation/
│   └── service.py
│
├── README.md
├── LICENSE
└── .gitignore
⚙️ Installation
Backend
Create a virtual environment:

Bash
python -m venv .venv
Activate it on Windows:

PowerShell
.venv\Scripts\Activate.ps1
Install dependencies:

Bash
pip install -r backend/requirements.txt
Install Basic Pitch if it is not already included:

Bash
pip install basic-pitch
Frontend
Navigate to the frontend:

Bash
cd frontend1
Install dependencies:

Bash
npm install
Run the development server:

Bash
npm run dev
🎤 Real-Time Mode
MyMusicBuddy provides a real-time microphone analysis mode.

The workflow is:

Microphone
    ↓
Audio Capture
    ↓
Audio Windows
    ↓
Backend Analysis API
    ↓
Pitch / Note Detection
    ↓
Chord Analysis
    ↓
Realtime Result
    ↓
Frontend
The interface continuously updates the currently detected musical event.
When the user stops listening, the backend finalizes the current analysis and generates additional musical suggestions.

🔐 Environment Variables
Do not commit private credentials, API keys, database passwords, or secret keys.

Create your local environment file from the provided example:

Bash
cp backend/.env.example backend/.env
On Windows PowerShell:

PowerShell
Copy-Item backend/.env.example backend/.env
Fill in the required values locally.
The .env file should remain untracked.

📦 Large Datasets
Large datasets and generated audio files are intentionally not included in the Git repository.
For example, the MAPS evaluation dataset and large WAV files may require separate downloading/storage.
This keeps the Git repository lightweight and makes cloning the source code significantly faster.
If you need the evaluation dataset, download it separately and place it in the expected directory described by the ML evaluation scripts.

📊 Evaluation
The project contains ML evaluation utilities under:

ml/evaluation/
These include tools for:

Ground-truth comparison

Note comparison

Prediction generation

Evaluation metrics

MAPS dataset evaluation

Large evaluation datasets are excluded from the Git repository.

⚖️ Third-Party ML Attribution
MyMusicBuddy uses Spotify Basic Pitch as a third-party machine-learning component.
Basic Pitch is developed by Spotify Audio Intelligence Lab.
Basic Pitch is released under the Apache License 2.0.

Copyright:

Copyright 2022 Spotify AB
For the complete license terms, see:
https://github.com/spotify/basic-pitch/blob/main/LICENSE

Please refer to the official Basic Pitch repository and research paper for the complete attribution and licensing information.

📚 References
Basic Pitch:
https://github.com/spotify/basic-pitch

Basic Pitch Model:
https://huggingface.co/spotify/basic-pitch

PyPI:
https://pypi.org/project/basic-pitch/

Research Paper:
https://arxiv.org/abs/2203.09893

Spotify Engineering:
https://engineering.atspotify.com/2022/6/meet-basic-pitch

👨‍💻 MyMusicBuddy
Project: MyMusicBuddy
Developer: Riktam45
GitHub:
https://github.com/Riktam45/MyMusicBuddy

📄 License
This project is distributed under the license included in this repository.
Third-party software and models may have their own licenses and attribution requirements.
Please review the respective third-party licenses before redistributing or modifying those components.

One correction I'd make to your wording
Don't call Basic Pitch "your ML model" in the README.

Call it:

"Third-party ML model used by MyMusicBuddy: Spotify Basic Pitch."

That's important because you integrated the model into MyMusicBuddy; you didn't author Basic Pitch itself. Spotify's official documentation confirms the model was developed by its Audio Intelligence Lab, and lists the research authors.

Also, the Hugging Face model page is a better "ML model download" destination than inventing a direct model-file URL. The official Basic Pitch package can also install the model/runtime through pip.

Basic Pitch — GitHub

Basic Pitch — Hugging Face Model

Basic Pitch — PyPI

Basic Pitch Research Paper
