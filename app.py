from flask import Flask, request, render_template
import joblib
import os
from feature_extraction import extract_features

app = Flask(__name__)

# Load the trained model
model = joblib.load('ML_model/malwareclassifier-V2.pkl')

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'dll', 'exe'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    # Check if a file is uploaded
    if 'file' in request.files:
        file = request.files['file']
        
        if file.filename == '' or not allowed_file(file.filename):
            return render_template('index.html', error="Unsupported file type.")
        
        # Construct the full file path
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)

        # Save the file
        file.save(file_path)

        # Use the model for prediction if the file is `.exe` or `.dll`
        if allowed_file(file.filename):
            features = extract_features(file_path)  # Your feature extraction function
            prediction = model.predict(features)     # Predict using your model
            result = {
                "type": "file",
                "prediction": "Malware" if prediction[0] == 1 else "Safe",
                "file_name": file.filename
            }

        return render_template('result.html', result=result)

    return render_template('index.html', error="No file uploaded.")

if __name__ == '__main__':
    app.run(port=5001, debug=True)

