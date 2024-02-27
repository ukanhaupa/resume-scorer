import os

import pdf2image
import pytesseract
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY, max_retries=10)

JOB_DESCRIPTION = "Software Engineer with 5 years of experience in Python and Java..."
PROMPT = "Given the resume content:\n{resume}\n\nAnd the job description:\n{job_description}\n\nScore this resume and provide feedback: "


def extract_text(file):
    if file.type == "application/pdf":
        images = pdf2image.convert_from_bytes(file.getvalue())
        text = ""
        for img in images:
            text += pytesseract.image_to_string(img)
    else:
        st.error("Invalid file type. Please upload pdf file.")
        return None
    return text


def query_response(resume):
    retry_count = 0
    while retry_count < 2:
        try:
            messages = [
                {
                    "role": "system",
                    "content": PROMPT.format(
                        job_description=JOB_DESCRIPTION, resume=resume
                    ),
                },
            ]
            response = client.chat.completions.create(
                model="gpt-3.5-turbo-1106", messages=messages, temperature=0.5
            )
            return response.choices[0].message.content
        except Exception as e:
            print(str(e))
            retry_count += 1


def score_resume(text):
    feedback = query_response(text)
    if "good fit" in feedback.lower():
        final_decision = "Take Forward"
    else:
        final_decision = "Reject"
    return feedback, final_decision


def main():
    st.title("Resume Scorer")
    file = st.file_uploader("Upload your resume", type=["pdf"])
    if file is not None:
        text = extract_text(file)
        if text is not None:
            feedback, decision = score_resume(text)
            st.write("Feedback:", feedback)
            st.write("Final Decision:", decision)


if __name__ == "__main__":
    main()
