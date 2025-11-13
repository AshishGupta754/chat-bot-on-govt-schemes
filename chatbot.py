import streamlit as st
import requests
import json
import time
import os

# --- Configuration ---

# Set your Streamlit page title and icon
st.set_page_config(
    page_title="GovScheme Chatbot",
    page_icon="🇮🇳"
)

# Add a title to the app
st.title("🇮🇳 Government Schemes Chatbot")
st.caption("Your AI assistant for finding Indian government schemes. Powered by Google Gemini.")

# --- Gemini API Configuration ---

# NOTE: The API key is left as an empty string.
# Canvas will automatically provide it in the runtime environment.
# Do not add your own key here.
API_KEY = "AIzaSyB_xYZ-NkS4GXBusW5TEN9LcWw61upfW_4" 
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-09-2025:generateContent?key={API_KEY}"

# System instruction to guide the chatbot
SYSTEM_PROMPT = (
    "You are a specialized AI assistant for Indian government schemes. "
    "Your name is 'Scheme Sahayak'. "
    "Your purpose is to provide clear, accurate, and helpful information about "
    "various schemes (Central and State) to citizens. "
    "When a user asks a question, use the provided Google Search tool to find "
    "the most relevant and up-to-date information. "
    "Always cite your sources clearly at the end of your answer. "
    "If a user asks a general question, you can respond in a friendly, "
    "conversational manner. "
    "Always answer in the context of India."
)

# --- Core Chatbot Function ---

def get_gemini_response(user_query, chat_history):
    """
    Calls the Gemini API to get a response for the user's query.
    Uses Google Search grounding to find real-time information.
    """
    
    # --- Exponential Backoff ---
    # This is crucial for handling potential API rate limits or transient errors.
    max_retries = 5
    base_delay = 1  # in seconds
    
    for attempt in range(max_retries):
        try:
            # Construct the payload for the API
            payload = {
                "contents": chat_history + [{"role": "user", "parts": [{"text": user_query}]}],
                "tools": [
                    {"google_search": {}}  # Enable Google Search grounding
                ],
                "systemInstruction": {
                    "parts": [{"text": SYSTEM_PROMPT}]
                }
            }

            # Make the POST request to the Gemini API
            response = requests.post(API_URL, headers={"Content-Type": "application/json"}, data=json.dumps(payload), timeout=60)
            
            # Check for a successful response
            if response.status_code == 200:
                result = response.json()
                
                # --- Extract Text and Sources ---
                candidate = result.get('candidates', [{}])[0]
                content = candidate.get('content', {}).get('parts', [{}])[0]
                text_response = content.get('text', "Sorry, I couldn't find an answer to that.")
                
                sources = []
                grounding_metadata = candidate.get('groundingMetadata', {})
                if 'groundingAttributions' in grounding_metadata:
                    for attribution in grounding_metadata.get('groundingAttributions', []):
                        if 'web' in attribution and 'uri' in attribution['web'] and 'title' in attribution['web']:
                            sources.append({
                                "uri": attribution['web']['uri'],
                                "title": attribution['web']['title']
                            })
                
                # --- Format the Response ---
                formatted_response = text_response
                if sources:
                    formatted_response += "\n\n**Sources:**\n"
                    for i, source in enumerate(sources, 1):
                        formatted_response += f"  {i}. [{source['title']}]({source['uri']})\n"
                
                return formatted_response

            # If not successful, raise an error to trigger retry
            else:
                st.error(f"API Error: Status Code {response.status_code}. Retrying...")
                st.error(f"Error Details: {response.text}") # Show error details in UI
                response.raise_for_status()

        except requests.exceptions.RequestException as e:
            if attempt < max_retries - 1:
                delay = base_delay * (2 ** attempt)
                # Do not log to console, as per instructions.
                # print(f"Retry {attempt + 1}/{max_retries} after {delay}s...")
                time.sleep(delay)
            else:
                # print(f"Max retries reached. Error: {e}")
                return f"Sorry, I am having trouble connecting. Please try again later. Error: {e}"
        except Exception as e:
            return f"An unexpected error occurred: {e}"

    return "Sorry, I was unable to get a response after several attempts."


# --- Streamlit Chat UI ---

# Initialize chat history in session state if it doesn't exist
if "messages" not in st.session_state:
    st.session_state.messages = []
    
# Initialize gemini_history (for API)
if "gemini_history" not in st.session_state:
    st.session_state.gemini_history = []

# Display past messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Get new user input
if prompt := st.chat_input("Ask about any government scheme..."):
    
    # 1. Add user message to session state and display it
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # 2. Prepare the API chat history (don't include "model" system messages)
    # The API payload will combine this history with the new prompt
    api_history = [
        {"role": msg["role"], "parts": [{"text": msg["content"]}]}
        for msg in st.session_state.messages
    ]
    
    # 3. Get bot response
    with st.chat_message("assistant"):
        with st.spinner("Searching for the best information..."):
            response = get_gemini_response(prompt, api_history)
        
        st.markdown(response)
    
    # 4. Add bot response to session state
    st.session_state.messages.append({"role": "assistant", "content": response})