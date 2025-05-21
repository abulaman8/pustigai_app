# Simulated database
users_db = {
    "us001": {"user_name": "John Doe", "exercise": "ex001"}
}

exercises_db = {
    "ex001": {
        "name": "Squat",
        "source": "squat_demo.mp4",
        "rep": 3,
        "timer": 30,
        "orientation": "front",
        "ori_error": "Incorrect orientation, face forward",
        "ori_pass": "Orientation correct",
        "condition": 0.1,
        "cond_error": "Adjust your stance",
        "cond_pass": "Stance correct",
        "state": 2,
        "wait_timer": 5,
        "error_move": "Exercise failed, try again",
        "pass_move": "Exercise completed",
        "error_id": "ex001",
        "pass_id": "",
        "ub_1": [170, 170, 90, 90, 170, 170, 90, 90, 90, 90, 90, 90],
        "lb_1": [160, 160, 80, 80, 160, 160, 80, 80, 80, 80, 80, 80],
        "pass_1": "State 1 passed",
        "lb_error_1": "Angle too low",
        "ub_error_1": "Angle too high",
        "sub_rep_1": 2,
        "sub_state_1": 2,
        "sub_ub_11": [160, 160, 80, 80, 160, 160, 80, 80, 80, 80, 80, 80],
        "sub_lb_11": [150, 150, 70, 70, 150, 150, 70, 70, 70, 70, 70, 70],
        "sub_pass_11": "Sub-state 1.1 passed",
        "sub_lb_error_11": "Sub-angle too low",
        "sub_ub_error_11": "Sub-angle too high",
        "sub_ub_12": [170, 170, 90, 90, 170, 170, 90, 90, 90, 90, 90, 90],
        "sub_lb_12": [160, 160, 80, 80, 160, 160, 80, 80, 80, 80, 80, 80],
        "sub_pass_12": "Sub-state 1.2 passed",
        "sub_lb_error_12": "Sub-angle too low",
        "sub_ub_error_12": "Sub-angle too high",
        "ub_2": [160, 160, 80, 80, 160, 160, 80, 80, 80, 80, 80, 80],
        "lb_2": [150, 150, 70, 70, 150, 150, 70, 70, 70, 70, 70, 70],
        "pass_2": "State 2 passed",
        "lb_error_2": "Angle too low",
        "ub_error_2": "Angle too high",
        "sub_rep_2": 2,
        "sub_state_2": 2,
        "sub_ub_21": [150, 150, 70, 70, 150, 150, 70, 70, 70, 70, 70, 70],
        "sub_lb_21": [140, 140, 60, 60, 140, 140, 60, 60, 60, 60, 60, 60],
        "sub_pass_21": "Sub-state 2.1 passed",
        "sub_lb_error_21": "Sub-angle too low",
        "sub_ub_error_21": "Sub-angle too high",
        "sub_ub_22": [160, 160, 80, 80, 160, 160, 80, 80, 80, 80, 80, 80],
        "sub_lb_22": [150, 150, 70, 70, 150, 150, 70, 70, 70, 70, 70, 70],
        "sub_pass_22": "Sub-state 2.2 passed",
        "sub_lb_error_22": "Sub-angle too low",
        "sub_ub_error_22": "Sub-angle too high"
    }
}


def get_user(user_id):
    return users_db.get(user_id)


def get_exercise(exid):
    return exercises_db.get(exid)
