import streamlit as st
import pdfplumber
import re

# Skill keywords
skill_keywords = [
    'python', 'java', 'c++', 'excel', 'sql', 'power bi', 'machine learning',
    'deep learning', 'matplotlib', 'pandas', 'numpy', 'tensorflow',
    'html', 'css', 'javascript', 'git', 'github', 'linux', 'mathematica'
]

# Job role templates
job_roles = [
    {
        "title": "Data Analyst",
        "required_skills": ['python', 'sql', 'excel', 'power bi']
    },
    {
        "title": "Machine Learning Engineer",
        "required_skills": ['python', 'numpy', 'pandas', 'scikit-learn', 'tensorflow']
    },
    {
        "title": "Web Developer",
        "required_skills": ['html', 'css', 'javascript', 'git', 'github']
    }
]

# Extract text from PDF
def extract_text_from_pdf(file):
    all_text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            all_text += page.extract_text() + "\n"
    return all_text

# Extract skills
def extract_skills(resume_text):
    resume_text = resume_text.lower()
    found_skills = []
    for skill in skill_keywords:
        if re.search(r'\b' + re.escape(skill) + r'\b', resume_text):
            found_skills.append(skill)
    return found_skills

# Match job roles
def match_jobs(resume_skills, job_roles):
    job_matches = []
    for job in job_roles:
        required = set(job['required_skills'])
        have = set(resume_skills)
        matched = required & have
        missing = required - have
        match_percent = int(len(matched) / len(required) * 100)
        job_matches.append({
            'title': job['title'],
            'matched_skills': list(matched),
            'missing_skills': list(missing),
            'match_percent': match_percent
        })
    return job_matches

# Streamlit app layout
st.set_page_config(page_title="AI Resume Job Matcher", layout="centered")
st.title("🤖 AI Resume Skill Matcher")

uploaded_file = st.file_uploader("📄 Upload your Resume (PDF only)", type="pdf")

if uploaded_file is not None:
    with st.spinner("🔍 Reading your resume..."):
        text = extract_text_from_pdf(uploaded_file)
        skills = extract_skills(text)
        matches = match_jobs(skills, job_roles)

    st.subheader("✅ Skills Detected:")
    st.write(skills)

    st.subheader("📊 Job Match Results:")
    for job in matches:
        st.markdown(f"### 🔍 {job['title']}")
        st.progress(job['match_percent'] / 100)
        st.write(f"**✅ You have:** {job['matched_skills']}")
        st.write(f"**❌ Missing:** {job['missing_skills']}")
