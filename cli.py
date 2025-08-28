import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db import init_db
from db.models import Trainer, Workout, Member, Schedule
from utils.helpers import prompt, safe_int

DB_URL = "sqlite:///gym_manager.db"


def get_session():
    engine = create_engine(DB_URL, echo=False)
    Session = sessionmaker(bind=engine)
    init_db(engine)
    return Session()


MEMBERSHIP_OPTIONS = ["Monthly", "Annual"]  # LIST
MEMBERSHIP_FEES = {"Monthly": 2000, "Annual": 22000}  # DICT


# ---------- Member actions ----------
def add_member(session):
    print("\n-- Add Member --")
    name = prompt("Name: ")
    if not name:
        print("⚠ Name required.")
        return

    print("Membership options:", MEMBERSHIP_OPTIONS)  # LIST displayed
    mem_type = prompt("Membership type (Monthly or Annual): ")
    if mem_type not in MEMBERSHIP_OPTIONS:
        print("⚠ Invalid membership type. Please choose 'Monthly' or 'Annual'.")
        return

    age = prompt("Age (optional): ")
    age_val = safe_int(age) if age else None
    try:
        m = Member.create(session, name=name, membership_type=mem_type, age=age_val)
        fee = MEMBERSHIP_FEES.get(mem_type)  # DICT usage
        print(f"✅ Created {m} (fee: {fee})")
    except Exception as e:
        print("⚠ Could not create member:", e)


def list_members(session):
    print("\n-- Members --")
    ms = Member.get_all(session)  # LIST of Member objects
    if not ms:
        print("No members.")
        return

    members_list = [(m.id, m.name, m.membership_type, m.age) for m in ms]  # LIST of TUPLES
    for m_id, m_name, m_type, m_age in members_list:
        print(f"{m_id}. {m_name} - {m_type} - Age: {m_age or 'N/A'}")


def delete_member(session):
    list_members(session)
    id_ = safe_int(prompt("Enter Member ID to delete: "))
    if id_ is None:
        print("⚠ Invalid ID.")
        return
    ok = Member.delete(session, id_)
    print("✅ Deleted." if ok else "⚠ Member not found or could not delete.")


def view_member_schedule(session):
    name = prompt("Member name to view schedule: ")
    m = Member.find_by_name(session, name)
    if not m:
        print("⚠ Member not found.")
        return
    print(f"\nSchedules for {m.name}:")
    if not m.schedules:
        print("No schedules.")
        return

    schedules_list = [
        {"schedule_id": s.id, "workout": s.workout.name,
         "trainer": s.workout.trainer.name, "day": s.day_of_week}
        for s in m.schedules
    ]  # LIST of DICTS
    for sched in schedules_list:
        print(f"{sched['schedule_id']}. Workout: {sched['workout']} "
              f"(Trainer: {sched['trainer']}) - Day: {sched['day']}")


# ---------- Trainer actions ----------
def add_trainer(session):
    print("\n-- Add Trainer --")
    name = prompt("Name: ")
    if not name:
        print("⚠ Name required.")
        return
    specialty = prompt("Specialty (optional): ")
    try:
        t = Trainer.create(session, name=name, specialty=specialty)
        print(f"✅ Created {t}")
    except Exception as e:
        print("⚠ Could not create trainer:", e)


def list_trainers(session):
    print("\n-- Trainers --")
    ts = Trainer.get_all(session)  # LIST of Trainer objects
    if not ts:
        print("No trainers.")
        return

    trainers_list = [(t.id, t.name, t.specialty or "General") for t in ts]  # LIST of TUPLES
    for tr in trainers_list:
        print(f"{tr[0]}. {tr[1]} - {tr[2]}")


def delete_trainer(session):
    list_trainers(session)
    id_ = safe_int(prompt("Enter Trainer ID to delete: "))
    if id_ is None:
        print("⚠ Invalid ID.")
        return
    ok = Trainer.delete(session, id_)
    print("✅ Deleted." if ok else "⚠ Trainer not found or could not delete.")


def view_trainer_workouts(session):
    name = prompt("Trainer name to view workouts: ")
    t = Trainer.find_by_name(session, name)
    if not t:
        print("⚠ Trainer not found.")
        return
    print(f"\nWorkouts by {t.name}:")
    if not t.workouts:
        print("No workouts.")
        return

    workouts_list = [(w.id, w.name, w.description or "") for w in t.workouts]  # LIST of TUPLES
    for wid, wname, wdesc in workouts_list:
        print(f"{wid}. {wname} - {wdesc}")


# ---------- Workout actions ----------
def add_workout(session):
    print("\n-- Add Workout --")
    trainer_name = prompt("Trainer name for this workout: ")
    t = Trainer.find_by_name(session, trainer_name)
    if not t:
        print("⚠ Trainer not found. Add the trainer first.")
        return
    name = prompt("Workout name: ")
    if not name:
        print("⚠ Workout name required.")
        return
    desc = prompt("Description (optional): ")
    try:
        w = Workout.create(session, name=name, trainer=t, description=desc)
        print(f"✅ Created {w}")
    except Exception as e:
        print("⚠ Could not create workout:", e)


def list_workouts(session):
    print("\n-- Workouts --")
    ws = Workout.get_all(session)  # LIST of Workout objects
    if not ws:
        print("No workouts.")
        return

    workouts_list = [(w.id, w.name, w.trainer.name) for w in ws]  # LIST of TUPLES
    for tup in workouts_list:
        print(f"{tup[0]}. {tup[1]} (Trainer: {tup[2]})")


