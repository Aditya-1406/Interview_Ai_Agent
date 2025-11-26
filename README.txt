AI Interview Practice

A complete AI-powered mock interview platform built using Streamlit,
Google Gemini API, Speech Recognition, and Offline Text-to-Speech.
This app simulates a real interview experience with voice input, dynamic
interview flow, adaptive hints, and a final performance report.

Environment:-
Os - macos Sequoia 15.5
Python - Python 3.12 (Stable Version)

Table of Contents :-

1.  Overview
2.  Features
3.  Tech Stack
4.  Architecture Overview
5.  Setup Instructions
6.  How to Create Google Gemini API Key
7.  Running the Application
8.  Code Structure
9.  Design Decisions
10. Future Enhancements
11. License


1. Overview:-

This project provides a realistic AI-driven interview practice tool
with: - Role-specific questions
- Voice + text responses
- Intelligent follow‑up questions
- Dynamic question difficulty
- Automated performance feedback in markdown format

Perfect for students, job seekers, and developers practicing interview
skills.


2. Features:-

Voice Interaction

-   Speak your answer using your microphone
-   App detects your speech and converts it into text
-   AI interviewer responds using Text‑to‑Speech

Smart Interviewer

-   Select interview role: Engineer, Sales, Marketing
-   Context-aware responses
-   Detects confusion using keywords
-   Gives hints and repeats questions if needed
-   Follow‑up questions automatically generated

Automated Feedback Report

Includes: - Overall Score
- Strengths
- Weaknesses
- Example of a better answer
- Clean markdown formatting

Dark-Themed UI

-   Modern, clean interface
-   Chat-style conversation panel
-   Voice + text input options


3. Tech Stack:-

Frontend

-   Streamlit (UI framework)

Backend Logic

-   Python 3.12
-   Google Gemini API (LLM interaction)

Speech Processing

-   SpeechRecognition (Speech-to-Text)
-   pyttsx3 (Offline Text-to-Speech)

Utilities

-   python-dotenv
-   Custom interview agents


4. Architecture Overview:-

    /app.py
    ├── QUESTION_BANK (role-wise questions)
    ├── InterviewTools
    │     ├── get_question()
    │     └── get_hint()
    ├── InterviewerAgent
    │     ├── start_interview()
    │     └── get_next_question()
    ├── FeedbackAgent
    │     └── analyze_session()
    └── Streamlit UI Layer (Frontend)


5. Setup Instructions:-

Step 1 — Clone Repository

    git clone <your-repo-url>
    cd your-folder

Step 2 — Create Virtual Environment

macOS/Linux:

    python3 -m venv .venv
    source .venv/bin/activate

Windows:

    python -m venv .venv
    .venv\Scripts\activate

Step 3 — Install Dependencies

    pip install -r requirements.txt

Or manually:

    pip install streamlit google-genai python-dotenv pyttsx3 SpeechRecognition PyAudio dotenv

Install PyAudio (Windows):

Download correct wheel for your Python version:

    https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio

    pip install PyAudio-0.2.13-cp312-cp312-win_amd64.whl


Step 4 — Create .env File

    GEMINI_API_KEY=your_api_key_here


6. How to Create Google Gemini API Key:-

Step 1 — Visit Google AI Studio

 https://aistudio.google.com/

Step 2 — Sign in using Google account

Step 3 — On sidebar, click “Get API Key”

Step 4 — Click “Create API Key”

Choose: > Use with Gemini API

Step 5 — Copy your key

Step 6 — Paste inside .env

    GEMINI_API_KEY=your_key_here

⚠ Without this key the app will not work.


7. Running the Application:-

Start the Streamlit app:

    streamlit run app.py



8. Code Structure:-

    project/
    │── app.py
    │── README.md
    │── .env

Main components inside app.py

-   InterviewerAgent: Manages question flow + LLM chat
-   FeedbackAgent: Generates final interview feedback
-   InterviewTools: Question fetching + hints
-   Streamlit UI: User interaction + chat display


9. Design Decisions:-

1. Gemini Flash Model:-

Chosen for speed, low cost, and high quality.

2. Offline Text-to-Speech:-

-   pyttsx3 is used instead of cloud TTS
-   Works offline, low latency

3. Google Speech API (SpeechRecognition):-

Good accuracy → easy integration
Zero-cost STT

4. Weighted Difficulty for Engineering Role:-

-   40% advanced
-   40% intermediate
-   20% beginner
    Creates realistic interview flow.

5. Streamlit Session State:-

Prevents resetting the chat on reruns.

6. Modular Agent-Based Architecture:-

Easier to maintain and upgrade
LLM logic separated from UI logic


10. Future Enhancements:-

-   Resume-based interview question generation
-   Behavioral round support
-   Coding editor with live execution
-   Save transcripts in Firebase/MongoDB
-   Downloadable PDF feedback report
-   Add different interviewer personalities
-   Add HR + Managerial interview modes



11. License:-

MIT License — open for personal & academic use.



Created By:-

Aditya
Python Developer | AI Enthusiast
