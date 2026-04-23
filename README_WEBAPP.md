# Job Recommendation System - Web Interface

A simple yet powerful web application that helps candidates find the most relevant job postings based on their skills and experience.

## Features

✨ **Key Capabilities:**
- 📄 **Resume Upload** - Upload PDF, TXT, or DOCX files
- 🎯 **Skill Input** - Enter skills manually or extract from resume
- 📊 **Smart Matching** - Uses TF-IDF algorithm (85% skill match + 15% experience bonus)
- 💼 **Detailed Recommendations** - Ranked list with match scores
- 🎓 **Experience Level** - Match by Entry Level, Mid Level, or Senior Level

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Application
```bash
python app.py
```

### 3. Open in Browser
```
http://localhost:5000
```

## How It Works

### Input Methods

**Option 1: Enter Skills Directly**
1. Go to the "Skills" tab
2. Enter your skills (comma-separated)
3. Select your experience level
4. Click "Find Matching Jobs"

**Option 2: Upload Resume**
1. Go to the "Resume" tab
2. Upload a PDF, TXT, or DOCX file
3. Select your experience level
4. Click "Analyze Resume"

### Recommendation Algorithm

The system uses a sophisticated matching algorithm:

- **Skill Similarity (85%)**: Uses TF-IDF vectorization to match your skills with job requirements
- **Experience Bonus (15%)**: Adds a bonus when your experience level matches the job level
  - Perfect match (same level): +10%
  - One level apart: +5%
  - Two+ levels apart: +0%

### Results

Each job recommendation shows:
- **Rank**: Position in the recommendation list
- **Job Details**: Title, Company, Location, Salary, Industry
- **Experience Level**: Entry/Mid/Senior
- **Required Skills**: Top skills needed
- **Match Scores**: 
  - Skill Match %: How well your skills align
  - Experience Match %: Level compatibility bonus
  - Overall Match %: Final recommendation score

## Project Structure

```
.
├── app.py                          # Flask application
├── backend/
│   ├── __init__.py
│   └── recommendation_engine.py    # Core recommendation logic
├── templates/
│   └── index.html                  # Web interface
├── data/
│   └── processed/
│       ├── jobs_clean.csv          # Job listings database
│       ├── job_tfidf.npz           # Pre-computed TF-IDF vectors
│       └── ...
├── requirements.txt                 # Python dependencies
└── README_WEBAPP.md                # This file
```

## API Endpoints

### GET /
Main web interface

### POST /api/recommend
Get job recommendations based on skills
```json
{
    "skills": "Python, Machine Learning, SQL",
    "experience_level": "Mid Level",
    "top_n": 10
}
```

### POST /api/upload-resume
Upload and analyze a resume
```
multipart/form-data:
- file: resume.pdf
- experience_level: Mid Level
- top_n: 10
```

### GET /api/health
Health check endpoint

## Supported File Formats

- **PDF** (.pdf) - Most recommended
- **Text** (.txt) - Plain text resumes
- **Word** (.docx) - Requires python-docx

Maximum file size: 5MB

## Configuration

Edit `backend/recommendation_engine.py` to customize:
- `TOP_N`: Default number of recommendations
- `SKILL_WEIGHT`: Skill matching weight (default: 0.85)
- `EXPERIENCE_WEIGHT`: Experience bonus weight (default: 0.15)
- `EXPERIENCE_BONUS`: Bonus percentages for level matches

## Troubleshooting

**Issue: "Recommendation engine not initialized"**
- Check that data files exist in `data/processed/`
- Ensure `jobs_clean.csv` is present

**Issue: "Could not extract text from file"**
- Try uploading a different PDF file
- Convert to .txt and try again

**Issue: Port 5000 already in use**
- Change port in `app.py`: `app.run(port=5001)`

## Data Requirements

The system needs the following data files in `data/processed/`:
- `jobs_clean.csv` - Job listings with skills and metadata
- `job_tfidf.npz` - Pre-computed TF-IDF vectors for jobs (optional)

## License

This project is part of the Job Recommendation System build.

## Support

For issues or feature requests, check the main project README.
