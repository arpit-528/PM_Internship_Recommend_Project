### Internship Recommendation API

A Flask-based API that recommends top internships to students based on their skills, sector of interest, qualification, location, and priority category.
The recommendation is calculated using Cosine Similarity on multiple features.

### Live API
Base URL - https://internship-recommend-api.onrender.com
API Endpoint - https://internship-recommend-api.onrender.com/recommend

### Request Format
Method: POST
Content-Type: application/json

Example request - 
{
    "skills": "machine learning python",
    "sector_interest": "aiml",
    "qualification": "BCA",
    "location": "Delhi",
    "priority_category": "ST"
}

### Response Format
The API returns the top 5 internships matching the student's profile. 

Example response - 

{
    "recommendations": [
        {
            "capacity": 36,
            "internship_id": "I0374",
            "location": "Delhi",
            "matching_score": 1.0,
            "priority_category": "ST",
            "qualification_required": "BCA",
            "required_skills": "machine learning python",
            "sector": "aiml",
            "title": "AI Engineer Intern"
        },
        {
            "capacity": 18,
            "internship_id": "I0442",
            "location": "Bangalore",
            "matching_score": 0.915845917619963,
            "priority_category":NaN,
            "qualification_required": "B.Tech ECE",
            "required_skills": "deep learning machine learning python",
            "sector": "aiml",
            "title": "AI Engineer Intern"
        },
        {
            "capacity": 28,
            "internship_id": "I0118",
            "location": "Hyderabad",
            "matching_score": 0.9055289798730622,
            "priority_category": "Rural",
            "qualification_required": "MCA",
            "required_skills": "machine learning pytorch python",
            "sector": "aiml",
            "title": "Data Scientist Intern"
        },
        {
            "capacity": 31,
            "internship_id": "I0367",
            "location": "Delhi",
            "matching_score": 0.8775697302834449,
            "priority_category": "Rural",
            "qualification_required": "BCA",
            "required_skills": "deep learning machine learning python tensorflow",
            "sector": "aiml",
            "title": "Data Scientist Intern"
        },
        {
            "capacity": 48,
            "internship_id": "I0454",
            "location": "Hyderabad",
            "matching_score": 0.8620594905602235,
            "priority_category": "EWS",
            "qualification_required": "M.Tech",
            "required_skills": "machine learning sql",
            "sector": "aiml",
            "title": "ML Research Intern"
        }
    ],
    "status": "success"
}

### How It Works

Input Processing: The API takes student's profile as JSON.
Text Cleaning: Removes special characters, converts to lowercase.
Feature Matching: Compares student's data with internships dataset using TF-IDF and Cosine Similarity.
Ranking: Internships are ranked by similarity score.
Output: Returns top 5 matches.

### Testing in Postman

Method: POST
URL: https://internship-recommend-api.onrender.com/recommend
Body → raw → JSON → Paste the example request.



## Arpit Gupta
