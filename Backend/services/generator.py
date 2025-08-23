from openai import OpenAI
import os

# Make sure your OpenAI API key is set as an environment variable
# Example (PowerShell):
# $env:OPENAI_API_KEY = "your_api_key_here"

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_hiring_report(candidate_info: dict, job_description: str) -> str:
    """
    Generates a hiring report using System and User prompts.
    
    candidate_info: dict with keys like name, skills, experience, etc.
    job_description: str describing the role
    """
    
    # ✅ System Prompt - defines the AI's role and behavior
    system_prompt = (
        "You are an expert HR analyst. Your job is to evaluate job candidates "
        "and produce detailed, professional hiring reports. Your analysis should "
        "cover skills match, strengths, weaknesses, and hiring recommendations."
    )
    
    # ✅ User Prompt - contains the candidate info & job description
    user_prompt = (
        f"Job Description:\n{job_description}\n\n"
        f"Candidate Information:\n{candidate_info}\n\n"
        "Please provide a structured hiring report with:\n"
        "1. Candidate Overview\n"
        "2. Skills Match Analysis\n"
        "3. Strengths\n"
        "4. Weaknesses\n"
        "5. Recommendation"
    )
    
    # ✅ Send prompts to LLM
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # Or another model of your choice
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.7,  # creativity level
        max_tokens=800
    )
    
    # Return the LLM's output
    return response.choices[0].message.content.strip()

def generate_zero_shot(candidate_data: str, job_description: str) -> str:
    """
    Zero-shot: only system + user prompt, no examples.
    """
    user_prompt = f"""
    Candidate Information:
    {candidate_data}

    Job Description:
    {job_description}

    Task: Generate a hiring insights report.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.7
    )
    return response.choices[0].message.content

def generate_one_shot(candidate_data: str, job_description: str) -> str:
    """
    One-shot: provide one example before the actual task.
    """
    example_job = "Software Engineer role requiring Python, APIs, teamwork."
    example_candidate = {"name": "Alex", "skills": ["Python", "APIs"], "experience": "2 years"}
    example_output = """
    Candidate Overview: Alex, 2 years of experience.
    Skills Match: Strong in Python & APIs.
    Strengths: Technical foundation, fast learner.
    Weaknesses: Limited leadership experience.
    Recommendation: Suitable for junior developer role.
    """

    user_prompt = f"""
    Example:
    Job Description: {example_job}
    Candidate: {example_candidate}
    Expected Hiring Report: {example_output}

    Now generate a hiring report for:

    Job Description: {job_description}
    Candidate: {candidate_data}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.7
    )
    return response.choices[0].message.content.strip()


def generate_multi_shot(candidate_data: str, job_description: str) -> str:
    """
    Multi-shot: provide multiple examples before the actual task.
    """
    examples = [
        {
            "job": "Data Analyst role with SQL, Excel, BI tools.",
            "candidate": {"name": "Maria", "skills": ["Excel", "SQL"], "experience": "3 years"},
            "report": "Overview: Maria, 3 years of experience.\n"
                      "Skills Match: Strong in SQL & Excel.\n"
                      "Strengths: Detail-oriented, analytical.\n"
                      "Weaknesses: Limited BI exposure.\n"
                      "Recommendation: Good fit with some training."
        },
        {
            "job": "Marketing Manager role needing strategy & leadership.",
            "candidate": {"name": "John", "skills": ["Strategy", "Leadership"], "experience": "6 years"},
            "report": "Overview: John, 6 years of marketing experience.\n"
                      "Skills Match: Strong alignment.\n"
                      "Strengths: Leadership, vision.\n"
                      "Weaknesses: Needs more digital marketing exposure.\n"
                      "Recommendation: Strong candidate."
        }
    ]

    examples_text = "\n\n".join(
        f"Example:\nJob: {ex['job']}\nCandidate: {ex['candidate']}\nReport: {ex['report']}"
        for ex in examples
    )

    user_prompt = f"""
    {examples_text}

    Now generate a hiring report for:

    Job Description: {job_description}
    Candidate: {candidate_data}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.7
    )
    return response.choices[0].message.content.strip()