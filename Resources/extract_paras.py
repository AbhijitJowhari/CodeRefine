import xml.etree.ElementTree as ET
import glob
import os

def extract_text_from_file(file_path):
    # Parse the XML file
    tree = ET.parse(file_path)
    root = tree.getroot()

    # Namespace dictionary to handle namespaces in the XML
    ns = {'tei': 'http://www.tei-c.org/ns/1.0'}

    # Extract headings and paragraphs
    body_elements = root.findall('.//tei:text//tei:body//*', ns)
    
    extracted_list = []

    current_heading = None
    for elem in body_elements:
        if elem.tag == '{http://www.tei-c.org/ns/1.0}head':
            # Set current heading
            current_heading = ''.join(elem.itertext()).strip()
        elif elem.tag == '{http://www.tei-c.org/ns/1.0}p':
            # Get paragraph text
            para_text = ''.join(elem.itertext()).strip()
            if current_heading:
                # Append heading and text to the list
                extracted_list.append(f"{current_heading} : {para_text}")
    
    return extracted_list

def process_directory(directory_path):
    # Get all .grobid.tei.xml files in the directory
    files = glob.glob(os.path.join(directory_path, '*.grobid.tei.xml'))
    
    all_extracted_text = []

    # Process each file
    for file_path in files:
        extracted_text = extract_text_from_file(file_path)
        all_extracted_text.extend(extracted_text)
    
    return all_extracted_text

# Example usage
directory_path = './Research_papers/papers_xml'
all_text_list = process_directory(directory_path)

# Print the extracted text
print(all_text_list[0])
