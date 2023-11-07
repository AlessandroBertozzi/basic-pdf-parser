from utilis import *
from dotenv import load_dotenv
from tqdm import tqdm

load_dotenv()
GROBID_URL = os.environ.get("GROBID_ENDPOINT")
repo_directory = os.environ.get("PDF_REPO")


pdf_files = list_pdfs(repo_directory)

for pdf in tqdm(pdf_files):
    parse_pdf(GROBID_URL, pdf)

