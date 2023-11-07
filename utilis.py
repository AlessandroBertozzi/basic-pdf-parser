import xml.etree.ElementTree as ET
import fnmatch
from lxml import etree
import os
import requests


def save_xml_to_file(xml_content, file_path):
    # Assuming you have a function that saves the xml_content to a file
    with open(file_path, 'w') as file:
        file.write(xml_content)


def parse_pdf(grobid_url, pdf_file_path, output_path='xml'):
    # Check if the output directory exists, if not, create it
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # Prepare the file as a multipart-form payload
    files = {'input': (pdf_file_path, open(pdf_file_path, 'rb'), 'application/pdf', {'Expires': '0'})}

    pdf_name = pdf_file_path.split('\\')[-1].split('.')[0]
    # Make the request
    response = requests.post(grobid_url, files=files)

    # Check if the request was successful
    if response.status_code == 200:
        # Get the XML content
        xml_content = response.text
        # Here you can process the xml_content further according to your needs
        file_path = f'{output_path}/{pdf_name}.xml'
        save_xml_to_file(xml_content, file_path)
    else:
        print("Error:", response.status_code, response.text)


def extract_body_and_paragraphs(file_path):
    # Define namespaces to use with XPath
    namespaces = {'ns0': "http://www.tei-c.org/ns/1.0"}

    # Read the content as bytes to avoid encoding issues
    with open(file_path, 'rb') as file:
        xml_content_bytes = file.read()

    # Parse the XML content
    root = etree.fromstring(xml_content_bytes)

    # Extract the body content
    body_content = root.xpath('.//ns0:body', namespaces=namespaces)

    # Define a function to extract paragraphs from a div
    def extract_paragraphs_from_div(div):
        # Extract the head title
        head_title = div.xpath('.//ns0:head/text()', namespaces=namespaces)

        # Extract paragraphs and exclude text within the 'ref' tags
        paragraphs = div.xpath('.//ns0:p', namespaces=namespaces)
        paragraphs_text = [''.join(para.xpath('.//text()[not(ancestor::ns0:ref)]', namespaces=namespaces)).strip() for
                           para in paragraphs]

        return {
            'head': head_title[0] if head_title else "No Title",
            'paragraphs': paragraphs_text
        }

    # Extract paragraphs for each div within the body
    body_divs = []
    for div in body_content[0]:
        body_divs.append(extract_paragraphs_from_div(div))

    return body_divs


def list_pdfs(directory):
    """
    List all PDF files in a given directory, including its subdirectories.

    :param directory: The path to the directory to search in.
    :return: A list of paths to PDF files.
    """
    pdf_files = []
    for root, dirs, files in os.walk(directory):
        for file in fnmatch.filter(files, '*.pdf'):
            pdf_files.append(os.path.join(root, file))
    return pdf_files


def list_xmls(directory):
    """
    List all PDF files in a given directory, including its subdirectories.

    :param directory: The path to the directory to search in.
    :return: A list of paths to PDF files.
    """
    pdf_files = []
    for root, dirs, files in os.walk(directory):
        for file in fnmatch.filter(files, '*.xml'):
            pdf_files.append(os.path.join(root, file))
    return pdf_files


def save_xml_to_file(xml_content, file_path):
    # Parse the XML content
    root = ET.fromstring(xml_content)

    # Create an ElementTree object from the root element
    tree = ET.ElementTree(root)

    # Write the XML content to the file
    tree.write(file_path, encoding='utf-8', xml_declaration=True)
