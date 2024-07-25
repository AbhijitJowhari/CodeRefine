import os
import xml.etree.ElementTree as ET
from mixedbread_ai.client import MixedbreadAI
import os
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


def get_embeddings(texts, model,mxbai,prompt=None):
    res = mxbai.embeddings(
        input=texts,
        model=model,
        prompt=prompt
    )
    embeddings = [entry.embedding for entry in res.data]
    return np.array(embeddings)

def extract_text_from_files(directory):
    # Namespace
    ns = {'tei': 'http://www.tei-c.org/ns/1.0'}

    # List to store the heading and its corresponding content
    content_list = []

    # Iterate over all XML files in the directory
    for filename in os.listdir(directory):
        if filename.endswith('.xml'):
            # Parse the XML file
            tree = ET.parse(os.path.join(directory, filename))
            root = tree.getroot()

            # Extract the contents under each heading
            current_heading = None
            for elem in root.iter():
                if elem.tag == '{http://www.tei-c.org/ns/1.0}head':
                    if elem.text is not None:
                        current_heading = elem.text.strip()
                elif elem.tag == '{http://www.tei-c.org/ns/1.0}p' and current_heading:
                    if elem.text is not None:
                        content_list.append(elem.text.strip())

    return content_list

    
