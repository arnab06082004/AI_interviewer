from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
load_dotenv()
llm = ChatGroq(model='llama-3.3-70b-versatile')

def generate_question_from_skill(state):
    skills = ','.join(state['skills'])
    prompt = PromptTemplate.from_template(
    '''
    You are an technical interviewer with 10 years of experience.
    Generate top 10 most asked interview questions based on these skills.
    Your questions answer should not very big and the questions must relevant to the skill.
    
        Skills:
        {skills}

        Return each question in a new line.
    '''
    )

    chain = prompt | llm 
    result = chain.invoke({"skills": skills})

    questions = [q.strip() for q in result.content.split("\n") if q.strip()]

    return {
        "questions": questions,
        "current_question": 0,
        "answers": [],
        "scores": []
    }