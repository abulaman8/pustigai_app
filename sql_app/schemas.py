from pydantic import BaseModel
from typing import Optional, Any, Dict


class ExerciseBase(BaseModel):
    id: str
    name: str
    source: str
    rep: int
    timer: int
    orientation: str
    ori_error: str
    ori_pass: str
    condition: float
    cond_error: str
    cond_pass: str
    state: int
    wait_timer: int
    error_move: str
    pass_move: str
    error_id: str
    pass_id: Optional[str] = None

    # State 1
    pass_1: str
    lb_error_1: str
    ub_error_1: str
    sub_rep_1: int
    sub_state_1: int
    sub_pass_11: str
    sub_lb_error_11: str
    sub_ub_error_11: str
    sub_pass_12: str
    sub_lb_error_12: str
    sub_ub_error_12: str

    # State 2
    pass_2: str
    lb_error_2: str
    ub_error_2: str
    sub_rep_2: int
    sub_state_2: int
    sub_pass_21: str
    sub_lb_error_21: str
    sub_ub_error_21: str
    sub_pass_22: str
    sub_lb_error_22: str
    sub_ub_error_22: str

    # Optional Sub-State 2
    sub_pass_23: Optional[str] = None
    sub_lb_error_23: Optional[str] = None
    sub_ub_error_23: Optional[str] = None
    sub_pass_24: Optional[str] = None
    sub_lb_error_24: Optional[str] = None
    sub_ub_error_24: Optional[str] = None

    # Typo Fix Fields
    sub_lb_pass_23: Optional[str] = None  # Added this field
    sub_lb_pass_24: Optional[str] = None  # Added this field

    # Optional State 3
    pass_3: Optional[str] = None
    lb_error_3: Optional[str] = None
    ub_error_3: Optional[str] = None


class ExerciseCreate(ExerciseBase):
    pass


class Exercise(ExerciseBase):
    class Config:
        from_attributes = True


class ExerciseUpdate(BaseModel):
    id: str
    updates: Dict[str, Any]
