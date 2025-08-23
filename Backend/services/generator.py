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
