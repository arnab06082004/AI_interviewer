def interview_node(state):
    q_index = state['current_question']
    question = state['questions'][q_index]
    return {
        "question": question,
        "current_question": q_index + 1   # advance so evaluate knows which Q was just asked
    }