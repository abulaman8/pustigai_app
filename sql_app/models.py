from sqlalchemy import Column, Integer, String, Float, JSON, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    user_name = Column(String, index=True)
    exercise_id = Column(String, ForeignKey("exercises.id"))

    exercise = relationship("Exercise")


class Exercise(Base):
    __tablename__ = "exercises"

    id = Column(String, primary_key=True, index=True)
    name = Column(String)
    source = Column(String)
    rep = Column(Integer)
    timer = Column(Integer)
    orientation = Column(String)
    ori_error = Column(String)
    ori_pass = Column(String)
    condition = Column(Float)
    cond_error = Column(String)
    cond_pass = Column(String)
    state = Column(Integer)
    wait_timer = Column(Integer)
    error_move = Column(String)
    pass_move = Column(String)
    error_id = Column(String)
    pass_id = Column(String)

    # State 1
    ub_1 = Column(JSON)
    lb_1 = Column(JSON)
    pass_1 = Column(String)
    lb_error_1 = Column(String)
    ub_error_1 = Column(String)
    sub_rep_1 = Column(Integer)
    sub_state_1 = Column(Integer)
    sub_ub_11 = Column(JSON)
    sub_lb_11 = Column(JSON)
    sub_pass_11 = Column(String)
    sub_lb_error_11 = Column(String)
    sub_ub_error_11 = Column(String)
    sub_ub_12 = Column(JSON)
    sub_lb_12 = Column(JSON)
    sub_pass_12 = Column(String)
    sub_lb_error_12 = Column(String)
    sub_ub_error_12 = Column(String)

    # State 2
    ub_2 = Column(JSON)
    lb_2 = Column(JSON)
    pass_2 = Column(String)
    lb_error_2 = Column(String)
    ub_error_2 = Column(String)
    sub_rep_2 = Column(Integer)
    sub_state_2 = Column(Integer)
    sub_ub_21 = Column(JSON)
    sub_lb_21 = Column(JSON)
    sub_pass_21 = Column(String)
    sub_lb_error_21 = Column(String)
    sub_ub_error_21 = Column(String)
    sub_ub_22 = Column(JSON)
    sub_lb_22 = Column(JSON)
    sub_pass_22 = Column(String)
    sub_lb_error_22 = Column(String)
    sub_ub_error_22 = Column(String)
