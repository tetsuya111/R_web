# 構築
```bash
$ pip3 install -r requirements.txt
```

# 起動方法
```bash
$ fastapi dev app/main.py
```

# 環境変数
Notionのアクセストークンを`.env`ファイルに記載する
## サンプル
```conf:.env
NOTION_TOKEN=<NOTION_TOKEN>
```

# データの取得法
```bash
$ curl http://127.0.0.1:8000/page/get/md/{page_id}/
```

## 例
```bash
$ curl http://127.0.0.1:8000/page/get/md/30a57039156180c2b702f1c632a60ed1/
```
