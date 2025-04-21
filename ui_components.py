import streamlit as st

def apply_custom_styles():
    """Apply custom CSS styling to the Streamlit app"""
    st.markdown("""
    <style>
    :root {
        --primary: #3A59D1;
        --secondary: #3D90D7;
        --accent: #7AC6D2;
        --highlight: #B5FCCD;
        --background: #f8f9fa;
        --card-bg: #3D9D07;
        --text-dark: #333333;
        --text-medium: #666666;
        --success: #28a745;
        --warning: #ffc107;
        --danger: #dc3545;
    }
    
    /* Layout fixes */
    .stApp {
        overflow-x: hidden;
    }
    
    [data-testid="column"] {
        align-items: flex-start;
        padding: 0 12px;
    }
    
    /* Header styles */
    .main-header {
        background: linear-gradient(90deg, var(--primary), var(--secondary));
        color: white;
        text-align: center;
        font-size: 2.5rem;
        margin-bottom: 1.5rem;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    
    .section-header {
        color: var(--primary);
        font-size: 1.5rem;
        font-weight: 600;
        margin: 1.5rem 0 1rem 0;
        padding: 0.5rem 0;
        border-bottom: 2px solid var(--accent);
    }
    
    /* Form elements */
    .stTextInput>div>div>input, 
    .stTextArea>div>div>textarea {
        border: 1px solid var(--accent) !important;
        border-radius: 8px !important;
        padding: 10px !important;
    }
    
    .stButton>button {
        background-color: var(--primary) !important;
        color: white !important;
        border: none !important;
        padding: 0.75rem 1.25rem !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        width: 100% !important;
        max-width: 100% !important;
        margin: 0 !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton>button:hover {
        background-color: var(--secondary) !important;
        transform: translateY(-2px) !important;
        color: white;        
        box-shadow: 0 4px 8px rgba(0,0,0,0.1) !important;
    }
    
    /* Job cards */
    .job-card {
        background-color: var(--card-bg) !important;
        border-radius: 12px !important;
        padding: 1.5rem !important;
        margin-bottom: 1.5rem !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1) !important;
        border-left: 5px solid var(--accent) !important;
        color: var(--text-dark) !important;
    }
    
    .job-title {
        color: var(--primary) !important;
        font-size: 1.3rem !important;
        font-weight: 700 !important;
        margin-bottom: 0.5rem !important;
    }
    
    .company-name {
        color: var(--secondary) !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        margin-bottom: 0.25rem !important;
    }
    
    .job-location {
        color: var(--text-medium) !important;
        font-size: 0.9rem !important;
        margin-bottom: 0.75rem !important;
    }
    
    /* Match scores */
    .match-score {
        font-size: 1.1rem !important;
        font-weight: 700 !important;
        margin: 0.5rem 0 !important;
    }
    
    .high-match {
        color: var(--success) !important;
    }
    
    .medium-match {
        color: var(--warning) !important;
    }
    
    .low-match {
        color: var(--danger) !important;
    }
    
    /* Skill chips */
    .skill-chip {
        display: inline-block !important;
        padding: 0.25rem 0.75rem !important;
        margin: 0.25rem !important;
        border-radius: 20px !important;
        font-size: 0.85rem !important;
        font-weight: 500 !important;
    }
    
    .matched-skill {
        background-color: var(--highlight) !important;
        color: #155724 !important;
    }
    
    .missing-skill {
        background-color: #f8d7da !important;
        color: #721c24 !important;
    }
    
    /* Footer */
    footer {
        text-align: center !important;
        padding: 1.5rem !important;
        margin-top: 2rem !important;
        background-color: #f0f4f8 !important;
        border-radius: 12px !important;
    }
    </style>
    """, unsafe_allow_html=True)

def render_job_card(job, idx, resume_text=""):
    """
    Render a job listing as a card
    
    Args:
        job (dict): Job listing information
        idx (int): Index for unique keys
        resume_text (str): Resume text if provided
    """
    with st.container():
        st.markdown(f"""
        <div class='job-card'>
            <h3 class='job-title'>{job.get("title", "No title")}</h3>
            <p class='company-name'>🏢 {job.get("company", "Company not specified")}</p>
            <p class='job-location'>📍 {job.get("location", "Location not specified")}</p>
        </div>
        """, unsafe_allow_html=True)
        
        score = job.get("similarity_score", 0)
        score_class = "high-match" if score >= 0.7 else "medium-match" if score >= 0.4 else "low-match"
        
        col1, col2 = st.columns([1, 1])
        with col1:
            if resume_text:
                st.markdown(f"<p class='match-score {score_class}'>📊 Match Score: {score:.0%}</p>", unsafe_allow_html=True)
        with col2:
            st.button(f"Apply Now", key=f"apply_{idx}", use_container_width=True)
        
        with st.expander("📖 View Job Description"):
            st.write(job.get("description", "No description available"))
        
        if resume_text:
            skill_col1, skill_col2 = st.columns(2)
            
            with skill_col1:
                if job.get("matched_skills"):
                    st.markdown("✅ **Matched Skills:**")
                    st.markdown("<div style='margin-top:0.5rem;'>" + 
                        "".join([f"<span class='skill-chip matched-skill'>{skill}</span>" 
                                for skill in job["matched_skills"]]) + 
                        "</div>", unsafe_allow_html=True)
                else:
                    st.info("No skill matches found")
                    
            with skill_col2:
                if job.get("missing_skills"):
                    st.markdown("⚠️ **Skills to Develop:**")
                    st.markdown("<div style='margin-top:0.5rem;'>" + 
                        "".join([f"<span class='skill-chip missing-skill'>{skill}</span>" 
                                for skill in job["missing_skills"]]) + 
                        "</div>", unsafe_allow_html=True)
                else:
                    st.success("You match all required skills!")
        
        st.markdown("---")