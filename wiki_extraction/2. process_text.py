import os
from typing import List
from pydantic import BaseModel
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

groq = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# Define the classification schema
class Classification(BaseModel):
    type: str  # Either 'Code' or 'Description'
    content: str

# Function to classify text using Groq AI
def classify_text(text: str) -> List[Classification]:
    chat_completion = groq.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a classifier that categorizes text as either 'Code' or 'Description'.\n"
                    "The JSON object must use the schema: "
                    f"{json.dumps(Classification.model_json_schema(), indent=2)}"
                ),
            },
            {
                "role": "user",
                "content": f"Classify the following text:\n{text}",
            },
        ],
        model="llama3-8b-8192",
        temperature=0,
        stream=False,
        response_format={"type": "json_object"}, 
    )
    # Return the classified text in the format
    return Classification.model_validate_json(chat_completion.choices[0].message.content)


def process_file_for_classification(file_path: str, total_lines: int, lines_per_batch: int = 10, ):
    result_batch = []
    
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    for i in range(0, total_lines, lines_per_batch):
        text_batch = ''.join(lines[i:i+lines_per_batch])
        print(f"Classifying batch {i//lines_per_batch + 1}...")
        
        classification_results = classify_text(text_batch)
        
        if classification_results:
            result_batch.append({
                "batch_number": i // lines_per_batch + 1,
                "classification": classification_results
            })
    
    return result_batch

# Function to display classified text in a readable format
def print_classification_results(result_batch):
    for batch in result_batch:
        print(f"\nBatch {batch['batch_number']}:")
        for classified in batch['classification']:
            print(f"Type: {classified.type}, Content: {classified.content[:50]}...")  # Print a snippet

# Example Usage
if __name__ == "__main__":
    file_path = 'extracted_text.txt'

    total_lines = int(input("Enter the lines to process: "))
    result_batch = process_file_for_classification(file_path,)

    # Print classified results
    print_classification_results(result_batch)

    # Save results to a JSON file
    output_json_path = 'extracted/formatted_projects_dataset.json'  # Adjust output path as needed
    with open(output_json_path, 'w', encoding='utf-8') as json_file:
        json.dump(result_batch, json_file, indent=4)
    
    print(f"Classification results saved to {output_json_path}")
