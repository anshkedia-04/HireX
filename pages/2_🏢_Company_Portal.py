import streamlit as st
from datetime import datetime
import os
import tempfile
from utils.database import InterviewDatabase
from utils.pdf_generator import InterviewPDFGenerator

# Page config
st.set_page_config(
    page_title="Company Portal | AI Interview System",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize DB and PDF generator
if 'db' not in st.session_state:
    st.session_state.db = InterviewDatabase()

pdf_generator = InterviewPDFGenerator()

# Reuse visual theme similar to Candidate Portal
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    * { font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; }

    /* Page background */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 0;
    }

    /* Header Card */
    .header-card {
        background: white;
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 10px 40px rgba(0,0,0,0.08);
        margin-bottom: 1.5rem;
        display:flex;
        align-items:center;
        justify-content:space-between;
        gap:1rem;
    }
    .header-left {
        display:flex;
        align-items:center;
        gap:1rem;
    }
    .header-icon{ font-size:3rem; }
    .header-title{ font-size:1.8rem; font-weight:800; color:#1e293b; margin:0; }
    .header-sub{ color:#64748b; margin:0; }

    /* Metric Cards */
    .metrics-row { display:flex; gap:1rem; margin-bottom:1.5rem; }
    .metric-card {
        background: white;
        border-radius: 16px;
        padding: 1.25rem;
        box-shadow: 0 8px 30px rgba(0,0,0,0.05);
        flex:1;
        text-align:center;
    }
    .metric-value { font-size:2rem; font-weight:800; color:#667eea; }
    .metric-label { color:#64748b; margin-top:0.5rem; }

    /* Interview Card */
    .interview-card {
        background: white;
        border-radius: 16px;
        padding: 1.25rem;
        box-shadow: 0 8px 30px rgba(0,0,0,0.04);
        margin-bottom: 1rem;
        border-left: 6px solid #667eea;
    }
    .interview-meta { display:flex; gap:1rem; align-items:center; flex-wrap:wrap; }
    .interview-name { font-size:1.15rem; font-weight:700; color:#0f172a; margin:0; }
    .interview-sub { color:#64748b; margin:0; font-size:0.95rem; }

    /* Controls */
    .controls { display:flex; gap:1rem; align-items:center; margin-bottom:1rem; }
    .search-input { flex:1; }

    /* Buttons */
    .btn { border-radius:10px; padding:0.5rem 0.85rem; font-weight:600; }
    .primary-btn { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color:white; border:none; }
    .secondary-btn { background:white; color:#667eea; border:2px solid #667eea; }

    /* Expander contents */
    .qa-pair { padding: 0.75rem 0; border-bottom: 1px dashed #e6edf8; }
    .qa-q { font-weight:700; color:#0f172a; margin-bottom:0.35rem; }
    .qa-a { color:#475569; margin:0; white-space:pre-wrap; }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    @media (max-width: 768px) {
        .metrics-row { flex-direction: column; }
        .controls { flex-direction: column; align-items:flex-start; }
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="header-card">
    <div class="header-left">
        <div class="header-icon">🏢</div>
        <div>
            <div class="header-title">Company Dashboard</div>
            <div class="header-sub">Interview management & reports — review candidate interviews and export PDFs</div>
        </div>
    </div>
    <div>
        <div style="text-align:right; color:#64748b; font-size:0.95rem;">
            <div>Last updated: {}</div>
        </div>
    </div>
</div>
""".format(datetime.now().strftime("%B %d, %Y %I:%M %p")), unsafe_allow_html=True)

# Fetch interviews
interviews = st.session_state.db.get_all_interviews() or []

# Metrics
total = len(interviews)
completed = len([i for i in interviews if i.get('status') == 'completed'])
today_count = len([i for i in interviews if datetime.fromisoformat(i['timestamp']).date() == datetime.now().date()])

st.markdown(f"""
<div class="metrics-row">
    <div class="metric-card">
        <div class="metric-value">{total}</div>
        <div class="metric-label">Total Interviews</div>
    </div>
    <div class="metric-card">
        <div class="metric-value">{completed}</div>
        <div class="metric-label">Completed Interviews</div>
    </div>
    <div class="metric-card">
        <div class="metric-value">{today_count}</div>
        <div class="metric-label">Today's Interviews</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Controls: search + filters + refresh
st.markdown('<div class="controls">', unsafe_allow_html=True)
search_term = st.text_input("🔍 Search by candidate name or ID", key="company_search", placeholder="Type candidate name or interview id...", help="Search interviews")
status_filter = st.selectbox("Status", options=["All", "completed", "in-progress"], index=0, key="status_filter")
if st.button("🔄 Refresh"):
    st.experimental_rerun()
st.markdown('</div>', unsafe_allow_html=True)

# Apply filters
filtered = interviews
if search_term:
    filtered = [
        i for i in filtered
        if search_term.lower() in i.get('candidate_name','').lower()
        or search_term.lower() in i.get('interview_id','').lower()
    ]

if status_filter != "All":
    filtered = [i for i in filtered if i.get('status') == status_filter]

st.markdown(f"**Showing {len(filtered)} of {len(interviews)} interviews**")
st.markdown("")

# Display interviews list
if not filtered:
    st.info("📭 No interviews found. Candidates can take interviews from the Candidate Portal.")
else:
    for interview in filtered:
        # Card header
        st.markdown(f"""
        <div class="interview-card">
            <div class="interview-meta">
                <div style="min-width:220px;">
                    <p class="interview-name">👤 {interview.get('candidate_name','—')}</p>
                    <p class="interview-sub"><strong>ID:</strong> {interview.get('interview_id','—')} &nbsp; • &nbsp; <strong>Date:</strong> {datetime.fromisoformat(interview['timestamp']).strftime('%b %d, %Y')}</p>
                </div>
                <div style="flex:1;">
                    <p class="interview-sub"><strong>Intro:</strong> {interview.get('introduction','—')[:250]}{'' if len(interview.get('introduction',''))<=250 else '...'}</p>
                </div>
                <div style="min-width:170px; text-align:right;">
                    <p class="interview-sub"><strong>Answered:</strong> {len(interview.get('qa_pairs',[]))} / 10</p>
                    <p class="interview-sub"><strong>Status:</strong> {interview.get('status','in-progress')}</p>
                </div>
            </div>
        """, unsafe_allow_html=True)

        # Actions and expander
        cols = st.columns([3,2,1])
        with cols[0]:
            with st.expander("👁️ View interview details"):
                st.markdown("<div style='margin-top:0.5rem;'>", unsafe_allow_html=True)
                st.markdown("**Full Introduction:**")
                st.write(interview.get('introduction','—'))
                st.markdown("---")
                for qa in interview.get('qa_pairs', []):
                    st.markdown(f"""
                    <div class="qa-pair">
                        <div class="qa-q">Q{qa['question_number']}: {qa['question']}</div>
                        <div class="qa-a">{qa['answer']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

        with cols[1]:
            # PDF generation & download
            try:
                btn_label = f"📥 Generate PDF"
                if st.button(btn_label, key=f"pdf_{interview['interview_id']}"):
                    # Create temporary PDF file
                    tmpdir = tempfile.gettempdir()
                    safe_name = f"{interview['interview_id']}_{interview.get('candidate_name','candidate').replace(' ','_')}.pdf"
                    tmp_path = os.path.join(tmpdir, safe_name)

                    # Generate PDF
                    pdf_generator.generate_pdf(interview, tmp_path)

                    # Provide download
                    with open(tmp_path, "rb") as f:
                        st.download_button(
                            label="💾 Download PDF",
                            data=f,
                            file_name=safe_name,
                            mime="application/pdf",
                            key=f"save_{interview['interview_id']}"
                        )

                    # Remove temp file after offering download
                    try:
                        os.remove(tmp_path)
                    except Exception:
                        pass

            except Exception as e:
                st.error(f"❌ Failed to generate PDF: {e}")

        with cols[2]:
            # Delete interview
            if st.button("🗑️ Delete", key=f"del_{interview['interview_id']}", use_container_width=True):
                if st.session_state.db.delete_interview(interview['interview_id']):
                    st.success("✅ Interview deleted")
                    st.experimental_rerun()
                else:
                    st.error("❌ Could not delete interview")

        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("---", unsafe_allow_html=True)

# Footer area: quick stats + export all (optional)
st.markdown("""
<div style="display:flex; gap:1rem; align-items:center; margin-top:1rem;">
    <div style="flex:1;">
        <small style="color:black;">Tip: Use the search and status filter to quickly find candidate reports. Click 'Generate PDF' to export a candidate summary.</small>
    </div>
</div>
""", unsafe_allow_html=True)

# Back to home
st.markdown("---")
if st.button("🔙 Back to Home"):
    st.switch_page("app.py")
