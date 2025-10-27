from sqlalchemy import Column, Integer, String, Float, ForeignKey
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
    pass_1 = Column(String)
    lb_error_1 = Column(String)
    ub_error_1 = Column(String)
    sub_rep_1 = Column(Integer)
    sub_state_1 = Column(Integer)
    sub_pass_11 = Column(String)
    sub_lb_error_11 = Column(String)
    sub_ub_error_11 = Column(String)
    sub_pass_12 = Column(String)
    sub_lb_error_12 = Column(String)
    sub_ub_error_12 = Column(String)

    # State 2
    pass_2 = Column(String)
    lb_error_2 = Column(String)
    ub_error_2 = Column(String)
    sub_rep_2 = Column(Integer)
    sub_state_2 = Column(Integer)
    sub_pass_21 = Column(String)
    sub_lb_error_21 = Column(String)
    sub_ub_error_21 = Column(String)
    sub_pass_22 = Column(String)
    sub_lb_error_22 = Column(String)
    sub_ub_error_22 = Column(String)
    # -- New Optional Sub-State 2 Fields --
    sub_pass_23 = Column(String, nullable=True)
    sub_lb_error_23 = Column(String, nullable=True)
    sub_ub_error_23 = Column(String, nullable=True)
    sub_pass_24 = Column(String, nullable=True)
    sub_lb_error_24 = Column(String, nullable=True)
    sub_ub_error_24 = Column(String, nullable=True)

    # -- Typo Fix Fields --
    sub_lb_pass_23 = Column(String, nullable=True)  # Added this field
    sub_lb_pass_24 = Column(String, nullable=True)  # Added this field

    # -- New Optional State 3 Fields --
    pass_3 = Column(String, nullable=True)
    lb_error_3 = Column(String, nullable=True)
    ub_error_3 = Column(String, nullable=True)
