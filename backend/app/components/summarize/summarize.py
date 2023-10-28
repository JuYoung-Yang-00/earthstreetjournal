import openai
import sys
import os
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
if project_root not in sys.path:
    sys.path.append(project_root)
from config import Config

openai.api_key = Config.OPENAI_API_KEY

class OpenAISummarizer:
    def __init__(self, api_key):
        openai.api_key = api_key

    def generate_summary(self, text, max_tokens=100):
        print(f"Content being fed to OpenAI: {text}\n")
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"Come up with a short title then summarize the content: {text}"}
            ],
            max_tokens=max_tokens
        )
        summarized_content = response.choices[0].message['content'].strip()
        
        # Split the summarized content at the first newline character
        title, summary = summarized_content.split("\n", 1)
        
        # Remove the "Title: " prefix from the title
        title = title.replace("Title:", "").strip()
        
        return title, summary.strip()
