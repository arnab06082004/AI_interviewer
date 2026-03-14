from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(model="llama-3.3-70b-versatile")

def evaluate_answer(state):
    if len(state["answers"]) == 0:
        return state

    # current_question was already incremented in interview_node,
    # so subtract 1 to get the question that was just answered
    q_index = state["current_question"] - 1

    if q_index < 0 or q_index >= len(state["questions"]):
        return state

    question = state["questions"][q_index]
    answer = state["answers"][-1]

    prompt = PromptTemplate.from_template(
        """
        Evaluate the candidate answer.

        Question:
        {question}

        Answer:
        {answer}

        Give only a score out of 10. Reply with a single integer, nothing else.
        """
    )

    chain = prompt | llm

    result = chain.invoke({
        "question": question,
        "answer": answer
    })

    # Be more robust: find first digit in the response
    import re
    match = re.search(r'\d+', result.content.strip())
    score = int(match.group()) if match else 5
    score = min(score, 10)  # clamp to valid range

    scores = list(state["scores"])   # avoid mutating state directly
    scores.append(score)

    return {"scores": scores}