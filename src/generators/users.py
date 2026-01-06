from faker import Faker
from src.utils.helpers import generate_uuid, get_db_connection, weighted_choice
from src.config import NUM_TEAMS_PER_ORG, NUM_USERS

fake = Faker()

DEPARTMENTS = [
    "Engineering", "Product", "Design", "Marketing", "Sales", 
    "HR", "Finance", "Operations"
]

def generate_organization_data(conn):
    cursor = conn.cursor()
    print("Generating Organization, Teams, and Users...")

    # 1. Create Organization
    org_id = generate_uuid()
    org_name = fake.company()
    org_domain = "asana-sim.com" # Simplified for consistency
    
    cursor.execute(
        "INSERT INTO organizations (id, name, domain) VALUES (?, ?, ?)",
        (org_id, org_name, org_domain)
    )

    # 2. Create Teams (Departments)
    team_ids = []
    for dept in DEPARTMENTS:
        team_id = generate_uuid()
        cursor.execute(
            "INSERT INTO teams (id, organization_id, name, description) VALUES (?, ?, ?, ?)",
            (team_id, org_id, f"{dept}", f"The {dept} department.")
        )
        team_ids.append(team_id)

    # 3. Create Users
    user_ids = []
    for _ in range(NUM_USERS):
        user_id = generate_uuid()
        first_name = fake.first_name()
        last_name = fake.last_name()
        name = f"{first_name} {last_name}"
        email = f"{first_name.lower()}.{last_name.lower()}@{org_domain}"
        
        # Handle duplicate emails simply
        count = 1
        while True:
            try:
                cursor.execute("INSERT INTO users (id, organization_id, name, email, role) VALUES (?, ?, ?, ?, ?)",
                               (user_id, org_id, name, email, weighted_choice(['Admin', 'Member', 'Guest'], [5, 90, 5])))
                break
            except sqlite3.IntegrityError:
                email = f"{first_name.lower()}.{last_name.lower()}{count}@{org_domain}"
                count += 1
        
        user_ids.append(user_id)

    # 4. Create Memberships
    # Every user belongs to 1 main team, and potentially 1 secondary team
    for user_id in user_ids:
        # Primary Team
        main_team = random.choice(team_ids)
        cursor.execute(
            "INSERT INTO team_memberships (user_id, team_id, role) VALUES (?, ?, ?)",
            (user_id, main_team, 'Contributor')
        )
        
        # 20% chance of secondary team (cross-functional)
        if random.random() < 0.2:
            second_team = random.choice([t for t in team_ids if t != main_team])
            cursor.execute(
                "INSERT OR IGNORE INTO team_memberships (user_id, team_id, role) VALUES (?, ?, ?)",
                (user_id, second_team, 'Guest')
            )

    conn.commit()
    print(f"Created Org '{org_name}', {len(team_ids)} Teams, {NUM_USERS} Users.")
    return org_id
    
import random
import sqlite3