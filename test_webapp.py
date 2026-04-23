"""
Quick test script to verify the recommendation engine works
"""
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

from backend.recommendation_engine import JobRecommendationEngine


def test_engine():
    """Test the recommendation engine."""
    print("\n" + "="*80)
    print("JOB RECOMMENDATION SYSTEM - ENGINE TEST")
    print("="*80 + "\n")
    
    try:
        # Initialize engine
        print("1. Initializing recommendation engine...")
        engine = JobRecommendationEngine()
        print("   ✓ Engine initialized successfully\n")
        
        # Test with sample skills
        print("2. Testing with sample skills...")
        sample_skills = "Python, Machine Learning, SQL, NumPy, Scikit-learn"
        print(f"   Input Skills: {sample_skills}")
        
        recs = engine.get_recommendations(sample_skills, 'Mid Level', top_n=5)
        print(f"   ✓ Generated {len(recs)} recommendations\n")
        
        # Display results
        print("3. Top 3 Recommendations:\n")
        for rec in recs[:3]:
            print(f"   #{rec['rank']} - {rec['job_title']}")
            print(f"       Company: {rec['company']}")
            print(f"       Location: {rec['location']}")
            print(f"       Match Score: {rec['match_percentage']}%")
            print(f"       Salary: {rec['salary']}")
            print()
        
        print("="*80)
        print("✓ ALL TESTS PASSED - Engine is working correctly!")
        print("="*80 + "\n")
        print("To start the web application, run:")
        print("  → python app.py")
        print("\nThen open: http://localhost:5000\n")
        
        return True
        
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        print("\nTroubleshooting:")
        print("  1. Check that data files exist in: data/processed/")
        print("  2. Ensure jobs_clean.csv is present")
        print("  3. Run: pip install -r requirements.txt")
        return False


if __name__ == '__main__':
    success = test_engine()
    sys.exit(0 if success else 1)
