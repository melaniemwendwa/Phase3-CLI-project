# Phase3-CLI-project -- GYM MANAGER CLI

A Command-Line Interface (CLI) application built with Python that helps manage a gym’s data such as members, trainers, workout plans, and schedules.
It simulates a real-world scenario where gyms track who their members are, which trainers they work with and what workout schedules they follow.
This project leverages SQLAlchemy ORM  for persistence and demonstrates clean code organization with modular utilities and helper functions.

## PROJECT STRUCTURE

```bash
CLI_PROJECT/
│
├── cli.py                # Entry point for running the CLI application
├── gym_manager.db         # SQLite database file (auto-created by SQLAlchemy)
│
├── db/                   
│   ├── __init__.py        # Database initialization and connection setup
│   └── models.py          # SQLAlchemy ORM models for database tables
│
├── utils/
│   └── helpers.py         # Utility functions used across the application
│
├── Pipfile                # Dependency management with Pipenv
├── Pipfile.lock           # Locked dependencies for reproducibility
└── README.md              # Documentation for the project
```

## FEATURES

### Data Management
- Storage of GYM data.
- Clear ORM-based table relationships.

### CLI Commands
- Add, update or delete gym members.
- Manaae trainer and workout schedules

## Utilities
- Input Validation
- Reusable functions for better modularity
- Uses Pipenv for dependancy and environment management


## INSTALLATION & SETUP

## Clone Repository
```bash
git clone <repo url>
cd cli_project
```

## Install Dependancies
```bash
pip install pipenv
pipenv install
```

## Virtual Environment
```bash
pipenv shell
```


## Run the application
```bash
python cli.py
```


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


## LICENSE
This project is under no license