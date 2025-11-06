import os
from typing import Dict
from datetime import datetime

from langchain_groq import ChatGroq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class InterviewAgent:
    """Agentic AI Interview System using LangChain with Groq"""
    
    def __init__(self):
        # Initialize Groq LLM
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables. Please add it to your .env file.")
        
        self.llm = ChatGroq(
            api_key=api_key,
            model_name="llama-3.1-70b-versatile",
            temperature=0.7,
            max_tokens=500
        )
    
    def initialize_state(self, candidate_name: str, introduction: str) -> Dict:
        """Initialize the interview state"""
        return {
            'candidate_name': candidate_name,
            'introduction': introduction,
            'question_count': 0,
            'qa_pairs': [],
            'current_question': '',
            'interview_complete': False
        }
    
    def get_next_question(self, state: Dict) -> str:
        """Generate the next interview question based on context"""
        question_num = state['question_count'] + 1
        
        if question_num == 1:
            prompt = f"""You are an expert technical interviewer. 
The candidate has introduced themselves as: "{state['introduction']}"

Based on this introduction, ask ONE specific, technical follow-up question that:
1. Probes deeper into their claimed expertise
2. Tests their practical knowledge
3. Is clear and answerable in 2-3 sentences

Ask ONLY the question, nothing else."""
        
        else:
            recent_qa = state['qa_pairs'][-1] if state['qa_pairs'] else {}
            previous_question = recent_qa.get('question', '')
            previous_answer = recent_qa.get('answer', '')
            
            prompt = f"""You are an expert technical interviewer conducting question {question_num} of 10.

Previous question: {previous_question}
Candidate's answer: {previous_answer}

Based on their answer, ask ONE follow-up question that:
1. Digs deeper into their response
2. Tests practical understanding
3. Explores related technical concepts
4. Is progressively more challenging

Ask ONLY the question, nothing else. Be conversational but professional."""
        
        try:
            response = self.llm.invoke(prompt)
            question = response.content.strip()
        except Exception as e:
            print(f"Error generating question: {e}")
            question = f"Could you elaborate more on your experience with the technologies you mentioned?"
        
        state['current_question'] = question
        state['question_count'] = question_num
        
        return question
    
    def add_answer(self, state: Dict, answer: str) -> Dict:
        """Add answer to state and prepare for next question"""
        qa_pair = {
            'question_number': state['question_count'],
            'question': state['current_question'],
            'answer': answer,
            'timestamp': datetime.now().isoformat()
        }
        state['qa_pairs'].append(qa_pair)
        
        if state['question_count'] >= 10:
            state['interview_complete'] = True
        
        return state
