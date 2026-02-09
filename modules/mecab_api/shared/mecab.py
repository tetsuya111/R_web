import subprocess as sp
from tempfile import NamedTemporaryFile
import re

def _process(text,n=None,**params):
    if n:
        params[f"-N{n}"]=""
    params_str=" ".join(map(lambda param:f"{param[0]} {param[1]}",params.items()))
    with NamedTemporaryFile("w+") as tmp:
        tmp.write(text)
        tmp.seek(0)
        command:str=f'cat {tmp.name} | mecab {params_str}'
        encoding="utf8"
        return sp.check_output(command,shell=True).decode(encoding,errors="ignore")

def process(text,**params):
    res=_process(text,**params)
    for line in re.split("\n+",res):
        line=line.strip()
        data=re.split("\t+",line,1)
        if not data:
            continue
        if len(data) == 1:
            yield {
                "data":data
            }
            continue
        word,data=data
        data=re.split(",+",data)
        yield {
            "word":word,
            "data":data

        }

def process2(text,**params):
    res=[]
    for data in process(text,**params):
        if not data.get("word"):
            if data["data"][0] == "EOS":
                yield res
                res=[]
        else:
            res.append(data)

def to_hiragana(text,n=1,**params):
    HIRAGANA_INDEX=5
    params[f"-N{n}"]=""
    def _():
        for res in process2(text,**params):
            res=filter(lambda data:data.get("word"),res)
            res=map(lambda data:data["data"][HIRAGANA_INDEX],res)
            yield "".join(res)
    return set(_())   