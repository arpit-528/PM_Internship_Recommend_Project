from flask import Flask, request, jsonify
from flask_cors import CORS  # Import the CORS library
import pandas as pd
import pickle
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Load trained vectorizers & internship dataset
try:
    with open("skills_vectorizer.pkl", "rb") as f:
        skills_vectorizer = pickle.load(f)

    with open("sector_vectorizer.pkl", "rb") as f:
        sector_vectorizer = pickle.load(f)

    internships_df = pd.read_csv("internships_cleaned_for_api.csv")
    
    # Ensure required columns exist to prevent errors later
    required_cols = ["required_skills", "sector"]
    for col in required_cols:
        if col not in internships_df.columns:
            raise FileNotFoundError(f"Column '{col}' not found in internships_cleaned_for_api.csv")

except FileNotFoundError as e:
    print(f"Error loading model or data file: {e}")
    # Exit or handle gracefully if files are missing
    exit()


# Initialize Flask app
app = Flask(__name__)

# --- FIX 1: Enable CORS ---
# This is the crucial step that allows your React frontend to communicate with this API.
CORS(app)

# Recommendation function
def recommend_internships(student_data, top_n=10):
    """Recommends internships based on student profile."""
    
    # --- FIX 2: Handle incoming data format from React app ---
    # The frontend sends arrays for skills and sector interests.
    # We join them into strings for the vectorizer.
    student_skills_list = student_data.get("skill", [])
    student_sector_list = student_data.get("sector_interest", [])
    
    student_skills_str = " ".join(student_skills_list)
    student_sector_str = " ".join(student_sector_list)

    # Vectorize student data
    student_skills_vec = skills_vectorizer.transform([student_skills_str])
    student_sector_vec = sector_vectorizer.transform([student_sector_str])

    # Vectorize internship data from the DataFrame
    internship_skills_vec = skills_vectorizer.transform(internships_df["required_skills"].fillna(""))
    internship_sector_vec = sector_vectorizer.transform(internships_df["sector"].fillna(""))

    # Calculate similarity scores
    skills_similarity = cosine_similarity(student_skills_vec, internship_skills_vec)[0]
    sector_similarity = cosine_similarity(student_sector_vec, internship_sector_vec)[0]

    # Weighted matching score (e.g., 60% skills + 40% sector)
    # This can be tuned for better performance
    matching_score = (0.6 * skills_similarity) + (0.4 * sector_similarity)

    # Create a copy of the dataframe to avoid modifying the original
    recommendation_df = internships_df.copy()
    recommendation_df["match_score"] = np.round(matching_score * 100, 2) # Store as percentage

    # Sort and get top N matches
    top_matches = recommendation_df.sort_values(by="match_score", ascending=False).head(top_n)

    # Convert to list of dictionaries for the JSON response
    recommendations = top_matches.to_dict(orient="records")

    return recommendations

# Flask route for recommendation
@app.route("/recommend", methods=["POST"])
def recommend():
    """API endpoint to get internship recommendations."""
    if not request.is_json:
        return jsonify({"status": "error", "message": "Request must be JSON"}), 400
        
    try:
        student_data = request.get_json()
        recommendations = recommend_internships(student_data, top_n=15)
        return jsonify({"status": "success", "recommendations": recommendations})
    except Exception as e:
        # Log the full error for debugging on the server
        print(f"An error occurred: {e}") 
        return jsonify({"status": "error", "message": "An internal error occurred."}), 500

# Run Flask app
# --- FIX 3: Corrected dunder name for running the script ---
if __name__ == "__main__":
    # For production on Render, you might use a production-ready server like Gunicorn
    # For local testing, app.run() is fine.
    app.run(debug=True, host='0.0.0.0')