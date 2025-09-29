from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
import json
from datetime import date, timedelta

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Define step and task hours estimates (in hours)
step_hours = [60, 60, 90, 40, 30]
task_hours = [
    [30, 20, 10],  # Step 1: Python (30h), Math (20h), Colab (10h)
    [30, 20, 10],  # Step 2: Core AI (30h), Applied AI (20h), Book (10h)
    [40, 30, 20],  # Step 3: Robotics (40h), Emerging Robots (30h), Ethics (20h)
    [20, 10, 10],  # Step 4: Projects (20h), Communities (10h), Certifications (10h)
    [15, 10, 5],   # Step 5: Open-Source (15h), Freelance (10h), Upskill (5h)
]

# Complete steps_template with full resource lists
steps_template = [
    {
        'title': 'Step 1: Build Foundational Skills (1-3 Months)',
        'tasks': [
            {
                'name': 'Learn Basic Computer Literacy and Programming (Python)',
                'completed': False,
                'test': 'programming',
                'resources': [
                    {'name': 'Khan Academy Intro to CS - Python', 'url': 'https://www.khanacademy.org/computing/intro-to-python-fundamentals'},
                    {'name': 'freeCodeCamp Python Full Course [2025] (YouTube)', 'url': 'https://www.youtube.com/watch?v=K5KVEU3aaeQ'},
                    {'name': 'Codecademy Learn Python 3', 'url': 'https://www.codecademy.com/learn/learn-python-3'},
                    {'name': "Google's Python Class", 'url': 'https://developers.google.com/edu/python'},
                    {'name': 'Coursera: Python for Everybody', 'url': 'https://www.coursera.org/learn/python'},
                    {'name': 'Reddit: r/learnpython', 'url': 'https://www.reddit.com/r/learnpython/'},
                    {'name': 'Corey Schafer Python Tutorials (YouTube)', 'url': 'https://www.youtube.com/playlist?list=PL-osiE80TeTt2d9bfVyTiXJA-UTHn6WwU'}
                ]
            },
            {
                'name': 'Math and Logic Basics (Algebra, Statistics)',
                'completed': False,
                'test': 'math',
                'resources': [
                    {'name': 'Khan Academy Algebra Basics', 'url': 'https://www.khanacademy.org/math/algebra'},
                    {'name': 'Khan Academy Intro to Statistics', 'url': 'https://www.khanacademy.org/math/statistics-probability'},
                    {'name': '3Blue1Brown Essence of Linear Algebra (YouTube)', 'url': 'https://www.youtube.com/playlist?list=PLZHQObOWTQDPD3MizzM2xVFitgF8hE_ab'},
                    {'name': 'StatQuest with Josh Starmer (YouTube for Stats)', 'url': 'https://www.youtube.com/c/joshstarmer'},
                    {'name': 'Reddit: r/learnmath', 'url': 'https://www.reddit.com/r/learnmath/'},
                    {'name': 'Mathematics for Machine Learning (Coursera)', 'url': 'https://www.coursera.org/specializations/mathematics-machine-learning'}
                ]
            },
            {
                'name': 'Intro to Tech Tools (Google Colab)',
                'completed': False,
                'test': None,
                'resources': [
                    {'name': 'Google Colab Official Welcome', 'url': 'https://colab.research.google.com/'},
                    {'name': 'Google Colab Tutorial for Beginners (YouTube)', 'url': 'https://www.youtube.com/watch?v=RLYoEyIHL6A'},
                    {'name': 'Marqo Guide: Getting Started with Google Colab', 'url': 'https://www.marqo.ai/blog/getting-started-with-google-colab-a-beginners-guide'}
                ]
            }
        ]
    },
    {
        'title': 'Step 2: Dive into AI Fundamentals (2-6 Months)',
        'tasks': [
            {
                'name': 'Core AI Concepts (Machine Learning, Neural Networks)',
                'completed': False,
                'test': 'ai_basics',
                'resources': [
                    {'name': 'Coursera: AI for Everyone by Andrew Ng', 'url': 'https://www.coursera.org/learn/ai-for-everyone'},
                    {'name': 'fast.ai Practical Deep Learning for Coders', 'url': 'https://course.fast.ai/'},
                    {'name': 'edX: Introduction to Artificial Intelligence (MIT)', 'url': 'https://www.edx.org/learn/artificial-intelligence/mitx-introduction-to-artificial-intelligence'},
                    {'name': 'StatQuest: Neural Networks (YouTube)', 'url': 'https://www.youtube.com/watch?v=CqOfi41LfDw'},
                    {'name': 'Reddit: r/MachineLearning', 'url': 'https://www.reddit.com/r/MachineLearning/'}
                ]
            },
            {
                'name': 'Specialize in Applied AI (NLP or Computer Vision)',
                'completed': False,
                'test': None,
                'resources': [
                    {'name': 'DeepLearning.AI: Natural Language Processing Specialization', 'url': 'https://www.coursera.org/specializations/natural-language-processing'},
                    {'name': 'OpenCV Course for Computer Vision (YouTube)', 'url': 'https://www.youtube.com/watch?v=IA3WxTTPXqQ'},
                    {'name': 'PyTorch Tutorials for NLP', 'url': 'https://pytorch.org/tutorials/beginner/nlp/'},
                    {'name': 'Reddit: r/learnmachinelearning', 'url': 'https://www.reddit.com/r/learnmachinelearning/'}
                ]
            },
            {
                'name': 'Read Hands-On Machine Learning Book',
                'completed': False,
                'test': None,
                'resources': [
                    {'name': 'Hands-On Machine Learning Book (O’Reilly)', 'url': 'https://www.oreilly.com/library/view/hands-on-machine-learning/9781492032649/'},
                    {'name': 'GitHub Companion Notebooks', 'url': 'https://github.com/ageron/handson-ml3'},
                    {'name': 'YouTube: Book Walkthrough (TensorFlow)', 'url': 'https://www.youtube.com/watch?v=5DknTFbcA2I'}
                ]
            }
        ]
    },
    {
        'title': 'Step 3: Explore Robotics and the "Robot Reality" (3-9 Months)',
        'tasks': [
            {
                'name': 'Robotics Basics (Sensors, Actuators)',
                'completed': False,
                'test': 'robotics',
                'resources': [
                    {'name': 'Udacity: Intro to Self-Driving Cars', 'url': 'https://www.udacity.com/course/intro-to-self-driving-cars--nd013'},
                    {'name': 'Arduino Robotics Tutorials (YouTube)', 'url': 'https://www.youtube.com/playlist?list=PLT6InZshkQJ2Uo3rI2z3jQ3kV1b1g8IQ'},
                    {'name': 'Robot Operating System (ROS) Tutorials', 'url': 'https://wiki.ros.org/ROS/Tutorials'},
                    {'name': 'Reddit: r/robotics', 'url': 'https://www.reddit.com/r/robotics/'}
                ]
            },
            {
                'name': 'Focus on Emerging Robots (Optimus Demos)',
                'completed': False,
                'test': None,
                'resources': [
                    {'name': 'Tesla AI Day 2024 (YouTube)', 'url': 'https://www.youtube.com/watch?v=6vHwsxoiW6A'},
                    {'name': 'Boston Dynamics Atlas Videos', 'url': 'https://www.bostondynamics.com/atlas'},
                    {'name': 'IEEE Spectrum Robotics News', 'url': 'https://spectrum.ieee.org/topic/robotics/'}
                ]
            },
            {
                'name': 'Ethical and Societal Prep (Read Life 3.0)',
                'completed': False,
                'test': None,
                'resources': [
                    {'name': 'Life 3.0 by Max Tegmark (Book)', 'url': 'https://www.amazon.com/Life-3-0-Being-Artificial-Intelligence/dp/1101946598'},
                    {'name': 'AI Ethics Course (Coursera)', 'url': 'https://www.coursera.org/learn/ai-ethics'},
                    {'name': 'Reddit: r/AIEthics', 'url': 'https://www.reddit.com/r/AIEthics/'}
                ]
            }
        ]
    },
    {
        'title': 'Step 4: Hands-On Practice and Networking',
        'tasks': [
            {
                'name': 'Build Projects for Portfolio',
                'completed': False,
                'test': None,
                'resources': [
                    {'name': 'GitHub: AI Project Ideas', 'url': 'https://github.com/topics/ai-projects'},
                    {'name': 'Kaggle Competitions', 'url': 'https://www.kaggle.com/competitions'},
                    {'name': 'YouTube: Build a Chatbot', 'url': 'https://www.youtube.com/watch?v=7vffvG4WqBc'}
                ]
            },
            {
                'name': 'Join Communities and Get Mentorship',
                'completed': False,
                'test': None,
                'resources': [
                    {'name': 'Meetup: AI & Robotics Groups', 'url': 'https://www.meetup.com/topics/artificial-intelligence/'},
                    {'name': 'Reddit: r/artificial', 'url': 'https://www.reddit.com/r/artificial/'},
                    {'name': 'Senior Planet Tech Community', 'url': 'https://seniorplanet.org/'}
                ]
            },
            {
                'name': 'Get Certifications',
                'completed': False,
                'test': None,
                'resources': [
                    {'name': 'Google Data Analytics Certificate', 'url': 'https://www.coursera.org/professional-certificates/google-data-analytics'},
                    {'name': 'IBM AI Engineering Certificate', 'url': 'https://www.coursera.org/professional-certificates/ai-engineer'},
                    {'name': 'AWS Certified AI Practitioner', 'url': 'https://aws.amazon.com/certification/certified-ai-practitioner/'}
                ]
            }
        ]
    },
    {
        'title': 'Step 5: Transition to Opportunities',
        'tasks': [
            {
                'name': 'Volunteer for Open-Source Projects',
                'completed': False,
                'test': None,
                'resources': [
                    {'name': 'GitHub Open Source AI Projects', 'url': 'https://github.com/topics/open-source-ai'},
                    {'name': 'Open Source Robotics Foundation', 'url': 'https://www.osrfoundation.org/'},
                    {'name': 'Reddit: r/opensource', 'url': 'https://www.reddit.com/r/opensource/'}
                ]
            },
            {
                'name': 'Freelance on Platforms like Fiverr',
                'completed': False,
                'test': None,
                'resources': [
                    {'name': 'Fiverr AI Gigs', 'url': 'https://www.fiverr.com/categories/data/artificial-intelligence'},
                    {'name': 'Upwork AI Jobs', 'url': 'https://www.upwork.com/freelance-jobs/artificial-intelligence/'},
                    {'name': 'YouTube: Freelancing with AI Skills', 'url': 'https://www.youtube.com/watch?v=1Yq3z4M4z1k'}
                ]
            },
            {
                'name': 'Upskill in Current Field with AI',
                'completed': False,
                'test': None,
                'resources': [
                    {'name': 'AI for Healthcare (Coursera)', 'url': 'https://www.coursera.org/specializations/ai-healthcare'},
                    {'name': 'AI in Manufacturing (edX)', 'url': 'https://www.edx.org/learn/artificial-intelligence/ai-for-manufacturing'},
                    {'name': 'LinkedIn Learning: AI in Your Industry', 'url': 'https://www.linkedin.com/learning/topics/artificial-intelligence'}
                ]
            }
        ]
    }
]

