from flask import Flask, render_template, request
import requests

# Flask 애플리케이션 초기화
app = Flask(__name__)

# Hugging Face API URL 및 헤더 설정
api_url = "https://api-inference.huggingface.co/models/microsoft/Phi-3-mini-4k-instruct"
headers = {"Authorization": "Bearer ?????"}

def generate_text(prompt):
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 50,
            "temperature": 0.5,
            "do_sample": False
        }
    }
    response = requests.post(api_url, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()[0]['generated_text']
    else:
        raise Exception(f"Request failed with status code {response.status_code}: {response.text}")

@app.route('/', methods=['GET', 'POST'])
def home():
    query = None
    response = None

    if request.method == 'POST':
        query = request.form['content']
        try:
            response = generate_text(query)
        except Exception as e:
            response = str(e)

    return render_template('index.html', query=query, response=response)

if __name__ == '__main__':
    app.run(debug=True)
