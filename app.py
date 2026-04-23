"""
Flask application for Job Recommendation System
Provides REST API and serves the web interface
"""
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
from pathlib import Path
import pypdf  # For PDF reading
import logging

# Import the recommendation engine
from backend.recommendation_engine import JobRecommendationEngine

# Configuration
app = Flask(__name__)
CORS(app)

# Upload folder setup
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'txt', 'docx'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# Create upload folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize recommendation engine
try:
    engine = JobRecommendationEngine()
    logger.info("✓ Recommendation engine initialized successfully")
except Exception as e:
    logger.error(f"✗ Failed to initialize recommendation engine: {e}")
    engine = None


def allowed_file(filename):
    """Check if file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def extract_text_from_pdf(filepath):
    """Extract text from PDF file."""
    try:
        text = ""
        with open(filepath, 'rb') as file:
            pdf_reader = pypdf.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text() + " "
        return text.strip()
    except Exception as e:
        logger.error(f"Error reading PDF: {e}")
        return ""


def extract_text_from_file(filepath):
    """Extract text from uploaded file."""
    file_ext = Path(filepath).suffix.lower().lstrip('.')
    
    try:
        if file_ext == 'pdf':
            return extract_text_from_pdf(filepath)
        elif file_ext == 'txt':
            with open(filepath, 'r', encoding='utf-8') as file:
                return file.read()
        elif file_ext == 'docx':
            # For docx, you'd need python-docx library
            # For now, we'll return a message
            return "DOCX support requires python-docx library. Please convert to PDF or TXT."
        else:
            return ""
    except Exception as e:
        logger.error(f"Error extracting text: {e}")
        return ""


@app.route('/')
def index():
    """Serve the main webpage."""
    return render_template('index.html')


@app.route('/api/recommend', methods=['POST'])
def get_recommendations():
    """
    Get job recommendations based on skills or resume.
    
    Expected JSON:
    {
        "skills": "Python, Machine Learning, ...",  // OR
        "resume_text": "Full resume text",
        "experience_level": "Mid Level",
        "top_n": 10
    }
    """
    if not engine:
        return jsonify({'error': 'Recommendation engine not initialized'}), 500
    
    try:
        data = request.get_json()
        
        # Get input data
        skills = data.get('skills', '').strip()
        resume_text = data.get('resume_text', '').strip()
        experience_level = data.get('experience_level', 'Mid Level')
        top_n = min(int(data.get('top_n', 10)), 20)  # Cap at 20
        
        # Validate input
        input_text = skills or resume_text
        if not input_text:
            return jsonify({'error': 'Please provide either skills or resume text'}), 400
        
        # Get recommendations
        recommendations = engine.get_recommendations(
            input_text,
            experience_level=experience_level,
            top_n=top_n
        )
        
        return jsonify({
            'success': True,
            'recommendations': recommendations,
            'count': len(recommendations)
        })
    
    except Exception as e:
        logger.error(f"Error in get_recommendations: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/upload-resume', methods=['POST'])
def upload_resume():
    """
    Upload and process a resume file.
    Returns extracted text and recommendations.
    """
    if not engine:
        return jsonify({'error': 'Recommendation engine not initialized'}), 500
    
    try:
        # Check if file is in request
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'File type not allowed. Use PDF, TXT, or DOCX'}), 400
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Extract text from file
        resume_text = extract_text_from_file(filepath)
        
        if not resume_text:
            return jsonify({'error': 'Could not extract text from file'}), 400
        
        # Get recommendations
        experience_level = request.form.get('experience_level', 'Mid Level')
        top_n = min(int(request.form.get('top_n', 10)), 20)
        
        recommendations = engine.get_recommendations(
            resume_text,
            experience_level=experience_level,
            top_n=top_n
        )
        
        # Clean up uploaded file
        try:
            os.remove(filepath)
        except:
            pass
        
        return jsonify({
            'success': True,
            'resume_text': resume_text[:500],  # Return first 500 chars
            'recommendations': recommendations,
            'count': len(recommendations)
        })
    
    except Exception as e:
        logger.error(f"Error in upload_resume: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'engine_initialized': engine is not None
    })


if __name__ == '__main__':
    print("="*60)
    print("JOB RECOMMENDATION SYSTEM - Web Interface")
    print("="*60)
    print("\n✓ Starting Flask application...")
    print("  → Open http://localhost:5000 in your browser")
    print("  → API docs available at http://localhost:5000")
    print("\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
