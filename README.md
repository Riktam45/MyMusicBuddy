# 🎵 MyMusicBuddy

> An AI-powered music analysis platform that helps musicians understand notes, chords, scales, intervals, arpeggios, chord progressions, and musical structure from audio.

---

# 👨‍💻 Authors

- **Riktam Das**
- **MyMusicBuddy Development Team**

GitHub: https://github.com/Riktam45

Project Repository: https://github.com/Riktam45/MyMusicBuddy

---

# 📌 About MyMusicBuddy

**MyMusicBuddy** is a full-stack AI-assisted music analysis application designed for musicians, music learners, guitar players, and music enthusiasts.

The application combines:

- 🎵 Real-time note detection
- 🎸 Chord detection
- 🎼 Scale recommendations
- 🎹 Chord progression suggestions
- 🎶 Arpeggio suggestions
- 📐 Interval analysis
- 🎸 Guitar fretboard visualization
- 🎧 Full-song audio analysis
- ⚡ Real-time microphone analysis
- 🤖 Machine-learning-assisted pitch analysis
- 🔐 User authentication
- 📊 Music analysis results

The project uses a hybrid approach combining **Digital Signal Processing (DSP), music theory algorithms, and machine learning**.

---

# ✨ Features

## 🎤 Real-Time Music Detection

MyMusicBuddy can listen to audio through the user's microphone and analyze the currently playing musical event.

The real-time system can detect:

- Musical notes
- Note + octave
- Chords
- Detected notes
- Confidence score
- Musical events

Example result:

A#2

Confidence: 44.4%

The real-time system continuously analyzes short audio windows and updates the detected musical information while the user is playing.

When the user stops listening, the application freezes the final result and generates musical suggestions.

---

## 🎼 Chord Detection

The application analyzes detected notes and determines possible chords.

Chord analysis includes:

- Major chords
- Minor chords
- Extended chords
- Chord candidates
- Chord formatting
- Chord interval analysis
- Chord smoothing
- Chord segmentation

The system attempts to provide musically meaningful chord interpretations rather than relying only on raw pitch detection.

---

## 🎹 Chord Progression Suggestions

After analyzing a musical event, MyMusicBuddy can generate suggested chord progressions.

Example:

C → G → Am → F

Chord progression suggestions can help musicians:

- Compose songs
- Experiment with harmony
- Find compatible chords
- Understand harmonic relationships
- Develop new musical ideas

---

## 🎶 Arpeggio Analysis

The project includes an arpeggio analysis and generation system.

It can provide:

- Arpeggio candidates
- Arpeggio suggestions
- Notes contained in an arpeggio
- Arpeggio descriptions
- Chord-to-arpeggio relationships

---

## 🎵 Scale Recommendations

Based on detected musical information, the system can recommend related scales.

The scale engine can work with:

- Detected notes
- Chord information
- Intervals
- Musical context

This is useful for:

- Improvisation
- Solo development
- Music theory learning
- Understanding which scales may fit a musical idea

---

## 📐 Interval Analysis

The application analyzes the interval relationships between detected notes.

It includes:

- Interval detection
- Interval schemas
- Interval analysis
- Interval recommendations
- Musical interval relationships

---

## 🎸 Guitar Fretboard

MyMusicBuddy includes an interactive guitar fretboard system.

The fretboard can be used to visualize:

- Notes
- Chords
- Scales
- Musical positions

This helps guitar players connect detected musical information with practical fingerboard positions.

---

# 🤖 Machine Learning

MyMusicBuddy uses machine learning as part of its music-analysis pipeline.

The ML system is integrated with the backend through adapters and services.

The project contains the following ML structure:

ml/
├── basic_pitch/
│   ├── inference.py
│   └── schema.py
│
├── hybrid/
│   ├── engine.py
│   └── schema.py
│
├── evaluation/
│   ├── ground_truth.py
│   ├── metrics.py
│   ├── note_comparison.py
│   ├── prediction.py
│   └── maps_evaluate.py
│
├── schema.py
└── service.py

The backend also contains ML integration components:

backend/app/ai/
├── ml_arpeggio_adapter.py
├── ml_chord_adapter.py
├── ml_context.py
├── ml_interval_adapter.py
├── ml_note_schema.py
└── ml_scale_adapter.py

These components allow the machine-learning layer to work together with the project's music-analysis engines.

---

# 🧠 Basic Pitch Model

The project uses the **Spotify Basic Pitch** system for automatic music transcription and pitch estimation.

Basic Pitch is an automatic music transcription model developed by Spotify.

It can process musical audio and produce note information that can then be processed by MyMusicBuddy's music-analysis pipeline.

## Official Basic Pitch Resources

GitHub:

https://github.com/spotify/basic-pitch

PyPI:

https://pypi.org/project/basic-pitch/

Official documentation:

https://basicpitch.spotify.com/

---

# 📥 ML Model / Resource Download

Large ML models, datasets, downloaded archives, generated audio files, and evaluation resources are intentionally **not stored inside this GitHub repository**.

This keeps the Git repository lightweight and avoids committing very large binary files.

For Basic Pitch, use the official Spotify project:

