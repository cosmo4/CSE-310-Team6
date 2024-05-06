# This program will upload a chosen file to chatGPT and get a response, then parse and display the response to the user.
### THIS WILL NOT WORK WITHOUT AN OPENAI API KEY ###
### TO APPLY A KEY TYPE "setx OPENAI_API_KEY 'your_api_key'" REPLACING 'your_api_key' WITH YOUR KEY ###
### BE SURE TO ALSO CHANGE file_name TO AN EXISTING FILE ###

# Import OpenAI library
from openai import OpenAI
# Initialize an OpenAI client
client = OpenAI()
# Set a file path
file_name = "notes.docx"

# Create a new assistant named "Note Summarizer" using the gpt-3.5-turbo model with the given instructions
assistant = client.beta.assistants.create(
  name="Note Summarizer",
  model="gpt-3.5-turbo",
  instructions="You are a note summarizer. You read a text document and summarize the key points of college student's notes.",
  # Make sure the file_search tool is used in order to upload and read files
  tools=[{"type":"file_search"}],
)

# Create a vector store to store the notes documents
vector_store = client.beta.vector_stores.create(name="Notes")
# Give the file path to the notes document
file_paths = [file_name]
# Open the file and store the stream
file_streams = [open(path, "rb") for path in file_paths]

# Upload the file to the vector store
file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
   vector_store_id=vector_store.id, files=file_streams
)

# Update the assistant to use the vector store for file access
assistant = client.beta.assistants.update(
   assistant_id=assistant.id,
   tool_resources={"file_search":{"vector_store_ids":[vector_store.id]}},
)

# Create a message file containing the notes
message_file = client.files.create(
   file=open("notes.docx", "rb"), purpose="assistants"
)

# Create a thread to interact with the assistant
thread = client.beta.threads.create(
   messages=[
      {
         "role": "user",
         "content": "Summarize these notes in a more compressed manner. They should still be useable as notes for the various topics, just shortened and summarized.",
         "attachments": [
            { "file_id": message_file.id, "tools": [{"type": "file_search"}]}
         ],
      }
   ]
)

# Run the assistant
run = client.beta.threads.runs.create_and_poll(
    thread_id=thread.id, assistant_id=assistant.id
)

# Retrieve the message from the assistant
messages = list(client.beta.threads.messages.list(thread_id=thread.id, run_id=run.id))

# Extract the content of the message
message_content = messages[0].content[0].text
# Extract any annotations and citations from the content
annotations = message_content.annotations
citations = []
for index, annotation in enumerate(annotations):
    # Replace the original text with annotatted references
    message_content.value = message_content.value.replace(annotation.text, f"[{index}]")
    # Retrieve file citations if any
    if file_citation := getattr(annotation, "file_citation", None):
        cited_file = client.files.retrieve(file_citation.file_id)
        citations.append(f"[{index}] {cited_file.filename}")

# Print the summarized notes and any citations
print(message_content.value)
print("\n".join(citations))