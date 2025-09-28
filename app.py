from flask import Flask, render_template, request, redirect, url_for, session, flash
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Change this to a random string for security

# Enhanced steps with resources for all steps
steps = [
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

# Advanced tests with multiple questions
tests = {
    'programming': {
        'title': 'Python Basics Test (10 Questions)',
        'pass_threshold': 70,
        'questions': [
            {'q': "What is the output of the following code?\nx = 10\ny = 3\nprint(x % y)", 'options': ["1", "3", "0", "10"], 'answer': "1"},
            {'q': "What is the output of the following code?\nresult = True and False\nprint(result)", 'options': ["True", "False", "None", "Error"], 'answer': "False"},
            {'q': "Which of the following data types is mutable in Python?", 'options': ["List", "String", "Tuple", "Integer"], 'answer': "List"},
            {'q': "Can we use the “else” block for a `for` loop?", 'options': ["Yes", "No", "Only with while loops", "Only with if statements"], 'answer': "Yes"},
            {'q': "What will be the output of `print(3 * \"Abc\")`?", 'options': ["AbcAbcAbc", "Abc3", "3Abc", "Error"], 'answer': "AbcAbcAbc"},
            {'q': "What is the output of the following code?\na = [1, 2, 3]\nb = a\nb.append(4)\nprint(a)", 'options': ["[1, 2, 3]", "[1, 2, 3, 4]", "[1, 2, 3, 4, 4]", "Error"], 'answer': "[1, 2, 3, 4]"},
            {'q': "What is the output of `print(10 // 3)`?", 'options': ["3", "3.333", "4", "10"], 'answer': "3"},
            {'q': "What is the output of the following code?\nmy_list = [1, 2, 3, 4]\nprint(my_list[2])", 'options': ["1", "2", "3", "4"], 'answer': "3"},
            {'q': "What is the correct operator for exponentiation in Python?", 'options': ["**", "^", "*", "//"], 'answer': "**"},
            {'q': "What will be the output of `print('Python' * 2 + ' is fun')`?", 'options': ["PythonPython is fun", "Python2 is fun", "PythonPython2 is fun", "Error"], 'answer': "PythonPython is fun"}
        ],
        'recommendations': {
            'low': "Focus on basics: Start with Khan Academy Python course or freeCodeCamp's Python tutorial.",
            'medium': "Good start! Review lists, operators, and loops with Corey Schafer's YouTube tutorials.",
            'high': "Excellent! Start building small projects like a calculator or to-do list app."
        }
    },
    'math': {
        'title': 'Math Basics Test (Algebra & Statistics, 10 Questions)',
        'pass_threshold': 70,
        'questions': [
            {'q': "If 3x + 5 = 14, what is the value of x?", 'options': ["x = 3", "x = 4", "x = 5", "x = 2"], 'answer': "x = 3"},
            {'q': "7 + 2x = 15, what is the value of x?", 'options': ["x = 4", "x = 3", "x = 5", "x = 2"], 'answer': "x = 4"},
            {'q': "Solve for y in the equation: y – 13 = –3", 'options': ["y = 10", "y = 16", "y = -10", "y = 3"], 'answer': "y = 10"},
            {'q': "Simplify the expression: 4(2x - 3) + 2(x + 5)", 'options': ["10x - 2", "8x - 1", "6x - 4", "10x + 2"], 'answer': "10x - 2"},
            {'q': "What is the slope of the line represented by the equation y = -2x + 5?", 'options': ["-2", "2", "5", "-5"], 'answer': "-2"},
            {'q': "Find the middle value in this series: 3, 5, 7, 9, 11", 'options': ["3", "5", "7", "9"], 'answer': "7"},
            {'q': "Which number appears most frequently in this list: 2, 3, 4, 2, 5, 2, 3", 'options': ["2", "3", "4", "5"], 'answer': "2"},
            {'q': "What is the median of these values: 12, 18, 25, 30, 36", 'options': ["18", "25", "30", "36"], 'answer': "25"},
            {'q': "Determine the mean of these numbers: 5, 10, 15, 20, 25", 'options': ["15", "20", "25", "30"], 'answer': "15"},
            {'q': "Calculate the range of these numbers: 15, 22, 29, 36, 43", 'options': ["28", "29", "36", "43"], 'answer': "28"}
        ],
        'recommendations': {
            'low': "Brush up on algebra with Khan Academy; stats with StatQuest videos.",
            'medium': "Solid foundation! Practice more on linear equations and mean/median with Khan Academy.",
            'high': "Ready for AI math! Check Mathematics for Machine Learning on Coursera."
        }
    },
    'ai_basics': {
        'title': 'AI Basics Test (5 Questions)',
        'pass_threshold': 70,
        'questions': [
            {'q': "What does ML stand for in AI?", 'options': ["Machine Language", "Machine Learning", "Model Logic", "Main Loop"], 'answer': "Machine Learning"},
            {'q': "Which algorithm is commonly used for classification tasks in machine learning?", 'options': ["Linear Regression", "K-Nearest Neighbors", "K-Means Clustering", "PCA"], 'answer': "K-Nearest Neighbors"},
            {'q': "What is the purpose of a neural network's activation function?", 'options': ["To initialize weights", "To introduce non-linearity", "To reduce dimensions", "To store data"], 'answer': "To introduce non-linearity"},
            {'q': "Which of these is a popular deep learning framework?", 'options': ["TensorFlow", "NumPy", "Pandas", "Matplotlib"], 'answer': "TensorFlow"},
            {'q': "What is overfitting in machine learning?", 'options': ["Model performs well on training data but poorly on new data", "Model performs poorly on all data", "Model is too simple", "Model has too few layers"], 'answer': "Model performs well on training data but poorly on new data"}
        ],
        'recommendations': {
            'low': "Start with AI for Everyone on Coursera to grasp AI basics.",
            'medium': "Good progress! Dive deeper with fast.ai's Practical Deep Learning course.",
            'high': "Great job! Explore neural networks with StatQuest videos."
        }
    },
    'robotics': {
        'title': 'Robotics Basics Test (5 Questions)',
        'pass_threshold': 70,
        'questions': [
            {'q': "What is an actuator in robotics?", 'options': ["A sensor", "A device that moves or controls", "A programming language", "A type of AI model"], 'answer': "A device that moves or controls"},
            {'q': "What does ROS stand for in robotics?", 'options': ["Robot Operating System", "Remote Operating Software", "Robotic Object Sensor", "Real-Time Optimization System"], 'answer': "Robot Operating System"},
            {'q': "Which sensor is commonly used to detect distance in robots?", 'options': ["Thermocouple", "Ultrasonic sensor", "Potentiometer", "Encoder"], 'answer': "Ultrasonic sensor"},
            {'q': "What is the role of a microcontroller in robotics?", 'options': ["To store data", "To process sensor inputs and control actuators", "To train AI models", "To connect to Wi-Fi"], 'answer': "To process sensor inputs and control actuators"},
            {'q': "What is a common application of humanoid robots like Tesla's Optimus?", 'options': ["Weather forecasting", "Factory automation", "Web development", "Data analysis"], 'answer': "Factory automation"}
        ],
        'recommendations': {
            'low': "Start with Arduino tutorials or ROS beginner guides.",
            'medium': "Good foundation! Try building a simple robot with an Arduino kit.",
            'high': "Excellent! Explore ROS tutorials or Udacity's self-driving car course."
        }
    }
}

@app.route('/', methods=['GET', 'POST'])
def index():
    # Reset all tasks to incomplete on startup
    for step in steps:
        for task in step['tasks']:
            task['completed'] = False
    session['progress'] = steps  # Initialize fresh session
    session.modified = True

    if request.method == 'POST':
        step_idx = int(request.form['step_idx'])
        task_idx = int(request.form['task_idx'])
        # Only allow manual completion for tasks without tests
        if not session['progress'][step_idx]['tasks'][task_idx]['test']:
            session['progress'][step_idx]['tasks'][task_idx]['completed'] = True
            session.modified = True
            flash('Task marked as complete!', 'success')
        else:
            flash('You must pass the test to complete this task!', 'info')
        return redirect(url_for('index'))

    return render_template('index.html', steps=session['progress'])

@app.route('/test/<test_type>', methods=['GET', 'POST'])
def take_test(test_type):
    if test_type not in tests:
        return redirect(url_for('index'))

    test = tests[test_type]
    step_idx = int(request.args.get('step_idx', 0))
    task_idx = int(request.args.get('task_idx', 0))

    if 'questions' in test:  # Multi-question test
        if request.method == 'POST':
            score = 0
            total = len(test['questions'])
            for i, q in enumerate(test['questions']):
                if request.form.get(f'q_{i}') == q['answer']:
                    score += 1
            percentage = (score / total) * 100
            result = 'high' if percentage >= 90 else 'medium' if percentage >= test['pass_threshold'] else 'low'
            rec = test['recommendations'][result]
            if percentage >= test['pass_threshold']:
                session['progress'][step_idx]['tasks'][task_idx]['completed'] = True
                session.modified = True
                flash(f'Passed with {percentage:.1f}%! {rec}', 'success')
            else:
                flash(f'Score: {percentage:.1f}%. {rec} Keep practicing!', 'info')
            return redirect(url_for('index'))

        return render_template('test.html', test=test, test_type=test_type,
                               step_idx=step_idx, task_idx=task_idx)
    else:  # Simple test (fallback, not used now)
        if request.method == 'POST':
            answer = request.form['answer']
            if answer == test['answer']:
                session['progress'][step_idx]['tasks'][task_idx]['completed'] = True
                session.modified = True
                flash('Test passed!', 'success')
            else:
                flash('Try again!', 'info')
            return redirect(url_for('index'))

        return render_template('simple_test.html', test=test, test_type=test_type,
                               step_idx=step_idx, task_idx=task_idx)

if __name__ == '__main__':
    app.run(debug=True)