def delete_workout(session):
    list_workouts(session)
    id_ = safe_int(prompt("Enter Workout ID to delete: "))
    if id_ is None:
        print("⚠ Invalid ID.")
        return
    ok = Workout.delete(session, id_)
    print("✅ Deleted." if ok else "⚠ Workout not found or could not delete.")


def view_workout_members(session):
    name = prompt("Workout name to view enrolled members: ")
    w = session.query(Workout).filter(Workout.name.ilike(name.strip())).first()
    if not w:
        print("⚠ Workout not found.")
        return
    print(f"\nMembers in workout {w.name}:")
    entries = session.query(Schedule).filter_by(workout_id=w.id).all()
    if not entries:
        print("No members enrolled.")
        return

    enrolled = [(s.id, s.member.name, s.day_of_week) for s in entries]  # LIST of TUPLES
    for row in enrolled:
        print(f"{row[0]}. {row[1]} - Day: {row[2]}")


# ---------- Schedule actions ----------
def add_schedule(session):
    print("\n-- Assign Workout to Member (Schedule) --")
    member_name = prompt("Member name: ")
    m = Member.find_by_name(session, member_name)
    if not m:
        print("⚠ Member not found.")
        return
    list_workouts(session)
    wid = safe_int(prompt("Enter Workout ID to assign: "))
    if wid is None:
        print("⚠ Invalid ID.")
        return
    w = Workout.find_by_id(session, wid)
    if not w:
        print("⚠ Workout not found.")
        return
    day = prompt("Day of week (e.g., Monday): ")
    if not day:
        print("⚠ Day is required.")
        return
    try:
        s = Schedule.create(session, member=m, workout=w, day_of_week=day)
        print(f"✅ Created {s}")
    except Exception as e:
        print("⚠ Could not create schedule:", e)


def list_schedules(session):
    print("\n-- Schedules --")
    ss = Schedule.get_all(session)
    if not ss:
        print("No schedules.")
        return

    schedules_list = [
        {"id": s.id, "member": s.member.name,
         "workout": s.workout.name, "trainer": s.workout.trainer.name,
         "day": s.day_of_week}
        for s in ss
    ]  # LIST of DICTS
    for sd in schedules_list:
        print(f"{sd['id']}. {sd['member']} -> {sd['workout']} "
              f"(Trainer: {sd['trainer']}) on {sd['day']}")


def delete_schedule(session):
    list_schedules(session)
    id_ = safe_int(prompt("Enter Schedule ID to delete: "))
    if id_ is None:
        print("⚠ Invalid ID.")
        return
    ok = Schedule.delete(session, id_)
    print("✅ Deleted." if ok else "⚠ Schedule not found or could not delete.")


# ---------- Menus ----------
def main_menu():
    print("""
--- Gym Manager ---
1. Members
2. Trainers
3. Workouts
4. Schedules
0. Exit
""")


def members_menu(session):
    print("""
--- Members Menu ---
1. Add Member
2. List Members
3. Delete Member
4. View Member Schedule
0. Back
""")
    choice = prompt("Choice: ")
    actions = {
        "1": lambda: add_member(session),
        "2": lambda: list_members(session),
        "3": lambda: delete_member(session),
        "4": lambda: view_member_schedule(session),
    }
    if choice == "0":
        return
    action = actions.get(choice)
    if action: action()
    else: print("⚠ Invalid choice.")


def trainers_menu(session):
    print("""
--- Trainers Menu ---
1. Add Trainer
2. List Trainers
3. Delete Trainer
4. View Trainer Workouts
0. Back
""")
    choice = prompt("Choice: ")
    actions = {
        "1": lambda: add_trainer(session),
        "2": lambda: list_trainers(session),
        "3": lambda: delete_trainer(session),
        "4": lambda: view_trainer_workouts(session),
    }
    if choice == "0":
        return
    action = actions.get(choice)
    if action: action()
    else: print("⚠ Invalid choice.")


def workouts_menu(session):
    print("""
--- Workouts Menu ---
1. Add Workout
2. List Workouts
3. Delete Workout
4. View Workout Members
0. Back
""")
    choice = prompt("Choice: ")
    actions = {
        "1": lambda: add_workout(session),
        "2": lambda: list_workouts(session),
        "3": lambda: delete_workout(session),
        "4": lambda: view_workout_members(session),
    }
    if choice == "0":
        return
    action = actions.get(choice)
    if action: action()
    else: print("⚠ Invalid choice.")


def schedules_menu(session):
    print("""
--- Schedules Menu ---
1. Add Schedule (Assign Workout)
2. List Schedules
3. Delete Schedule
0. Back
""")
    choice = prompt("Choice: ")
    actions = {
        "1": lambda: add_schedule(session),
        "2": lambda: list_schedules(session),
        "3": lambda: delete_schedule(session),
    }
    if choice == "0":
        return
    action = actions.get(choice)
    if action: action()
    else: print("⚠ Invalid choice.")


# ---------- Main loop ----------
def main():
    session = get_session()
    while True:
        main_menu()
        choice = prompt("Choice: ")
        if choice == "1":
            members_menu(session)
        elif choice == "2":
            trainers_menu(session)
        elif choice == "3":
            workouts_menu(session)
        elif choice == "4":
            schedules_menu(session)
        elif choice == "0":
            sys.exit(0)
        else:
            print("⚠ Invalid choice, try again.")


if __name__ == "__main__":
    main()
