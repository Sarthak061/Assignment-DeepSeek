from transformers import AutoModelForCausalLM, AutoTokenizer
from flask import Flask, request, jsonify, render_template_string
from threading import Thread
from queue import Queue
import time

def load_model():
    model_name = "deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)
    print("Model loaded successfully!")
    return model, tokenizer

model, tokenizer = load_model()

app = Flask(__name__)

task_queue = Queue()

def process_queue():
    while True:
        func, args = task_queue.get()
        func(*args)
        task_queue.task_done()

worker_thread = Thread(target=process_queue, daemon=True)
worker_thread.start()

html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DeepSeek R1 WebUI</title>
    <style>
        body { font-family: Arial, sans-serif; padding: 20px; }
        textarea { width: 100%; height: 100px; margin-bottom: 10px; }
        button { padding: 10px 20px; background-color: #007BFF; color: white; border: none; cursor: pointer; }
        button:hover { background-color: #0056b3; }
        #response { margin-top: 20px; white-space: pre-wrap; }
    </style>
</head>
<body>
    <h1>DeepSeek R1 WebUI</h1>
    <form id="query-form">
        <textarea id="query" placeholder="Enter your query here..."></textarea><br>
        <button type="button" onclick="sendQuery()">Submit</button>
    </form>
    <div id="response"></div>
    <script>
        async function sendQuery() {
            const query = document.getElementById("query").value;
            const responseDiv = document.getElementById("response");
            responseDiv.textContent = "Processing...";

            try {
                const response = await fetch("/process", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ query })
                });

                const result = await response.json();
                responseDiv.textContent = result.response;
            } catch (error) {
                responseDiv.textContent = "Error: " + error.message;
            }
        }
    </script>
</body>
</html>
"""

def process_query(query):
    print(f"Processing query: {query}")
    prompt = f"### Instruction:\n{query}\n\n### Response:"

    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
        tokenizer.pad_token_id = tokenizer.eos_token_id

    inputs = tokenizer(prompt, return_tensors="pt", padding=True)

    outputs = model.generate(
        inputs["input_ids"],
        max_length=500
    )
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    response = response.split("### Response:")[1].strip()
    return response


@app.route('/')
def index():
    return render_template_string(html_template)

@app.route('/process', methods=['POST'])
def process_request():
    data = request.get_json()
    query = data.get('query', '')

    if not query:
        return jsonify({"error": "No query provided."}), 400

    result = []

    def task():
        result.append(process_query(query))

    task_queue.put((task, []))
    task_queue.join()

    return jsonify({"response": result[0]})

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
