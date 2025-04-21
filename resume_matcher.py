import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


SKILL_SET = [
    # Technical Skills
    "Python", "Java", "JavaScript", "C++", "C#", "Ruby", "Go", "Rust", "Swift", "Kotlin",
    "SQL", "NoSQL", "Database Design", "Data Modeling", "ETL", "Data Warehousing",
    "HTML/CSS", "React", "Angular", "Vue.js", "Node.js", "Django", "Flask", "Spring",
    "REST APIs", "GraphQL", "Microservices", "Docker", "Kubernetes", "CI/CD",
    "AWS", "Azure", "GCP", "Cloud Architecture", "DevOps", "Terraform",
    "Machine Learning", "Deep Learning", "NLP", "Computer Vision", "Data Science",
    "Big Data", "Hadoop", "Spark", "PySpark", "Pandas", "NumPy", "TensorFlow", "PyTorch",
    "Cybersecurity", "Ethical Hacking", "Penetration Testing", "Network Security",
    
    # Business & Management
    "Business Analysis", "Process Improvement", "Lean Six Sigma", "Agile Methodologies",
    "Scrum", "Kanban", "SAFe", "Product Ownership", "UX/UI Design", "Prototyping",
    "Market Research", "Competitive Analysis", "Financial Modeling", "Risk Management",
    "Investment Banking", "Mergers & Acquisitions", "Venture Capital", "Private Equity",
    "Corporate Finance", "Financial Reporting", "Taxation", "Auditing", "Compliance",
    "Regulatory Affairs", "Corporate Governance", "Stakeholder Management",
    
    # Creative & Design
    "Graphic Design", "Illustration", "Motion Graphics", "3D Modeling", "Animation",
    "Video Editing", "Photography", "Videography", "Sound Design", "Game Design",
    "UI/UX Design", "Interaction Design", "User Research", "Wireframing", "Figma",
    "Adobe Creative Suite", "Photoshop", "Illustrator", "InDesign", "Premiere Pro",
    
    # Healthcare & Science
    "Clinical Research", "Biostatistics", "Epidemiology", "Public Health",
    "Pharmaceuticals", "Medical Devices", "Healthcare IT", "HIPAA Compliance",
    "Biotechnology", "Genomics", "Bioinformatics", "Chemistry", "Physics",
    "Environmental Science", "Geology", "Meteorology",
    
    # Soft Skills
    "Leadership", "Team Management", "Conflict Resolution", "Negotiation",
    "Public Speaking", "Presentation Skills", "Storytelling", "Emotional Intelligence",
    "Critical Thinking", "Problem Solving", "Decision Making", "Time Management",
    "Adaptability", "Creativity", "Collaboration", "Mentoring", "Coaching",
    
    # Industry-Specific
    "Supply Chain Optimization", "Logistics", "Inventory Management", "Procurement",
    "Retail Management", "E-commerce", "Digital Marketing", "SEO/SEM", "PPC",
    "Content Marketing", "Social Media Marketing", "Email Marketing", "Marketing Analytics",
    "Brand Management", "Event Planning", "Hospitality Management", "Tourism",
    "Real Estate", "Urban Planning", "Architecture", "Construction Management",
    "Education Technology", "Curriculum Development", "Instructional Design",
    "Nonprofit Management", "Grant Writing", "Fundraising", "Public Policy",
    "International Relations", "Journalism", "Technical Writing", "Translation"
]

class ResumeMatcher:
    def __init__(self, job_description):
        self.job_description = job_description
        self.vectorizer = TfidfVectorizer(stop_words="english")
        self.job_tfidf = self.vectorizer.fit_transform([job_description])
    
    def match_resume(self, resume_text):
        if not resume_text.strip():
            return {"similarity_score": 0.0, "missing_skills": [], "matched_skills": []}
        
        resume_tfidf = self.vectorizer.transform([resume_text])
        similarity = cosine_similarity(self.job_tfidf, resume_tfidf)[0][0]
        
        job_skills = self.extract_skills(self.job_description)
        resume_skills = self.extract_skills(resume_text)
        
        missing_skills = job_skills - resume_skills
        matched_skills = job_skills.intersection(resume_skills)
        
        return {
            "similarity_score": similarity,
            "missing_skills": list(missing_skills),
            "matched_skills": list(matched_skills)  # Added matched_skills to the return dictionary
        }
    
    @staticmethod
    def extract_skills(text):
        text = text.lower()
        return {skill.lower() for skill in SKILL_SET if skill.lower() in text}