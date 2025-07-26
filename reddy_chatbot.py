import streamlit as st
import openai

# 🔑 Set your OpenAI API key
openai.api_key = "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"

# 🧠 Streamlit UI
st.title("🤖 Reddy - Your Smart Study Assistant")
user_input = st.text_input("Ask Reddy something...")

# 📢 On Button Click
if st.button("Send"):
    if user_input:
        with st.spinner("Reddy is thinking..."):
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a helpful study assistant."},
                        {"role": "user", "content": user_input}
                    ]
                )
                reply = response['choices'][0]['message']['content']
                st.success(reply)
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
    else:
        st.warning("Please ask something first!")



        
import pyttsx3
import speech_recognition as sr
def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Listening...")
        audio = recognizer.listen(source)
        try:
            return recognizer.recognize_google(audio)
        except:
            return "Sorry, I didn’t catch that."
    user_input = st.text_input("Ask me anything...", key="ask_input_1")
if st.button("🎤 Speak"):
    user_input = listen()
st.subheader("📤 Upload a File (PDF / Word)")
uploaded_file = st.file_uploader("Choose a file", type=['pdf', 'docx'])

if uploaded_file:
    st.success("File uploaded!")

    if uploaded_file.name.endswith('.pdf'):
        import pdfplumber
        with pdfplumber.open(uploaded_file) as pdf:
            text = ''
            for page in pdf.pages:
                text += page.extract_text()
    elif uploaded_file.name.endswith('.docx'):
        import docx
        doc = docx.Document(uploaded_file)
        text = '\n'.join([para.text for para in doc.paragraphs])

    st.info("Summarizing content...")
    summary = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": f"Summarize this: {text}"}]
    )
    st.success(summary['choices'][0]['message']['content'])
st.subheader("🖼️ Create Image from Text")
image_prompt = st.text_input("Enter description for image")

if st.button("Generate Image"):
    response = openai.Image.create(prompt=image_prompt, n=1, size="512x512")
    img_url = response['data'][0]['url']
    st.image(img_url)
st.subheader("🧪 Auto Quiz Generator")
quiz_topic = st.text_input("Enter quiz topic")

if st.button("Generate Quiz"):
    quiz_prompt = f"Create 4 quiz questions with 4 options (A,B,C,D) and answers on '{quiz_topic}'"
    quiz = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": quiz_prompt}]
    )
    st.text_area("Quiz:", quiz['choices'][0]['message']['content'], height=250)
import random

def generate_quiz(topic):
    prompt = f"Create 3 MCQ questions about {topic}. Each should have 4 options (A, B, C, D) and clearly mark the correct answer."
    quiz = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return quiz['choices'][0]['message']['content']

st.subheader("📚 Quiz Generator & Evaluator")

quiz_topic = st.text_input("Enter topic for quiz")
if st.button("Create Quiz"):
    quiz_data = generate_quiz(quiz_topic)
    st.session_state.quiz_data = quiz_data
    st.session_state.answers = {}

if "quiz_data" in st.session_state:
    lines = st.session_state.quiz_data.strip().split('\n')
    questions = []
    current_question = ""
    options = []

    for line in lines:
        if line.startswith("Q"):
            if current_question:
                questions.append((current_question, options))
                options = []
            current_question = line
        elif line.startswith(("A", "B", "C", "D")):
            options.append(line)
        elif "Answer:" in line:
            correct = line.split("Answer:")[-1].strip()
            questions.append((current_question, options, correct))

    user_answers = {}

    st.write("### Choose your answers below:")
    for i, (q, opts, corr) in enumerate(questions):
        st.write(f"**{q}**")
        selected = st.radio(f"Select for Q{i+1}", opts, key=f"q{i}")
        user_answers[f"Q{i+1}"] = (selected, corr)

    if st.button("Submit Quiz"):
        score = 0
        total = len(user_answers)
        feedback = []
        for q, (selected, corr) in user_answers.items():
            if selected.startswith(corr):
                score += 1
            else:
                feedback.append(f"{q} - Correct: {corr}, You chose: {selected[0]}")

        st.success(f"Your Score: {score}/{total}")
        if feedback:
            st.error("Questions to Improve:")
            for item in feedback:
                st.write(item)
import os
import datetime

history_file = "chat_history.txt"
recycle_file = "recycle_bin.txt"

def save_chat(user, bot):
    with open(history_file, "a") as f:
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        f.write(f"[{now}] You: {user}\n[{now}] Reddy: {bot}\n")

def show_history():
    if os.path.exists(history_file):
        with open(history_file, "r") as f:
            st.text_area("Chat History", f.read(), height=250)

def delete_history():
    if os.path.exists(history_file):
        os.rename(history_file, recycle_file)
        st.warning("Chat moved to Recycle Bin!")

def restore_history():
    if os.path.exists(recycle_file):
        os.rename(recycle_file, history_file)
        st.success("Chat history restored!")
st.sidebar.header("🗂️ History & Privacy")
if st.sidebar.button("📖 View Chat History"):
    show_history()

if st.sidebar.button("🗑️ Move History to Recycle Bin"):
    delete_history()

if st.sidebar.button("♻️ Restore from Recycle Bin"):
    restore_history()

