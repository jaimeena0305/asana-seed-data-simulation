import random
import datetime
from src.utils.helpers import generate_uuid, random_date, weighted_choice
from src.config import MIN_TASKS_PER_PROJECT, MAX_TASKS_PER_PROJECT

# Heuristic Templates for Tasks (Simulating LLM output)
TASK_VERBS = ["Fix", "Create", "Update", "Review", "Delete", "Investigate", "Design"]
TASK_NOUNS = ["API Endpoint", "Login Flow", "User Dashboard", "Database Schema", "Documentation", "Button Styles"]
MARKETING_NOUNS = ["Blog Post", "Tweet", "LinkedIn Copy", "Ad Creative", "Email Header"]

COMMENTS_GENERIC = [
    "Can you take a look at this?", "Done.", "Moving this to next sprint.", 
    "Blocked by external dependency.", "LGTM!", "Please update the description."
]

def generate_task_name(team_context):
    if "Engineering" in team_context:
        return f"{random.choice(TASK_VERBS)} {random.choice(TASK_NOUNS)}"
    elif "Marketing" in team_context:
        return f"{random.choice(TASK_VERBS)} {random.choice(MARKETING_NOUNS)}"
    else:
        return f"{random.choice(TASK_VERBS)} Item"

def generate_tasks(conn, org_id):
    cursor = conn.cursor()
    print("Generating Tasks (this may take a moment)...")

    # Fetch projects with team context
    cursor.execute("""
        SELECT p.id, p.created_at, p.due_date, t.name 
        FROM projects p 
        JOIN teams t ON p.team_id = t.id
        WHERE p.organization_id = ?
    """, (org_id,)) # Actually projects doesn't have org_id directly in schema, need join
    
    # Fix query based on schema: Projects -> Teams -> Org
    cursor.execute("""
        SELECT p.id, p.created_at, p.due_date, t.name 
        FROM projects p
        JOIN teams t ON p.team_id = t.id
        WHERE t.organization_id = ?
    """, (org_id,))
    
    projects = cursor.fetchall()

    # Fetch all users for assignment
    cursor.execute("SELECT id FROM users WHERE organization_id = ?", (org_id,))
    users = [row[0] for row in cursor.fetchall()]

    for proj_id, proj_start, proj_due, team_name in projects:
        # Convert string dates back to datetime if sqlite returned strings
        if isinstance(proj_start, str):
            proj_start = datetime.datetime.fromisoformat(proj_start)
        
        # Get Sections for this project
        cursor.execute("SELECT id FROM sections WHERE project_id = ?", (proj_id,))
        sections = [row[0] for row in cursor.fetchall()]
        
        if not sections: continue

        num_tasks = random.randint(MIN_TASKS_PER_PROJECT, MAX_TASKS_PER_PROJECT)

        for _ in range(num_tasks):
            task_id = generate_uuid()
            name = generate_task_name(team_name)
            description = f"Detailed description for {name}. Requirements:\n- Requirement A\n- Requirement B"
            
            section = random.choice(sections)
            assignee = random.choice(users) if random.random() > 0.15 else None # 15% unassigned
            
            # Task Timeline logic
            created_at = random_date(proj_start, proj_start + datetime.timedelta(days=30))
            due_date = created_at + datetime.timedelta(days=random.randint(1, 14))
            
            # Completion logic
            is_completed = random.random() < 0.7
            completed_at = None
            if is_completed:
                completed_at = random_date(created_at, due_date + datetime.timedelta(days=5)) # Might be late
            
            cursor.execute("""
                INSERT INTO tasks (id, project_id, section_id, assignee_id, name, description, priority, due_date, created_at, completed, completed_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (task_id, proj_id, section, assignee, name, description, 
                  weighted_choice(['High', 'Medium', 'Low'], [20, 60, 20]),
                  due_date.date(), created_at, is_completed, completed_at))

            # Generate Comments
            if random.random() < 0.4: # 40% of tasks have comments
                generate_comments(cursor, task_id, users, created_at)

    conn.commit()
    print("Tasks generated.")

def generate_comments(cursor, task_id, users, task_created_at):
    num_comments = random.randint(1, 5)
    prev_time = task_created_at
    
    for _ in range(num_comments):
        comment_id = generate_uuid()
        user = random.choice(users)
        text = random.choice(COMMENTS_GENERIC)
        created_at = prev_time + datetime.timedelta(hours=random.randint(1, 48))
        
        cursor.execute("""
            INSERT INTO comments (id, task_id, user_id, text, created_at)
            VALUES (?, ?, ?, ?, ?)
        """, (comment_id, task_id, user, text, created_at))
        prev_time = created_at