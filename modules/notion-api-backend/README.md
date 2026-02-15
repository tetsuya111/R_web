# Notion API Backend 🚀

FastAPIベースのNotion API連携バックエンドサービス

## 概要

このプロジェクトは、Notion APIと連携してページデータを取得するRESTful APIバックエンドです。
FastAPIを使用して高速かつ型安全なAPIを提供します。

## 機能

- ✅ Notion APIからページデータを取得
- ✅ アクセストークンによる認証
- ✅ POST/GETの両方のメソッドをサポート
- ✅ 自動生成されるAPIドキュメント（Swagger UI / ReDoc）
- ✅ CORS対応（フロントエンドからのアクセス可能）
- ✅ エラーハンドリング
- ✅ ヘルスチェックエンドポイント

## 技術スタック

- **Python**: 3.9+
- **FastAPI**: 高速なWeb APIフレームワーク
- **Uvicorn**: ASGI サーバー
- **httpx**: 非同期HTTPクライアント
- **Pydantic**: データバリデーション

## セットアップ

### 1. 依存関係のインストール

```bash
pip install -r requirements.txt
```

### 2. 環境変数の設定

`.env.example` をコピーして `.env` を作成:

```bash
cp .env.example .env
```

`.env` ファイルを編集して、Notion APIトークンを設定:

```env
NOTION_API_TOKEN=your_actual_notion_api_token_here
```

#### Notion APIトークンの取得方法

1. [Notion Integrations](https://www.notion.so/my-integrations) にアクセス
2. 「New integration」をクリック
3. Integration名を入力して作成
4. 「Internal Integration Token」をコピー
5. `.env` ファイルに貼り付け

### 3. サーバーの起動

```bash
# 開発モード（自動リロード有効）
python main.py

# または uvicorn を直接使用
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

サーバーは `http://localhost:8000` で起動します。

## API エンドポイント

### ルート

```
GET /
```

APIの基本情報を返します。

**レスポンス例:**
```json
{
  "message": "Notion API Backend",
  "version": "1.0.0",
  "docs": "/docs",
  "health": "/health"
}
```

### ヘルスチェック

```
GET /health
```

サービスの健全性を確認します。

**レスポンス例:**
```json
{
  "status": "healthy",
  "message": "Notion API Backend is running",
  "notion_api_configured": true
}
```

### Notionページ取得（POST）

```
POST /api/notion/page
Content-Type: application/json
```

**リクエストボディ:**
```json
{
  "page_id": "12345678-1234-1234-1234-123456789abc"
}
```

**レスポンス例:**
```json
{
  "success": true,
  "data": {
    "object": "page",
    "id": "12345678-1234-1234-1234-123456789abc",
    "created_time": "2024-01-01T00:00:00.000Z",
    "last_edited_time": "2024-01-02T00:00:00.000Z",
    "properties": { ... },
    ...
  },
  "error": null
}
```

### Notionページ取得（GET）

```
GET /api/notion/page/{page_id}
```

**パスパラメータ:**
- `page_id`: NotionページのID（ハイフンあり/なし両方対応）

**レスポンス例:**
```json
{
  "success": true,
  "data": {
    "object": "page",
    "id": "12345678-1234-1234-1234-123456789abc",
    ...
  },
  "error": null
}
```

## API ドキュメント

サーバー起動後、以下のURLでインタラクティブなAPIドキュメントにアクセスできます:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 使用例

### cURLでの使用例

```bash
# POST メソッド
curl -X POST "http://localhost:8000/api/notion/page" \
  -H "Content-Type: application/json" \
  -d '{"page_id": "12345678-1234-1234-1234-123456789abc"}'

# GET メソッド
curl "http://localhost:8000/api/notion/page/12345678-1234-1234-1234-123456789abc"
```

### Pythonでの使用例

```python
import requests

# POST メソッド
response = requests.post(
    "http://localhost:8000/api/notion/page",
    json={"page_id": "12345678-1234-1234-1234-123456789abc"}
)
data = response.json()
print(data)

# GET メソッド
response = requests.get(
    "http://localhost:8000/api/notion/page/12345678-1234-1234-1234-123456789abc"
)
data = response.json()
print(data)
```

### JavaScriptでの使用例

```javascript
// POST メソッド
const response = await fetch('http://localhost:8000/api/notion/page', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    page_id: '12345678-1234-1234-1234-123456789abc'
  })
});
const data = await response.json();
console.log(data);

// GET メソッド
const response = await fetch(
  'http://localhost:8000/api/notion/page/12345678-1234-1234-1234-123456789abc'
);
const data = await response.json();
console.log(data);
```

## エラーハンドリング

APIは以下のHTTPステータスコードを返します:

- **200**: 成功
- **404**: ページが見つからない
- **401**: 認証エラー（無効なトークン）
- **500**: サーバー内部エラー
- **503**: Notion APIへの接続エラー
- **504**: タイムアウト

**エラーレスポンス例:**
```json
{
  "success": false,
  "data": null,
  "error": "ページが見つかりません: 12345678-1234-1234-1234-123456789abc"
}
```

## プロジェクト構成

```
notion-api-backend/
├── main.py              # メインアプリケーションファイル
├── requirements.txt     # Python依存関係
├── .env                 # 環境変数（秘密情報）
├── .env.example         # 環境変数テンプレート
├── .gitignore           # Git除外設定
└── README.md            # このファイル
```

## 開発

### テスト

```bash
# ヘルスチェック
curl http://localhost:8000/health

# ページ取得テスト
curl -X POST http://localhost:8000/api/notion/page \
  -H "Content-Type: application/json" \
  -d '{"page_id": "your-page-id"}'
```

### デバッグ

FastAPIは自動的に詳細なエラーログを出力します。
追加のログが必要な場合は、`main.py` にロギング設定を追加してください。

## 本番環境へのデプロイ

### Docker を使用する場合

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### systemd サービスとして実行

```ini
[Unit]
Description=Notion API Backend
After=network.target

[Service]
User=www-data
WorkingDirectory=/path/to/notion-api-backend
ExecStart=/usr/bin/python3 main.py
Restart=always

[Install]
WantedBy=multi-user.target
```

## セキュリティ考慮事項

- ⚠️ **本番環境では以下の対策を必ず実施してください:**
  - `.env` ファイルを Git にコミットしない
  - CORS設定を特定のオリジンのみに制限
  - HTTPS を使用
  - レート制限の実装
  - アクセスログの記録

## ライセンス

MIT License

## 作者

Amazon イケイケ天才プログラマー 💪⚡

## サポート

問題が発生した場合は、GitHub Issues で報告してください。
