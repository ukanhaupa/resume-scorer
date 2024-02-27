import os

import pdf2image
import pytesseract
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY, max_retries=3)

JOB_DESCRIPTION = f"""Full Stack Developer

Frontend: React
Backend: Nodejs

Job Purpose: Your role will be to develop/extend/enhance complex web/mobile applications
in a collaborative environment.

Duties and responsibilities:
- Planning a new feature or planning to enhance an existing one
- Developing new features
- Enhancing the current application
- Fixing existing/new bugs
- Adding tests to the current test kit
- Write technical documentation

Qualifications:
- Degree in Computer Science or Computer Applications
- Should be a Full stack web developer
- 3+ Years Experience

Specialized knowledge:
- Single Page Applications
- Restful APIs
- Database Schema

Skills:
- Problem Solving

Frontend:
- JavaScript
- HTML/CSS + Bootstrap (or any other framework)
- Mandatory Experience In ReactJS
- Fundamentals of bundling tools like Webpack
- Chrome dev tools
- Application State Management
- Request/response interceptors
- Browser storage mechanisms

Backend:
- Mandatory Experience in NodeJS
- Conventions to build Restful APIs
- Middleware
- Database schema and queries
- Request validators
- Asynchronous Tasks
- Debugging Skills

Tools/Utilities:
- Git
- Basic knowledge of web servers like Apache or Nginx
- npm
- yarn
- Bonus Skills
- Docker
- AWS
- Firebase

Abilities:
- Should be able to write simple and modular logic.
- Should be able to perform various tests on his/her developed/modified code
- Should be able to review the code developed by peers.
"""

PROMPT = "Given the resume content:\n{resume}\n\nAnd the job description:\n{job_description}\n\nIt is mandatory to score this resume based on job description and provide the response strictly in mardown format with Score out of 10 and Information in bullet points stating, why or why not, the candidate is a good fit. Avoid hallucinating and it is mandatory to be strict with scoring. Highlight positive and negative points."


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


def main():
    st.title("Resume Screening")
    file = st.file_uploader("Upload the resume", type=["pdf"])
    if file is not None:
        text = extract_text(file)
        if text is not None:
            response = query_response(text)
            st.write(response)


if __name__ == "__main__":
    main()
