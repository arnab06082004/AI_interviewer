def next_question(state):
    next_index = state['current_question'] + 1
    if next_index < len(state['questions']):
        return "interview"
    else:
        return "report"