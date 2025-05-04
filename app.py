from flask import Flask, render_template, request, redirect, url_for, jsonify
from google import genai
import os
import requests
import google.generativeai as genai
import sqlite3
import markdown

# Load environment variables from .env file
from dotenv import load_dotenv, dotenv_values 
load_dotenv()

# SQLite database setup
current_dir = os.path.dirname(os.path.abspath(__file__))
file = "responses.db"

def init_db():
    connection = sqlite3.connect(current_dir + "/responses.db")
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS analyses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            repo_url TEXT NOT NULL,
            response TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    connection.commit()
    connection.close()

# Gemini API 
GEMINI_API_KEY = os.getenv("API_KEY")
genai.configure(api_key=GEMINI_API_KEY)
chat = genai.GenerativeModel("gemini-2.0-flash")

# GitHub API
GITHUB_API_KEY = os.getenv("GITHUB_API_KEY")

headers = {
    "Authorization": f"token {GITHUB_API_KEY}",
    "Accept": "application/vnd.github.v3+json"
}

app = Flask(__name__)

def extract_owner_and_repo(url):
    try:
        url = url.rstrip('/')
        parts = url.strip().split('/')
        owner = parts[-2]
        repo = parts[-1]
        return owner, repo
    except:
        return None, None

def get_repo_readme(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}/readme"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        content = response.json().get("content")
        encoding = response.json().get("encoding")
        if encoding == "base64":
            import base64
            return base64.b64decode(content).decode("utf-8")
    return "README not found or inaccessible."

init_db()

@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == "POST":
        repo_url = request.form.get('repo')
        owner, repo = extract_owner_and_repo(repo_url)

        if not owner or not repo:
            return render_template("index.html", analysis="Invalid GitHub URL. Please provide a valid URL.")

        readme_text = get_repo_readme(owner, repo)

        prompt = f"""
            You are a technical reviewer for internship resume projects.

            You will analyze the README content of a GitHub repository and return a structured evaluation with the following **six** clearly labeled sections.

            Respond strictly in clean HTML using <strong>, <ul>, <li>, <em>, etc. Do not use Markdown or code blocks. Do not wrap the response in html code blocks or any of that sort of thing. Do not include any other text or explanations outside of the six sections.

            Begin your response directly with the <strong>1. Technologies Used</strong> section. Do not include introductory text, headings, or explanations. Do not use Markdown or plaintext formatting — only HTML tags like <strong>, <ul>, <li>, and <em>.
            Do not include any other text or explanations outside of the six sections. Do not use code blocks or any other formatting. Just provide the six sections in HTML format.
            Use the following format for each section:

            The six required sections are:

            <strong>1. Technologies Used</strong>
            <ul><li>List all languages, frameworks, and tools mentioned in the README.</li></ul>

            <strong>2. Project Purpose</strong>
            <ul><li>Briefly describe what the project does or solves.</li></ul>

            <strong>3. Quality Assessment</strong>
            <ul>
            <li>How well is the documentation written?</li>
            <li>Is the project organized, understandable, and complete?</li>
            </ul>

            <strong>4. Suggestions for Improvement</strong>
            <ul>
            <li>What should the author add or improve for clarity, professionalism, or completeness?</li>
            </ul>

            <strong>5. Suitability for FAANG Resume</strong>
            <ul>
            <li>Give a short evaluation of whether this project is suitable for a high-level software internship application.</li>
            </ul>

            <strong>6. Resume Bullet Point</strong>
            <ul>
            <li>Provide a single bullet point in professional resume language (1 to 2 lines) that describes the impact of the project and technologies used.</li>
            </ul>

            Here is the README content to analyze:
            {readme_text}
            """


        try:
            response = chat.generate_content(prompt)
            raw_output = response.text
            html_output = markdown.markdown(raw_output, extensions=['extra'])

            conn = sqlite3.connect('responses.db')
            c = conn.cursor()
            c.execute("INSERT INTO analyses (repo_url, response) VALUES (?, ?)", (repo_url, html_output))
            conn.commit()
            conn.close()

            return render_template("index.html", analysis=html_output)
        
        except Exception as e:
            error_message = f"<p><strong>Gemini Error:</strong> {e}</p>"
            return render_template("index.html", analysis=error_message)
        
    return render_template("index.html", analysis=None)

@app.route('/history')
def history():
    conn = sqlite3.connect('responses.db')
    c = conn.cursor()
    c.execute("SELECT repo_url, response, timestamp FROM analyses ORDER BY timestamp DESC")
    rows = c.fetchall()
    conn.close()
    return render_template("history.html", rows=rows)


if __name__ == '__main__':
    app.run(debug=True)