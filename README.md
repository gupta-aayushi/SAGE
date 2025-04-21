# 🌟 SAGE: Skill Analysis and Gap Evaluation

**SAGE** is an intelligent web-based application that helps users identify relevant job opportunities and evaluate how well their skills align with those roles. It scrapes real-time job data from LinkedIn, compares it with user-uploaded resumes, and highlights skill gaps to enhance job-readiness.

---

## ✅ Key Features

- **🔎 Real-Time Job Scraping**  
  Automatically extracts job listings from LinkedIn based on user-defined roles or keywords using Selenium.

- **📝 Resume & Job Matching**  
  Calculates a compatibility score between job descriptions and the user's resume using TF-IDF and cosine similarity.

- **📉 Skill Gap Identification**  
  Identifies skills required by job postings that are missing from the user's resume.

- **📊 Ranked Job Listings**  
  Displays jobs sorted by compatibility score through an intuitive Streamlit interface.

- **📂 Multiple Resume Formats**  
  Supports PDF, DOCX, TXT, and even manual resume entry.

---

## 🧰 Tech Stack

- **Frontend**: Streamlit  
- **Backend**: Python  
- **Web Scraping**: Selenium, BeautifulSoup  
- **Natural Language Processing**: scikit-learn (TF-IDF), NLTK, cosine similarity  
- **Data Storage**: JSON  
- **Deployment**: Streamlit Cloud  
- **Security**: SHA-256 password encryption

---
