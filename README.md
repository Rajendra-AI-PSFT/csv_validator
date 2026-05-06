# CSV Validator & Corrector

A web application that validates and corrects newline characters in CSV, XLSX, and XLS files. Upload your file, identify problematic newlines, and download a corrected version.

## Features

- 📁 Upload CSV, XLSX, or XLS files
- ✅ Validate for embedded newline characters
- 🔧 Automatically correct issues (replace newlines with spaces)
- 📊 Detailed report showing issues found
- 📥 Download corrected file
- 🎨 Modern, user-friendly interface
- 📱 Responsive design

## Tech Stack

- **Backend**: Flask (Python)
- **Data Processing**: Pandas
- **Frontend**: HTML5, CSS3, JavaScript

## Installation

### Prerequisites
- Python 3.8+
- pip

### Local Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/csv-validator.git
cd csv-validator
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python app.py
```

5. Open your browser and navigate to:
```
http://localhost:5000
```

## Deployment

### Deploy to Heroku

1. Install Heroku CLI and login:
```bash
heroku login
```

2. Create a new Heroku app:
```bash
heroku create your-app-name
```

3. Add gunicorn to requirements.txt:
```bash
echo "gunicorn==21.2.0" >> requirements.txt
```

4. Deploy:
```bash
git push heroku main
```

### Deploy to PythonAnywhere

1. Upload your files to PythonAnywhere
2. Set up a new web app with Flask
3. Configure the WSGI file to point to `app:app`
4. Reload the web app

### Deploy to Render

1. Push to GitHub
2. Connect your GitHub repository to Render
3. Create a new Web Service
4. Set Build Command: `pip install -r requirements.txt`
5. Set Start Command: `gunicorn app:app`

## Usage

1. **Upload a file**: Click the upload area or drag and drop a CSV/XLSX/XLS file
2. **Validate**: Click "Validate & Correct"
3. **Review results**: Check the detected issues
4. **Download**: Download the corrected file

## API Endpoints

### POST `/upload`
Upload a file for validation and correction.

**Request:**
- `file` (multipart/form-data): CSV, XLSX, or XLS file

**Response:**
```json
{
  "status": "success",
  "rows": 1000,
  "file_id": "uuid-string",
  "corrected_filename": "file_corrected.csv",
  "validation": {
    "has_issues": true,
    "newline_count": 5,
    "issues": [
      {
        "column": "name",
        "row": 5,
        "value": "John\nDoe"
      }
    ]
  }
}
```

### GET `/download/<file_id>`
Download the corrected CSV file.

## Configuration

### Environment Variables

- `PORT`: Server port (default: 5000)
- `MAX_FILE_SIZE`: Maximum file size in bytes (default: 50MB)

Set environment variables:
```bash
export PORT=8000
export FLASK_ENV=production
```

## Supported File Formats

- **CSV** (.csv)
- **Excel** (.xlsx, .xls)

Maximum file size: 50MB

## How It Works

1. **Upload**: File is received and read based on extension
2. **Parse**: Data is parsed into a pandas DataFrame
3. **Validate**: Each cell is scanned for `\n` and `\r` characters
4. **Correct**: Newlines are replaced with spaces and trimmed
5. **Download**: Corrected data is converted back to CSV format

## Troubleshooting

### "File is too large"
The maximum file size is 50MB. Try splitting your file into smaller chunks.

### "Unsupported file type"
Only CSV, XLSX, and XLS files are supported.

### "Error processing file"
Ensure your file is not corrupted and follows standard format for the file type.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues and feature requests, please create an issue on GitHub.

## Author

Your Name - [Your GitHub Profile](https://github.com/yourusername)