https://github.com/spotify/basic-pitch

Official Basic Pitch documentation:

https://basicpitch.spotify.com/

Follow the official installation and documentation instructions to obtain the required model dependencies.

> ⚠️ Do not commit large model files, datasets, downloaded archives, or generated audio files directly into the Git repository.

---

# 🔬 ML Evaluation

The project contains an evaluation pipeline for testing music transcription performance.

Evaluation resources include:

- Ground-truth data
- Prediction data
- Note comparison
- Evaluation metrics
- MAPS dataset integration
- MIDI predictions
- Audio evaluation

The evaluation system is located under:

ml/evaluation/

Large datasets and downloaded archives are intentionally excluded from the GitHub repository.

---

# 🏗️ Project Architecture

MyMusicBuddy follows a full-stack architecture.

                    ┌─────────────────────────┐
                    │        Frontend         │
                    │    React + TypeScript   │
                    │         + Vite          │
                    └────────────┬────────────┘
                                 │
                                 │ HTTP / API
                                 ▼
                    ┌─────────────────────────┐
                    │         Backend         │
                    │          FastAPI        │
                    │                         │
                    │ Authentication          │
                    │ Music Analysis          │
                    │ Realtime Analysis       │
                    │ Fretboard               │
                    │ Playlists               │
                    └────────────┬────────────┘
                                 │
              ┌──────────────────┼──────────────────┐
              │                  │                  │
              ▼                  ▼                  ▼
       ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
       │ DSP / Music │    │ ML Pipeline │    │  Database   │
       │   Engines   │    │ Basic Pitch │    │    Layer    │
       └─────────────┘    └─────────────┘    └─────────────┘

---

# 🖥️ Frontend

The frontend is built using:

- React
- TypeScript
- Vite
- CSS
- Tailwind CSS utility classes

Main frontend location:

frontend1/

Important components include:

frontend1/src/
├── components/
│   ├── ArpeggioList.tsx
│   ├── ChordTimeline.tsx
│   ├── GuitarFretboard.tsx
│   ├── IntervalList.tsx
│   ├── RealtimePanel.tsx
│   └── ScaleRecommendations.tsx
│
├── pages/
│   ├── LandingPage.tsx
│   ├── LoginPage.tsx
│   ├── MainApp.tsx
│   └── SignupPage.tsx
│
├── api/
│   ├── analysis.ts
│   ├── auth.ts
│   ├── authState.ts
│   ├── fretboard.ts
│   └── music.ts
│
└── realtime/
    └── microphone.ts

---

# ⚙️ Backend

The backend is built using **FastAPI** and Python.

Main backend location:

backend/

Major backend modules include:

backend/app/
├── admin/
├── ai/
├── analysis/
├── api/
├── auth/
├── common/
├── core/
├── fretboard/
├── music/
├── playlists/
├── realtime/
└── users/

---

# 🔐 Authentication

MyMusicBuddy includes user authentication.

Authentication functionality includes:

- User registration
- Login
- Authentication state
- Protected routes
- User-related API endpoints
- Authorization and security utilities

Frontend protected pages are handled using:

frontend1/src/ProtectedRoute.tsx

Backend authentication logic is located under:

backend/app/auth/

---

# 🎧 Real-Time Audio Pipeline

The real-time analysis flow is approximately:

Microphone
    ↓
Audio Capture
    ↓
Audio Window
    ↓
Backend API
    ↓
Pitch / Note Analysis
    ↓
Chord / Music Analysis
    ↓
Realtime Result
    ↓
Frontend Display

When the user stops listening:

Stop Listening
      ↓
Finish Current Analysis
      ↓
Backend Final Snapshot
      ↓
Suggestions Generated
      ↓
Chord / Scale / Arpeggio / Progression Suggestions

---

# 🎵 Music Analysis Pipeline

The full analysis pipeline can process audio through several stages:

Audio
  ↓
Audio Processing
  ↓
Feature Extraction
  ↓
Pitch Detection
  ↓
Note Detection
  ↓
Segmentation
  ↓
Chord Detection
  ↓
Key / Scale Analysis
  ↓
Intervals
  ↓
Arpeggios
  ↓
Musical Suggestions

---

# 📂 Repository Structure

MyMusicBuddy/
│
├── ai-engine/
│   └── README.md
│
├── backend/
│   ├── app/
│   │   ├── admin/
│   │   ├── ai/
│   │   ├── analysis/
│   │   ├── api/
│   │   ├── auth/
│   │   ├── common/
│   │   ├── core/
│   │   ├── fretboard/
│   │   ├── music/
│   │   ├── playlists/
│   │   ├── realtime/
│   │   └── users/
│   │
│   ├── requirements.txt
│   └── tests
│
├── frontend1/
│   ├── src/
│   │   ├── api/
│   │   ├── components/
│   │   ├── pages/
│   │   └── realtime/
│   │
│   ├── package.json
│   └── vite.config.ts
│
├── ml/
│   ├── basic_pitch/
│   ├── evaluation/
│   ├── hybrid/
│   ├── schema.py
│   └── service.py
│
├── .gitignore
├── LICENSE
├── README.md
└── ml_test.py

