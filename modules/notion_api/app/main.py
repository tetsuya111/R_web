from fastapi import FastAPI
from dotenv import load_dotenv
import os

from app.utils import get_page_text_as_md

# 環境変数の読み込み
load_dotenv()

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/page/get/md/{page_id}/")
async def get_md_page(page_id):
    text=get_page_text_as_md(page_id)
    return {
        "result":{
            "text":text
        }
    }