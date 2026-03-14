from typing import TypedDict, List
from streamlit.runtime.uploaded_file_manager import UploadedFile

class state(TypedDict):
    resume_file: UploadedFile
    resume_text: str
    skills: List[str]
    questions: List[str]
    question: str          # the current question being asked
    current_question: int  # index of the *next* question to ask
    answers: List[str]
    scores: List[int]
    report: str