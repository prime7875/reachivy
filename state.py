
def init_state():
    return {
        "conversation": [],
        "transcript": [],
        "started": False,
        "waiting_for_user": False,
        "draft_answer": "",
        "has_draft": False,
        "ended": False,
        "report": None
    }


def add_turn(state, role, content):
    state["conversation"].append({"role": role, "content": content})
    state["transcript"].append({
        "role": role,
        "content": content
    })