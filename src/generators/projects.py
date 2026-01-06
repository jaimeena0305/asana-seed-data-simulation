import random
import datetime
from src.utils.helpers import generate_uuid, random_date, weighted_choice
from src.config import MIN_PROJECTS_PER_TEAM, MAX_PROJECTS_PER_TEAM, SIMULATION_START_DAYS_AGO

PROJECT_TEMPLATES = {
    "Engineering": ["Q1 Roadmap", "Backend Migration", "Mobile App v2", "Bug Bash", "Infra Scaling"],
    "Marketing": ["Brand Refresh", "Social Media Q3", "Conference Prep", "Email Drip Campaign"],
    "Product": ["User Research", "Feature Launch: Analytics", "Competitor Analysis"],
    "Sales": ["Q4 Pipe Gen", "Enterprise Outreach", "Sales Enablement"],
    "HR": ["Hiring Pipeline", "Onboarding Revamp", "Performance Reviews"],
    "Design": ["Design System v2", "Website Redesign", "Asset Library"]
}

DEFAULT_SECTIONS = ["To Do", "In Progress", "Review", "Done"]
ENG_SECTIONS = ["Backlog", "Ready for Dev", "In Development", "Code Review", "QA", "Deployed"]

def generate_projects(conn, org_id):
    cursor = conn.cursor()
    print("Generating Projects and Sections...")

    # Get Teams
    cursor.execute("SELECT id, name FROM teams WHERE organization_id = ?", (org_id,))
    teams = cursor.fetchall()

    # Get Users for Owners
    cursor.execute("SELECT id FROM users WHERE organization_id = ?", (org_id,))
    all_users = [row[0] for row in cursor.fetchall()]

    for team_id, team_name in teams:
        num_projects = random.randint(MIN_PROJECTS_PER_TEAM, MAX_PROJECTS_PER_TEAM)
        
        # Determine templates based on team name
        templates = PROJECT_TEMPLATES.get(team_name, ["General Tasks", "Weekly Sync", "Q1 Goals"])
        
        for _ in range(num_projects):
            proj_id = generate_uuid()
            base_name = random.choice(templates)
            name = f"{base_name} - {fake_suffix()}" # e.g., "Backend Migration - Alpha"
            
            owner = random.choice(all_users)
            
            # Project Timeline
            start_date = random_date(
                datetime.datetime.now() - datetime.timedelta(days=SIMULATION_START_DAYS_AGO),
                datetime.datetime.now()
            )
            # Due date is 1-4 months after start
            due_date = start_date + datetime.timedelta(days=random.randint(30, 120))
            
            status = weighted_choice(
                ['On Track', 'At Risk', 'Off Track', 'Completed'], 
                [60, 20, 10, 10]
            )

            cursor.execute("""
                INSERT INTO projects (id, team_id, owner_id, name, status, created_at, due_date)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (proj_id, team_id, owner, name, status, start_date, due_date))

            # Generate Sections
            sections = ENG_SECTIONS if "Engineering" in team_name else DEFAULT_SECTIONS
            for idx, sec_name in enumerate(sections):
                cursor.execute("""
                    INSERT INTO sections (id, project_id, name, order_index)
                    VALUES (?, ?, ?, ?)
                """, (generate_uuid(), proj_id, sec_name, idx))

    conn.commit()
    print("Projects generated.")

def fake_suffix():
    return random.choice(["Alpha", "Beta", "2024", "Phase 1", "Core", "Legacy"])