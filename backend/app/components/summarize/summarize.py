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

    def generate_summary(self, article_json_string, max_tokens=400):
        # Assuming article_json_string is a serialized JSON of the article
        # with all necessary fields.
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"I will provide you with a JSON output that relates to one specific article. Here is the JSON output: {article_json_string}. Now, give me a summary of the JSON output filling in the blanks below. Give me your final output as the same format as below, with the blanks filled, with the proper quotation marks and brackets to look like a JSON. No explanatory sentence before, in between, or afterwards. (Category: [blank - keep it exactly the same as the JSON output. do not include things like u2018], Title: [blank - keep it exactly the same as the JSON output. do not include things like u2018], Authors: [blank - keep it exactly the same as the JSON output. do not include things like u2018], Source: [blank - keep it exactly the same as the JSON output. do not include things like u2018], Date: [blank -  do not keep it exactly the same as the JSON output, and make it MM-DD-YYYY format, like Oct 25, 2023 for example. do not include things like u2018], Link: [blank - keep it exactly the same as the JSON output. do not include things like u2018], Content: [blank - do not keep it exactly the same as the JSON output, and make it a five bullet points summary starting with 1., 2., and finally 5. If there are any key metrics or dollar figures, feel free to include those as well. do not include things like u2018])."}
            ],
            max_tokens=max_tokens,
            temperature=0.2,
        )

        # Get the content from the response which should be a summarized JSON
        summarized_content = response.choices[0].message['content'].strip()

        return summarized_content
