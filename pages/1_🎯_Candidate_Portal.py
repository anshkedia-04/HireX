import streamlit as st
from datetime import datetime
import uuid
from utils.interview_agent import InterviewAgent
from utils.database import InterviewDatabase

# Page config
st.set_page_config(
    page_title="Candidate Portal | AI Interview System",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize session state
if 'interview_started' not in st.session_state:
    st.session_state.interview_started = False
if 'interview_state' not in st.session_state:
    st.session_state.interview_state = None
if 'agent' not in st.session_state:
    st.session_state.agent = None
if 'db' not in st.session_state:
    st.session_state.db = InterviewDatabase()
if 'interview_id' not in st.session_state:
    st.session_state.interview_id = None

# Professional CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 0;
    }
    
    .block-container {
        padding: 2rem;
        max-width: 1200px;
    }
    
    /* Header Card */
    .header-card {
        background: white;
        border-radius: 20px;
        padding: 2.5rem;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
        margin-bottom: 2rem;
        text-align: center;
    }
    
    .header-icon {
        font-size: 3.5rem;
        margin-bottom: 1rem;
    }
    
    .header-title {
        font-size: 2.5rem;
        font-weight: 800;
        color: #1e293b;
        margin-bottom: 0.5rem;
    }
    
    .header-subtitle {
        font-size: 1.1rem;
        color: #64748b;
        font-weight: 400;
    }
    
    /* Welcome Card */
    .welcome-card {
        background: white;
        border-radius: 20px;
        padding: 3rem;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
        margin-bottom: 2rem;
    }
    
    .welcome-title {
        font-size: 2rem;
        font-weight: 700;
        color: #1e293b;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    
    .info-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }
    
    .info-box {
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
        padding: 1.5rem;
        border-radius: 16px;
        border: 1px solid #e2e8f0;
        transition: all 0.3s ease;
    }
    
    .info-box:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 24px rgba(102, 126, 234, 0.15);
    }
    
    .info-icon {
        font-size: 2rem;
        margin-bottom: 0.5rem;
    }
    
    .info-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #1e293b;
        margin-bottom: 0.5rem;
    }
    
    .info-text {
        font-size: 0.95rem;
        color: #64748b;
        line-height: 1.5;
    }
    
    /* Form Card */
    .form-card {
        background: white;
        border-radius: 20px;
        padding: 3rem;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
        margin-bottom: 2rem;
    }
    
    .form-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #1e293b;
        margin-bottom: 2rem;
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    
    /* Question Card */
    .question-card {
        background: white;
        border-radius: 20px;
        padding: 3rem;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
        margin-bottom: 2rem;
        border-left: 6px solid #667eea;
    }
    
    .question-header {
        display: flex;
        align-items: center;
        gap: 1rem;
        margin-bottom: 1.5rem;
    }
    
    .question-number {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        width: 50px;
        height: 50px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.3rem;
        font-weight: 700;
        flex-shrink: 0;
    }
    
    .question-label {
        font-size: 1.1rem;
        font-weight: 600;
        color: #64748b;
    }
    
    .question-text {
        font-size: 1.3rem;
        font-weight: 600;
        color: #1e293b;
        line-height: 1.6;
        margin-bottom: 2rem;
    }
    
    /* Progress Bar */
    .progress-container {
        background: white;
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
        margin-bottom: 2rem;
    }
    
    .progress-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1rem;
    }
    
    .progress-title {
        font-size: 1.2rem;
        font-weight: 700;
        color: #1e293b;
    }
    
    .progress-count {
        font-size: 1.1rem;
        font-weight: 600;
        color: #667eea;
    }
    
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        height: 12px;
        border-radius: 6px;
    }
    
    /* Completion Card */
    .completion-card {
        background: white;
        border-radius: 20px;
        padding: 4rem;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .completion-icon {
        font-size: 5rem;
        margin-bottom: 1.5rem;
        animation: bounce 1s ease-in-out;
    }
    
    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-20px); }
    }
    
    .completion-title {
        font-size: 2.5rem;
        font-weight: 800;
        color: #1e293b;
        margin-bottom: 1rem;
    }
    
    .completion-text {
        font-size: 1.2rem;
        color: #64748b;
        margin-bottom: 2rem;
        line-height: 1.6;
    }
    
    .interview-id-box {
        background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%);
        padding: 1.5rem;
        border-radius: 16px;
        margin: 2rem auto;
        max-width: 500px;
        border: 2px solid #667eea30;
    }
    
    .interview-id-label {
        font-size: 0.9rem;
        color: #64748b;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    .interview-id {
        font-size: 1.5rem;
        font-weight: 700;
        color: #667eea;
        letter-spacing: 1px;
    }
    
    /* Review Card */
    .review-card {
        background: #f8fafc;
        border-radius: 16px;
        padding: 2rem;
        margin-bottom: 1.5rem;
        border: 1px solid #e2e8f0;
    }
    
    .review-question {
        font-size: 1.1rem;
        font-weight: 600;
        color: #1e293b;
        margin-bottom: 1rem;
    }
    
    .review-answer {
        font-size: 1rem;
        color: #475569;
        line-height: 1.6;
        padding-left: 1rem;
        border-left: 3px solid #667eea;
    }
    
    /* Input Styling */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        border-radius: 12px;
        border: 2px solid #e2e8f0;
        padding: 1rem;
        font-size: 1rem;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Button Styling */
    .stButton > button {
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        border: none;
    }
    
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        box-shadow: 0 8px 24px rgba(102, 126, 234, 0.4);
    }
    
    .stButton > button[kind="primary"]:hover {
        box-shadow: 0 12px 32px rgba(102, 126, 234, 0.5);
        transform: translateY(-2px);
    }
    
    .stButton > button[kind="secondary"] {
        background: white;
        color: #667eea;
        border: 2px solid #667eea;
    }
    
    .stButton > button[kind="secondary"]:hover {
        background: #667eea;
        color: white;
    }
    
    /* Alert Styling */
    .stAlert {
        border-radius: 12px;
        border: none;
        padding: 1rem 1.5rem;
    }
    
    /* Expander Styling */
    .streamlit-expanderHeader {
        background: #f8fafc;
        border-radius: 12px;
        padding: 1rem 1.5rem;
        font-weight: 600;
        color: #1e293b;
        border: 1px solid #e2e8f0;
    }
    
    /* Hide Streamlit Elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    @media (max-width: 768px) {
        .header-title {
            font-size: 2rem;
        }
        .info-grid {
            grid-template-columns: 1fr;
        }
        .completion-title {
            font-size: 2rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="header-card">
    <div class="header-icon">🎯</div>
    <div class="header-title">Candidate Interview Portal</div>
    <div class="header-subtitle">AI-Powered Adaptive Technical Assessment</div>
</div>
""", unsafe_allow_html=True)

# Main interview flow
if not st.session_state.interview_started:
    # Welcome Section
    st.markdown("""
    <div class="welcome-card">
        <div class="welcome-title">
            <span style="font-size:2.5rem">👋</span>
            <span>Welcome to Your AI Interview</span>
        </div>
        <p style="font-size:1.1rem; color:#64748b; line-height:1.8;">
            This intelligent interview system adapts to your responses in real-time, providing a personalized 
            assessment experience. Our AI interviewer will ask 10 carefully crafted questions based on your 
            technical background and answers.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Information boxes
    st.markdown('<div class="info-grid">', unsafe_allow_html=True)
    
    info_items = [
        ("⏱️", "Duration", "Approximately 20-30 minutes"),
        ("🎯", "Questions", "10 adaptive questions"),
        ("🤖", "AI-Powered", "Real-time question generation"),
        ("📊", "Evaluation", "Comprehensive skill assessment")
    ]
    
    for icon, title, text in info_items:
        st.markdown(f"""
        <div class="info-box">
            <div class="info-icon">{icon}</div>
            <div class="info-title">{title}</div>
            <div class="info-text">{text}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Candidate Information Form
    st.markdown('<div class="form-card">', unsafe_allow_html=True)
    st.markdown('<div class="form-title"><span style="font-size:1.5rem">📝</span><span>Candidate Information</span></div>', unsafe_allow_html=True)
    
    with st.form("candidate_info_form"):
        st.markdown("##### Personal Details")
        candidate_name = st.text_input(
            "Full Name *",
            placeholder="Enter your full name (e.g., John Doe)",
            help="Your complete name as you'd like it to appear"
        )
        
        st.markdown("")
        st.markdown("##### Technical Profile")
        introduction = st.text_area(
            "Professional Introduction *",
            placeholder="Share your technical expertise, programming languages, frameworks, projects, and professional experience...\n\nExample: I'm a Full Stack Developer with 3+ years of experience in React, Node.js, and Python. I've worked on e-commerce platforms and have expertise in cloud deployment using AWS...",
            height=250,
            help="Provide a comprehensive overview of your technical skills, experience, and areas of expertise (minimum 20 words)"
        )
        
        st.markdown("")
        col1, col2 = st.columns([3, 1])
        
        with col2:
            submit_button = st.form_submit_button("🚀 Begin Interview", type="primary", use_container_width=True)
        
        if submit_button:
            if not candidate_name or not introduction:
                st.error("❌ Please complete all required fields to proceed")
            elif len(introduction.split()) < 20:
                st.error("❌ Please provide a more detailed introduction (minimum 20 words). This helps us tailor questions to your background.")
            else:
                with st.spinner("🔄 Initializing your personalized interview..."):
                    # Initialize interview
                    st.session_state.agent = InterviewAgent()
                    st.session_state.interview_state = st.session_state.agent.initialize_state(
                        candidate_name=candidate_name,
                        introduction=introduction
                    )
                    st.session_state.interview_id = f"INT_{uuid.uuid4().hex[:8].upper()}"
                    st.session_state.interview_started = True
                    st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

else:
    # Interview in progress
    state = st.session_state.interview_state
    
    # Check if interview is complete
    if state['question_count'] >= 10:
        # Save interview to database
        interview_data = {
            'interview_id': st.session_state.interview_id,
            'candidate_name': state['candidate_name'],
            'introduction': state['introduction'],
            'qa_pairs': state['qa_pairs'],
            'timestamp': datetime.now().isoformat(),
            'status': 'completed'
        }
        
        st.session_state.db.save_interview(interview_data)
        
        # Completion Screen
        st.markdown("""
        <div class="completion-card">
            <div class="completion-icon">🎉</div>
            <div class="completion-title">Interview Completed!</div>
            <p class="completion-text">
                Congratulations <strong>{}</strong>! You've successfully completed your AI interview.<br>
                Your responses have been recorded and will be reviewed by our team.
            </p>
            <div class="interview-id-box">
                <div class="interview-id-label">Your Interview Reference ID</div>
                <div class="interview-id">{}</div>
            </div>
            <p style="color:#64748b; margin-top:1.5rem;">
                Please save this ID for your records. You can use it to track your application status.
            </p>
        </div>
        """.format(state['candidate_name'], st.session_state.interview_id), unsafe_allow_html=True)
        
        st.success("✅ Your interview has been successfully submitted to the hiring team!")
        
        # Interview Summary
        with st.expander("📊 View Complete Interview Summary", expanded=False):
            st.markdown(f"**Total Questions Answered:** {len(state['qa_pairs'])}")
            st.markdown("---")
            
            for idx, qa in enumerate(state['qa_pairs'], 1):
                st.markdown(f"""
                <div class="review-card">
                    <div class="review-question">
                        <strong>Question {idx}:</strong> {qa['question']}
                    </div>
                    <div class="review-answer">
                        {qa['answer']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        # Action buttons
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🏠 Return to Home", type="primary", use_container_width=True):
                # Reset session
                st.session_state.interview_started = False
                st.session_state.interview_state = None
                st.session_state.agent = None
                st.session_state.interview_id = None
                st.switch_page("app.py")
    
    else:
        # Progress Display
        progress = state['question_count'] / 10
        st.markdown("""
        <div class="progress-container">
            <div class="progress-header">
                <div class="progress-title">Interview Progress</div>
                <div class="progress-count">Question {} of 10</div>
            </div>
        """.format(state['question_count'] + 1), unsafe_allow_html=True)
        st.progress(progress)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Generate question if needed
        if not state['current_question']:
            with st.spinner("🤔 AI is analyzing your profile and generating the next question..."):
                question = st.session_state.agent.get_next_question(state)
                state['current_question'] = question
        
        # Display current question
        st.markdown(f"""
        <div class="question-card">
            <div class="question-header">
                <div class="question-number">Q{state['question_count'] + 1}</div>
                <div class="question-label">Question {state['question_count'] + 1} of 10</div>
            </div>
            <div class="question-text">{state['current_question']}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Answer form
        with st.form(f"answer_form_{state['question_count']}", clear_on_submit=True):
            st.markdown("##### Your Response")
            answer = st.text_area(
                "Type your answer here",
                placeholder="Provide a detailed and thoughtful answer. Be specific and include relevant examples from your experience...",
                height=200,
                key=f"answer_{state['question_count']}",
                label_visibility="collapsed"
            )
            
            col1, col2 = st.columns([3, 1])
            with col2:
                submitted = st.form_submit_button("➡️ Submit Answer", type="primary", use_container_width=True)
            
            if submitted:
                if not answer or len(answer.strip()) < 10:
                    st.error("❌ Please provide a more detailed answer (minimum 10 characters)")
                else:
                    with st.spinner("💾 Saving your response..."):
                        # Add answer to state
                        st.session_state.interview_state = st.session_state.agent.add_answer(state, answer)
                        st.session_state.interview_state['current_question'] = ''
                        st.success("✅ Answer recorded successfully!")
                        st.rerun()
        
        # Previous Q&A Review
        if state['qa_pairs']:
            with st.expander(f"📝 Review Previous Questions ({len(state['qa_pairs'])} answered)"):
                for idx, qa in enumerate(state['qa_pairs'], 1):
                    st.markdown(f"""
                    <div class="review-card">
                        <div class="review-question">
                            <strong>Q{idx}:</strong> {qa['question']}
                        </div>
                        <div class="review-answer">
                            {qa['answer']}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

# Footer navigation
st.markdown("---")
col1, col2, col3 = st.columns([1, 2, 1])
with col1:
    if st.button("🔙 Back to Home", use_container_width=True):
        st.switch_page("app.py")