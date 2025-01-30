import re
import os
import g4f
import json
import ollama
import openai
import google.generativeai as genai

from g4f.client import Client
from termcolor import colored
from dotenv import load_dotenv
from typing import Tuple, List

# Load environment variables
load_dotenv("../.env")

# Set environment variables
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
openai.api_key = OPENAI_API_KEY
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)

def generate_response(prompt: str, ai_model: str) -> str:
    """
    Generate a response using the specified AI model.

    Args:
        prompt (str): The input prompt for the AI model.
        ai_model (str): The AI model to use for generation.

    Returns:
        str: The generated response from the AI model.
    """
    if ai_model == 'g4f':
        client = Client()
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            provider=g4f.Provider.You, 
            messages=[{"role": "user", "content": prompt}],
        ).choices[0].message.content

    elif ai_model in ["gpt3.5-turbo", "gpt4"]:
        model_name = "gpt-3.5-turbo" if ai_model == "gpt3.5-turbo" else "gpt-4-1106-preview"
        response = openai.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
        ).choices[0].message.content

    elif ai_model == "llama3" or ai_model == "llama3.1":
        response = ollama.generate(
            model=ai_model,
            prompt=prompt,
        )
        response_content = response.get("response", "")

    elif ai_model == 'gemmini':
        model = genai.GenerativeModel('gemini-pro')
        response_model = model.generate_content(prompt)
        response_content = response_model.text

    else:
        raise ValueError("Invalid AI model selected.")

    return response_content

def generate_script(video_subject: str, paragraph_number: int, ai_model: str, voice: str, custom_prompt: str = None) -> str:
    """
    Generate a script for a video based on the subject, number of paragraphs, and AI model.

    Args:
        video_subject (str): The subject of the video.
        paragraph_number (int): The number of paragraphs to generate.
        ai_model (str): The AI model to use for generation.
        voice (str): The language or voice tone for the script.
        custom_prompt (str): An optional custom prompt to override the default one.

    Returns:
        str: The generated script for the video.
    """
    if custom_prompt:
        prompt = custom_prompt
    else:
        prompt = """
            Generate a script for a video based on the subject.

            The script should contain the specified number of paragraphs.
            Do not reference this prompt or any instructions in the response.
            Write the script in the specified language.

            YOU MUST NOT INCLUDE ANY TYPE OF MARKDOWN OR FORMATTING IN THE SCRIPT.
            ONLY RETURN THE RAW CONTENT OF THE SCRIPT.
        """

    prompt += f"\n\nSubject: {video_subject}\nNumber of paragraphs: {paragraph_number}\nLanguage: {voice}"

    response = generate_response(prompt, ai_model)

    if response:
        response = response.replace("*", "").replace("#", "")
        response = re.sub(r"\[.*\]", "", response)
        response = re.sub(r"\(.*\)", "", response)
        paragraphs = response.split("\n\n")
        selected_paragraphs = paragraphs[:paragraph_number]
        final_script = "\n\n".join(selected_paragraphs)
        print(colored(f"Number of paragraphs used: {len(selected_paragraphs)}", "green"))
        return final_script
    else:
        print(colored("[-] GPT returned an empty response.", "red"))
        return None

def get_search_terms(video_subject: str, amount: int, script: str, ai_model: str) -> List[str]:
    """
    Generate search terms for stock videos based on the video subject.

    Args:
        video_subject (str): The subject of the video.
        amount (int): The number of search terms to generate.
        script (str): The script of the video.
        ai_model (str): The AI model to use for generation.

    Returns:
        List[str]: A list of search terms for the video subject.
    """
    prompt = f"""
    Generate {amount} search terms for stock videos based on the subject of a video.
    Subject: {video_subject}

    Return the search terms as a JSON array of strings.
    Each search term should consist of 1-3 words and relate to the main subject.

    Here is the full text for context:
    {script}
    """

    response = generate_response(prompt, ai_model)
    print(response)

    try:
        search_terms = json.loads(response)
        if not isinstance(search_terms, list) or not all(isinstance(term, str) for term in search_terms):
            raise ValueError("Response is not a list of strings.")
    except (json.JSONDecodeError, ValueError):
        response = response[response.find("[") + 1:response.rfind("]")]
        match = re.search(r'\["(?:[^"\\]|\\.)*"(?:,\s*"[^"\\]*")*\]', response)
        if match:
            try:
                search_terms = json.loads(match.group())
            except json.JSONDecodeError:
                print(colored("[-] Could not parse response.", "red"))
                return []

    print(colored(f"\nGenerated {len(search_terms)} search terms: {', '.join(search_terms)}", "cyan"))
    return search_terms

