import json

from openai import OpenAI
import os
import time

from assistant_creator import get_assistant_id_by_name

OPEN_API_KEY = os.getenv("OPEN_API_KEY")
client = OpenAI(api_key=OPEN_API_KEY)


# code_msg = sys.argv[1]
# assistant_name = sys.argv[2]


# --------------------------------------------------------------
# Generate response
# --------------------------------------------------------------
def generate_response(message_body, assistant_name):
    if assistant_name != "FirstAssistant":
        print("the error assistant was called")
        return "the error assistant was called"
    thread_id = get_thread_id(assistant_name)

    # Add message to thread
    message = client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=message_body,
    )

    # Run the assistant and get the new message
    new_message = run_assistant(thread_id, assistant_name)
    # return extract_code(run_assistant(thread))
    print("new message:" + new_message)
    return new_message


def get_thread_id(assistant_name):
    if assistant_name == "FirstAssistant":
        thread = client.beta.threads.create()
        print("new thread id: " + thread.id)
        write_thread_id_to_file("same", thread.id)
        return thread.id

    # Retrieve the thread ID
    thread_id = get_thread_id_by_name("same")

    # If the thread ID is not found, create a new thread
    if thread_id is None:
        thread = client.beta.threads.create()
        thread_id = thread.id
        write_thread_id_to_file("same", thread_id)

    # # Retrieve the thread
    # thread = client.beta.threads.retrieve(thread_id)
    return thread_id


## method to save the thread id to a file
def write_thread_id_to_file(assistant_name, thread_id):
    # Define the path to the JSON file where the assistant IDs will be stored
    json_file_path = "threads.json"

    # Read the existing data, if any
    if os.path.exists(json_file_path):
        with open(json_file_path, 'r') as file:
            threads = json.load(file)
    else:
        threads = {}

    # Update the dictionary with the new assistant's name and ID
    threads[assistant_name] = thread_id

    # Write the updated dictionary back to the file
    with open(json_file_path, 'w') as file:
        json.dump(threads, file)


# method to get the thread id by assistant name
def get_thread_id_by_name(assistant_name):
    # Define the path to the JSON file where the assistant IDs are stored
    json_file_path = "threads.json"

    # Ensure the file exists
    if not os.path.exists(json_file_path):
        return None

    # Read the file and search for the assistant ID by name
    with open(json_file_path, 'r') as file:
        threads = json.load(file)
        return threads.get(assistant_name, None)


# --------------------------------------------------------------
# Run assistant
# --------------------------------------------------------------
def run_assistant(thread_id, assistant_name):
    # Retrieve the Assistant
    # assistant = client.beta.assistants.retrieve(get_assistant_id_by_name(assistant_name))
    assistant_id = get_assistant_id_by_name(assistant_name)

    # Run the assistant
    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id,
    )

    # Wait for completion
    while run.status != "completed":
        # Be nice to the API
        time.sleep(0.5)
        run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)

    # Retrieve the Messages
    messages = client.beta.threads.messages.list(thread_id=thread_id)
    new_message = messages.data[0].content[0].text.value
    # print(f"Generated message: {new_message}")
    print(new_message)
    return new_message


# --------------------------------------------------------------
# Test assistant
# --------------------------------------------------------------

# method to extract the code from the message between the tags '''java and '''
def extract_code(message):
    code = message.split("'''java")[1].split("'''")[0]
    return code

# new_message = generate_response(code_msg, assistant_name)
# new_message = generate_response("gello", "FirstAssistant")
