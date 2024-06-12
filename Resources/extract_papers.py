import os
import json
import fitz  # PyMuPDF
import nltk
from nltk.tokenize import word_tokenize

nltk.download('punkt')

def extract_paragraphs_from_pdf(pdf_path):
    pdf_document = fitz.open(pdf_path)
    paragraphs = []
    current_paragraph = ""

    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        blocks = page.get_text("blocks")
        
        for block in blocks:
            text = block[4].strip()
            if text:
                if current_paragraph:
                    current_paragraph += " " + text
                else:
                    current_paragraph = text
            else:
                if current_paragraph:
                    paragraphs.append(current_paragraph)
                    current_paragraph = ""
    
    if current_paragraph:
        paragraphs.append(current_paragraph)
    
    return paragraphs

def chunk_text(text, chunk_size, chunk_overlap):
    words = word_tokenize(text)
    chunks = []
    for i in range(0, len(words), chunk_size - chunk_overlap):
        chunk = words[i:i + chunk_size]
        chunks.append(' '.join(chunk))
        if i + chunk_size >= len(words):
            break
    return chunks

def extract_papers_from_folder(folder_path, chunk_size=2048, chunk_overlap=24):
    papers = []
    for index, filename in enumerate(os.listdir(folder_path)):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(folder_path, filename)
            paragraphs = extract_paragraphs_from_pdf(pdf_path)
            full_text = " ".join(paragraphs)
            chunks = chunk_text(full_text, chunk_size, chunk_overlap)
            paper = {
                "paper_index": index,
                "paper_title": filename,
                "paper_content": chunks
            }
            papers.append(paper)
    return papers

def save_papers_to_json(papers, output_path):
    with open(output_path, 'w', encoding='utf-8') as json_file:
        json.dump(papers, json_file, ensure_ascii=False, indent=4)

def main():
    folder_path = "papers"
    output_path = "papers.json"
    papers = extract_papers_from_folder(folder_path)
    save_papers_to_json(papers, output_path)
    print(f"Extracted {len(papers)} papers and saved to {output_path}")

if __name__ == "__main__":
    main()
