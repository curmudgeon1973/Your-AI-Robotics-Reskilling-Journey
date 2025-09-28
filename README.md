Reskilling Tracker
A Flask-based web application to guide users through a structured AI and robotics reskilling journey. The app tracks progress across five steps, each with tasks, resources, and optional tests to validate skills in Python, math, AI basics, and robotics. Built for learners transitioning into tech, it provides a clear roadmap with curated learning resources and interactive tests.
Features

Structured Learning Path: Five steps with tasks covering foundational skills (Python, math), AI fundamentals, robotics, hands-on projects, and career opportunities.
Progress Tracking: Tasks can be marked complete manually (for non-test tasks) or by passing associated tests (≥70% score).
Curated Resources: Each task includes verified learning resources (e.g., Khan Academy, Coursera, YouTube) with clickable links in a modal and fallback display.
Interactive Tests: Multiple-choice tests for Python (10 questions), Math (10 questions), AI Basics (5 questions), and Robotics (5 questions) with tailored feedback based on scores.
Responsive UI: Clean, modern design with Font Awesome icons and a gradient background, optimized for desktop and mobile.

Project Structure
reskill/
├── app.py                   # Main Flask application
├── templates/
│   ├── index.html           # Home page with task list and resource modals
│   ├── test.html            # Multiple-choice test page
│   ├── simple_test.html     # Fallback single-question test page (unused)
├── run_app.bat              # Windows batch file to run the app
└── README.md                # This file

Prerequisites

Python 3.8+ (tested with Python 3.13)
pip (Python package manager)
A modern web browser (e.g., Chrome, Firefox)

Setup Instructions

Clone the Repository:
git clone https://github.com/your-username/reskilling-tracker.git
cd reskilling-tracker


Create a Virtual Environment (recommended):
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate


Install Dependencies:
pip install flask


Run the Application:

On Windows, double-click run_app.bat or run:python app.py


On macOS/Linux:python app.py




Access the App:Open http://127.0.0.1:5000/ in your browser.


Usage

Home Page: View five steps with tasks (e.g., "Learn Basic Computer Literacy and Programming"). Tasks with tests (e.g., Python, Math) require passing a test to mark complete.
Resources: Click a task name to open a modal with learning links (e.g., Khan Academy). If the modal fails, use the fallback links below each task.
Tests: For tasks with tests, click "Take Test to Prove" to answer multiple-choice questions. Score ≥70% to pass and mark the task complete. Feedback suggests resources based on your score (e.g., low score: "Start with Khan Academy").
Manual Completion: Tasks without tests (e.g., "Intro to Tech Tools") can be checked off manually via a checkbox.

Troubleshooting

App Won’t Start:
Ensure Python and Flask are installed (pip show flask).
Check for syntax errors in app.py. Run python -m py_compile app.py to validate.
Verify the folder structure matches the one above.


Resource Links Not Working:
Check the browser console (F12 → Console) for errors like “Modal failed to open.”
Ensure popups are allowed for 127.0.0.1 (in Chrome: lock icon → Site settings → Allow popups).
Test links directly (e.g., https://www.khanacademy.org/computing/intro-to-python-fundamentals).
Use fallback links below each task if the modal fails.


Test Errors:
If a test page fails to load, verify test.html uses loop.index0 for radio button names.
Ensure app.py has correct test data (e.g., tests['programming']).


Tasks Still Checked:
The app resets tasks to incomplete on startup. If tasks remain checked, clear browser cookies or restart the app.



Contributing

Fork the repository.
Create a feature branch (git checkout -b feature/your-feature).
Commit changes (git commit -m "Add your feature").
Push to the branch (git push origin feature/your-feature).
Open a pull request.

Future Enhancements

Save progress to a JSON file for persistence across sessions.
Add a progress bar to visualize completion percentage.
Include detailed test feedback (e.g., “Review Python lists with Corey Schafer”).
Support more test types or question formats.

License
MIT License. See LICENSE for details.
Acknowledgments

Built with Flask.
Icons from Font Awesome.
Inspired by resources like Khan Academy, Coursera, and freeCodeCamp.


Created by [Marc Ridgway]. Feel free to open issues or suggest features on GitHub!