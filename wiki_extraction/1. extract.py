import os
import markdown
from pathlib import Path

# Define the path to the 'content' directory
content_dir = Path(__file__).parent / 'content'

# Output file to store the extracted text
output_file = Path(__file__).parent / 'extracted_text.txt'

# Initialize a list to hold the extracted text
extracted_text = []

def extract_text_from_markdown(file_path):
    """Extract text from a single Markdown file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        md_content = file.read()
        html = markdown.markdown(md_content)
        # Extract text from HTML
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')
        text = soup.get_text()
        extracted_text.append(text)

def traverse_directory(directory):
    """Recursively traverse the directory to find all Markdown files."""
    for item in directory.iterdir():
        if item.is_dir():
            traverse_directory(item)
        elif item.suffix == '.md':
            extract_text_from_markdown(item)

# Start the extraction process
traverse_directory(content_dir)

# Write the extracted text to the output file
with open(output_file, 'w', encoding='utf-8') as output:
    output.write('\n\n'.join(extracted_text))

print(f"Extraction complete. Text saved to {output_file}")
