import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils.helpers import init_db
from src.generators.users import generate_organization_data
from src.generators.projects import generate_projects
from src.generators.tasks import generate_tasks

def main():
    print("=== Asana RL Data Generator ===")
    
    # 1. Init Database
    conn = init_db()
    
    # 2. Generate Organization & Users
    org_id = generate_organization_data(conn)
    
    # 3. Generate Projects
    generate_projects(conn, org_id)
    
    # 4. Generate Tasks & Comments
    generate_tasks(conn, org_id)
    
    print("\n=== Generation Complete ===")
    print("Database saved to: output/asana_simulation.sqlite")
    conn.close()

if __name__ == "__main__":
    main()