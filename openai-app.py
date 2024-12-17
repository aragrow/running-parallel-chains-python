from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnableParallel, RunnableLambda
from langchain_openai import ChatOpenAI
from flask import Flask, render_template, request, jsonify, make_response, url_for, render_template_string
from flask_restful import Resource, Api
from flask_httpauth import HTTPBasicAuth
import asyncio
import time  # Import the time module for adding delays

# Load environment variables from .env
load_dotenv()

resume = """David Arago
+1 (952) 228 1752  (US) || davidarago@aragrow.me || linkedin.com/in/davidarago
Results-oriented IT leader with over 25 years of experience driving technology transformations, aligning IT strategies with business goals, and delivering scalable solutions. Fluent in both Spanish and English at a native level, with proven expertise in overseeing IT operations, implementing automated systems, and managing cross-functional teams to enhance productivity and cost efficiency. Seeking strategic leadership roles to drive business value through innovative technology solutions.
WORK EXPERIENCE
Founder & Strategic Consultant Aragrow, US — July 2023 – Present
Led the migration of web applications to enhance security and scalability.
Provided strategic consulting in system design and business analysis, optimizing the integration of the OpenCTI platform.
Implemented modular systems that simplified data management and audit functions. 

Hubbard Broadcasting, Inc. US – Jun 2000 – July 2023 Development Team Lead
Led the integration of WordPress and ERP, including the migration to NetSuite, resulting in a significant improvement in operational efficiency.
Implemented large-scale solutions that optimized critical functions such as accounting, asset management, and permission systems.
Improved system configuration and reporting processes, reducing manual tasks and increasing operational accuracy.
Collaborated closely with the CIO, CFO, and President to align technological objectives with the strategic needs of the business, ensuring the selection of the best vendors.
EDUCATION
Oracle Database Administrator || Atrium, Spain
This course is solidifying and renewing my understanding of Oracle Database architecture and administration. 
Agile Certificate || University of Minnesota
Gained expertise in the Agile philosophy, and methodologies like Scrum, Lean, and Kanban. 
Project Management and Business Analyst Certificate || University of Minnesota
Trained in gathering and documenting business requirements and translating them into functional design specifications that can be executed by IT development teams.
Computer Programming  || Minneapolis Community College
Earned Degree in programming languages as well as relational databases like DB2 and MSSQL.
Specialist in Transportation and Commerce || Miguel Delibes, Spain
Earned Degree in custom procedures to import and export goods.
SKILLS
Business Analysis: Requirements gathering, gap analysis, process improvement, user story creation, use case modeling, stakeholder management
Project Management: Project planning, execution, monitoring, and control, risk management
Communication: Excellent written and verbal communication skills, ability to present complex information clearly and concisely
Technical Skills: WordPress, PHP, Laravel, SQL (MySQL, MSSQL), Oracle, HTML, CSS, JavaScript, Agile methodologies, Git, Report generation tools (Jet Reports, Crystal Reports)
Soft Skills: Analytical thinking, problem-solving, critical thinking, attention to detail, teamwork, adaptability
Languages
English, Spanish"""

job = """
Job Title: Manager IT Administrator
At Lifespace, team members are at the center of delivering a purpose driven experience for our residents! We provide an environment where each team member can live their aspirations, developing in their career, making a difference, and being a part of a meaningful mission. Join our IT team today as our new Manager of Community Technology.

A few details about the role:

    Handle customer expectations (both internal staff and residents) regarding IT services, identify gaps between customer needs and IT capabilities, and find innovative solutions to bridge those gaps.
    Deliver high levels of customer service with a positive, outgoing approach to service delivery.
    Provide periodic technology training sessions with staff and residents.
    Ensure the overall technical health and stability of the assigned community, including remote locations, and maintain high levels of resident and team member satisfaction.
    Coach and encourage business stakeholders on the potential use of technologies that add value to business units.
    Represent and communicate business unit management’s technology needs to the wider IT department.
    Vendor management to coordinate with key vendors to diagnose and troubleshoot complex technical issues, holding them accountable for SLAs.
    Own and facilitate timely root cause analysis for community level severity 1 and 2 outages, including follow-up communication to affected team members and/or residents.
    Coach and mentor junior team members, resident volunteers, and first level help desk support team on resolving incidents, escalating complex tickets, and communicating updates effectively.
    Gain a deep understanding of the technical infrastructure at all communities, including core applications, network connectivity, Wi-Fi capabilities, and service issues.
    Lead local project efforts for community technical improvements and contribute to enterprise-wide IT initiatives.
    Research, define, and document IT support processes and procedures, including incident management, problem management, change management, and asset management.

And here’s what you need to apply:

    Bachelor’s degree in management information systems, computer science, or business preferred.
    Five to eight years of IT infrastructure experience with demonstrated progression of skills and responsibilities.
    Advanced Professional Certification (e.g., MCDT, MCSE).
    Experience providing IT support in the healthcare industry is a plus.
    Ability and willingness to work in an environment providing 24x7x365 support to our communities.

"""

# Create a ChatOpenAI model
model = ChatOpenAI(model="gpt-4o-mini")

# Define prompt template
prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", "You are an expert recruiter helping applicants applay for a job."),
        ("human", f"""Give my resume: {resume} and the job description: {job}, 
                        - Tailor my resume to match the job description. 
                        - create the response in HTML format that is professional and modern.
                        - Do not include Modifications Made.
                        - Return Only the htmi within <body></body>"""),
    ]
)