---

# 🚀 Installation

## 1. Clone the Repository

git clone https://github.com/Riktam45/MyMusicBuddy.git

cd MyMusicBuddy

---

# 🐍 Backend Setup

Create a Python virtual environment:

python -m venv .venv

Activate it on Windows:

.venv\Scripts\activate

Install backend dependencies:

pip install -r backend/requirements.txt

---

# 🔑 Environment Variables

Create your environment configuration based on:

backend/.env.example

Do not commit your real `.env` file.

The `.env.example` file contains example configuration and is safe to include in the repository.

Add your own local environment variables according to the requirements of the application.

---

# ▶️ Run the Backend

From the project root:

uvicorn backend.app.main:app --reload

Depending on your local Python package configuration, the backend may also be started from inside the `backend` directory.

---

# ⚛️ Frontend Setup

Go to the frontend:

cd frontend1

Install dependencies:

npm install

Start the development server:

npm run dev

The Vite development server will provide the local frontend address.

---

# 🧪 Testing

The repository contains several test and evaluation scripts.

Examples include:

backend/test_basic_pitch.py

backend/test_chord_engine.py

backend/test_full_song.py

backend/test_full_song_real.py

backend/test_hybrid.py

backend/test_ml_vs_dsp.py

ml_test.py

Run individual tests using Python.

Example:

python backend/test_basic_pitch.py

or:

python ml_test.py

---

# 📊 DSP + ML Hybrid Approach

One of the main ideas behind MyMusicBuddy is combining traditional music-processing techniques with machine learning.

Instead of depending exclusively on an ML model, the application contains dedicated music-analysis engines for:

- Pitch
- Chords
- Intervals
- Scales
- Arpeggios
- Key detection
- Beat tracking
- Segmentation
- Fretboard analysis

The ML system can provide pitch and note information while the music-analysis layer interprets that information using music theory and DSP-based processing.

This hybrid architecture allows the application to combine machine-learning capabilities with deterministic music-analysis algorithms.

---

# 🛡️ Git & Large Files

Large datasets, downloaded archives, generated audio, and model resources are intentionally excluded from GitHub.

For example, large MAPS dataset archives should not be committed directly into the repository.

Instead:

1. Clone the repository.
2. Install the required dependencies.
3. Download the required external ML/model resources.
4. Place them in the appropriate local directory.
5. Run the application.

This keeps the GitHub repository manageable while still allowing the project to be reproduced.

---

# ⚠️ Important

Some ML and evaluation resources are intentionally **not included in this repository** because of their large size and/or external dataset distribution requirements.

The GitHub repository contains the source code required to integrate and process those resources.

Users should obtain third-party datasets and models from their official sources and follow their respective licenses and terms.

---

# 📦 Large Dataset Handling

The project previously used large evaluation resources including MAPS-related files.

These files can include:

- WAV audio
- MIDI files
- ZIP archives
- Ground-truth data
- Prediction data
- Evaluation datasets

These resources should remain outside the Git repository when they are too large for normal GitHub storage.

The source code is maintained in GitHub, while large external resources can be downloaded separately when needed.

---

# 📜 Third-Party Resources

This project may use or integrate with third-party technologies and datasets.

## Spotify Basic Pitch

GitHub:

https://github.com/spotify/basic-pitch

Documentation:

https://basicpitch.spotify.com/

PyPI:

https://pypi.org/project/basic-pitch/

## MAPS Dataset

The MAPS database is used in music-information-retrieval research and evaluation.

Users should obtain the dataset from its official distribution source and comply with the applicable dataset license and terms.

---

# 🎯 Project Goals

The main goals of MyMusicBuddy are:

- Make music analysis easier
- Help beginners understand music theory
- Assist musicians during practice
- Provide real-time musical feedback
- Connect audio analysis with practical guitar knowledge
- Combine AI with traditional music-processing techniques
- Provide useful musical suggestions instead of only raw detection results
- Make complex music-analysis concepts easier to understand

---

# 🔮 Future Improvements

Possible future improvements include:

- 🎤 Improved real-time transcription
- 🎼 More accurate chord recognition
- 🎹 Better polyphonic transcription
- 🎸 More guitar-specific analysis
- 🎵 Melody tracking
- 🥁 Improved beat and rhythm analysis
- 📈 Visualization of musical events over time
- 🤖 Improved ML models
- ☁️ Cloud-based ML inference
- 📱 Mobile application
- 🎧 Better full-song analysis
- 🎼 More advanced harmonic analysis

---

# 👨‍💻 Author

## Riktam Das

GitHub:

https://github.com/Riktam45

MyMusicBuddy Repository:

https://github.com/Riktam45/MyMusicBuddy

---

# 📄 License

This project is distributed under the license included in the repository.

See:

LICENSE

for the complete license terms.

---

# ⭐ Support

If you find MyMusicBuddy useful:

⭐ Star the repository

🐛 Report bugs

💡 Suggest improvements

🔧 Contribute improvements

---

# 🎵 MyMusicBuddy

**Listen. Analyze. Understand. Create.**

An AI-assisted music-analysis platform built to help musicians turn audio into musical knowledge.
