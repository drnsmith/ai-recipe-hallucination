import os
import openai
import anthropic
import mistralai
import time

# Load API keys from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

# Initialize API Clients
openai_client = openai.OpenAI(api_key=OPENAI_API_KEY)
anthropic_client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
mistral_client = mistralai.client.MistralClient(api_key=MISTRAL_API_KEY)

# Function to call OpenAI (GPT-4)
def get_openai_response(prompt, model="gpt-4o", max_tokens=750):
    try:
        response = openai_client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"❌ OpenAI API Error: {e}")
        return None

# Function to call Anthropic (Claude)
def get_claude_response(prompt, model="claude-3.5-haiku", max_tokens=750):
    try:
        response = anthropic_client.messages.create(
            model=model,
            max_tokens=max_tokens,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text.strip()
    except Exception as e:
        print(f"❌ Anthropic API Error: {e}")
        return None

# Function to call Mistral
def get_mistral_response(prompt, model="mistral-small-latest", max_tokens=750):
    try:
        response = mistral_client.chat(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"❌ Mistral API Error: {e}")
        return None

# Function to query all models at once
def get_all_model_responses(prompt):
    responses = {
        "OpenAI (GPT-4o)": get_openai_response(prompt),
        "Anthropic (Claude)": get_claude_response(prompt),
        "Mistral": get_mistral_response(prompt)
    }
    return responses

if __name__ == "__main__":
    test_prompt = "Generate a simple recipe for Spaghetti Carbonara."
    print("🔍 Testing API Calls...\n")
    results = get_all_model_responses(test_prompt)
    for model, response in results.items():
        print(f"🔹 {model} Response:\n{response}\n{'-'*50}\n")