# Tests (unchanged, included for completeness)
tests = {
    'programming': {
        'title': 'Python Proficiency Test (15 Questions)',
        'pass_threshold': 70,
        'questions': [
            {
                'q': "What is the output of the following code?\n```python\nx = [1, 2, 3]\ny = x[:]\ny.append(4)\nprint(x)\n```",
                'type': 'multiple_choice',
                'options': ["[1, 2, 3]", "[1, 2, 3, 4]", "[4, 1, 2, 3]", "Error"],
                'answer': "[1, 2, 3]",
                'feedback': "Correct! `y = x[:]` creates a shallow copy, so appending to `y` doesn't affect `x`. Review list slicing in [Corey Schafer's Python Tutorials](https://www.youtube.com/playlist?list=PL-osiE80TeTt2d9bfVyTiXJA-UTHn6WwU)."
            },
            {
                'q': "What is the output of `print(len({1, 2, 2, 3}))`?",
                'type': 'multiple_choice',
                'options': ["3", "4", "2", "Error"],
                'answer': "3",
                'feedback': "Correct! A set removes duplicates, so `{1, 2, 2, 3}` has 3 unique elements. See [Python's Python Class](https://developers.google.com/edu/python)."
            },
            {
                'q': "The following code has an error. Identify it:\n```python\nfor i in range(5)\n    print(i)\n```",
                'type': 'multiple_choice',
                'options': ["Missing colon after `range(5)`", "Missing parentheses in `print`", "Invalid range syntax", "No error"],
                'answer': "Missing colon after `range(5)`",
                'feedback': "Correct! A colon is required after `range(5)` in a for loop. Review loops in [Khan Academy Python](https://www.khanacademy.org/computing/intro-to-python-fundamentals)."
            },
            {
                'q': "True or False: In Python, `list.append()` modifies the list in place.",
                'type': 'true_false',
                'options': ["True", "False"],
                'answer': "True",
                'feedback': "Correct! `append()` modifies the list directly. See [freeCodeCamp Python Course](https://www.youtube.com/watch?v=K5KVEU3aaeQ)."
            },
            {
                'q': "Write a Python function to return the square of a number.",
                'type': 'short_answer',
                'answer': "def square(num):\n    return num * num",
                'feedback': "Correct answer should be `def square(num):\n    return num * num`. Review functions in [Coursera: Python for Everybody](https://www.coursera.org/learn/python)."
            },
            {
                'q': "What is the output of the following code?\n```python\nx = 'hello'\nprint(x.upper())\n```",
                'type': 'multiple_choice',
                'options': ["HELLO", "hello", "Hello", "Error"],
                'answer': "HELLO",
                'feedback': "Correct! `upper()` converts a string to uppercase. See [Python Docs](https://docs.python.org/3/library/stdtypes.html#str.upper)."
            },
            {
                'q': "What is the output of `print([x for x in range(5) if x % 2 == 0])`?",
                'type': 'multiple_choice',
                'options': ["[0, 2, 4]", "[1, 3]", "[0, 1, 2, 3, 4]", "[2, 4]"],
                'answer': "[0, 2, 4]",
                'feedback': "Correct! List comprehension filters even numbers. Review in [Corey Schafer's Tutorials](https://www.youtube.com/playlist?list=PL-osiE80TeTt2d9bfVyTiXJA-UTHn6WwU)."
            },
            {
                'q': "True or False: Python is a dynamically typed language.",
                'type': 'true_false',
                'options': ["True", "False"],
                'answer': "True",
                'feedback': "Correct! Python doesn't require type declarations. See [Google's Python Class](https://developers.google.com/edu/python)."
            },
            {
                'q': "What is the output of the following code?\n```python\nd = {'a': 1, 'b': 2}\nprint(d.get('c', 0))\n```",
                'type': 'multiple_choice',
                'options': ["0", "None", "Error", "2"],
                'answer': "0",
                'feedback': "Correct! `get()` returns the default (0) if key is missing. Review dictionaries in [Khan Academy](https://www.khanacademy.org/computing/intro-to-python-fundamentals)."
            },
            {
                'q': "Write a Python function to check if a string is a palindrome.",
                'type': 'short_answer',
                'answer': "def is_palindrome(s):\n    return s.lower() == s.lower()[::-1]",
                'feedback': "Correct answer should be `def is_palindrome(s):\n    return s.lower() == s.lower()[::-1]`. Review string slicing in [freeCodeCamp](https://www.youtube.com/watch?v=K5KVEU3aaeQ)."
            },
            {
                'q': "What is the output of `print(10 // 3)`?",
                'type': 'multiple_choice',
                'options': ["3", "3.333", "4", "Error"],
                'answer': "3",
                'feedback': "Correct! `//` performs floor division. See [Python Docs](https://docs.python.org/3/reference/expressions.html#binary-arithmetic-operations)."
            },
            {
                'q': "True or False: A Python tuple can be modified after creation.",
                'type': 'true_false',
                'options': ["True", "False"],
                'answer': "False",
                'feedback': "Correct! Tuples are immutable. Review in [Codecademy Python](https://www.codecademy.com/learn/learn-python-3)."
            },
            {
                'q': "What is the output of the following code?\n```python\nx = [1, 2, 3]\nprint(x.pop())\n```",
                'type': 'multiple_choice',
                'options': ["3", "1", "[1, 2]", "Error"],
                'answer': "3",
                'feedback': "Correct! `pop()` removes and returns the last element. See [Python Docs](https://docs.python.org/3/tutorial/datastructures.html)."
            },
            {
                'q': "What is the output of the following code?\n```python\ndef func(x):\n    return x * 2\nprint(func(5))\n```",
                'type': 'multiple_choice',
                'options': ["5", "10", "Error", "None"],
                'answer': "10",
                'feedback': "Correct! The function doubles the input. Review functions in [Coursera](https://www.coursera.org/learn/python)."
            },
            {
                'q': "Write a Python list comprehension to get squares of numbers 1 to 5.",
                'type': 'short_answer',
                'answer': "[x**2 for x in range(1, 6)]",
                'feedback': "Correct answer should be `[x**2 for x in range(1, 6)]`. Review list comprehensions in [Corey Schafer](https://www.youtube.com/playlist?list=PL-osiE80TeTt2d9bfVyTiXJA-UTHn6WwU)."
            }
        ],
        'recommendations': {
            'low': "Focus on Python basics: Start with [Khan Academy](https://www.khanacademy.org/computing/intro-to-python-fundamentals) or [freeCodeCamp](https://www.youtube.com/watch?v=K5KVEU3aaeQ).",
            'medium': "Good progress! Deepen your understanding of lists, dictionaries, and functions with [Corey Schafer](https://www.youtube.com/playlist?list=PL-osiE80TeTt2d9bfVyTiXJA-UTHn6WwU).",
            'high': "Excellent! Build projects like a calculator or text analyzer using [Google's Python Class](https://developers.google.com/edu/python)."
        }
    },
    'math': {
        'title': 'Math Proficiency Test (Algebra & Statistics, 15 Questions)',
        'pass_threshold': 70,
        'questions': [
            {
                'q': "Solve for x: 2x + 3 = 11",
                'type': 'multiple_choice',
                'options': ["x = 4", "x = 5", "x = 3", "x = 6"],
                'answer': "x = 4",
                'feedback': "Correct! Subtract 3 and divide by 2: (11-3)/2 = 4. Review algebra in [Khan Academy](https://www.khanacademy.org/math/algebra)."
            },
            # ... (other math questions unchanged)
        ],
        'recommendations': {
            'low': "Brush up on algebra and stats with [Khan Academy](https://www.khanacademy.org/math/algebra) and [StatQuest](https://www.youtube.com/c/joshstarmer).",
            'medium': "Solid foundation! Practice linear algebra with [3Blue1Brown](https://www.youtube.com/playlist?list=PLZHQObOWTQDPD3MizzM2xVFitgF8hE_ab).",
            'high': "Ready for AI math! Explore [Mathematics for Machine Learning](https://www.coursera.org/specializations/mathematics-machine-learning)."
        }
    },
    'ai_basics': {
        'title': 'AI Fundamentals Test (10 Questions)',
        'pass_threshold': 70,
        'questions': [
            {
                'q': "What is the primary goal of supervised learning?",
                'type': 'multiple_choice',
                'options': ["Cluster data", "Predict labels", "Reduce dimensions", "Optimize rewards"],
                'answer': "Predict labels",
                'feedback': "Correct! Supervised learning maps inputs to outputs. See [Coursera: AI for Everyone](https://www.coursera.org/learn/ai-for-everyone)."
            },
            # ... (other AI questions unchanged)
        ],
        'recommendations': {
            'low': "Start with [AI for Everyone](https://www.coursera.org/learn/ai-for-everyone) to grasp AI basics.",
            'medium': "Good progress! Dive deeper with [fast.ai](https://course.fast.ai/).",
            'high': "Great job! Explore neural networks with [StatQuest](https://www.youtube.com/watch?v=CqOfi41LfDw)."
        }
    },
    'robotics': {
        'title': 'Robotics Fundamentals Test (10 Questions)',
        'pass_threshold': 70,
        'questions': [
            {
                'q': "What is the primary function of a sensor in robotics?",
                'type': 'multiple_choice',
                'options': ["Control movement", "Detect environmental data", "Train AI models", "Store energy"],
                'answer': "Detect environmental data",
                'feedback': "Correct! Sensors gather data like distance or light. See [ROS Tutorials](https://wiki.ros.org/ROS/Tutorials)."
            },
            # ... (other robotics questions unchanged)
        ],
        'recommendations': {
            'low': "Start with [Arduino Tutorials](https://www.youtube.com/playlist?list=PLT6InZshkQJ2Uo3rI2z3jQ3kV1b1g8IQ) or [ROS Tutorials](https://wiki.ros.org/ROS/Tutorials).",
            'medium': "Good foundation! Build a simple robot with [Arduino](https://www.youtube.com/playlist?list=PLT6InZshkQJ2Uo3rI2z3jQ3kV1b1g8IQ).",
            'high': "Excellent! Explore advanced ROS with [Udacity Self-Driving Cars](https://www.udacity.com/course/intro-to-self-driving-cars--nd013)."
        }
    }
}

