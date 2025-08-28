from sqlalchemy import Column, Integer, String, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship, validates
from db import Base
from sqlalchemy import func


# Models: Trainer, Workout, Member, Schedule


class Trainer(Base):
    __tablename__ = "trainers"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    specialty = Column(String, nullable=True)


    workouts = relationship("Workout", back_populates="trainer", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Trainer {self.id}: {self.name} ({self.specialty or 'General'})>"


    @validates("name")
    def validate_name(self, key, value):
        if not value or not value.strip():
            raise ValueError("Trainer name cannot be empty.")
        return value.strip()

    # ORM methods
    @classmethod
    def create(cls, session, name, specialty=None):
        try:
            t = cls(name=name.strip(), specialty=(specialty.strip() if specialty else None))
            session.add(t)
            session.commit()
            return t
        except Exception:
            session.rollback()
            raise

    @classmethod
    def get_all(cls, session):
        return session.query(cls).order_by(cls.id).all()

    @classmethod
    def find_by_id(cls, session, id_):
        return session.get(cls, id_)

    @classmethod
    def find_by_name(cls, session, name):
        if not name:
            return None
        return session.query(cls).filter(func.lower(cls.name) == name.strip().lower()).first()

    @classmethod
    def delete(cls, session, id_):
        obj = cls.find_by_id(session, id_)
        if obj:
            session.delete(obj)
            session.commit()
            return True
        return False


class Workout(Base):
    __tablename__ = "workouts"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    trainer_id = Column(Integer, ForeignKey("trainers.id"), nullable=False)

    trainer = relationship("Trainer", back_populates="workouts")
    schedules = relationship("Schedule", back_populates="workout", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Workout {self.id}: {self.name} (Trainer: {self.trainer.name if self.trainer else self.trainer_id})>"

    @validates("name")
    def validate_name(self, key, value):
        if not value or not value.strip():
            raise ValueError("Workout name cannot be empty.")
        return value.strip()

    @classmethod
    def create(cls, session, name, trainer, description=None):
        try:
            w = cls(name=name.strip(), trainer=trainer, description=(description.strip() if description else None))
            session.add(w)
            session.commit()
            return w
        except Exception:
            session.rollback()
            raise

    @classmethod
    def get_all(cls, session):
        return session.query(cls).order_by(cls.id).all()

    @classmethod
    def find_by_id(cls, session, id_):
        return session.get(cls, id_)

    @classmethod
    def find_by_name_and_trainer(cls, session, name, trainer_id):
        if not name:
            return None
        return session.query(cls).filter(
            func.lower(cls.name) == name.strip().lower(),
            cls.trainer_id == trainer_id
        ).first()

    @classmethod
    def delete(cls, session, id_):
        obj = cls.find_by_id(session, id_)
        if obj:
            session.delete(obj)
            session.commit()
            return True
        return False


class Member(Base):
    __tablename__ = "members"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=True)
    membership_type = Column(String, nullable=False)  # 'Monthly' or 'Annual'

    schedules = relationship("Schedule", back_populates="member", cascade="all, delete-orphan")

    # database-level constraint
    __table_args__ = (
        CheckConstraint("membership_type IN ('Monthly','Annual')", name="membership_type_check"),
    )

    def __repr__(self):
        return f"<Member {self.id}: {self.name} ({self.membership_type})>"

    @validates("name")
    def validate_name(self, key, value):
        if not value or not value.strip():
            raise ValueError("Member name cannot be empty.")
        return value.strip()

    @validates("membership_type")
    def validate_membership_type(self, key, value):
        if not value or value.strip() not in ("Monthly", "Annual"):
            raise ValueError("membership_type must be 'Monthly' or 'Annual'.")
        return value.strip()

    @classmethod
    def create(cls, session, name, membership_type, age=None):
        try:
            m = cls(name=name.strip(), membership_type=membership_type.strip(), age=(int(age) if age else None))
            session.add(m)
            session.commit()
            return m
        except Exception:
            session.rollback()
            raise

    @classmethod
    def get_all(cls, session):
        return session.query(cls).order_by(cls.id).all()

    @classmethod
    def find_by_id(cls, session, id_):
        return session.get(cls, id_)

    @classmethod
    def find_by_name(cls, session, name):
        if not name:
            return None
        return session.query(cls).filter(func.lower(cls.name) == name.strip().lower()).first()

    @classmethod
    def delete(cls, session, id_):
        obj = cls.find_by_id(session, id_)
        if obj:
            session.delete(obj)
            session.commit()
            return True
        return False


class Schedule(Base):
    __tablename__ = "schedules"

    id = Column(Integer, primary_key=True)
    member_id = Column(Integer, ForeignKey("members.id"), nullable=False)
    workout_id = Column(Integer, ForeignKey("workouts.id"), nullable=False)
    day_of_week = Column(String, nullable=False)  # e.g. Monday

    member = relationship("Member", back_populates="schedules")
    workout = relationship("Workout", back_populates="schedules")

    def __repr__(self):
        return f"<Schedule {self.id}: Member {self.member.name if self.member else self.member_id} - Workout {self.workout.name if self.workout else self.workout_id} on {self.day_of_week}>"

    @validates("day_of_week")
    def validate_day(self, key, value):
        if not value or not value.strip():
            raise ValueError("day_of_week cannot be empty.")
        return value.strip()

    @classmethod
    def create(cls, session, member, workout, day_of_week):
        try:
            s = cls(member=member, workout=workout, day_of_week=day_of_week.strip())
            session.add(s)
            session.commit()
            return s
        except Exception:
            session.rollback()
            raise

    @classmethod
    def get_all(cls, session):
        return session.query(cls).order_by(cls.id).all()

    @classmethod
    def find_by_id(cls, session, id_):
        return session.get(cls, id_)

    @classmethod
    def delete(cls, session, id_):
        obj = cls.find_by_id(session, id_)
        if obj:
            session.delete(obj)
            session.commit()
            return True
        return False
