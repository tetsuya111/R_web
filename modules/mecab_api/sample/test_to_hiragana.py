import sys
import structlog

import requests
import urllib.parse as up

logger=structlog.getLogger()

host="localhost"
port="8000"
path="to-hiragana"

name=sys.argv[1]
n=int(sys.argv[2])

base_url=f"http://{host}:{port}/"
url=up.urljoin(base_url,path)

msg=f"url : {url}"
logger.info(msg)

params={
    "name":name,
    "n":n
}

res=requests.get(url,params=params)

print(res.json())
