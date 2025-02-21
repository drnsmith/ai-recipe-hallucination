import gradio as gr
from models import generate_recipe
from prompts import prompt_options
import os
from dotenv import load_dotenv

# ✅ Load API keys from .env
load_dotenv()

# ✅ Retrieve API keys securely
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

# ✅ Print API key status (DO NOT print actual keys!)
print(f"🔑 OpenAI Key Loaded: {'✅' if OPENAI_API_KEY else '❌'}")
print(f"🔑 Anthropic Key Loaded: {'✅' if ANTHROPIC_API_KEY else '❌'}")
print(f"🔑 Mistral Key Loaded: {'✅' if MISTRAL_API_KEY else '❌'}")

# ✅ Function to fetch AI-generated recipes from multiple models
def compare_recipes(models, dish):
    """Fetches AI-generated recipes from multiple selected models."""
    results = {model: generate_recipe(model, dish) for model in models}
    return results

# ✅ Build UI
with gr.Blocks() as demo:
    gr.Markdown("# 🍽️ AI Recipe Hallucination Tester")

    # 🔹 Multi-select AI model checkbox
    model_choice = gr.CheckboxGroup(["GPT-4", "Claude", "Mixtral"], label="Choose AI Models")

    # 🔹 Dish selection dropdown
    dish_choice = gr.Dropdown(list(prompt_options.keys()), label="Select a Dish")

    # 🔹 Display output as a dictionary (side-by-side model comparison)
    output = gr.JSON(label="AI Responses")

    submit_btn = gr.Button("Generate Recipe")

    # 🔹 Run all selected models and show side-by-side results
    submit_btn.click(compare_recipes, inputs=[model_choice, dish_choice], outputs=output)

# ✅ Run App
if __name__ == "__main__":
    demo.launch()




