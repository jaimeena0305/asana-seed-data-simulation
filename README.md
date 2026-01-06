# **Asana RL Environment Seed Data Generator**

This repository contains the logic to generate high-quality, synthetic seed data for a Reinforcement Learning (RL) environment simulating the Asana project management platform.

## **Overview**

The generator creates a realistic B2B SaaS organization structure including:

* **Structure:** Organization \-\> Teams \-\> Projects \-\> Sections \-\> Tasks.  
* **People:** Users with roles and team memberships.  
* **Activity:** Tasks with descriptions, due dates, priorities, comments, and completion statuses.

The data is statistically distributed to mirror real-world usage patterns (e.g., weekend lulls, "at risk" projects, team-specific terminologies).

## **Setup & Usage**

### **Prerequisites**

* Python 3.8+

### **Installation**

1. Clone the repository.  
2. Install dependencies:  
   pip install \-r requirements.txt

### **Running the Simulation**

Execute the main script to generate the SQLite database:

python src/main.py

The output will be saved to output/asana\_simulation.sqlite.

### **Configuration**

You can adjust the scale of the simulation in src/config.py:

* NUM\_USERS: Total employees.  
* NUM\_TEAMS\_PER\_ORG: Number of departments.  
* SIMULATION\_START\_DAYS\_AGO: How far back history goes.

## **Project Structure**

├── README.md  
├── requirements.txt  
├── schema.sql                   \# SQLite DDL  
├── src/  
│   ├── main.py                  \# Entry point  
│   ├── config.py                \# Settings  
│   ├── generators/              \# Data generation logic  
│   │   ├── users.py             \# Orgs, Teams, Users  
│   │   ├── projects.py          \# Projects, Sections  
│   │   └── tasks.py             \# Tasks, Comments  
│   └── utils/  
│       └── helpers.py           \# UUIDs, Date math, DB connectors  
└── output/  
    └── asana\_simulation.sqlite  \# Generated artifact

## **Methodology**

The generation strategy uses a mix of:

1. **Faker**: For PII (Names, Emails).  
2. **Heuristic Templates**: For domain-specific task names (Engineering vs Marketing).  
3. **Probabilistic Distributions**: For dates, statuses, and completion rates.

See the [Documentation](https://docs.google.com/document/d/1qhyhSYLBE3NP5xYVJHPC94rjyXEWPh_Lbyly7wWQFdA/edit?tab=t.0) for the full schema and design decisions.