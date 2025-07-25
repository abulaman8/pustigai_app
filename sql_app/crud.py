from sqlalchemy.orm import Session
from . import models, schemas
import json


def get_user(db: Session, user_id: str):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_exercise(db: Session, exid: str):
    return db.query(models.Exercise).filter(models.Exercise.id == exid).first()


def get_all_exercises(db: Session):
    return db.query(models.Exercise).all()


def create_exercise(db: Session, exercise: schemas.ExerciseCreate):
    db_exercise = models.Exercise(**exercise.dict())
    db.add(db_exercise)
    db.commit()
    db.refresh(db_exercise)
    return db_exercise


def update_exercise(db: Session, exid: str, exercise_data: dict):
    db_exercise = db.query(models.Exercise).filter(
        models.Exercise.id == exid).first()
    if db_exercise:
        for key, value in exercise_data.items():
            # For JSON fields, ensure they are stored as JSON strings
            if key in ['ub_1', 'lb_1', 'sub_ub_11', 'sub_lb_11', 'sub_ub_12', 'sub_lb_12', 'ub_2', 'lb_2', 'sub_ub_21', 'sub_lb_21', 'sub_ub_22', 'sub_lb_22']:
                if isinstance(value, str):
                    try:
                        value = json.loads(value)
                    except json.JSONDecodeError:
                        # Handle case where string is not valid JSON
                        pass
            setattr(db_exercise, key, value)
        db.commit()
        db.refresh(db_exercise)
    return db_exercise


def delete_exercise(db: Session, exid: str):
    db_exercise = db.query(models.Exercise).filter(
        models.Exercise.id == exid).first()
    if db_exercise:
        db.delete(db_exercise)
        db.commit()
        return True
    return False


def to_dict(obj):
    """Converts a SQLAlchemy model instance to a dictionary."""
    if obj is None:
        return None
    return {c.key: getattr(obj, c.key) for c in obj.__table__.columns}
