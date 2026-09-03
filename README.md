# 🎓 Sentiment Analysis of Student Feedback Using NLP

An NLP-powered web application that analyzes student feedback text and classifies it as **Positive 😊**, **Negative 😞**, or **Neutral 😐** — helping educational institutions quickly understand student sentiment at scale.

Built as a Text & Speech Analysis mini-project.

🔗 **Repository:** [github.com/danyaramesh1647-lang/student-feedback-sentiment](https://github.com/danyaramesh1647-lang/student-feedback-sentiment)

---

## 📌 Features

- **Real-time sentiment classification** of student feedback text
- **Confidence scoring** via VADER's compound polarity score
- **Keyword extraction** highlighting the most relevant words in the feedback
- **Feedback history** with running statistics (total / positive / negative / neutral counts)
- Clean, responsive UI with color-coded sentiment cards

---

## 🧠 NLP Pipeline

Student Feedback
↓
Text Preprocessing
↓
Tokenization
↓
Feature Extraction
↓
Sentiment Classification (VADER)
↓
Positive / Neutral / Negative


### How classification works

This project uses **VADER (Valence Aware Dictionary and sEntiment Reasoner)** from NLTK, a rule-based sentiment analysis tool tuned for real-world text. It computes a compound polarity score between -1 and +1 for each piece of feedback:

| Compound Score | Sentiment |
|---|---|
| ≥ 0.05 | Positive 😊 |
| ≤ -0.05 | Negative 😞 |
| Between -0.05 and 0.05 | Neutral 😐 |

VADER's lexicon was extended with education-domain-specific terms (e.g., "noisy", "engaging", "confusing") to improve accuracy on classroom feedback specifically. **TextBlob** is used alongside it to calculate subjectivity scores and for word tokenization during keyword extraction.

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | HTML, CSS, JavaScript (Jinja2 templating) |
| Backend | Python, Flask |
| NLP | NLTK (VADER), TextBlob |
| Storage | JSON file-based storage |

---

## 📂 Project Structure

student-feedback-sentiment/
│
├── app.py # Flask backend + NLP logic
├── requirements.txt # Python dependencies
├── templates/
│ ├── base.html # Shared layout (navbar, footer)
│ ├── index.html # Home / Dashboard
│ ├── analyze.html # Feedback analysis page
│ └── history.html # Feedback history page
├── static/
│ ├── css/style.css
│ └── js/script.js
└── feedback_data.json # Auto-generated feedback storage (gitignored)


---

## 🚀 Running Locally

1. **Clone the repository**
```bash
   git clone https://github.com/danyaramesh1647-lang/student-feedback-sentiment.git
   cd student-feedback-sentiment
```

2. **Create and activate a virtual environment**
```bash
   python -m venv venv
   venv\Scripts\activate      # Windows
   source venv/bin/activate   # macOS/Linux
```

3. **Install dependencies**
```bash
   pip install -r requirements.txt
```

4. **Download required NLTK data** (one-time)
```bash
   python -c "import nltk; nltk.download('punkt'); nltk.download('brown'); nltk.download('vader_lexicon')"
```

5. **Run the app**
```bash
   python app.py
```

6. Open **http://127.0.0.1:5000** in your browser.

---

## 📱 App Screens

1. **Home / Dashboard** — project overview and entry point
2. **Feedback Analysis** — text input, sentiment result, polarity/subjectivity scores, extracted keywords
3. **Feedback History** — all previously analyzed feedback with summary statistics

---

## ⚠️ Known Limitations

- As a lexicon/rule-based model, VADER may occasionally misclassify ambiguous or sarcastic feedback where meaning depends heavily on context (e.g., "Nothing special about the lectures" is classified as mildly negative, which is debatable).
- Sentiment accuracy could be further improved with a trained ML/deep learning model (e.g., fine-tuned BERT) given a labeled dataset of student feedback, as a future enhancement.

---

## 🔮 Future Enhancements

- Deploy live on Render
- Add a database (e.g., PostgreSQL) instead of JSON file storage
- Support batch analysis of feedback via CSV upload
- Add sentiment trend charts over time

---

## 👩‍💻 Author

**Danya Ramesh** — [GitHub](https://github.com/danyaramesh1647-lang)
