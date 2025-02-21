import gradio as gr
from models import generate_recipe
from prompts import prompt_options

# Gradio UI function
def ai_recipe_test(model, dish):
    """Fetches AI-generated recipes and compares results."""
    response = generate_recipe(model, dish)
    return response

# Build UI
with gr.Blocks() as demo:
    gr.Markdown("# 🍽️ AI Recipe Hallucination Tester")
    
    model_choice = gr.Radio(["GPT-4", "Claude", "Mixtral"], label="Choose AI Model")
    dish_choice = gr.Dropdown(list(prompt_options.keys()), label="Select a Dish")

    output = gr.Textbox(label="AI Response")

    submit_btn = gr.Button("Generate Recipe")

    submit_btn.click(ai_recipe_test, inputs=[model_choice, dish_choice], outputs=output)

# Run App
if __name__ == "__main__":
    demo.launch()


