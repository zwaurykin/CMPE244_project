import openai
import json

def load_config(filepath):
    """
    Loads the API key and model ID from a JSON file.

    :param filepath: The path to the JSON file containing the configuration.
    :return: A dictionary with the API key and model ID.
    """
    with open(filepath, 'r') as file:
        return json.load(file)

def query_chatgpt(prompt, model_name, api_key):
    """
    Queries the fine-tuned ChatGPT model and returns the response.

    :param prompt: The input prompt to send to the model.
    :param model_name: The name of your fine-tuned model.
    :param api_key: Your OpenAI API key.
    :return: The model's response as a string.
    """
    openai.api_key = api_key

    response = openai.ChatCompletion.create(
        model=model_name,
        messages=[
            {"role": "system", "content": "You are a technical support assistant for the CMPE244 project."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message['content']

def run_chatbot():
    """
    Runs the chatbot, taking user input and providing responses.
    """
    config = load_config('config.json')
    api_key = config['api_key']
    model_name = config['model_id']

    print("Chatbot started. Type 'quit' to exit.")

    while True:
        user_input = input("You: ")
        if user_input.lower() == 'quit':
            break
        response = query_chatgpt(user_input, model_name, api_key)
        print("Bot:", response)

# Run the chatbot
run_chatbot()
