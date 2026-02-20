import sys
from tempfile import NamedTemporaryFile
from pathlib import Path
import uuid

from fastapi import FastAPI
from dotenv import load_dotenv
from notion2md.exporter.block import MarkdownExporter


# 環境変数の読み込み
load_dotenv()

def get_page_text_as_md(page_id):

    base_filename=str(uuid.uuid4())
    output_filename=f"{base_filename}.md"
    MarkdownExporter(block_id=page_id,output_filename=base_filename,output_path="./",unzipped=True).export()

    with open(output_filename,"r") as f:
        response=f.read()
    Path(output_filename).unlink()
    return response 

page_id=sys.argv[1]
response=get_page_text_as_md(page_id)
print(response)