# Create the combined chain using LangChain Expression Language (LCEL)
chain = (
    prompt_template
    | model
    | StrOutputParser()
)
new_resume = chain.invoke({"resume": resume, "job": job})
print (new_resume)

# Define pros analysis step
def create_pros(text, resume, job):
    pros_template = ChatPromptTemplate.from_messages(
        [
            ("system", "You are an expert recruiter reviewer."),
            (
                "human",
                f"""Given my resume: {resume} and a job description: {job}, 
                list the ways that I can help the organization with my experience the job.
                Use the first person pronoun.
                Return HTML bulleted list.""",
            ),
        ]
    )
    return pros_template.format_prompt(text=text, resume=resume, job=job)


# Define cons analysis step
def create_cons(text, resume, job):
    cons_template = ChatPromptTemplate.from_messages(
        [
            ("system", "You are an expert recruiter reviewer."),
            (
                "human",
                f"""Given my resume: {resume} and a job description: {job}, 
                    list a plan of how can I improve my skills to help the organization with the skills that I do not have for the job.
                    Use the first person pronoun.
                    Return the five most important points.
                    Return HTML bulleted list.""",
            ),
        ]
    )
    return cons_template.format_prompt(text=text, resume=resume, job=job)


# Define cover creation step
def create_cover(resume, job, pros, cons):
    cover_template = ChatPromptTemplate.from_messages(
        [
            ("system", "You are an expert recruiter creating a cover letter."),
            (
                "human",
                f"Given my resume: {resume} and a job description: {job}, create a professional cover letter based on the pros and cons: {pros} and {cons}.",
            ),
        ]
    )
    return cover_template.format_prompt(resume=resume, job=job, pros=pros, cons=cons)


# Combine pros and cons into a final review
def combine_pros_cons(pros, cons):
    return f"Pros:\n{pros}\n\nCons:\n{cons}"

# Simplify branches with LCEL
pros_branch_chain = (
    RunnableLambda(lambda x: create_pros('', resume, job)) | model | StrOutputParser()
)


cons_branch_chain = (
    RunnableLambda(lambda x: create_cons('', resume, job)) | model | StrOutputParser()
)

# Run the combined pros and cons chain with a 10-second delay
time.sleep(20)  # Add a 10-second delay

# Combine pros and cons into a final result
combined_pros_cons_chain = (
    RunnableParallel(branches={"pros": pros_branch_chain, "cons": cons_branch_chain})
    | RunnableLambda(lambda x: combine_pros_cons(x["branches"]["pros"], x["branches"]["cons"]))
)

print ('------------------------------------')
result = combined_pros_cons_chain.invoke({})
print (result)
print ('------------------------------------')

'''
# Create the cover letter using the pros, cons, and job description
cover_letter_chain = (
    RunnableLambda(lambda x: create_cover(new_resume, job, x["pros"], x["cons"])) | model | StrOutputParser()
)

# Create the combined chain using LangChain Expression Language (LCEL)
final_chain = (
    combined_pros_cons_chain
    | cover_letter_chain
)


# Run the chain
result = final_chain.invoke({})

print("Updated Resume:\n", new_resume)
print("\nCover Letter:\n", result)

'''

'''
# Define pros analysis step
def create_pros(text, resume, job):
    pros_template = ChatPromptTemplate.from_messages(
        [
            ("system", "You are an expert recruiter reviewer."),
            (
                "human",
                f"Given my resume : {resume} and a job description: {job}, list the ways that my skills can help the organization.",
            ),
        ]
    )
    return pros_template.format_prompt(text=text)


# Define cons analysis step
def create_cons(text, resume, job):
    cons_template = ChatPromptTemplate.from_messages(
        [
            ("system", "You are an expert recruiter reviewer."),
            (
                "human",
                f"Given my resume : {resume} and a job description: {job}, list the ways that I can improve my skills to help the organization.",
            ),
        ]
    )
    return cons_template.format_prompt(text=text)

# Define cons analysis step
def create_cover(text, resume, job):
    cons_template = ChatPromptTemplate.from_messages(
        [
            ("system", "You are an expert recruiter reviewer."),
            (
                "human",
                f"Given my resume : {resume} and a job description: {job}, list the ways that I can improve my skills to help the organization.",
            ),
        ]
    )
    return cons_template.format_prompt(text=text)

# Combine pros and cons into a final review
def combine_pros_cons(pros, cons):
    return f"Pros:\n{pros}\n\nCons:\n{cons}"


# Simplify branches with LCEL
pros_branch_chain = (
    RunnableLambda(lambda x: create_pros('', resume, job)) | model | StrOutputParser()
)

cons_branch_chain = (
    RunnableLambda(lambda x: create_cons(('', resume, job))) | model | StrOutputParser()
)

cover_branch_chain = (
    RunnableLambda(lambda x: create_cover(('', job, pros_branch_chain, cons_branch_chain))) | model | StrOutputParser()
)

# Create the combined chain using LangChain Expression Language (LCEL)
chain = (
    prompt_template
    | model
    | StrOutputParser()
    | RunnableParallel(branches={"pros": pros_branch_chain, "cons": cons_branch_chain})
    | RunnableLambda(lambda x: combine_pros_cons(x["branches"]["pros"], x["branches"]["cons"]))
)

# Run the chain
result = chain.invoke({})

# Output
print(result)

'''