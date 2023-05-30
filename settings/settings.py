import os

# Get the absolute path to the project directory.
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
MAIN_SCRIPT_PATH = os.path.join(PROJECT_ROOT, 'datumo-numduo-python', 'main.py')
LOG_SCRIPT_PATH = os.path.join(PROJECT_ROOT,'datumo-numduo-python', 'logs', 'app.log')
