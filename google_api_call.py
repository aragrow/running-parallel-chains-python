
from flask import Flask, make_response, request, jsonify
from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnableParallel, RunnableLambda
from langchain_google_genai import ChatGoogleGenerativeAI

#from nonce_tool import NonceTool
class GoogleAPICall:

    def __init__(self):
        print('--- Exec: GoogleAPICall.__init__')
        # Create a ChatGooglePalm self.model for Google Gemini
        self.model = ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp")

        #self.nonce = NonceTool.generate_nonce()
        self.nonce = 'hello'
        self.is_debug = True

        self.resume = """DEMO RESUME
        +1 (999) 222 1111  (US) || demo@resume.me || linkedin.com/in/demoresume
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
        Business Analysis: Requirements gathering, gap analysis, process improvement, user story creation, use case self.modeling, stakeholder management
        Project Management: Project planning, execution, monitoring, and control, risk management
        Communication: Excellent written and verbal communication skills, ability to present complex information clearly and concisely
        Technical Skills: WordPress, PHP, Laravel, SQL (MySQL, MSSQL), Oracle, HTML, CSS, JavaScript, Agile methodologies, Git, Report generation tools (Jet Reports, Crystal Reports)
        Soft Skills: Analytical thinking, problem-solving, critical thinking, attention to detail, teamwork, adaptability
        Languages
        English, Spanish"""

        self.job = """
        Job Title: DEMO - Manager IT Administrator
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
    # End of __init__

    def main1(self):

        print('--- Exec: GoogleAPICall.__main__')
        html_content = f"{self.resume}"
        return html_content
    
    def main(self):
        print('--- Exec: GoogleAPICall.main')
        
        json_data = request.get_json() 
        # Convert JSON string to Python list
        if 'resume' not in json_data:
            return {"error": "Missing 'resume' in the request body"}, 400
        job = json_data['job']
        if 'job' not in json_data:
            return {"error": "Missing 'resume' in the request body"}, 400
        
        self.resume = json_data['resume']
        self.job = json_data['job']
     
        self.resume = self.modify_resume(self.resume, self.job)
        
        # Simplify branches with LCEL
        pros_branch_chain = (
            RunnableLambda(lambda x: self.create_pros('', self.resume, self.job)) | self.model | StrOutputParser()
        )

        cons_branch_chain = (
            RunnableLambda(lambda x: self.create_cons('', self.resume, self.job)) | self.model | StrOutputParser()
        )

        # Combine pros and cons into a final result
        
        '''    1.Purpose:
                Runs the pros_branch_chain and cons_branch_chain computations in parallel.

                Key Points:

                The branches are defined as a dictionary where:
                    The key (e.g., pros and cons) represents the name of the branch.
                    The value is a Runnable or chain of operations (e.g., pros_branch_chain and cons_branch_chain) that will execute.
                The output of this step will be a dictionary:
                {
                    pros: <result from pros_branch_chain>,
                    cons: <result from cons_branch_chain>
                }
            2.Purpose:
                Takes the results from the RunnableParallel step and combines them using the combine_pros_cons function.

                Key Points:

                The lambda function accepts x, the dictionary output from RunnableParallel (1):
                It accesses the pros and cons keys from x:

                x['branches'[['pros']  # Output of pros_branch_chain
                x['branches']['cons']  #Output of cons_branch_chain

                These values are passed to the combine_pros_cons function, which merges or processes them into a final result.
        '''
    
        combined_pros_cons_chain = (
            RunnableParallel(
                branches={
                    "pros": pros_branch_chain, 
                    "cons": cons_branch_chain
                }
            )
            | RunnableLambda(lambda x: self.combine_pros_cons(x))  # Access results using keys
        )

        # Generate Pros and Cons
        combined = combined_pros_cons_chain.invoke({})

        print ('<h2>------------- COVER LETTER -----------------------</h2>')
        # Create the cover letter using the pros, cons, and job description
        cover_letter_chain = (
            RunnableLambda(lambda x: ChatPromptTemplate.from_messages(
                [
                    ("system", "You are an expert recruiter creating a cover letter."),
                    ("human", f"""Given my resume: {self.resume}, job description: {self.job}, 
                                and combined feedback from pros and cons: {combined}, 
                                create a professional cover letter.
                                The output should be in HTML format."""),
                ]
            ).format_prompt())
            | self.model
            | StrOutputParser()
        )

        # Generate the Cover Letter
        cover_letter = cover_letter_chain.invoke({})


        response_array = {
            "resume": self.resume,
            "cover": cover_letter
        }

        html_content = f"{self.resume}<h2>Cover Letter</h2>{cover_letter}"
        # Create a response object and set the correct content type
        #response = make_response(html_content)
        #response.headers['Content-Type'] = 'text/html'  # Ensure the content is treated as HTML
        return html_content
    
    # End of main

    # Define pros analysis step
    def modify_resume(self, resume, job):
        if self.is_debug:
            print('[DEBUG] Executing modify_resume...')
        try:
            # Define prompt template
            prompt_template = ChatPromptTemplate.from_messages(
            [
                ("system", "You are an expert recruiter helping applicants apply for a job."),
                ("human", f"""Give my resume: {resume} and the job description: {job}. 
                                - Tailor my resume to match the job description. 
                                - create the response in HTML format that is professional and modern.
                                - Do not include Modifications Made.
                                - Return Only the HTML within <body></body>"""),
            ]
            )

            # Define the chain
            chain = (
                prompt_template
                | self.model
                | StrOutputParser()
            )

            # Execute the chain
            new_resume = chain.invoke({"resume": resume, "job": job}) 
            return new_resume
        
        except Exception as e:
            print("Error in modify_resume:", e)
            raise  # Re-raise the exception for further handling

    # End of modify resume

    # Define pros analysis step
    def create_pros(self, text, resume, job):
        if self.is_debug:
            print('[DEBUG] Executing create_pros function...')
        pros_template = ChatPromptTemplate.from_messages(
            [
                ("system", "You are an expert recruiter reviewer."),
                (
                    "human",
                    f"""Given my resume: {resume} and a job description: {job}. 
                        -list the ways that I can help the organization with my experience the job.
                        -Return the five most important points.
                        -Return HTML bulleted list.""",
                ),
            ]
        )
        return pros_template.format_prompt(text=text)
    # End of create_pros

    # Define cons analysis step
    def create_cons(self, text, resume, job):
        if self.is_debug:
            print('[DEBUG] Executing create_cons function...')
        cons_template = ChatPromptTemplate.from_messages(
            [
                ("system", "You are an expert recruiter reviewer."),
                (
                    "human",
                    f"""Given my resume: {resume} and a job description: {job}.
                        -List a plan of how can I improve my skills to help the organization with the skills that I do not have for the job.
                        -Use the first person pronoun.
                        -Return the five most important points.
                        -Return HTML bulleted list.""",
                ),
            ]
        )
        return cons_template.format_prompt(text=text)
    # End of create_cons

    # Define cover creation step
    def create_cover(self, text, resume, job, other):
        if self.is_debug:
            print('[DEBUG] Executing create_cover function...')
        cover_template = ChatPromptTemplate.from_messages(
            [
                ("system", "You are an expert recruiter creating a cover letter."),
                (
                    "human",
                    f"""Given my resume: {resume} and a job description: {job}, and the 'How can I help' and 'Improvements' {other} . 
                        -Create a professional cover letter integrating seemsless the combination of the resume, job, and other.
                        -Create the response in HTML format that is professional and modern.
                        -clReturn Only the HTML within <body></body>""",
                ),
            ]
        )
        return cover_template.format_prompt(text=text)
    #End of create_cover

    # Combine pros and cons into a final review
    def combine_pros_cons(self,x):
        if self.is_debug:
            print('[DEBUG] Executing combine_pros_cons function...')
        
        pros = x['branches']['pros']
        cons = x['branches']['pros']
        combined = f"Pros:\n{pros}\n\nCons:\n{cons}"
        return combined
    #End of combine_pros_cons