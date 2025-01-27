# Assignment-DeepSeek

This repository provides a lightweight Flask-based web interface for interacting with the **DeepSeek-R1-Distill-Qwen-1.5B** model, powered by Hugging Face's `transformers` library. The interface allows users to submit queries and receive model-generated responses in real-time.

---

## Setup and Usage

### Prerequisites
- Python 3.8 or later
- Install required dependencies:
  ```bash
  pip install transformers flask
  ```

### Running the Application
1. Clone this repository and navigate to the project folder.
2. Start the Flask server:
   ```bash
   python app.py
   ```
3. Open your browser and navigate to `http://localhost:5000`.

---

## Query Flow
1. Enter your query in the text box provided on the web page.
2. Press **Submit**.
3. View the model's response below the input field.

---

## Key Components
- **Model Loading**: Loads the `DeepSeek-R1-Distill-Qwen-1.5B` model at startup.
- **Task Queue**: Processes queries asynchronously using a worker thread.
- **HTML Frontend**: Provides a clean and intuitive interface for user interaction.

---

## Notes
- By default, the app runs on port `5000` and binds to all interfaces (`0.0.0.0`).
- Modify the model or tokenizer in the `load_model()` function if needed.

--- 
