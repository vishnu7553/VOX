from flask import Flask, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename
from src.main import predict_audio_file
import jsonify

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10MB limit
app.config['SECRET_KEY'] = 'your-secret-key-here'

# Allowed file extensions
ALLOWED_EXTENSIONS = {'wav', 'mp3', 'flac'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/learn_more')
def learn_more():
    return render_template('learn_more.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files and 'audio' not in request.files:
        return redirect(request.url)
    
    # Handle both file upload and recorded audio
    audio_file = request.files.get('file') or request.files.get('audio')
    
    if audio_file.filename == '':
        return redirect(request.url)
    
    if audio_file and allowed_file(audio_file.filename):
        filename = secure_filename(audio_file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        audio_file.save(filepath)
        
        result = predict_audio_file(file_path=filepath)
        
        
        result = predict_audio_file(file_path=filepath)
        
        # Convert and round probabilities
        human_prob = round(result["human_prob"] * 100, 1)
        ai_prob = round(result["ai_prob"] * 100, 1)
        
        # Ensure values are within 0-100 range
        human_prob = max(0, min(100, human_prob))
        ai_prob = max(0, min(100, ai_prob))
        
        # Normalize to sum to 100% (handles floating point rounding)
        total = human_prob + ai_prob
        if total != 100:
            human_prob = round(human_prob * 100 / total, 1)
            ai_prob = 100 - human_prob
        
        return render_template('results.html',
                           filename=filename,
                           is_real=result["prediction"] == "HumanVoice",
                           human_prob=human_prob,
                           ai_prob=ai_prob,
                           chunks_processed=result["chunks_processed"])
    
    return redirect(request.url)

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)