def save_progress():
    with open('progress.json', 'w') as f:
        json.dump(session['progress'], f)

@app.route('/', methods=['GET', 'POST'])
def index():
    if os.path.exists('progress.json'):
        with open('progress.json', 'r') as f:
            session['progress'] = json.load(f)
    else:
        session['progress'] = {'steps': steps_template, 'start_date': None, 'daily_hours': 1.0, 'test_attempts': {}}

    progress = session['progress']
    steps = progress['steps']

    if request.method == 'POST':
        if 'start_date' in request.form:
            progress['start_date'] = request.form['start_date']
            progress['daily_hours'] = float(request.form['daily_hours'])
            save_progress()
            flash('Settings saved! Projections updated.', 'success')
            return redirect(url_for('index'))
        else:
            step_idx = int(request.form['step_idx'])
            task_idx = int(request.form['task_idx'])
            if not steps[step_idx]['tasks'][task_idx]['test']:
                steps[step_idx]['tasks'][task_idx]['completed'] = True
                save_progress()
                flash('Task marked as complete!', 'success')
            else:
                flash('You must pass the test to complete this task!', 'info')
            return redirect(url_for('index'))

    total_tasks = sum(len(step['tasks']) for step in steps)
    completed_tasks = sum(1 for step in steps for task in step['tasks'] if task['completed'])
    progress_percent = completed_tasks / total_tasks if total_tasks > 0 else 0

    current_task = None
    current_step_idx = None
    current_task_idx = None
    today = date.today()
    if progress['start_date']:
        start = date.fromisoformat(progress['start_date'])
        daily = progress['daily_hours']
        cum_hours = 0
        for step_idx, step in enumerate(steps):
            for task_idx, task in enumerate(step['tasks']):
                if not task['completed']:
                    current_task = {
                        'name': task['name'],
                        'step_title': step['title'],
                        'hours': task_hours[step_idx][task_idx],
                        'days_total': task_hours[step_idx][task_idx] / daily,
                        'days_spent': min((today - start).days - cum_hours / daily, task_hours[step_idx][task_idx] / daily),
                        'days_remaining': max(0, task_hours[step_idx][task_idx] / daily - ((today - start).days - cum_hours / daily))
                    }
                    current_step_idx = step_idx
                    current_task_idx = task_idx
                    break
                cum_hours += task_hours[step_idx][task_idx]
            if current_task:
                break
        if not current_task:
            current_task = {'name': 'All tasks completed!', 'step_title': '', 'hours': 0, 'days_total': 0, 'days_spent': 0, 'days_remaining': 0}

    projected = None
    status = None
    if progress['start_date']:
        start = date.fromisoformat(progress['start_date'])
        daily = progress['daily_hours']
        total_hours = sum(step_hours)
        days_elapsed = (today - start).days
        expected_hours = days_elapsed * daily
        expected_progress = expected_hours / total_hours if total_hours > 0 else 0
        status = "Ahead" if progress_percent > expected_progress + 0.1 else "Behind" if progress_percent < expected_progress - 0.1 else "On Track"

        cum_hours = 0
        projected = []
        for i, hours in enumerate(step_hours):
            days_for_step = hours / daily
            cum_days = cum_hours / daily
            proj_start = start + timedelta(days=cum_days)
            proj_end = proj_start + timedelta(days=days_for_step)
            projected.append({'step': i+1, 'start': proj_start, 'end': proj_end})
            cum_hours += hours

    return render_template('index.html', steps=steps, progress_percent=progress_percent, projected=projected, status=status,
                           first_time=progress['start_date'] is None, daily_hours=progress['daily_hours'],
                           current_task=current_task, current_step_idx=current_step_idx, current_task_idx=current_task_idx)

