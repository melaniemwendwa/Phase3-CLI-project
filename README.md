# Phase3-CLI-project -- GYM MANAGER CLI

A Command-Line Interface (CLI) application built with Python that helps manage a gym’s data such as members, trainers, workout plans, and schedules.
It simulates a real-world scenario where gyms track who their members are, which trainers they work with and what workout schedules they follow.
This project leverages SQLAlchemy ORM  for persistence and Alembic migration hence demonstrates clean code organization with modular utilities and helper functions.

## PROJECT STRUCTURE

```bash
cli_project/
│
├── cli.py                # Main entry point for the CLI (menus, input handling, workflow)
├── gym_manager.db        # SQLite database file (auto-created by SQLAlchemy + Alembic)
│
├── db/                   # Database package
│   ├── __init__.py       # Initializes DB engine & session maker
│   ├── models.py         # SQLAlchemy ORM models (Member, Trainer, Workout, Schedule)
│
├── migrations/           # Alembic migration folder
│   ├── env.py            # Alembic environment setup
│   ├── script.py.mako    # Alembic migration template
│   └── versions/         # Auto-generated migration files
│       └── 3fb4665d76c... # Example migration file (creates tables, etc.)
│
├── utils/                # Utility/helper functions
│   ├── helpers.py        # Input validation, formatting helpers, etc.
│
├── alembic.ini           # Alembic configuration file
├── Pipfile               # Project dependencies (SQLAlchemy, Alembic, etc.)
├── Pipfile.lock          # Locked dependency versions
└── README.md             # Project documentation

```

## FEATURES
- Add, list, and delete Members  
- Add, list, and delete Trainers  
- Add, list, and delete Workouts  
- Create Schedules (assign workouts to members on specific days)  
- View trainer-specific workouts & member-specific schedules  
- Clean database persistence with SQLAlchemy ORM 
- Schema migration support with Alembic  
- Input validation and helpful CLI feedback (⚠ for warnings, ✅ for success)  
- Uses Python data structures (lists, tuples, dicts) to organize CLI data  


## INSTALLATION & SETUP

## Clone Repository
```bash
git clone <repo url>
cd cli_project
```

## Install Dependancies
```bash
pipenv install
```


## Run database migrations
```bash
pipenv run alembic upgrade head
```

## Virtual Environment
```bash
pipenv shell
```


## Running the application
```bash
python cli.py
```

## You'll see :

--- Gym Manager ---
1. Members
2. Trainers
3. Workouts
4. Schedules
0. Exit

## CLI WORKFLOW & FUNCTIONS

## 1. Members Menu
--- Members Menu ---
1. Add Member
2. List Members
3. Delete Member
4. View Member Schedule
0. Back

• Add member -> Prompts for name, age and membership type (Monthly or Annual)
• List Members -> Displays the members
• Delete Member -> Promps ID and removes member.
• View Member Schedule -> Shows all workouts assigned to a member

## 2. Trainers Menu

--- Trainers Menu ---
1. Add Trainer
2. List Trainers
3. Delete Trainer
4. View Trainer Workouts
0. Back

• Add Trainer- Register a trainer with name and specialty.
• List Trainers -  View all trainers.
• Delete Trainer - Prompts ID and removes trainer.
• View Trainer Workouts - see workouts for a specific trainer.

## 3. Workouts Menu

--- Workouts Menu ---
1. Add Workout
2. List Workouts
3. Delete Workout
4. View Workout Members
0. Back

• Add workout - assign a workout to a trainer.
• List workouts - view all workouts with assigned trainers.
• Delete workout - remove workout by ID.
• View Workout members - see members enrolled in a workout.

## 4. Schedules Menu

--- Schedules Menu ---
1. Add Schedule (Assign Workout)
2. List Schedules
3. Delete Schedule
0. Back

• Add schedule - assign a workout to a member on a chosen day(s)
• List schedule - view all schedules in the system.
• Delete schedule - removes a schedule entry by ID.


## DATABASE SCHEMA

## Member
- id (Primary Key)
- name
- age
- membership_type

## Trainer
- id (Primary Key)
- name
- speciality

## Workout
- id (Primary Key)
- name
- description
- trainer_id

## Schedule
- id (Primary Key)
- member_id
- workout_id
- day_of_week


## TECHNOLOGIES USED
• Python 3.8
• SQLAlchemy
• Alembic (database migrations)
• SQLite (database backend)

## LICENSE
This project is under no license