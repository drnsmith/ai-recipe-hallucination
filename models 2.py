import os
import openai
import anthropic
import mistralai
from dotenv import load_dotenv

# ✅ Load API Keys from .env
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")


# ✅ Function to Call OpenAI API
def get_gpt4_response(prompt):
    client = openai.OpenAI(api_key=OPENAI_API_KEY)
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=750
    )
    return response.choices[0].message.content


# ✅ Function to Call Claude API
def get_claude_response(prompt):
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    response = client.messages.create(
        model="claude-3.5-haiku",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=750
    )
    return response.content[0].text


# ✅ Function to Call Mistral API
def get_mistral_response(prompt):
    client = mistralai.client.MistralClient(api_key=MISTRAL_API_KEY)
    response = client.chat(
        model="mistral-small-latest",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=750
    )
    return response.choices[0].message.content


# ✅ Main Function to Call AI Models
def generate_recipe(model, dish):
    """Fetches a recipe from the selected AI model."""
    prompt = f"Generate a recipe for {dish}. Keep it simple and authentic."
    
    if model == "GPT-4":
        return get_gpt4_response(prompt)
    elif model == "Claude":
        return get_claude_response(prompt)
    elif model == "Mixtral":
        return get_mistral_response(prompt)
    else:
        return "⚠️ Error: Unsupported model!"
