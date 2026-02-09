from fastapi import FastAPI
from shared import mecab

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/to-hiragana/")
async def to_hiragana(name,n=1):
    data=mecab.to_hiragana(name,n=n)
    data=map(lambda dat:{
        "Name":name,
        "Yomi":dat,
    },data)
    return {
        "result":list(data)
    }
