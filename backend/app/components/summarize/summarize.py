# app/components/summarize/summarize.py
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

    def generate_summary(self, article_json_string):
        response = openai.chat.completions.create(
            model="ft:gpt-3.5-turbo-1106:personal::8I5FRF9j",
            messages=[
                {"role": "system", "content": "Your task is to process the input text, which is a structured JSON document containing a news article related to environment and politics. You should generate a JSON formatted output that summarizes the article in 400-600 words, creates a new title, and provides the date without the time. The summarization should include important facts, figures, and citations where relevant. It should conclude with three main takeaway points listed in bullet points in a new attribute named 'mainpoints' that is a list of strings. Avoid language that makes it obvious that the text is a summary; instead, present the information as if it were a condensed original article. Make sure to include all attributes in the input json in the output and add the 'mainpoints' attribute."},
                {"role": "user", "content": f"{article_json_string}"}
            ],
        )

        summarized_content = response.choices[0].message.content
        return summarized_content
