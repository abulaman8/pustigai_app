from sql_app.database import SessionLocal, engine
from sql_app.models import Base, User, Exercise
from generated_db_seed_data import exercises_db

users_db = {
    "us001": {"user_name": "John Doe", "exercise": "ex001"}
}


def init_db():
    # Create all tables in the database.
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    # Check if data already exists
    if db.query(Exercise).first():
        print("Database already seeded.")
        db.close()
        return

    # Add exercises
    for exid, data in exercises_db.items():
        db_exercise = Exercise(**data)
        db.add(db_exercise)
    db.commit()

    # Add users
    for userid, data in users_db.items():
        db_user = User(
            id=userid, user_name=data['user_name'], exercise_id=data['exercise'])
        db.add(db_user)
    db.commit()

    print("Database seeded successfully.")
    db.close()


if __name__ == "__main__":
    init_db()
