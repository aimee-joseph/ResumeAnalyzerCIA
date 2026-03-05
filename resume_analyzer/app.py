import streamlit as st
from pathlib import Path
from utils.resume_parser import extract_text_from_resume
from utils.text_cleaner import clean_text
from utils.skill_extractor import load_skills, extract_skills
from utils.matcher import match_skills, evaluate_experience

st.set_page_config(page_title = "Resume Analyzer", page_icon = "📜", layout = "wide")

st.title("Resume Analyzer and Job Matcher Tool")
st.subheader("Check how well your resume matches a job description.")
st.markdown("---")

message_placeholder = st.empty()

st.sidebar.header("Input Details")
uploaded_resume = st.sidebar.file_uploader("Upload your resume (PDF format)", type = ["pdf"])
job_description = st.sidebar.text_area("Paste the job description ...", height = 200)
# target_role = st.sidebar.selectbox("Select the target role", ["Software Engineer", "Data Analyst", "ML Engineer", "Web Developer"])
experience_level = st.sidebar.radio("Experience level: ", ["Fresher", "1 - 3 Years", "3+ Years"])
analyze_button = st.sidebar.button("Analyze my resume")

resume_uploaded = uploaded_resume is not None
jd_provided = job_description.strip() != ""

invalid_file = False
if resume_uploaded:
    if not uploaded_resume.name.lower().endswith(".pdf"):
        invalid_file = True

message_type = None
message_text = None

if not analyze_button:
    if not resume_uploaded and not jd_provided:
        message_type = "info"
        message_text = "Please upload your resume and paste the job description to begin."
    elif resume_uploaded and not jd_provided:
        message_type = "warning"
        message_text = "Resume uploaded. Please paste a job description."
    elif not resume_uploaded and jd_provided:
        message_type = "warning"
        message_text = "Job description provided. Please upload a resume."
else:
    if not resume_uploaded and not jd_provided:
        message_type = "warning"
        message_text = "Please upload your resume and paste the job description."
    elif resume_uploaded and not jd_provided:
        message_type = "warning"
        message_text = "Resume uploaded. Please paste a job description."
    elif resume_uploaded and invalid_file:
        message_type = "error"
        message_text = "Invalid file type. Please upload your resume in PDF format only."
    elif not resume_uploaded and jd_provided:
        message_type = "warning"
        message_text = "Job description provided. Please upload a resume."
    else:
        message_type = "success"
        message_text = "Resume and job description received successfully!"

if message_type == "info":
    message_placeholder.info(message_text)
elif message_type == "warning":
    message_placeholder.warning(message_text)
elif message_type == "error":
    message_placeholder.error(message_text)
elif message_type == "success":
    message_placeholder.success(message_text)

if analyze_button and resume_uploaded and jd_provided and not invalid_file:
    try:
        resume_text = extract_text_from_resume(uploaded_resume)
        # with st.expander("Preview extracted resume text"):
        #     st.text(resume_text[:3000])
        clean_resume_text = clean_text(resume_text)
        clean_jd_text = clean_text(job_description)

        BASE_DIR = Path(__file__).resolve().parent
        SKILLS_PATH = BASE_DIR / "data" / "skills_list.txt"

        skills_db = load_skills(SKILLS_PATH)

        resume_skills = extract_skills(clean_resume_text, skills_db)
        jd_skills = extract_skills(clean_jd_text, skills_db)

        results = match_skills(resume_skills, jd_skills)

        st.markdown("---")
        st.success("Analysis completed successfully!")

        st.metric(label = "Resume Match %", value = f"{results["match_percentage"]}%")
        st.progress(results["match_percentage"]/100)

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Matched Skills")
            if results["matched_skills"]:
                st.table(sorted(results["matched_skills"]))
            else:
                st.info("No matching skills found.")

        with col2:
            st.subheader("Missing Skills")
            if results["missing_skills"]:
                st.table(sorted(results["missing_skills"]))
            else:
                st.info("No missing skills.")
    except Exception as e:
        st.error(str(e))

    st.markdown("---")
    st.subheader("Experience Fit Assessment")
    experience_feedback = evaluate_experience(experience_level, job_description)
    st.info(experience_feedback)
