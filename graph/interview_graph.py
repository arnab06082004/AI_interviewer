from langgraph.graph import StateGraph,START,END
from graph.graph_state import state
from graph.next_question_decide_node import next_question
from graph.current_question_node import interview_node
from modules.evaluate_answer import evaluate_answer
from modules.final_report import generate_final_report
from modules.pdf_loader import extract_text_from_pdf
from modules.question_generator import generate_question_from_skill
from modules.skill_extractor import extract_skill_from_resume


graph_builder = StateGraph(state)
graph_builder.add_node('resume_parser',extract_text_from_pdf)
graph_builder.add_node('skill',extract_skill_from_resume)
graph_builder.add_node('generate_question',generate_question_from_skill)
graph_builder.add_node('interview',interview_node)
graph_builder.add_node('evaluate',evaluate_answer)
graph_builder.add_node('report',generate_final_report)

graph_builder.add_edge(START,'resume_parser')
graph_builder.add_edge('resume_parser','skill')
graph_builder.add_edge('skill','generate_question')
graph_builder.add_edge('generate_question','interview')
graph_builder.add_edge('interview','evaluate')

graph_builder.add_conditional_edges(
    'evaluate',
    next_question,
    {
        'report' : 'report',
        'interview' : 'interview'
    }
)
graph_builder.add_edge('report',END)

graph = graph_builder.compile()