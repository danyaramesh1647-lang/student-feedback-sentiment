from flask import Flask, render_template, request, jsonify
from textblob import TextBlob
import json
import os
from datetime import datetime
from nltk.sentiment import SentimentIntensityAnalyzer

app = Flask(__name__)
sia = SentimentIntensityAnalyzer()

# Domain-specific boost words — VADER's general lexicon misses education-context terms.
# We update its internal lexicon with scores from -4 (very negative) to +4 (very positive).
sia.lexicon.update({
    "noisy": -2.0,
    "boring": -2.5,
    "difficult": -1.5,
    "confusing": -2.0,
    "unclear": -1.5,
    "clear": 1.5,
    "helpful": 2.0,
    "interesting": 2.0,
    "engaging": 2.0,
    "informative": 1.5,
    "concentration": -0.5,
    "okay": 0.0,     # lukewarm word — should not tip sentiment either way
    "ok": 0.0,
    "fine": 0.0,
    "alright": 0.0,
    "average": 0.0,
    "decent": 0.3,   # slightly positive but mild, not enough to cross threshold strongly
})
DATA_FILE = "feedback_data.json"


# ---------- Helper Functions ----------

def load_feedback_history():
    """Load previously analyzed feedback from the JSON file."""
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_feedback_entry(entry):
    """Append a new feedback entry to the JSON file."""
    history = load_feedback_history()
    history.insert(0, entry)  # newest first
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2)


def analyze_sentiment(text):
    """
    Use VADER's compound score (-1 to +1) which combines all word scores
    in the sentence, accounting for negation, intensity, and punctuation.
    Standard VADER thresholds (from their research paper):
      compound >= 0.05  -> Positive
      compound <= -0.05 -> Negative
      otherwise         -> Neutral
    """
    scores = sia.polarity_scores(text)
    compound = scores["compound"]

    if compound >= 0.05:
        return "Positive", "😊", compound
    elif compound <= -0.05:
        return "Negative", "😞", compound
    else:
        return "Neutral", "😐", compound


def extract_keywords(text, limit=5):
    """
    Very simple keyword extraction:
    - Tokenize the text
    - Remove common stopwords and punctuation
    - Return the most relevant remaining words
    """
    stopwords = {
        "the", "is", "and", "are", "was", "were", "a", "an", "of", "to",
        "in", "on", "for", "it", "this", "that", "very", "with", "as",
        "but", "so", "too", "not", "i", "we", "you", "they", "he", "she",
        "be", "been", "has", "have", "had", "at", "by", "from", "or"
    }

    blob = TextBlob(text)
    words = [word.lower() for word in blob.words if word.isalpha()]
    keywords = [w for w in words if w not in stopwords]

    # Remove duplicates while preserving order
    seen = set()
    unique_keywords = []
    for w in keywords:
        if w not in seen:
            seen.add(w)
            unique_keywords.append(w)

    return unique_keywords[:limit]


# ---------- Routes ----------

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["GET", "POST"])
def analyze():
    result = None

    if request.method == "POST":
        feedback_text = request.form.get("feedback", "").strip()

        if feedback_text:
            label, emoji, polarity = analyze_sentiment(feedback_text)
            polarity = round(polarity, 3)

            blob = TextBlob(feedback_text)  # used for subjectivity + keyword tokenizing
            subjectivity = round(blob.sentiment.subjectivity, 3)
            keywords = extract_keywords(feedback_text)

            result = {
                "text": feedback_text,
                "label": label,
                "emoji": emoji,
                "polarity": polarity,
                "subjectivity": subjectivity,
                "keywords": keywords,
                "timestamp": datetime.now().strftime("%d %b %Y, %I:%M %p")
            }

            save_feedback_entry(result)

    return render_template("analyze.html", result=result)


@app.route("/history")
def history():
    all_feedback = load_feedback_history()

    total = len(all_feedback)
    positive_count = sum(1 for f in all_feedback if f["label"] == "Positive")
    negative_count = sum(1 for f in all_feedback if f["label"] == "Negative")
    neutral_count = sum(1 for f in all_feedback if f["label"] == "Neutral")

    stats = {
        "total": total,
        "positive": positive_count,
        "negative": negative_count,
        "neutral": neutral_count
    }

    return render_template("history.html", feedback_list=all_feedback, stats=stats)


if __name__ == "__main__":
    app.run(debug=True)