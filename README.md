# 🔍 DevLens

DevLens is a clean, minimal web app that lets you paste a GitHub repo and instantly get:
- 📦 Analyzed tech stack (languages, frameworks, libraries)
- ✍️ Feedback on documentation and structure
- 🚀 Suggestions for improvement
- 💼 A professional resume bullet point
- 🎯 A judgment on whether it’s FAANG-internship ready

It uses Gemini 2.0 Flash and the GitHub API to do all the heavy lifting for you.

---

## 🖼️ Demo

![Demo](assets/github_analyzer.gif)

---

## ✨ Features

- Paste any GitHub repo URL
- Automatically fetches the README file
- Uses Gemini 2.0 Flash to analyze and format results
- Shows past analyses with timestamps
- Cozy UI: soft background, Inter font, blurred cards, subtle shadows
- Stores responses in a local SQLite database

---

## 🚀 Tech Stack

- Flask
- Google Gemini API (via `google.generativeai`)
- GitHub REST API (for README access)
- SQLite
- HTML, CSS (custom, no Tailwind)
- Python 3.13
- dotenv for environment management

---

## 📂 Folder Structure

```
devlens/
├── templates/
│   ├── index.html
│   └── history.html
├── static/
│   └── styles.css
├── app.py
├── responses.db
├── .env
└── README.md
```

---

## ⚙️ How to Run Locally

```bash
git clone https://github.com/yourusername/devlens.git
cd devlens
python3 -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
```

Create a `.env` file:

```env
API_KEY=your_gemini_api_key
GITHUB_API_KEY=your_github_token
```

Then run:

```bash
flask run
```

Go to [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.

---

## 🧪 Ideas for Expansion

- Let users paste the full repo and analyze code files
- Add visual ratings for clarity, completeness, and structure
- Export results to PDF or LaTeX resume
- Add GitHub OAuth login and personalized dashboards
- Deployment to Render, Fly.io, or Railway

---

## 📄 License

MIT — free to use, improve, and deploy.
