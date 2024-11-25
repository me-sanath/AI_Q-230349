import re
import json
import csv
import os

# Define the base path
base_path = 'data'

# Define patterns for extraction
patterns = {
    "title": r"^(.*?)(?:\n|$)",  # Title line
    "code_block": r"```(?:typescript|bash|javascript|python|.*?)\n(.*?)```",  # Code blocks
    "description": r"^(.*?)$",  # Extract other lines
}

# Helper function to classify line type
def classify_line(line):
    if re.match(patterns["code_block"], line, re.DOTALL):
        return "Code"
    elif re.match(patterns["title"], line):
        return "Title"
    else:
        return "Description"

# Function to process each project's extracted text
def process_project(project_name):
    file_path = os.path.join(base_path, project_name, 'extracted_text.txt')

    # Initialize data container
    data = []

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            lines = content.split("\n")
            for line in lines:
                line_type = classify_line(line)
                if line_type == "Code":
                    match = re.search(patterns["code_block"], line, re.DOTALL)
                    if match:
                        data.append({"type": "Code", "content": match.group(1).strip()})
                elif line_type == "Title":
                    match = re.match(patterns["title"], line)
                    if match:
                        data.append({"type": "Title", "content": match.group(1).strip()})
                elif line_type == "Description":
                    data.append({"type": "Description", "content": line.strip()})

        # Save as a JSON file
        output_json_path = f"{project_name}_formatted_dataset.json"
        with open(output_json_path, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, indent=4)

        # Save as a CSV file
        output_csv_path = f"{project_name}_formatted_dataset.csv"
        with open(output_csv_path, 'w', newline='', encoding='utf-8') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=["type", "content"])
            writer.writeheader()
            writer.writerows(data)

        print(f"Dataset for '{project_name}' saved as {output_json_path} and {output_csv_path}")

    except UnicodeDecodeError as e:
        print(f"Error reading the file for project '{project_name}': {e}")
    except FileNotFoundError as e:
        print(f"File not found for project '{project_name}': {e}")

# Automatically process all projects in the base_path directory
def process_all_projects():
    # List all subdirectories in the base_path directory
    project_dirs = [d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))]

    for project_name in project_dirs:
        process_project(project_name)

# Start processing all projects
process_all_projects()
