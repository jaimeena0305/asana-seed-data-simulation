import os

# Database Settings
DB_PATH = os.path.join("output", "asana_simulation.sqlite")
SCHEMA_PATH = "schema.sql"

# Simulation Scale (Adjust these to resize the dataset)
NUM_ORGANIZATIONS = 1
NUM_TEAMS_PER_ORG = 8  # e.g., Eng, Sales, Marketing, HR, etc.
NUM_USERS = 150       # Total users in the org
MIN_PROJECTS_PER_TEAM = 5
MAX_PROJECTS_PER_TEAM = 12
MIN_TASKS_PER_PROJECT = 20
MAX_TASKS_PER_PROJECT = 60

# Date Configuration
SIMULATION_START_DAYS_AGO = 365  # Generate data for the last year
WORK_WEEK_ONLY = True # Prefer weekdays for dates

# LLM / Text Generation Settings
# Set to True if you want to use simpler, faster templates.
# Set to False if you were hooking up a real LLM (logic mocked in utils).
USE_HEURISTIC_GENERATION = True