def generate_metadata(video_subject: str, script: str, ai_model: str) -> Tuple[str, str, List[str]]:  
    """  
    Generate metadata for a YouTube video, including the title, description, and keywords.  
  
    Args:  
        video_subject (str): The subject of the video.  
        script (str): The script of the video.  
        ai_model (str): The AI model to use for generation.  
  
    Returns:  
        Tuple[str, str, List[str]]: The title, description, and keywords for the video.  
    """  
  
    title_prompt = f"""  
    Generate a catchy and SEO-friendly title for a YouTube shorts video about {video_subject}.  
    """  
  
    title = generate_response(title_prompt, ai_model).strip()  
    
    description_prompt = f"""  
    Write a brief and engaging description for a YouTube shorts video about {video_subject}.  
    The video is based on the following script:  
    {script}  
    """  
  
    description = generate_response(description_prompt, ai_model).strip()  
    keywords = get_search_terms(video_subject, 6, script, ai_model)  

    return title, description, keywords


def create_responsibilities_prompt(job_title: str, company_name: str, duration: str, additional_details: str = "") -> str:
    """
    Create a prompt to generate responsibilities or achievements based on job details.

    Args:
        job_title (str): The job title.
        company_name (str): The company name.
        duration (str): The duration of employment.
        additional_details (str): Any additional details or focus areas for the responsibilities.

    Returns:
        str: The constructed prompt ready to be sent to an AI model.
    """
    prompt = f"""
    You are a {education} highly skilled professional with deep knowledge of various job roles. 
    Based on the job title, company name, and duration of employment provided, 
    generate a detailed list of key responsibilities and achievements. 
    These should reflect the typical tasks and accomplishments associated with the role.

    Job Title: {job_title}
    Company: {company_name}
    Duration: {duration}

    {additional_details}

    Provide a concise, bullet-point list of responsibilities and achievements without any introductory text. Focus on action verbs and quantify accomplishments where possible.
    """
    return prompt

def autogenerate_responsibilities(prompt: str, ai_model: str) -> str:
    """
    Generate responsibilities or achievements based on job details.

    Args:
        prompt (str): The input prompt containing job details such as the job title, company name, and duration.
        ai_model (str): The AI model to use for generating the responsibilities.

    Returns:
        str: The generated responsibilities or achievements based on the provided prompt.
    """
    if ai_model == 'g4f':
        client = Client()
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            provider=g4f.Provider.You, 
            messages=[{"role": "user", "content": prompt}],
        ).choices[0].message.content

    elif ai_model in ["gpt3.5-turbo", "gpt4"]:
        model_name = "gpt-3.5-turbo" if ai_model == "gpt3.5-turbo" else "gpt-4"
        response = openai.ChatCompletion.create(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
        )
        response_content = response.choices[0].message['content']

    elif ai_model in ["llama3", "llama3.1"]:
        response = ollama.generate(
            model=ai_model,
            prompt=prompt,
        )
        response_content = response.get("response", "")

    elif ai_model == 'gemmini':
        model = genai.GenerativeModel('gemini-pro')
        response_model = model.generate_content(prompt)
        response_content = response_model.text


    

    else:
        raise ValueError("Invalid AI model selected.")

    return response_content


