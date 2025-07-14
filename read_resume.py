import pdfplumber
import re

# STEP 1: Read resume PDF
def extract_text_from_pdf(pdf_path):
    all_text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            all_text += page.extract_text() + "\n"
    return all_text

# STEP 2: Extract skills
skill_keywords = [
    'python', 'java', 'c++', 'excel', 'sql', 'power bi', 'machine learning',
    'deep learning', 'matplotlib', 'pandas', 'numpy', 'tensorflow',
    'html', 'css', 'javascript', 'git', 'github', 'linux', 'mathematica'
]

def extract_skills(resume_text):
    resume_text = resume_text.lower()
    found_skills = []
    for skill in skill_keywords:
        if re.search(r'\b' + re.escape(skill) + r'\b', resume_text):
            found_skills.append(skill)
    return found_skills

# STEP 3: Sample job roles
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

# STEP 4: Match resume skills with jobs
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

# STEP 5: Run the full process
resume_text = extract_text_from_pdf("resume.pdf")
matched_skills = extract_skills(resume_text)

print("\n📋 ✅ Skills found in your resume:", matched_skills)

results = match_jobs(matched_skills, job_roles)

for job in results:
    print(f"\n🔍 Job: {job['title']}")
    print(f"✅ Match: {job['match_percent']}%")
    print(f"✅ You have: {job['matched_skills']}")
    print(f"❌ Missing: {job['missing_skills']}")
