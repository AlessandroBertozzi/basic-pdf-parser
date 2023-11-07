from utilis import *
import pandas as pd
from tqdm import tqdm
import json


def get_metadata_by_pdf_name(pdf_name, dataframe):
    """
    Extracts metadata for a given PDF name from a dataframe.

    :param pdf_name: The name of the PDF file to search for in the dataframe.
    :param dataframe: The pandas dataframe containing the metadata.
    :return: A dictionary containing the metadata for the PDF, or None if not found.
    """
    # Filter the dataframe for the given pdf_name
    metadata = dataframe[dataframe['Nome_PDF'] == pdf_name]

    # If the PDF is found in the dataframe, return its metadata as a dictionary
    if not metadata.empty:
        return metadata.iloc[0].to_dict()
    else:
        return None


# Load the CSV file into a DataFrame
file_path = 'data/metadati_indice_documenti.csv'
data = pd.read_csv(file_path)
data.fillna('')

xml_file_path = "data/xml"
xml_files = list_xmls(xml_file_path)

resources = list()

for xml in tqdm(xml_files):
    name_file = xml.split('\\')[-1].split('.')[0]
    metadata = get_metadata_by_pdf_name(f"{name_file}.pdf", data)
    chunks = extract_body_and_paragraphs(xml)
    for chunk in chunks:
        paragraphs = chunk['paragraphs']
        head = chunk['head']
        if head != "No Title":
            for i, paragraph in enumerate(paragraphs):
                single_resource = {
                    "page_content": paragraph,
                    "metadata": {
                        'head': head,
                        'name_pdf': metadata['Nome_PDF'] if not pd.isnull(metadata['Nome_PDF']) else "",
                        'number_of_paragraphs': i + 1,
                        'url': metadata['URL'] if not pd.isnull(metadata['URL']) else "",
                        'title': metadata['Headline'] if not pd.isnull(metadata['Headline']) else "",
                        "author": metadata['Author'] if not pd.isnull(metadata['Author']) else "",
                        "date_published": metadata['Date Published'] if not pd.isnull(metadata['Date Published']) else None
                    }
                }
                resources.append(single_resource)

# Define the path for the JSON file to save the metadata
json_file_path = 'resources_metadata.json'

print(len(resources))

# Write the metadata dictionary to a JSON file
with open(json_file_path, 'w', encoding='utf-8') as json_file:
    json.dump(resources, json_file, ensure_ascii=False, indent=4)
