# 構築
```bash
$ cd mecab_api/modules
$ pip install -r requrements.txt
```
# サーバー
## 起動
### コマンド
```bash
$ cd modules/mecab_api/
$ fastapi dev app/main.py
```
## データの取得
## コマンド
```
$ curl http://127.0.0.1:8000/to-hiragana?name=<名前>&n=<取得数> 
```
### 例
```
$ curl "http:///127.0.0.1:8000/to-hiragana/?name=%E5%B1%B1%E7%94%B0%E5%A4%AA%E9%83%8E&n=5"
{"result":[{"Name":"山田太郎","Yomi":"やまだたろう"},{"Name":"山田太郎","Yomi":"やまだふとし*"}]}
```

※名前はurlエンコードする
※取得数は、重複可でデータを取得し、重複を排除した数

## テストコード
```bash
$ cd modules/mecab_api/
$ python3 sample/test_to_hiragana.py <名前> <取得数>
```

### 例

```
$ cd modules/mecab_api/
$ python3 sample/test_to_hiragana.py 山田太郎 5
2026-02-09 19:39:42 [info     ] url : http://localhost:8000/to-hiragana

{'result': [{'Name': '山田太郎', 'Yomi': 'やまだたろう'}, {'Name': '山田太郎', 'Yomi': 'やまだふとし*'}]}

```
