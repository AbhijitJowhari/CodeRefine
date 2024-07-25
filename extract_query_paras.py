import xml.etree.ElementTree as ET
import os

# Iterate over all XML files in the directory
def get_content_list(directory):
    content_list = []
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