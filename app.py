from flask import Flask, request, jsonify
import openai
import pandas as pd
from tqdm import tqdm

# Set up your OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')

app = Flask(__name__)

# Function to generate a summary using OpenAI GPT-3.5
def generate_summary(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=2048,
            n=1,
            stop=None,
            temperature=0.7
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        return f"Error generating summary: {e}"

# Function to format text into the specified ChatML format
def format_chatml(extracted_info, summaries):
    chatml_format = []
    chatml_format.append({"role": "system", "content": ""})
    for key, text in extracted_info.items():
        summary_text = summaries.get(key, "")
        if summary_text:
            chatml_format.append({"role": "user", "content": f"{key.capitalize()}:\n\n{text.strip()}"})
            chatml_format.append({"role": "assistant", "content": f"Summary of {key.capitalize()}:\n\n{summary_text.strip()}"})
    chatml_format.append({"role": "user", "content": ""})
    return chatml_format

# Function to check if the extracted information is meaningful
def is_meaningful(text):
    return text and len(text.split()) > 3

# Endpoint to process the file and generate summaries
@app.route('/process', methods=['POST'])
def process_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    summaries = []
    chatml_format = []

    df = pd.read_csv(file, on_bad_lines='skip')

    tqdm.pandas()
    for index, row in tqdm(df.iterrows(), total=len(df)):
        if isinstance(row['TEXT'], str):
            extracted_info = {}
            if is_meaningful(row['TEXT']):
                extracted_info["chief_complaint"] = row['TEXT']
            if is_meaningful(row['TEXT']):
                extracted_info["assessment"] = row['TEXT']
            if is_meaningful(row['TEXT']):
                extracted_info["investigations"] = row['TEXT']
            if is_meaningful(row['TEXT']):
                extracted_info["plan_treatment"] = row['TEXT']

            summary_dict = {}
            for key, text in extracted_info.items():
                prompt = f"Extract and summarize '{key.replace('_', ' ')}' from the following medical note:\n\n{text}"
                summary_text = generate_summary(prompt)
                if summary_text and "error" not in summary_text.lower():
                    summary_dict[key] = summary_text

            summaries.append({"EXTRACTED": extracted_info, "SUMMARY": summary_dict})
            chatml_format.extend(format_chatml(extracted_info, summary_dict))

    return jsonify({"summaries": summaries, "chatml_format": chatml_format}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
