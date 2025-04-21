import streamlit as st
import time
import pandas as pd
from utils import extract_text_from_file
from scraper import detect_job_cards_with_description
from resume_matcher import ResumeMatcher
from ui_components import apply_custom_styles, render_job_card

# Page configuration
st.set_page_config(
    page_title="SAGE - Skill Analysis & Gap Evaluation",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom styles
def apply_custom_styles():
    st.markdown("""
    <style>
        :root {
            --primary: #3A59D1;
            --secondary: #3D90D7;
            --accent: #7AC6D2;
            --highlight: #B5FCCD;
            --background: #f8f9fa;
            --card-bg: white;
            --text: black;
            --success: #28a745;
            --warning: #ffc107;
            --danger: #dc3545;
        }
        
        body {
            background-color: var(--background);
            color: var(--text);
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        
        .main-header {
            background: linear-gradient(90deg, var(--primary), var(--secondary));
            color: white;
            text-align: center;
            font-size: 2.5rem;
            margin-bottom: 1rem;
            padding: 1rem;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }
        
        .section-header {
            color: var(--primary);
            font-size: 1.5rem;
            font-weight: 600;
            margin-bottom: 1rem;
            padding: 0.5rem 0;
            border-bottom: 2px solid var(--accent);
        }
        
        .stButton>button {
            background-color: var(--primary);
            color: white;
            border: none;
            padding: 0.5rem 1rem;
            border-radius: 8px;
            font-weight: 600;
            transition: all 0.3s ease;
            width: 100%;
        }
        
        .stButton>button:hover {
            background-color: var(--secondary);
            transform: translateY(-2px);
            color: white;    
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        
        .stTextInput>div>div>input, .stTextArea>div>div>textarea {
            border: 1px solid var(--accent);
            border-radius: 8px;
            padding: 0.5rem;
        }
        
        .job-card {
            color: black;    
            background-color: var(--card-bg);
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            border-left: 5px solid var(--accent);
        }
        
        .job-title {
            color: black;
            font-size: 1.3rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
        }
        
        .company-name {
            color: black;
            font-size: 1.1rem;
            font-weight: 600;
            margin-bottom: 0.5rem;
        }
        
        .match-score {
            font-size: 1.2rem;
            font-weight: 700;
            margin: 1rem 0;
        }
        
        .high-match {
            color: var(--success);
        }
        
        .medium-match {
            color: var(--warning);
        }
        
        .low-match {
            color: var(--danger);
        }
        
        .skill-chip {
            display: inline-block;
            padding: 0.25rem 0.75rem;
            margin: 0.25rem;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 500;
        }
        
        .matched-skill {
            background-color: var(--highlight);
            color: #155724;
        }
        
        .missing-skill {
            background-color: #f8d7da;
            color: #721c24;
        }
        
        .stExpander .stExpanderHeader {
            background-color: var(--accent);
            color: white;
            border-radius: 8px 8px 0 0;
            padding: 0.75rem 1rem;
        }
        
        .stExpander .stExpanderContent {
            background-color: var(--card-bg);
            border-radius: 0 0 8px 8px;
            padding: 1rem;
            border: 1px solid #dee2e6;
        }
        
        .stTabs [data-baseweb="tab-list"] {
            gap: 10px;
        }
        
        .stTabs [data-baseweb="tab"] {
            background-color: var(--danger);
            border-radius: 8px 8px 0 0;
            padding: 0.5rem 1.5rem;
            transition: all 0.3s ease;
        }
        
        .stTabs [aria-selected="true"] {
            background-color: var(--primary);
            color: white;
        }
        
        footer {
            text-align: center;
            padding: 1rem;
            color: var(--primary);
            font-size: 0.9rem;
        }
        
        /* Fix for search button column */
        [data-testid="column"] {
            align-items: flex-start;
        }
    </style>
    """, unsafe_allow_html=True)

apply_custom_styles()

# Header with new title and logo
st.markdown("""
<div style="text-align: center; margin-bottom: 2rem;">
    <h1 class='main-header'>🧠 SAGE - Skill Analysis & Gap Evaluation</h1>
    <p style="font-size: 1.1rem; color: var(--secondary);">Intelligent Job Matching with Resume Analysis</p>
</div>
""", unsafe_allow_html=True)

# Create two columns for search parameters
col1, col2 = st.columns([2, 1])

with col1:
    # Job search parameters
    st.markdown("<div class='section-header'>🔎 Job Search Parameters</div>", unsafe_allow_html=True)
    keyword = st.text_input("Enter job title or keyword:", placeholder="e.g., Web Developer, Data Scientist")
    
    # Additional filters in an expander
    with st.expander("🔧 Advanced Search Options", expanded=False):
        location = st.text_input("Location:", placeholder="e.g., New York, Remote")
        experience_level = st.multiselect(
            "Experience Level:",
            ["Entry level", "Associate", "Mid-Senior level", "Director", "Executive"],
            default=None
        )
        job_type = st.multiselect(
            "Job Type:",
            ["Full-time", "Part-time", "Contract", "Temporary", "Internship"],
            default=["Full-time"]
        )

with col2:
    st.markdown("<div class='section-header'>📄 Resume Analysis</div>", unsafe_allow_html=True)
    
    upload_option = st.radio("Choose resume input method:", ("Upload File", "Paste Text"), horizontal=True)
    
    resume_text = ""
    if upload_option == "Upload File":
        resume_file = st.file_uploader("Upload your resume", type=["pdf", "docx", "txt"])
        
        if resume_file is not None:
            file_details = {"Filename": resume_file.name, "FileType": resume_file.type, "FileSize": f"{resume_file.size / 1024:.2f} KB"}
            st.write(file_details)
            
            try:
                resume_text = extract_text_from_file(resume_file)
                st.success("✅ Resume successfully processed!")
            except Exception as e:
                st.error(f"❌ Error processing file: {str(e)}")
    else:
        resume_text = st.text_area("Paste your resume text:", height=200, placeholder="Copy and paste your resume here...")

# Fixed search button alignment
search_col1, search_col2 = st.columns([2, 1])
with search_col1:
    if st.button("🔍 Search Jobs", use_container_width=True):
        st.session_state.search_clicked = True
    else:
        st.session_state.search_clicked = False

if st.session_state.get('search_clicked', False):
    if keyword.strip():
        with st.spinner("🔍 Fetching and analyzing job listings... This may take a moment."):
            # Calling scraper
            job_listings = detect_job_cards_with_description(keyword)
            
            if job_listings:
                # Resume matcher
                for job in job_listings:
                    if resume_text:
                        matcher = ResumeMatcher(job["description"])
                        match_result = matcher.match_resume(resume_text)
                        job["similarity_score"] = match_result["similarity_score"]
                        job["missing_skills"] = match_result["missing_skills"]
                        job["matched_skills"] = match_result.get("matched_skills", [])
                    else:
                        job["similarity_score"] = 0
                        job["missing_skills"] = []
                        job["matched_skills"] = []
                
                # Sorting by % match
                if resume_text:
                    job_listings.sort(key=lambda x: x["similarity_score"], reverse=True)
                
                st.markdown(f"<div class='section-header'>📊 Results: Found {len(job_listings)} Job Listings</div>", unsafe_allow_html=True)
                tab1, tab2 = st.tabs(["Card View", "Table View"])
                
                with tab1:
                    for idx, job in enumerate(job_listings):
                        render_job_card(job, idx, resume_text)
                
                with tab2:
                    job_df = pd.DataFrame(job_listings)
                    if "similarity_score" in job_df.columns:
                        job_df["match_percentage"] = job_df["similarity_score"].apply(lambda x: f"{x:.0%}")
                    
                    display_cols = ["title", "company"]
                    if resume_text:
                        display_cols.append("match_percentage")
                    
                    st.dataframe(
                        job_df[display_cols],
                        use_container_width=True,
                        column_config={
                            "title": "Job Title",
                            "company": "Company",
                            "match_percentage": st.column_config.ProgressColumn(
                                "Match Score",
                                format="%f",
                                min_value=0,
                                max_value=1
                            )
                        }
                    )
            else:
                st.warning("⚠️ No jobs found matching your search criteria. Try broadening your search.")
    else:
        st.error("⚠️ Please enter a valid job keyword to start your search.")

# Enhanced Footer
st.markdown("""
<footer>
    <div style="padding: 1.5rem; background-color: #f0f4f8; border-radius: 12px; margin-top: 2rem;">
        <p style="font-weight: 600; color: var(--primary); margin-bottom: 0.5rem;">🧠 SAGE - Skill Analysis & Gap Evaluation</p>
        <p style="font-size: 0.9rem; margin-bottom: 0.5rem; color: var(--secondary);">Built with ❤️ using Streamlit | Data sourced from LinkedIn</p>
        <p style="font-size: 0.8rem; color: var(--text);">Use this tool responsibly and in accordance with LinkedIn's terms of service.</p>
    </div>
</footer>
""", unsafe_allow_html=True)