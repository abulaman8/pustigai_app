from pydantic import BaseModel
from typing import List, Optional


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
    pass_id: Optional[str] = ""
    ub_1: List[int]
    lb_1: List[int]
    pass_1: str
    lb_error_1: str
    ub_error_1: str
    sub_rep_1: int
    sub_state_1: int
    sub_ub_11: List[int]
    sub_lb_11: List[int]
    sub_pass_11: str
    sub_lb_error_11: str
    sub_ub_error_11: str
    sub_ub_12: List[int]
    sub_lb_12: List[int]
    sub_pass_12: str
    sub_lb_error_12: str
    sub_ub_error_12: str
    ub_2: List[int]
    lb_2: List[int]
    pass_2: str
    lb_error_2: str
    ub_error_2: str
    sub_rep_2: int
    sub_state_2: int
    sub_ub_21: List[int]
    sub_lb_21: List[int]
    sub_pass_21: str
    sub_lb_error_21: str
    sub_ub_error_21: str
    sub_ub_22: List[int]
    sub_lb_22: List[int]
    sub_pass_22: str
    sub_lb_error_22: str
    sub_ub_error_22: str


class ExerciseCreate(ExerciseBase):
    pass


class Exercise(ExerciseBase):
    class Config:
        from_attributes = True  # FIXED: Renamed 'orm_mode'
