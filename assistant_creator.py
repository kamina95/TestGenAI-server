import json

from openai import OpenAI
import os

OPEN_API_KEY = os.getenv("OPEN_API_KEY")
client = OpenAI(api_key=OPEN_API_KEY)


def write_assistant_id_to_file(assistant_name, assistant_id):
    # Define the path to the JSON file where the assistant IDs will be stored
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Define the path to the JSON file where the assistant IDs are stored
    # This creates a path relative to the script's location
    json_file_path = os.path.join(script_dir, "assistants.json")

    # Ensure the file exists
    if not os.path.exists(json_file_path):
        return None


    # Read the existing data, if any
    if os.path.exists(json_file_path):
        with open(json_file_path, 'r') as file:
            assistants = json.load(file)
    else:
        assistants = {}

    # Update the dictionary with the new assistant's name and ID
    assistants[assistant_name] = assistant_id

    # Write the updated dictionary back to the file
    with open(json_file_path, 'w') as file:
        json.dump(assistants, file)


def get_assistant_id_by_name(assistant_name):
    # Define the path to the JSON file where the assistant IDs are stored

    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Define the path to the JSON file where the assistant IDs are stored
    # This creates a path relative to the script's location
    json_file_path = os.path.join(script_dir, "assistants.json")

    # Ensure the file exists
    if not os.path.exists(json_file_path):
        return None

    # Ensure the file exists
    if not os.path.exists(json_file_path):
        return None

    # Read the file and search for the assistant ID by name
    with open(json_file_path, 'r') as file:
        assistants = json.load(file)
        return assistants.get(assistant_name, None)


def create_assistant(instruction_file_path, name):
    with open(instruction_file_path, 'r') as file:
        instructions = file.read()

    assistant = client.beta.assistants.create(
        name=name,
        instructions=instructions,
        tools=[{"type": "code_interpreter"}],
        model="gpt-4-1106-preview",
    )
    write_assistant_id_to_file(name, assistant.id)
    return assistant


# assistant = create_assistant("assistant_instructions/OpenAI_Assistant_Test_Creation_Guidelines.md", "FirstAssistant")
# assistant = create_assistant("assistant_instructions/Fixed_OpenAI_Assistant_Error_Analysis_Guidelines.md",
#                              "RetryAssistant")
#
# assistant_id = get_assistant_id_by_name("FirstAssistant")
# print("Assistant ID:", assistant_id)
