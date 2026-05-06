from flask import Flask, request, jsonify, send_file
import pandas as pd
from io import BytesIO, StringIO
import os
import uuid
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'temp_uploads'
ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'xls'}
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# Store corrected files temporarily
corrected_files = {}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return send_file('templates/index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Unsupported file type. Use CSV, XLSX, or XLS'}), 400
    
    try:
        # Read file based on extension
        filename = secure_filename(file.filename)
        file_ext = filename.rsplit('.', 1)[1].lower()
        
        if file_ext == 'csv':
            df = pd.read_csv(file, dtype=str)
        elif file_ext in ['xlsx', 'xls']:
            df = pd.read_excel(file, dtype=str)
        else:
            return jsonify({'error': 'Unsupported file type'}), 400
        
        # Validate for newline characters
        validation_results = validate_newlines(df)
        
        # Correct newline characters
        df_corrected = correct_newlines(df)
        
        # Store corrected file
        file_id = str(uuid.uuid4())
        corrected_filename = filename.rsplit('.', 1)[0] + '_corrected.csv'
        corrected_files[file_id] = {
            'dataframe': df_corrected,
            'filename': corrected_filename
        }
        
        return jsonify({
            'status': 'success',
            'rows': len(df),
            'validation': validation_results,
            'file_id': file_id,
            'corrected_filename': corrected_filename
        }), 200
    
    except Exception as e:
        return jsonify({'error': f'Error processing file: {str(e)}'}), 500

@app.route('/download/<file_id>')
def download_file(file_id):
    if file_id not in corrected_files:
        return jsonify({'error': 'File not found'}), 404
    
    try:
        df = corrected_files[file_id]['dataframe']
        filename = corrected_files[file_id]['filename']
        
        # Convert dataframe to CSV in memory
        csv_buffer = StringIO()
        df.to_csv(csv_buffer, index=False)
        csv_buffer.seek(0)
        
        # Clean up
        del corrected_files[file_id]
        
        return send_file(
            BytesIO(csv_buffer.getvalue().encode()),
            mimetype='text/csv',
            as_attachment=True,
            download_name=filename
        )
    except Exception as e:
        return jsonify({'error': f'Error downloading file: {str(e)}'}), 500

def validate_newlines(df):
    """Check for newline characters in dataframe"""
    issues = []
    
    for col in df.columns:
        for idx, value in enumerate(df[col]):
            if pd.isna(value):
                continue
            
            value_str = str(value)
            if '\n' in value_str or '\r' in value_str:
                issues.append({
                    'column': col,
                    'row': idx + 2,  # +2 because header is row 1 and index starts at 0
                    'value': value_str[:50]  # Preview first 50 chars
                })
    
    return {
        'has_issues': len(issues) > 0,
        'newline_count': len(issues),
        'issues': issues
    }

def correct_newlines(df):
    """Replace newline characters with spaces"""
    df_copy = df.copy()
    
    for col in df_copy.columns:
        df_copy[col] = df_copy[col].apply(
            lambda x: str(x).replace('\n', ' ').replace('\r', ' ').strip()
            if pd.notna(x) else x
        )
    
    return df_copy

@app.errorhandler(413)
def request_entity_too_large(error):
    return jsonify({'error': 'File is too large. Maximum size is 50MB'}), 413

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
