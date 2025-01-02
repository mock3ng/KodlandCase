markdown

Copy
# Quiz Application Quick Start Guide

A simple quiz application built with Flask that supports both multiple-choice and text-based questions.

## Features
- User registration and authentication
- Multiple choice questions
- Text-based questions 
- Score tracking
- Best score display

## Prerequisites
- Python 3.7+
- pip (Python package installer)

## Installation

1. Clone the repository
```bash
git clone git@github.com:mock3ng/KodlandCase.git
cd quiz-app
Create and activate virtual environment
For Windows:

bash

Copy
python -m venv env
env\Scripts\activate
For macOS/Linux:

bash

Copy
python3 -m venv env
source env/bin/activate
Install required packages
bash

Copy
pip install -r requirements.txt
Configuration
Create a questions.json file in the root directory with your quiz questions
The application uses SQLite database by default - it will be created automatically
Running the Application
Start the Flask development server:
bash

Copy
python app.py
Open your web browser and navigate to:

Copy
http://localhost:5000
Project Structure
basic

Copy
quiz-app/
│
├── app.py              # Main application file
├── questions.json      # Quiz questions
├── requirements.txt    # Project dependencies
├── templates/         
│   ├── login.html     # Login page template
│   ├── register.html  # Registration page template
│   ├── quiz.html      # Quiz page template
│   └── quiz_result.html # Results page template
└── instance/          
    └── users.db       # SQLite database
Requirements
Key dependencies:

Flask
Flask-SQLAlchemy
Flask-Login
Werkzeug
See requirements.txt for complete list.

License
This project is licensed under the MIT License - see the LICENSE file for details

Author
Ergün Çalbay
