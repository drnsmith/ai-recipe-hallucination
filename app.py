import gradio as gr
import os
import json
import openai
import mistralai
import anthropic

# Set API keys from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

# Define AI Models
MODELS = {
    "GPT-4o": "gpt-4o",
    "Claude 3.5": "claude-3-5-haiku-20241022",
    "Mixtral": "mistral-small-latest"
}

# Define a folder for caching API responses
CACHE_DIR = "cache"
os.makedirs(CACHE_DIR, exist_ok=True)

def load_cache(file_name):
    """Loads cached API responses if available"""
    file_path = os.path.join(CACHE_DIR, file_name)
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            return json.load(f)
    return {}

def save_cache(file_name, data):
    """Saves API responses to cache"""
    file_path = os.path.join(CACHE_DIR, file_name)
    with open(file_path, "w") as f:
        json.dump(data, f)

def get_ai_response(model, prompt):
    """Fetch AI-generated recipe from the specified model"""
    cache_file = f"{model}_recipes.json"
    cache = load_cache(cache_file)

    if prompt in cache:
        return cache[prompt]  # Return cached result

    if model == "GPT-4o":
        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=750
        )
        output = response.choices[0].message.content

    elif model == "Claude 3.5":
        client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
        response = client.messages.create(
            model="claude-3-5-haiku-20241022",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=750
        )
        output = response.content[0].text

    elif model == "Mixtral":
        client = mistralai.client.MistralClient(api_key=MISTRAL_API_KEY)
        response = client.chat(
            model="mistral-small-latest",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=750
        )
        output = response.choices[0].message.content

    else:
        output = "Model not supported."

    cache[prompt] = output  # Store in cache
    save_cache(cache_file, cache)  # Save to file

    return output

def compare_recipes(dish_name):
    """Generates recipes for a selected dish using different AI models"""
    prompt = f"Generate a traditional recipe for {dish_name}. Include ingredients, step-by-step instructions, and cooking time. Avoid unnecessary ingredients."

    results = {model: get_ai_response(model, prompt) for model in MODELS.keys()}
    return results["GPT-4o"], results["Claude 3.5"], results["Mixtral"]

# Gradio UI
with gr.Blocks() as demo:
    gr.Markdown("# 🍽️ AI Recipe Hallucination Tester")
    gr.Markdown("Compare how different AI models generate recipes and spot any hallucinations.")

    dish_input = gr.Textbox(label="Enter a dish name (e.g., Lasagna, Risotto, Sushi)")
    generate_button = gr.Button("Generate Recipes")
    
    with gr.Row():
        gpt_output = gr.Textbox(label="GPT-4o Recipe", lines=10)
        claude_output = gr.Textbox(label="Claude 3.5 Recipe", lines=10)
        mixtral_output = gr.Textbox(label="Mixtral Recipe", lines=10)

    generate_button.click(compare_recipes, inputs=[dish_input], outputs=[gpt_output, claude_output, mixtral_output])

demo.launch()

