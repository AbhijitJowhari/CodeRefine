import fitz  # PyMuPDF
import os
import json

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def tokenize_into_paragraphs(text):
    paragraphs = text.split('\n\n')
    paragraphs = [para.replace('\n', ' ').strip() for para in paragraphs if para.strip()]
    return paragraphs

def process_papers(directory):
    papers = []
    for i, filename in enumerate(os.listdir(directory)):
        if filename.endswith('.pdf'):
            file_path = os.path.join(directory, filename)
            paper_title = os.path.splitext(filename)[0]
            paper_content = extract_text_from_pdf(file_path)
            paragraphs = tokenize_into_paragraphs(paper_content)
            paper_obj = {
                'paper_index': i,
                'paper_title': paper_title,
                'paper_content': paragraphs
            }
            papers.append(paper_obj)
    return papers

def save_as_json(data, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def main():
    directory = 'papers'
    output_file = 'papers.json'
    papers = process_papers(directory)
    save_as_json(papers, output_file)

if __name__ == '__main__':
    main()
