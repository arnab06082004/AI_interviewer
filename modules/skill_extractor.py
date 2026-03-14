from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
load_dotenv()
llm = ChatGroq(model='llama-3.3-70b-versatile')

def extract_skill_from_resume(state):
    prompts = PromptTemplate.from_template('''
        Extract all technical skills from the resume.

        Resume:
        {resume}

        Return skills as a comma separated list.
        '''
    )

    chain = prompts | llm 

    result = chain.invoke({"resume": state['resume_text']})

    skills = result.content.split(",")

    return {'skills' : [skill.strip() for skill in skills]}
