🇮🇳 Government Schemes Chatbot

This is a simple but powerful AI chatbot built with Python, Streamlit, and the Google Gemini API. It's designed to help Indian citizens find clear and up-to-date information about various government schemes.

The chatbot uses Google Search grounding (RAG) to find real-time information and cite its sources, ensuring the information is accurate and trustworthy.

(Suggestion: Run your app locally, take a screenshot, and replace the URL above)

🚀 How to Deploy This App

The easiest way to deploy this app is with Streamlit Community Cloud.

Step 1: Push to GitHub

Create a new, public repository on GitHub.

Push these four files to your new repository:

chatbot.py

requirements.txt

.gitignore

README.md

Step 2: Deploy on Streamlit Community Cloud

Sign up or log in to share.streamlit.io.

Click the "New app" button.

Connect your GitHub account and select the repository you just created.

The main file path should be chatbot.py.

Click the "Advanced settings" link.

Go to the "Secrets" section. This is where you will securely add your API key.

Paste the following into the Secrets text box (replacing the value with your actual key):

GEMINI_API_KEY="AIzaSy...your...long...api...key...here"


Click "Save" and then "Deploy!"

Your app will be live and accessible to anyone in just a few minutes!

💻 How to Run Locally

To test the app on your own computer:

Clone the repository:

git clone <your-repo-url>
cd <your-repo-name>


Create and activate a virtual environment:

python -m venv venv
.\venv\Scripts\activate  # On Windows
source venv/bin/activate # On macOS/Linux


Install the required libraries:

pip install -r requirements.txt


Set the API Key Environment Variable:

On Windows (Command Prompt):

set GEMINI_API_KEY="YOUR_API_KEY_HERE"


On Windows (PowerShell):

$env:GEMINI_API_KEY="YOUR_API_KEY_HERE"


On macOS/Linux:

export GEMINI_API_KEY="YOUR_API_KEY_HERE"


Run the app:

streamlit run chatbot.py
