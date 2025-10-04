from flask import Flask, render_template, request, jsonify
import json
import difflib

app = Flask(__name__)

with open("static/qna.json", "r", encoding="utf-8") as f:
    qna = json.load(f)

greetings = {
    "hi": "Hello 👋! I’m your Current Affairs Bot.",
    "hello": "Hi there! Ask me anything about current events.",
    "hey": "Hey! Ready to dive into some current affairs?",
    "good morning": "Good morning 🌞! What news are you curious about?",
    "good evening": "Good evening 🌆! Let’s talk current affairs.",
    "thanks": "You're welcome 🙌. Feel free to ask more!"
}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    user_question = request.json.get("question", "").lower().strip()

    # Normalize contractions and short forms
    replacements = {
        "who's": "who is",
        "pm": "prime minister",
        "india's": "india",
        "govt": "government"
    }
    for k, v in replacements.items():
        user_question = user_question.replace(k, v)

    # Check greetings
    for key, reply in greetings.items():
        if user_question.startswith(key):
            return jsonify({"answer": reply})

    # Fuzzy matching for QnA
    questions = [qa["question"].lower() for qa in qna]
    match = difflib.get_close_matches(user_question, questions, n=1, cutoff=0.4)

    if match:
        for qa in qna:
            if qa["question"].lower() == match[0]:
                return jsonify({"answer": qa["answer"]})

    return jsonify({"answer": "Hmm 🤔 I don’t know that one yet. Try asking about recent events like the budget, elections, or world news."})

if __name__ == "__main__":
    app.run(debug=True)
