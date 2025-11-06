import streamlit as st
from pathlib import Path

# Configure page
st.set_page_config(
    page_title="AI Interview System | Enterprise Recruitment Platform",
    page_icon="👨🏻‍💼",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Professional CSS with modern design
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
        padding: 3rem 2rem 2rem 2rem;
        max-width: 1400px;
    }
    
    .hero-section {
        text-align: center;
        padding: 4rem 2rem;
        background: rgba(255, 255, 255, 0.98);
        border-radius: 24px;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
        margin-bottom: 3rem;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.3);
    }
    
    .logo-icon {
        font-size: 4rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        filter: drop-shadow(0 4px 8px rgba(102, 126, 234, 0.3));
    }
    
    .main-title {
        font-size: 3.5rem;
        font-weight: 800;
        color: #1e293b;
        margin-bottom: 1rem;
        letter-spacing: -1px;
        line-height: 1.2;
    }
    
    .subtitle {
        font-size: 1.3rem;
        color: #64748b;
        font-weight: 400;
        margin-bottom: 2rem;
        max-width: 700px;
        margin-left: auto;
        margin-right: auto;
        line-height: 1.6;
    }
    
    .trust-badges {
        display: flex;
        justify-content: center;
        gap: 2rem;
        margin-top: 2rem;
        flex-wrap: wrap;
    }
    
    .badge {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.75rem 1.5rem;
        background: #f8fafc;
        border-radius: 50px;
        font-size: 0.9rem;
        color: #475569;
        font-weight: 500;
        border: 1px solid #e2e8f0;
    }
    
    .portal-card {
        background: white;
        border-radius: 20px;
        padding: 3rem;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        border: 2px solid transparent;
        position: relative;
        overflow: hidden;
        margin-bottom: 2rem;
    }
    
    .portal-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 6px;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        transform: scaleX(0);
        transition: transform 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .portal-card:hover::before {
        transform: scaleX(1);
    }
    
    .portal-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 20px 60px rgba(102, 126, 234, 0.25);
        border-color: rgba(102, 126, 234, 0.3);
    }
    
    .portal-header {
        display: flex;
        align-items: center;
        gap: 1.5rem;
        margin-bottom: 2rem;
    }
    
    .portal-icon {
        font-size: 4rem;
        width: 90px;
        height: 90px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 20px;
        flex-shrink: 0;
    }
    
    .candidate-icon {
        background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%);
    }
    
    .company-icon {
        background: linear-gradient(135deg, #f093fb15 0%, #f5576c15 100%);
    }
    
    .portal-title {
        font-size: 2rem;
        font-weight: 700;
        color: #1e293b;
        margin-bottom: 0.5rem;
    }
    
    .portal-subtitle {
        font-size: 1rem;
        color: #64748b;
        font-weight: 400;
    }
    
    .feature-list {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 1rem;
        margin: 2rem 0;
    }
    
    .feature-box {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        padding: 1rem;
        background: #f8fafc;
        border-radius: 12px;
        font-size: 0.95rem;
        color: #475569;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .feature-box:hover {
        background: #f1f5f9;
        transform: translateX(5px);
    }
    
    .stButton > button {
        width: 100%;
        height: 60px;
        font-size: 1.1rem;
        font-weight: 600;
        border-radius: 14px;
        border: none;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        text-transform: none;
        letter-spacing: 0.3px;
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
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        box-shadow: 0 8px 24px rgba(240, 147, 251, 0.4);
    }
    
    .stButton > button[kind="secondary"]:hover {
        box-shadow: 0 12px 32px rgba(240, 147, 251, 0.5);
        transform: translateY(-2px);
    }
    
    .stats-section {
        background: white;
        border-radius: 20px;
        padding: 3rem;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.08);
        margin-bottom: 3rem;
    }
    
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 2rem;
        margin-top: 2rem;
    }
    
    .stat-card {
        text-align: center;
        padding: 1.5rem;
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
        border-radius: 16px;
        border: 1px solid #e2e8f0;
    }
    
    .stat-number {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    
    .stat-label {
        font-size: 0.95rem;
        color: #64748b;
        font-weight: 500;
    }
    
    .footer-section {
        background: white;
        border-radius: 20px;
        padding: 2.5rem;
        text-align: center;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.08);
    }
    
    .tech-stack {
        display: flex;
        justify-content: center;
        gap: 2rem;
        flex-wrap: wrap;
        margin-top: 1.5rem;
    }
    
    .tech-badge {
        padding: 0.75rem 1.5rem;
        background: linear-gradient(135deg, #667eea10 0%, #764ba210 100%);
        border-radius: 50px;
        color: #667eea;
        font-weight: 600;
        font-size: 0.9rem;
        border: 1px solid #667eea30;
    }
    
    .footer-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #1e293b;
        margin-bottom: 1rem;
    }
    
    .footer-text {
        color: #64748b;
        font-size: 1rem;
        line-height: 1.6;
    }
    
    @media (max-width: 768px) {
        .main-title {
            font-size: 2.5rem;
        }
        .feature-list {
            grid-template-columns: 1fr;
        }
        .stats-grid {
            grid-template-columns: 1fr;
        }
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Hero Section
st.markdown('<div class="hero-section">', unsafe_allow_html=True)
st.markdown('<div class="logo-icon" style="color:black;">👨🏻‍💼</div>', unsafe_allow_html=True)
st.markdown('<h1 class="main-title">HireX : AI-Powered Interview System</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle" style="color:black;">Next-generation technical recruitment platform powered by adaptive AI agents. Conduct intelligent, dynamic interviews that assess true candidate potential.</p>', unsafe_allow_html=True)

# Trust badges
st.markdown("""
<div class="trust-badges">
    <div class="badge"><span style="font-size:1.2rem">⚡</span> Lightning Fast</div>
    <div class="badge"><span style="font-size:1.2rem">🔒</span> Enterprise Security</div>
    <div class="badge"><span style="font-size:1.2rem">🎯</span> 95% Accuracy</div>
    <div class="badge"><span style="font-size:1.2rem">🌐</span> Cloud-Based</div>
</div>
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Portal Cards
col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown('<div class="portal-card">', unsafe_allow_html=True)
    st.markdown("""
    <div class="portal-header">
        <div class="portal-icon candidate-icon">👨‍💼</div>
        <div>
            <div class="portal-title">Candidate Portal</div>
            <div class="portal-subtitle" style="color:black;">Begin your AI interview journey</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="feature-list">', unsafe_allow_html=True)
    features_candidate = [
        ("🧠", "Adaptive AI Questioning"),
        ("📊", "Technical Depth Analysis"),
        ("⚡", "Real-Time Follow-ups"),
        ("🎯", "10 Dynamic Questions"),
        ("💬", "Natural Conversation"),
        ("📝", "Instant Feedback")
    ]
    
    for icon, text in features_candidate:
        st.markdown(f'<div class="feature-box"><span style="font-size:1.2rem;color:#667eea">{icon}</span><span>{text}</span></div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("🚀 Start Interview", type="primary", use_container_width=True, key="candidate"):
        st.switch_page("pages/1_🎯_Candidate_Portal.py")

with col2:
    st.markdown('<div class="portal-card">', unsafe_allow_html=True)
    st.markdown("""
    <div class="portal-header">
        <div class="portal-icon company-icon">🏢</div>
        <div>
            <div class="portal-title">Company Dashboard</div>
            <div class="portal-subtitle" style="color:black;">Enterprise recruitment management</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="feature-list">', unsafe_allow_html=True)
    features_company = [
        ("📊", "Analytics Dashboard"),
        ("📄", "Detailed Reports"),
        ("⬇️", "PDF Export"),
        ("🎯", "Performance Metrics"),
        ("👥", "Candidate Comparison"),
        ("🔍", "Deep Insights")
    ]
    
    for icon, text in features_company:
        st.markdown(f'<div class="feature-box"><span style="font-size:1.2rem;color:#667eea">{icon}</span><span>{text}</span></div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("📊 Access Dashboard", type="secondary", use_container_width=True, key="company"):
        st.switch_page("pages/2_🏢_Company_Portal.py")

# Stats Section
st.markdown("""
<div class="stats-section">
    <div class="footer-title">Trusted by Leading Organizations</div>
    <div class="stats-grid">
        <div class="stat-card">
            <div class="stat-number">10K+</div>
            <div class="stat-label">Interviews Conducted</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">95%</div>
            <div class="stat-label">Accuracy Rate</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">500+</div>
            <div class="stat-label">Companies</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">50%</div>
            <div class="stat-label">Time Saved</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer-section">
    <div class="footer-title">Powered by Cutting-Edge Technology</div>
    <p class="footer-text">Built with enterprise-grade AI infrastructure for reliable, scalable recruitment</p>
    <div class="tech-stack">
        <div class="tech-badge">🚀 Groq API</div>
        <div class="tech-badge">🔗 LangChain</div>
        <div class="tech-badge">📊 LangGraph</div>
        <div class="tech-badge">⚡ Streamlit</div>
    </div>
</div>
""", unsafe_allow_html=True)