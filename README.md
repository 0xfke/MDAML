# Malware Analysis Web Application

![Project Banner](Image/Staticw.png)

The Malware Analysis and Detection web app is created to address the need for an accessible and user-friendly platform that enables efficient malware analysis for files, URLs, and executables.

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [File Types Supported](#file-types-supported)
- [Screenshots](#screenshots)
- [Contributing](#contributing)
- [License](#license)

## Features

### Static Analysis using API
- Allows quick, static analysis of files, URLs, and hashes by leveraging VirusTotal’s extensive threat intelligence database.
- This tool integrates two key methods to detect potential threats, providing users with a comprehensive approach to assess security risks.

### Machine Learning-Based Detection
- Focused on executable files (.exe and .dll), using machine learning and feature extraction to identify malicious behavior.

## Technologies Used

- Python
- Flask
- scikit-learn
- pandas
- pefile
- Jinja2
- HTML/CSS
- JavaScript

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/YOUR_USERNAME/malware-analysis-webapp.git
2. Navigate into the project directory:

   ```bash
   cd malware-analysis-webapp

3. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv

4. Activate the virtual environment:

 On Windows:
 bash 

    venv\Scripts\activate

On macOS/Linux:
bash

    source venv/bin/activate

5. Install the required packages:

bash

    pip install -r requirements.txt

## Usage

   Run the Flask application:

   bash

    python app.py

    Open your web browser and go to http://127.0.0.1:5001.
    Upload a file for analysis by selecting it from your local file system and clicking the Analyze button.
    View the results of the analysis on the result page.

## File Types Supported

    Executable files: .exe, .dll
    Archive files: .zip, .tar

Screenshots
Upload Page

Analysis Results

Contributing

Contributions are welcome! If you'd like to contribute, please follow these steps:

    Fork the repository.
    Create a new branch (git checkout -b feature/YourFeature).
    Make your changes and commit them (git commit -m 'Add some feature').
    Push to the branch (git push origin feature/YourFeature).
    Open a pull request.

License

This project is licensed under the MIT License. See the LICENSE file for details.
