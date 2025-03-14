import tkinter as tk
import tkinter.scrolledtext as scrolledtext
import google.generativeai as genai
import os
from dotenv import load_dotenv

GOOGLE_API_KEY = ""  # Your API Key
genai.configure(api_key=GOOGLE_API_KEY)

def list_available_models():
    """Prints available models and their supported generation methods."""
    print("\nAvailable Models:")
    try:
        for model in genai.list_models():
            if 'generateContent' in model.supported_generation_methods:
                print(f"Model Name: {model.name}")
                print(f"  Description: {model.description}")
                print("-" * 40)
    except Exception as e:
        print(f"Error listing models: {e}")

def generate_text(prompt_text, model_name='models/gemini-1.5-pro-002'): #updated default model
    """Generates text using the Gemini API."""
    try:
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(prompt_text)
        return response.text
    except Exception as e:
        return f"An error occurred while generating text: {e}"

def generate_and_display():
    """Gets user input, generates text, and updates the GUI."""
    user_prompt = prompt_entry.get("1.0", tk.END).strip()
    if not user_prompt:
        update_result("Please enter a prompt.")
        return

    update_result("Generating...")
    root.update()

    # Select model dynamically (after running list_available_models())
    selected_model = 'models/gemini-1.5-pro-002'  #  Replace with your preferred model

    generated_response = generate_text(user_prompt, model_name=selected_model)
    update_result(generated_response)

def update_result(message):
    """Updates the result display in the GUI."""
    result_text.config(state=tk.NORMAL)
    result_text.delete("1.0", tk.END)
    result_text.insert(tk.END, message)
    result_text.config(state=tk.DISABLED)

# --- GUI Setup ---
root = tk.Tk()
root.title("Gemini API Text Generator")

# Prompt Input
tk.Label(root, text="Enter your prompt:").pack(pady=5)
prompt_entry = scrolledtext.ScrolledText(root, height=5, width=50, wrap=tk.WORD)
prompt_entry.pack(padx=10, pady=5)

# Generate Button
tk.Button(root, text="Generate", command=generate_and_display).pack(pady=10)

# Result Display
tk.Label(root, text="Generated Text:").pack()
result_text = scrolledtext.ScrolledText(root, height=10, width=50, wrap=tk.WORD, state=tk.DISABLED)
result_text.pack(padx=10, pady=5)

# List Models at Startup
list_available_models()

root.mainloop()
