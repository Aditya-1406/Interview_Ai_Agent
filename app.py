import os
import random
from typing import List
from dotenv import load_dotenv
import streamlit as st

# --- LLM CLIENT IMPORTS ---
try:
    from google import genai
    from google.genai import types
    from google.genai.errors import APIError
except ImportError:
    st.error("Please install 'google-genai' and 'python-dotenv'")
    st.stop()

# --- Text-to-Speech ---
try:
    import pyttsx3
except ImportError:
    st.error("Please install 'pyttsx3'")
    st.stop()

# --- Speech Recognition ---
try:
    import speech_recognition as sr
except ImportError:
    st.error("Please install 'SpeechRecognition' and 'PyAudio'")
    st.stop()

# Initialize TTS engine
tts_engine = pyttsx3.init()
tts_engine.setProperty('rate', 170)
tts_engine.setProperty('volume', 1.0)

def speak(text: str):
    tts_engine.say(text)
    tts_engine.runAndWait()

# Load environment variables
load_dotenv()
MODEL_NAME = "gemini-2.5-flash"


# --- Question Bank ---

QUESTION_BANK = {
    "engineer": {
        "beginner": [
            "Tell me about a project you're proud of.",
            "Explain the difference between a list and a tuple in Python."
        ],
        "intermediate": [
            "How would you optimize a slow database query in Django?",
            "Describe a time you dealt with a technical disagreement."
        ],
        "advanced": [
            "Given an array of integers, find the subarray with the maximum sum.",
            "Implement a function to detect if a linked list has a cycle.",
            "Explain how you would implement a stack using queues.",
            "Find the kth largest element in an unsorted array efficiently."
        ]
    },
    "sales": {
        "beginner": [
            "Tell me about a successful sale you closed.",
            "How do you handle rejection from a client?"
        ],
        "intermediate": [
            "Describe a time you exceeded your sales targets.",
            "How would you approach a new market segment?"
        ],
        "advanced": [
            "Simulate a cold call to a challenging client.",
            "Design a strategy to enter a competitive market."
        ]
    },
    "marketing": {
        "beginner": [
            "Explain a marketing campaign you executed successfully.",
            "How do you measure the effectiveness of a campaign?"
        ],
        "intermediate": [
            "How would you increase brand engagement in a competitive market?",
            "Describe a time when you used data to optimize a campaign."
        ],
        "advanced": [
            "Design a 6-month marketing strategy for a new product.",
            "Analyze a failing campaign and suggest improvements."
        ]
    }
}

# --- Tools ---
class InterviewTools:
    @staticmethod
    def get_question(role: str, level: str) -> str:
        role = role.lower()
        level = level.lower()
        questions = QUESTION_BANK.get(role, QUESTION_BANK["engineer"]).get(
            level, QUESTION_BANK["engineer"]["beginner"]
        )
        return random.choice(questions)

    @staticmethod
    def get_hint(question: str) -> str:
        hints = {
            "subarray": "Consider Kadane's algorithm for max sum subarray.",
            "linked list": "Try using two pointers to detect the cycle.",
            "stack using queues": "Use two queues and simulate push/pop operations.",
            "kth largest": "You can use a min-heap of size k for efficiency."
        }
        for key, hint in hints.items():
            if key in question.lower():
                return hint
        return "Think logically and break down the problem step by step."

# --- Interviewer Agent ---

class InterviewerAgent:
    def __init__(self, client: genai.Client, job_description: str, role: str):
        self.client = client
        self.role = role
        self.system_prompt = f"""
        You are a professional interviewer for {role} roles.
        INSTRUCTIONS:
        1. Ask one question at a time.
        2. If candidate is confused, provide a short hint and repeat question.
        3. Keep follow-ups shallow.
        """
        self.chat_session = self.client.chats.create(
            model=MODEL_NAME,
            config=types.GenerateContentConfig(system_instruction=self.system_prompt)
        )

    def start_interview(self) -> str:
        if self.role.lower() == "engineer":
            question = InterviewTools.get_question(self.role, "advanced")
        else:
            question = InterviewTools.get_question(self.role, "beginner")
        response = self.chat_session.send_message(question)
        return response.text, question

    def get_next_question(self, user_response: str, last_question: str):
        confusion_keywords = ["don't understand", "unable to", "explain", "clarify", "not sure"]
        if any(word in user_response.lower() for word in confusion_keywords):
            hint = InterviewTools.get_hint(last_question)
            clarification = f"Sure, let me clarify: {last_question}\nHint: {hint}"
            response = self.chat_session.send_message(clarification)
            return response.text

        if self.role.lower() == "engineer":
            next_level = random.choices(
                ["advanced", "intermediate", "beginner"], weights=[0.4, 0.4, 0.2], k=1
            )[0]
        else:
            next_level = "intermediate"

        next_question = InterviewTools.get_question(self.role, next_level)
        response = self.chat_session.send_message(user_response + "\n" + next_question)
        return response.text, next_question

