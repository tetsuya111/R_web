import uuid
from pathlib import Path

from notion2md.exporter.block import MarkdownExporter

def get_page_text_as_md(page_id):

    base_filename=str(uuid.uuid4())
    output_filename=f"{base_filename}.md"
    MarkdownExporter(block_id=page_id,output_filename=base_filename,output_path="./",unzipped=True).export()

    with open(output_filename,"r") as f:
        response=f.read()
    Path(output_filename).unlink()
    return response 