

from flask import Flask, request, jsonify
import pandas as pd
import pickle
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

#  Load trained vectorizers & internship dataset
with open("skills_vectorizer.pkl", "rb") as f:
    skills_vectorizer = pickle.load(f)

with open("sector_vectorizer.pkl", "rb") as f:
    sector_vectorizer = pickle.load(f)

internships_df = pd.read_csv("internships_cleaned_for_api.csv")

#  Initialize Flask app
app = Flask(__name__)

#  Recommendation function
def recommend_internships(student_data, top_n=5):
    # Extract student info
    student_skills = student_data.get("skills", "")
    student_sector = student_data.get("sector_interest", "")

    # Vectorize student data
    student_skills_vec = skills_vectorizer.transform([student_skills])
    student_sector_vec = sector_vectorizer.transform([student_sector])

    # Vectorize internship data
    internship_skills_vec = skills_vectorizer.transform(internships_df["required_skills"])
    internship_sector_vec = sector_vectorizer.transform(internships_df["sector"])

    # Calculate similarity
    skills_similarity = cosine_similarity(student_skills_vec, internship_skills_vec)[0]
    sector_similarity = cosine_similarity(student_sector_vec, internship_sector_vec)[0]

    # Weighted matching score (60% skills + 40% sector)
    matching_score = (0.6 * skills_similarity) + (0.4 * sector_similarity)

    # Add score to DataFrame
    internships_df["matching_score"] = matching_score

    # Sort and get top N
    top_matches = internships_df.sort_values(by="matching_score", ascending=False).head(top_n)

    # Convert to list of dicts for JSON response
    recommendations = top_matches[[
        "internship_id", "title", "required_skills", "qualification_required",
        "location", "sector", "capacity", "priority_category", "matching_score"
    ]].to_dict(orient="records")

    return recommendations

# Flask route for recommendation
@app.route("/recommend", methods=["POST"])
def recommend():
    try:
        student_data = request.get_json()
        recommendations = recommend_internships(student_data, top_n=5)
        return jsonify({"status": "success", "recommendations": recommendations})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

#  Run Flask app
if __name__ == "__main__":
    app.run(debug=True)