# --- Feedback Agent---

class FeedbackAgent:
    def __init__(self, client: genai.Client, job_description: str):
        self.client = client
        self.job_description = job_description
        self.system_prompt = f"""
        You are a Senior Manager analyzing candidate performance.
        Provide feedback in a **stylish and user-friendly markdown format**:
        - Overall Score: X/5
        - Strengths
        - Areas for Improvement
        - Example of Better Answer
        """

    def analyze_session(self, conversation_history: List[str]) -> str:
        transcript = "\n".join(conversation_history)
        prompt = f"{self.system_prompt}\nFull Transcript:\n{transcript}\nGenerate feedback."
        response = self.client.models.generate_content(
            model=MODEL_NAME,
            contents=[prompt]
        )
        return response.text

# --- Streamlit App ---

st.set_page_config(page_title="AI Interview Practice", layout="wide", initial_sidebar_state="collapsed")
st.markdown("""
<style>
body { background-color: #1e1e1e; color: white; }
div.stTextInput > label, div.stTextInput > input { color: white; background-color: #333; }
.stButton>button { background-color: #444; color: white; }
.stMarkdown { color: white; }
</style>
""", unsafe_allow_html=True)

st.title("AI Interview Practice Partner")

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    st.error("GEMINI_API_KEY not set in .env")
    st.stop()

client = genai.Client(api_key=api_key)
role = st.selectbox("Select Role:", ["Engineer", "Sales", "Marketing"])

# Session state
if "conversation" not in st.session_state:
    st.session_state.conversation = []
if "last_question" not in st.session_state:
    st.session_state.last_question = ""
if "interviewer" not in st.session_state:
    st.session_state.interviewer = None
if "feedback_agent" not in st.session_state:
    st.session_state.feedback_agent = None
if "greeted" not in st.session_state:
    st.session_state.greeted = False

# Display conversation dynamically
def display_conversation():
    st.empty()  # placeholder
    for chat in st.session_state.conversation:
        if chat.startswith("Interviewer:"):
            st.markdown(f"<p style='color:#a8ff60'><b>{chat}</b></p>", unsafe_allow_html=True)
        else:
            st.markdown(f"<p style='color:#ffffff'><b>{chat}</b></p>", unsafe_allow_html=True)

# Start Interview
if st.button("Start Interview") and not st.session_state.interviewer:
    st.session_state.interviewer = InterviewerAgent(client, f"Role: {role}", role)
    st.session_state.feedback_agent = FeedbackAgent(client, f"Role: {role}")
    greeting = "Hello! Welcome to your AI interview practice session."
    st.session_state.conversation.append(f"Interviewer: {greeting}")
    speak(greeting)
    first_output, last_question = st.session_state.interviewer.start_interview()
    st.session_state.last_question = last_question
    st.session_state.conversation.append(f"Interviewer: {first_output}")
    speak(first_output)

# Function to submit text
def submit_text(user_response: str):
    if user_response and st.session_state.interviewer:
        st.session_state.conversation.append(f"Candidate: {user_response}")
        output = st.session_state.interviewer.get_next_question(user_response, st.session_state.last_question)
        if isinstance(output, tuple):
            next_output, last_question = output
            st.session_state.last_question = last_question
        else:
            next_output = output
        st.session_state.conversation.append(f"Interviewer: {next_output}")
        speak(next_output)

# Text input
user_text = st.text_input("Type your answer here:", key="user_input")
if st.button("Submit Text") and user_text:
    submit_text(user_text)

# Voice input
if st.button("🎤 Speak Answer"):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Listening... Please speak now.")
        audio = r.listen(source)
        try:
            user_speech = r.recognize_google(audio)
            st.success(f"You said: {user_speech}")
            submit_text(user_speech)
        except sr.UnknownValueError:
            st.error("Could not understand your speech.")
        except sr.RequestError as e:
            st.error(f"Speech recognition error: {e}")

# Display chat history
display_conversation()

# End Interview
if st.button("End Interview") and st.session_state.feedback_agent:
    st.subheader("✨ Interview Concluded. Feedback:")
    speak("Thank you for attending the session. You will see your report below.")
    final_report = st.session_state.feedback_agent.analyze_session(st.session_state.conversation)
    st.markdown(f"<div style='background-color:#333; padding:10px; border-radius:8px'><pre style='color:#fff'>{final_report}</pre></div>", unsafe_allow_html=True)