@app.route('/test/<test_type>', methods=['GET', 'POST'])
def take_test(test_type):
    if test_type not in tests:
        return redirect(url_for('index'))

    test = tests[test_type]
    step_idx = int(request.args.get('step_idx', 0))
    task_idx = int(request.args.get('task_idx', 0))

    if request.method == 'POST':
        score = 0
        total = len(test['questions'])
        results = []
        for i, q in enumerate(test['questions']):
            user_answer = request.form.get(f'q_{i}')
            is_correct = user_answer == q['answer'] if q['type'] != 'short_answer' else user_answer.strip().replace('\n', ' ') == q['answer']
            if is_correct:
                score += 1
            results.append({
                'question': q['q'],
                'user_answer': user_answer,
                'correct_answer': q['answer'],
                'is_correct': is_correct,
                'feedback': q['feedback']
            })
        percentage = (score / total) * 100
        result = 'high' if percentage >= 90 else 'medium' if percentage >= test['pass_threshold'] else 'low'
        rec = test['recommendations'][result]

        if 'test_attempts' not in session['progress']:
            session['progress']['test_attempts'] = {}
        if test_type not in session['progress']['test_attempts']:
            session['progress']['test_attempts'][test_type] = []
        session['progress']['test_attempts'][test_type].append({
            'score': percentage,
            'results': results,
            'timestamp': str(date.today())
        })
        save_progress()

        if percentage >= test['pass_threshold']:
            session['progress']['steps'][step_idx]['tasks'][task_idx]['completed'] = True
            save_progress()
            flash(f'Passed with {percentage:.1f}%! {rec}', 'success')
        else:
            flash(f'Score: {percentage:.1f}%. {rec} Review your answers below.', 'info')
        return render_template('test_results.html', test=test, results=results, percentage=percentage, recommendation=rec)

    return render_template('test.html', test=test, test_type=test_type, step_idx=step_idx, task_idx=task_idx)

@app.route('/reset_timeline', methods=['POST'])
def reset_timeline():
    reset_progress = request.form.get('reset_progress') == 'true'
    session['progress']['start_date'] = None
    session['progress']['daily_hours'] = 1.0
    if reset_progress:
        session['progress']['steps'] = steps_template
        session['progress']['test_attempts'] = {}
    save_progress()
    flash('Timeline reset! Please set a new start date and daily hours.', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)