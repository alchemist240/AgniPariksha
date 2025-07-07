# 🔥 AgniPariksha – Human or Bot Detection System

**AgniPariksha** (अग्निपरीक्षा) — a term from Indian mythology meaning *“trial by fire”* — was a symbolic test of purity and truth.  
This project carries that metaphor into the digital age, where the **trial** is not fire, but **behavior** — and the **truth** lies in how you move, type, and think.

**AgniPariksha** is a next-gen human verification system inspired by CAPTCHA — but smarter. Instead of image puzzles, it uses **behavioral and cognitive signals** to determine if a user is a human or a bot.

---

## 🚀 Features

- ✅ Tracks **keystrokes**, **mouse movements**, and **reaction time**
- ✅ Collects cognitive responses (e.g., question answering)
- ✅ Sends behavioral data to a **Flask backend**
- ✅ Uses an ML model to predict: **human vs bot**
- ✅ Displays prediction and confidence score on frontend

---

## 🧠 Architecture Overview

```txt
Frontend (React + Vite)
    |
    |-- Tracks user behavior (mouse, keyboard, time)
    |-- Sends data to backend via API
    |
Backend (Flask)
    |
    |-- Receives data from frontend
    |-- Extracts behavioral features
    |-- Feeds data to pre-trained ML model
    |-- Returns classification result (human/bot)
```

---

## 📁 Project Structure

```bash
AgniPariksha/
├── backend/
│   ├── app.py                  # Flask entry point
│   ├── routes/                 # Flask routes
│   ├── models/                 # Saved ML models
│   ├── utils/                  # Feature extraction logic
│   ├── data/                   # Input data (ignored in git)
│   ├── requirements.txt        # Backend dependencies
│   └── train_model.py          # Training logic
│
├── frontend/
│   └── agni-ui/                # React frontend
│       ├── node_modules/       # npm packages
│       ├── src/                # Tracker.jsx & UI logic
│       ├── public/             # Static assets
│       ├── package.json        # Frontend dependencies
│       └── vite.config.js      # Vite config
│
├── venv/                       # Python virtual env (ignored)
├── .gitignore
├── README.md
└── requirements.txt
```

---

## 🛠️ Installation Instructions

### 🐍 Backend (Flask + ML)

Create and activate virtual environment (from root):

```bash
python -m venv venv
.\venv\Scripts\activate      # Windows
source venv/bin/activate    # Linux/Mac
```

Install dependencies:

```bash
pip install -r backend/requirements.txt
```

Run the Flask server:

```bash
cd backend
python app.py
```

---

### 🌐 Frontend (React + Vite)

Navigate to the UI folder:

```bash
cd frontend/agni-ui
```

Install npm packages:

```bash
npm install
```

Start the frontend dev server:

```bash
npm run dev
```

---

## 🧠 ML Features Used

| Feature Name         | Description                                      |
|----------------------|--------------------------------------------------|
| `reaction_time`      | Time taken to respond after prompt appears       |
| `answer_length`      | Number of characters in the submitted response   |
| `avg_key_interval`   | Average time between keystrokes                  |
| `std_key_interval`   | Standard deviation of keystroke intervals        |
| `mouse_distance`     | Total distance of mouse movement during prompt   |
| `mouse_avg_speed`    | Average speed of mouse movements                 |
| `mouse_movements`    | Total count of mouse movement events             |

These features are passed to a trained machine learning model to classify users as either **human** or **bot** with a confidence score.

---



---

## 🤖 Tech Stack

- **Frontend**: React, Vite, JavaScript, CSS
- **Backend**: Flask, Python
- **ML**: Scikit-learn, Pandas, NumPy
- **Dev Tools**: VS Code, Git, Postman
- **Deployment-ready**: Localhost (can extend to Render/Heroku/Netlify)

---

## 📦 Future Ideas

- [ ] Add voice/audio-based verification
- [ ] Deploy the ML model on Hugging Face
- [ ] Add fallback classic CAPTCHA
- [ ] Build an admin dashboard to view logs and predictions
- [ ] Implement real-time heatmap visualizations of mouse movement

---

## 👨‍💻 Author

**Kshitij Hundre**  
[GitHub](https://github.com/alchemist240)  
[LinkedIn](https://in.linkedin.com/in/kshitij-hundre-b0a3602b0) <!-- Add your actual profile -->

---


Feel free to use, modify, and contribute!
