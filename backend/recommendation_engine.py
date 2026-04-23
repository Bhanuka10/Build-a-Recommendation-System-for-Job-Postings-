"""
Recommendation Engine for Job Postings
Handles skill matching and job recommendations based on candidate input
"""
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from pathlib import Path
import re
from typing import List, Dict, Tuple


class JobRecommendationEngine:
    """Engine to generate job recommendations based on candidate skills."""
    
    def __init__(self, data_dir: str = None):
        """Initialize the recommendation engine with data and models."""
        if data_dir is None:
            # Find data directory relative to this file
            current_dir = Path(__file__).parent
            project_root = current_dir.parent
            data_dir = project_root / 'data' / 'processed'
        
        self.data_dir = Path(data_dir)
        self.jobs = None
        self.jobs_tfidf = None
        self.vectorizer = None
        self.top_n = 10
        
        self._load_data()
        self._initialize_vectorizer()
    
    def _load_data(self):
        """Load jobs data and TF-IDF vectors."""
        try:
            self.jobs = pd.read_csv(self.data_dir / 'jobs_clean.csv')
            print(f"✓ Loaded {len(self.jobs)} jobs")
        except Exception as e:
            print(f"✗ Error loading jobs: {e}")
            raise
    
    def _initialize_vectorizer(self):
        """Initialize TF-IDF vectorizer with job skills."""
        try:
            # Create a simple character-level vectorizer
            # We'll use a more efficient approach by splitting skills
            self.vectorizer = TfidfVectorizer(
                analyzer='char',
                ngram_range=(2, 3),
                lowercase=True,
                max_features=1000  # Limit features for efficiency
            )
            
            # Fit on a sample of job skills for speed
            # Take every 10th job to create vocabulary
            sample_skills = self.jobs['Required_Skills_Clean'].fillna('').iloc[::10].values
            sample_text = ' '.join(sample_skills)
            
            self.vectorizer.fit([sample_text])
            print(f"✓ Initialized vectorizer with {len(self.vectorizer.get_feature_names_out())} features")
            
            # Note: TF-IDF vectors will be computed on-the-fly for candidates
            # This avoids computing all 50k job vectors upfront
        except Exception as e:
            print(f"✗ Error initializing vectorizer: {e}")
            raise
    
    def extract_skills(self, text: str) -> str:
        """Extract and clean skills from text."""
        # Convert to lowercase
        text = text.lower()
        # Remove special characters but keep spaces
        text = re.sub(r'[^a-z0-9\s,]', '', text)
        return text
    
    def get_recommendations(
        self, 
        skills_text: str, 
        experience_level: str = 'Mid Level',
        top_n: int = 10
    ) -> List[Dict]:
        """
        Get top job recommendations for a candidate.
        
        Args:
            skills_text: Comma-separated skills or resume text
            experience_level: 'Entry Level', 'Mid Level', or 'Senior Level'
            top_n: Number of recommendations to return
        
        Returns:
            List of dictionaries with job recommendations and scores
        """
        # Extract and clean skills
        clean_skills = self.extract_skills(skills_text)
        
        # Transform candidate skills to TF-IDF
        try:
            cand_tfidf = self.vectorizer.transform([clean_skills])
        except Exception as e:
            print(f"✗ Error transforming candidate skills: {e}")
            return []
        
        # Transform all job skills to TF-IDF vectors
        # Split into batches to avoid memory issues
        batch_size = 5000
        all_scores = []
        
        for i in range(0, len(self.jobs), batch_size):
            batch_end = min(i + batch_size, len(self.jobs))
            batch_skills = self.jobs['Required_Skills_Clean'].fillna('').iloc[i:batch_end].values
            
            # Transform batch
            batch_tfidf = self.vectorizer.transform(batch_skills)
            
            # Calculate similarity for this batch
            batch_scores = cosine_similarity(cand_tfidf, batch_tfidf)[0]
            all_scores.extend(batch_scores)
        
        skill_scores = np.array(all_scores)
        
        # Experience level bonus
        exp_bonus = self._calculate_experience_bonus(experience_level)
        
        # Final score: 85% skill similarity + 15% experience bonus
        final_scores = 0.85 * skill_scores + 0.15 * exp_bonus
        
        # Get top N indices
        top_indices = np.argsort(final_scores)[::-1][:top_n]
        
        # Build recommendations
        recommendations = []
        for rank, idx in enumerate(top_indices, 1):
            job = self.jobs.iloc[idx]
            recommendations.append({
                'rank': rank,
                'job_title': job['Job Title'],
                'company': job['Company'],
                'location': job['Location'],
                'salary': f"${job['Salary']:,.0f}" if pd.notna(job['Salary']) else 'Not specified',
                'industry': job['Industry'],
                'required_skills': job['Required_Skills_Clean'],
                'experience_level': job['Experience Level'],
                'skill_match_score': round(float(skill_scores[idx]), 4),
                'experience_match_bonus': round(float(exp_bonus[idx]), 4),
                'final_score': round(float(final_scores[idx]), 4),
                'match_percentage': round(float(final_scores[idx]) * 100, 1)
            })
        
        return recommendations
    
    def _calculate_experience_bonus(self, cand_level: str) -> np.ndarray:
        """Calculate experience matching bonus for all jobs."""
        bonus = np.zeros(len(self.jobs))
        
        # Map experience levels to numeric values
        level_map = {'Entry Level': 0, 'Mid Level': 1, 'Senior Level': 2}
        cand_numeric = level_map.get(cand_level, 1)
        
        for idx, job_level in enumerate(self.jobs['Experience Level'].fillna('Mid Level')):
            job_numeric = level_map.get(job_level, 1)
            diff = abs(cand_numeric - job_numeric)
            
            if diff == 0:
                bonus[idx] = 0.10
            elif diff == 1:
                bonus[idx] = 0.05
            else:
                bonus[idx] = 0.0
        
        return bonus


if __name__ == '__main__':
    # Test the engine
    engine = JobRecommendationEngine()
    
    # Test with sample skills
    sample_skills = "Python, Machine Learning, SQL, NumPy, Scikit-learn"
    recs = engine.get_recommendations(sample_skills, 'Mid Level', top_n=5)
    
    print("\n" + "="*80)
    print("SAMPLE RECOMMENDATIONS")
    print("="*80)
    for rec in recs:
        print(f"\n#{rec['rank']} - {rec['job_title']}")
        print(f"   Company: {rec['company']} | Location: {rec['location']}")
        print(f"   Salary: {rec['salary']} | Industry: {rec['industry']}")
        print(f"   Required Skills: {rec['required_skills']}")
        print(f"   Match Score: {rec['match_percentage']}%")
