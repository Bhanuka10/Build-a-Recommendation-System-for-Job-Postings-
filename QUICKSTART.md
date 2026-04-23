# QUICKSTART GUIDE - Job Recommendation Web App

## 🚀 Getting Started in 3 Steps

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Start the Application
**Windows:**
```bash
run.bat
```

**Mac/Linux:**
```bash
bash run.sh
```

**Or manually:**
```bash
python app.py
```

### Step 3: Open in Browser
```
http://localhost:5000
```

---

## 📋 How to Use the Web App

### Method 1: Enter Skills Directly

1. Click the **"Skills"** tab
2. Enter your skills (separated by commas):
   ```
   Python, Machine Learning, SQL, NumPy, Scikit-learn
   ```
3. Select your experience level:
   - Entry Level (0-2 years)
   - Mid Level (3-7 years)
   - Senior Level (8+ years)
4. Choose number of recommendations (5-20)
5. Click **"Find Matching Jobs"**

### Method 2: Upload Resume

1. Click the **"Resume"** tab
2. Upload your resume (PDF, TXT, or DOCX)
3. Select your experience level
4. Choose number of recommendations
5. Click **"Analyze Resume"**

---

## 📊 Understanding Your Results

Each recommendation shows:

| Field | What It Means |
|-------|---------------|
| **#1, #2, #3** | Ranking (1 is best match) |
| **Job Title** | Position being recommended |
| **Company** | Hiring company name |
| **Location** | Job location |
| **Salary** | Annual salary range |
| **Industry** | Industry sector |
| **Required Skills** | Skills they're looking for |
| **Skill Match** | How well your skills match (%) |
| **Experience Match** | Bonus for matching experience level (%) |
| **Overall Match** | Combined recommendation score (%) |

---

## 🎯 Matching Algorithm Explained

The system scores each job using:

```
Overall Score = (Skill Match × 0.85) + (Experience Match × 0.15)
```

### Skill Match (85% of score)
- Uses TF-IDF vectorization to compare your skills with job requirements
- More precise skill overlap = higher score
- Score range: 0-100%

### Experience Match (15% of score)
- Bonus when your level matches the job level
- **Perfect match**: +10% bonus
- **One level apart**: +5% bonus
- **Two levels apart**: +0% bonus

---

## 💡 Tips for Best Results

1. **Be Specific with Skills**
   - ✓ Good: "Python, Machine Learning, TensorFlow, SQL"
   - ✗ Avoid: "programming, data science"

2. **Match Your Experience Level**
   - Entry Level: 0-2 years experience
   - Mid Level: 3-7 years experience
   - Senior Level: 8+ years experience

3. **Try Different Skill Combinations**
   - Your current skills
   - Desired skills you're learning
   - Industry-specific skills

4. **Resume Tips**
   - Use clear, professional formatting
   - Include all relevant skills
   - Mention programming languages and tools
   - List certifications and technologies

---

## 🔧 Troubleshooting

### "No matching jobs found"
- Your skills might be too specific or niche
- Try with common skills: "Python, SQL, Communication"
- Check that you selected the right experience level

### "Could not extract text from resume"
- Your PDF might be image-based (scanned)
- Try converting to TXT first
- Use a simple, standard PDF format

### Port 5000 Already in Use
Edit `app.py` and change:
```python
app.run(port=5001)  # Use 5001 instead
```

### "Recommendation engine not initialized"
- Check that data files exist:
  - `data/processed/jobs_clean.csv`
  - `data/processed/job_tfidf.npz`
- Run: `pip install -r requirements.txt`

---

## 📱 Browser Compatibility

Works on:
- Chrome / Chromium
- Firefox
- Safari
- Edge
- Mobile browsers (iOS Safari, Chrome Mobile)

Recommended: Use latest version of Chrome or Firefox

---

## 🔐 Privacy & Data

- Resumes are processed in-memory only
- Files are deleted immediately after processing
- No data is stored or logged
- All processing happens locally

---

## 📧 API Usage (For Developers)

### Get Recommendations via API
```bash
curl -X POST http://localhost:5000/api/recommend \
  -H "Content-Type: application/json" \
  -d '{
    "skills": "Python, SQL, Machine Learning",
    "experience_level": "Mid Level",
    "top_n": 10
  }'
```

### Upload Resume via API
```bash
curl -X POST http://localhost:5000/api/upload-resume \
  -F "file=@resume.pdf" \
  -F "experience_level=Mid Level" \
  -F "top_n=10"
```

### Health Check
```bash
curl http://localhost:5000/api/health
```

---

## 📚 Project Structure

```
Build-a-Recommendation-System-for-Job-Postings/
├── app.py                           # Main Flask application
├── backend/
│   ├── __init__.py
│   └── recommendation_engine.py     # Core recommendation logic
├── templates/
│   └── index.html                   # Web interface
├── data/
│   └── processed/
│       ├── jobs_clean.csv           # Job database
│       └── job_tfidf.npz            # Pre-computed vectors
├── requirements.txt                 # Dependencies
├── README_WEBAPP.md                 # Detailed documentation
├── QUICKSTART.md                    # This file
├── run.bat                          # Windows startup
├── run.sh                           # Mac/Linux startup
└── test_webapp.py                   # Test script
```

---

## ⚡ Quick Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run tests
python test_webapp.py

# Start application
python app.py

# Stop application
Press Ctrl+C

# View logs
# Check browser console (F12) for frontend logs
```

---

## 🎓 How the Algorithm Works

1. **Text Processing**
   - Skills are converted to lowercase
   - Special characters are removed
   - Text is tokenized into character n-grams

2. **TF-IDF Vectorization**
   - Each job's required skills → TF-IDF vector
   - Your skills → TF-IDF vector
   - Uses 2-3 character n-grams for robustness

3. **Similarity Calculation**
   - Cosine similarity between vectors
   - Measures angle between skill vectors
   - Higher = better skill match

4. **Experience Bonus**
   - Checks if your level matches job level
   - Adds bonus percentage to base score

5. **Final Ranking**
   - Scores all jobs
   - Returns top N ranked by final score

---

## 📈 Performance

- **Database**: 50,000+ jobs
- **Candidates**: 815 in training data
- **Recommendation Time**: < 500ms
- **Supported**: Up to 20 recommendations per query

---

## 🆘 Getting Help

1. **Check the logs in the browser console** (Press F12)
2. **Review README_WEBAPP.md** for detailed docs
3. **Check data files exist** in `data/processed/`
4. **Try the test script**: `python test_webapp.py`

---

## ✨ Features

✓ Upload CV/Resume (PDF, TXT, DOCX)
✓ Enter skills manually
✓ Smart TF-IDF based matching
✓ Experience level compatibility
✓ Detailed job information
✓ Match percentage scores
✓ Responsive design
✓ Fast recommendations
✓ No data stored

---

## 🚀 Next Steps

1. ✅ Start the application
2. ✅ Try entering your skills
3. ✅ Explore the recommendations
4. ✅ Upload a resume
5. ✅ Experiment with different search criteria

**Enjoy finding your perfect job match!** 💼

---

*Created as part of the Job Recommendation System build*
