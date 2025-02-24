import pandas as pd
import gradio as gr

# Load AI hallucination test results
def load_results():
    try:
        df = pd.read_csv("hallucination_results.csv")
        return df
    except FileNotFoundError:
        return pd.DataFrame(columns=["Dish", "AI Model", "Response"])

# Display AI responses side by side
def compare_models(dish):
    df = load_results()
    filtered_df = df[df["Dish"] == dish]

    if filtered_df.empty:
        return f"No results found for {dish}. Run the tests first."

    # Convert results to dictionary for better formatting
    response_dict = filtered_df.set_index("AI Model")["Response"].to_dict()

    return response_dict

# Create Gradio UI
def launch_dashboard():
    df = load_results()
    
    if df.empty:
        return "No data available. Please run hallucination tests first."

    dish_options = df["Dish"].unique().tolist()

    with gr.Blocks() as demo:
        gr.Markdown("# 🤖 AI Recipe Hallucination Dashboard")
        gr.Markdown("### Compare AI models on different recipes")

        dish_selector = gr.Dropdown(dish_options, label="Select a Dish")
        output = gr.JSON(label="AI Model Responses")

        dish_selector.change(compare_models, inputs=dish_selector, outputs=output)

    demo.launch()

# Run the dashboard
if __name__ == "__main__":
    launch_dashboard()
