from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
load_dotenv()

llm = ChatGroq(model='llama-3.3-70b-versatile')

def generate_final_report(state):
    prompt = PromptTemplate.from_template(
        '''
        You have 10 years of experience in making final report and providing feed back to the students.
        generate a final interview summary based on the scores, question and the answers.
        Also be very professional and precise about you report.
        questions : {questions}
        answer : {answer}
        scores : {scores}

        now generate 
        -few strengths (each strengths will be one liner )
        -few weakness (each weakness will be one liner )
        -few improvements suggestions (each improvements will be one liner )

        Your report must be very precise and short but long enough to cover everything.
        '''
    )
    chain = prompt | llm 
    result = chain.invoke({
        'questions' : state['questions'],
        'answer' : state['answers'],
        'scores' : state["scores"]
    })
    return {'report' : result.content}