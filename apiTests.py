import requests
import json

# Define the API URL and the model
url = 'http://ip.address/api/generate'
headers = {'Content-Type': 'application/json'}

# Correct path to your text file
txt_file_path = 'file/path.txt'  # Update this path

# Read the content of the .txt file
try:
    with open(txt_file_path, 'r') as file:
        text = file.read()
except FileNotFoundError:
    print(f"File not found: {txt_file_path}")
    exit()

# Define a function that will turn the text into Q&A pairs
def generate_qa_pairs(text):
    prompt = f'You are a Q/A expert. You read through the provided text and create JSONL question and answer format explanations for all terms within the document.\n\n{text}'
    
    data = {
        "model": 'mistral',
        "prompt": prompt,
        "stream": False  # Set stream to False
    }

    # Make the POST request
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        
        # Raw response for debugging
        print("Raw response content:", response.text)
        
        # If the request is successful and the response is JSON
        if response.status_code == 200:
            try:
                response_data = json.loads(response.json().get("response", "{}"))
                
                jsonl_data = ""
                for term, qa_pair in response_data.items():
                    jsonl_data += json.dumps({
                        "question": qa_pair["Question"],
                        "answer": qa_pair["Answer"]
                    }) + "\n"
                
                return jsonl_data
            except json.JSONDecodeError as e:
                print(f"JSON decode error: {e}")
                return None
        else:
            print(f"Failed to get a valid response. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error occurred: {e}")
        return None

# Call the function to generate Q&A
qa_jsonl = generate_qa_pairs(text)

if qa_jsonl:
    print("Generated Q&A pairs in JSONL format:")
    print(qa_jsonl)
