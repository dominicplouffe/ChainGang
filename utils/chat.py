import time
import json
import requests
from openai import OpenAI
from chaingang.settings import OPENAI_KEY

OPENAI_BASE_URL = "https://api.openai.com/v1"


def upload_file(file_content, client):
    file_path = "/tmp/input_data.json"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(file_content)

    with open(file_path, "rb") as f:
        file = client.files.create(file=f, purpose="assistants")

    print("Uploaded file ID:", file.id)
    return file.id


# Attach file to Assistant using raw REST API (since SDK doesn't support it yet)
def attach_file_to_assistant(assistant_id, file_id):
    url = f"{OPENAI_BASE_URL}/assistants/{assistant_id}/files"
    headers = {
        "Authorization": f"Bearer {OPENAI_KEY}",
        "Content-Type": "application/json",
        "OpenAI-Beta": "assistants=v2",
    }
    data = {"file_id": file_id}
    response = requests.post(url, headers=headers, json=data)

    if response.status_code != 200:
        raise Exception(f"Failed to attach file: {response.text}")
    print(f"File {file_id} attached to Assistant {assistant_id}")


# Create new assistant dynamically
def create_assistant(instructions, tools=[], client=None, model="gpt-4o-mini"):

    if client is None:
        client = OpenAI(api_key=OPENAI_KEY)

    assistant = client.beta.assistants.create(
        model=model,
        instructions="You are a helpful assistant.",
        tools=tools,
    )
    print(f"Created Assistant ID: {assistant.id}")
    return assistant.id


def create_thread(client=None):

    if client is None:
        client = OpenAI(api_key=OPENAI_KEY)

    thread = client.beta.threads.create()

    return thread.id


# Run assistant with Assistant API
def run_assistant(thread_id, assistant_id, prompt, client, file_id=None):

    client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=prompt,
        attachments=(
            [{"file_id": file_id, "tools": [{"type": "code_interpreter"}]}]
            if file_id
            else None
        ),
    )

    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id,
    )

    while True:
        run_status = client.beta.threads.runs.retrieve(
            thread_id=thread_id, run_id=run.id
        )
        if run_status.status == "completed":
            break
        elif run_status.status in ["failed", "cancelled", "expired"]:
            raise Exception(f"Run failed: {run_status.status}")
        time.sleep(1)

    messages = client.beta.threads.messages.list(thread_id=thread_id)
    response = messages.data[0].content[0].text.value
    return response


# Run simple chat completion (no assistant API)
def run_chat_completion(prompt, client, model):
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
    )
    return response.choices[0].message.content


# Unified entry point
def get_response(
    prompt, file_content=None, model="gpt-4o-mini", assistant_id=None, thread_id=None
):
    client = OpenAI(api_key=OPENAI_KEY)

    file_id = None
    if file_content is not None:
        file_id = upload_file(file_content, client)

    if not thread_id:
        thread_id = create_thread(client)

    if assistant_id:
        response = run_assistant(
            thread_id, assistant_id, prompt, client, file_id=file_id
        )
    else:
        response = run_chat_completion(prompt, client, model)

    res = None
    i = 0
    while res is None and i < 2:
        try:
            print(response)
            if i == 0:
                res = json.loads(response.replace("```json", "").replace("```", ""))
            elif i == 1:
                res = json.loads(response.split("```json")[1].split("```")[0])
        except (json.JSONDecodeError, IndexError):
            res = None

        i += 1
        if res is not None:
            break

    if file_id:
        client.files.delete(file_id)

    return res
