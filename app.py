from flask import Flask, render_template, request, jsonify
import json
import difflib
import string
import re

app = Flask(__name__)

# Load QnA data
with open("static/qna.json", "r", encoding="utf-8") as f:
    qna = json.load(f)

# Greeting responses
greetings = {
    "hi": "Hello 👋! I’m your Current Affairs Bot.",
    "hello": "Hi there! Ask me anything about current events.",
    "hey": "Hey! Ready to dive into some current affairs?",
    "good morning": "Good morning 🌞! What news are you curious about?",
    "good evening": "Good evening 🌆! Let’s talk current affairs.",
    "thanks": "You're welcome 🙌. Feel free to ask more!"
}

# Normalize text: lowercase, remove punctuation, handle abbreviations
def normalize(text):
    text = text.lower().strip()
    text = text.translate(str.maketrans("", "", string.punctuation))
    replacements = {
        "who's": "who is",
        "pm": "prime minister",
        "india's": "india",
        "govt": "government"
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    return text

# Remove :contentReference[...] from answers
def clean_answer(answer):
    return re.sub(r":contentReference\[.*?\]{index=\d+}", "", answer).strip()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    user_question = normalize(request.json.get("question", ""))

    # Check for greetings
    for key, reply in greetings.items():
        if user_question.startswith(key):
            return jsonify({"answer": reply})

    # Match against stored questions
    questions = [normalize(qa["question"]) for qa in qna]
    match = difflib.get_close_matches(user_question, questions, n=1, cutoff=0.4)

    if match:
        for qa in qna:
            if normalize(qa["question"]) == match[0]:
                cleaned = clean_answer(qa["answer"])
                return jsonify({"answer": cleaned})

    # Default fallback
    return jsonify({
        "answer": "Hmm 🤔 I don’t know that one yet. Try asking about recent events like the budget, elections, or world news."
    })

if __name__ == "__main__":
    app.run(debug=True)
