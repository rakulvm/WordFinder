from flask import Flask, request, jsonify
import pandas as pd
import numpy as np 
from flask_cors import CORS

# Initialize Flask app
print("Initializing Flask...")
app = Flask(__name__)
print("Flask Initialized.")

# Enable CORS for the Flask app
CORS(app)

# Load Excel data
excel_file = "vocalbulary_tracker.xlsx"
sheet_name = "Vocabulary tracker"
df = pd.read_excel(excel_file, sheet_name=sheet_name)

# Function to fetch synonym and antonym
def get_synonym_antonym(word):
    result = df[df["Word"].str.strip().str.lower() == word.strip().lower()]
    if not result.empty:
        synonym = result.iloc[0].get("Synonyms", "Synonym not found")
        antonym = result.iloc[0].get("Antonyms", "Antonym not found")

        # Handle NaN values (if synonym/antonym are NaN in the sheet)
        if isinstance(synonym, float) and np.isnan(synonym):
            synonym = "Synonym not found"
        if isinstance(antonym, float) and np.isnan(antonym):
            antonym = "Antonym not found"

        return synonym, antonym
    else:
        return "Synonym not found", "Antonym not found"
    
@app.route("/api/validate_quiz", methods=["POST"])
def validate_quiz():
    data = request.get_json()
    word = data.get("word", "").strip().lower()
    answer = data.get("answer", "").strip().lower()
    type_of_check = data.get("type", "").strip().lower()  # 'synonym' or 'antonym'

    # Fetch data from the sheet
    result = df[df["Word"].str.lower() == word]
    
    if result.empty:
        return jsonify({"message": "No such word found"}), 400

    # Based on the type (synonym or antonym), validate the answer
    if type_of_check == "synonym":
        synonym_str = result.iloc[0].get("Synonyms", "Synonym not found")
        
        # Handle NaN or missing synonyms
        if pd.isna(synonym_str) or synonym_str == "Synonym not found":
            return jsonify({"message": "Oops! No value found for synonym"}), 400
        
        synonyms = synonym_str.split(",")  # Split multiple synonyms
        if answer in [synonym.strip().lower() for synonym in synonyms]:
            return jsonify({"message": "Hurray! that's the right answer!", "status": "success"}), 200
        else:
            return jsonify({"message": "Oops! that's an wrong synonym!", "status": "failure"}), 400

    elif type_of_check == "antonym":
        antonym_str = result.iloc[0].get("Antonyms", "Antonym not found")
        
        # Handle NaN or missing antonyms
        if pd.isna(antonym_str) or antonym_str == "Antonym not found":
            return jsonify({"message": "Oops! No value found for synonym"}), 400
        
        antonyms = antonym_str.split(",")  # Split multiple antonyms
        if answer in [antonym.strip().lower() for antonym in antonyms]:
            return jsonify({"message": "Hurray! that's the right answer!", "status": "success"}), 200
        else:
            return jsonify({"message": "Oops! that's an wrong synonym!", "status": "failure"}), 400

    else:
        return jsonify({"message": "Invalid type, must be either 'synonym' or 'antonym'"}), 400


# API endpoint for page 1 logic
@app.route("/api/vocabulary", methods=["POST"])
def vocabulary():
    data = request.json
    word = data.get("word")

    if not word:
        return jsonify({"error": "Word is required"}), 400

    synonym, antonym = get_synonym_antonym(word)
    return jsonify({"synonym": synonym, "antonym": antonym})

# Run Flask app
if __name__ == "__main__":
    print("Starting Flask App...")
    app.run(host="0.0.0.0", debug=True)

