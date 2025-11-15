import fitz
import docx
from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

api_key  = os.getenv("GEMINI_KEY")

client = genai.Client(api_key=api_key)


def process(query):
    try:
        print("Processing...")

        prompted_query = """
        You are Saathi.
        You are a mentor specializing in STEM — science, technology, engineering, and mathematics.
        Your purpose is teaching and guiding, never directly solving. You are a sophisticated, smart “rubber duck”—a partner in reasoning and understanding.
    
        Core Identity & Rules:
    
        Explain, Don’t Answer
        - Always break down the *why* behind any concept, derivation, or problem.
        - Focus on the underlying laws, patterns, and logic — not just formulas or results.
        - Avoid directly solving or computing the final answer. Instead, help the learner understand the reasoning path.
    
        Teach Theory
        - Always connect the question to fundamental scientific or mathematical principles.
        - Relate it to real-world intuition: why it works, where it fails, and how it connects to other ideas.
        - Prioritize explanations that build conceptual depth and long-term understanding.
    
        Guide, Don’t Solve
        - Never provide step-by-step solutions or final numeric results.
        - Instead, ask Socratic questions, hint toward relevant formulas or laws, and guide through conceptual checkpoints.
        - Encourage the learner to derive and reason, not memorize or copy.
    
        Encourage Cross-Disciplinary Thinking
        - Show how physics connects to math, how biology links with chemistry, or how computer science overlaps with logic.
        - Promote cognitive discipline — learning how to *think*, not what to memorize.
    
        Strict Prohibitions:
        - No giving final answers, complete solutions, or formula substitutions.
        - No oversimplifying to the point of removing reasoning.
        - No workarounds that skip understanding.
    
        Tone & Style:
        - Mentor-like, curious, and deeply insightful.
        - Use analogies, visual descriptions (in text), and everyday examples to make abstract concepts vivid.
        - Treat every question as a discovery — spark curiosity, not just clarity.
    
        Your mission:
        Transform every question into a learning moment. 
        Make the user walk away thinking more deeply, understanding more clearly, and reasoning more confidently.
        """ + query

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompted_query
        )

        return response.text
    except Exception as e:
        print(e)




def read_pdf(file):
    
    doc = fitz.open(stream=file.read(), filetype="pdf")
    all_text = []
    for page in doc:
        
        text = page.get_text("text")
        text = " ".join(text.split()) 
        all_text.append(text)  


    return "\n\n".join(all_text).strip()

def read_docx(file):

    doc = docx.Document(file)
    all_text = []

    for page in doc.paragraphs:
        text = page.text
        if text != "":
            all_text.append(text)
    
    return "\n\n".join(all_text).strip()



def return_prompt(file=None, text=None):

    content = ""

    if file:

        ext = file.name.lower().split(".")[-1]

        if ext == "pdf":
            content = read_pdf(file)
        
        elif ext == "docx":
            content = read_docx(file)

        elif ext == "txt":
            content = file.read().decode("utf-8")

    if text:
        content += "\n" + text

    

    
    prompt = f"""You are generating a multiple-choice quiz strictly based on the provided content.

        Rules:
        - The number of questions must depend on the content length (minimum 5, maximum 20).
        - If the content is too short, produce exactly 5 questions.
        - Use ONLY information from the content. Do not add external knowledge.
        - Every question must be answerable using the content alone.
        - Follow the output format exactly with no extra text.

        Output format (strict):
        Return a JSON array.
        Each question must be a JSON object containing these fields:

        "number": integer

        "question": string

        "options": list of 4 strings in order [A, B, C, D]

        "answer": string ("A" | "B" | "C" | "D")

        Do not include explanations, comments, or summaries. Output raw JSON only.
        No commentary.
        No markdown.
        No backticks.
        The response must be a valid JSON array that can be parsed with json.loads().

        CONTENT START
        {content}
        CONTENT END
        """

    return prompt


def get_quiz(prompt):

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    
    return response.text


def get_quiz_list(quiz):

    final_quiz_list = []
    temp_chunk = {}


    quiz_list = quiz.split("Q")

    for question in quiz_list:
        chunks = question.split("\n")
        temp_chunk["number"] = int(chunks[0])
        temp_chunk["text"] = chunks[1].split(":")[-1]

        options =  []
        for i in range(2, 6):
            options.append(chunks[i].split(":")[-1])

        temp_chunk["options"] = options

        temp_chunk["answer"] = chunks[6].split(":")[-1]

        final_quiz_list.append(temp_chunk)








