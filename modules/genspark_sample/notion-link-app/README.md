# Notion Link App

Reactで作成されたシンプルなWebアプリケーションです。Notionページへのリンクを提供し、アクセストークンを使用して認証なしでページに遷移できます。

## 機能

- ボタンをクリックしてNotionページに遷移
- アクセストークンを使用した認証（仮の値を使用）
- シンプルで直感的なUI

## 技術スタック

- **React**: UIライブラリ
- **Vite**: ビルドツール
- **CSS**: スタイリング

## セットアップ

### 依存関係のインストール

```bash
npm install
```

### 開発サーバーの起動

```bash
npm run dev
```

アプリケーションは `http://localhost:3000` で起動します。

### ビルド

```bash
npm run build
```

ビルドされたファイルは `dist/` ディレクトリに出力されます。

## 使い方

1. アプリケーションを起動します
2. 「Notionページを開く」ボタンをクリックします
3. 新しいタブでNotionページが開きます

## カスタマイズ

`src/App.jsx` ファイルで以下の値を変更できます:

- `NOTION_ACCESS_TOKEN`: Notionのアクセストークン
- `NOTION_PAGE_ID`: 遷移先のNotionページID

```javascript
const NOTION_ACCESS_TOKEN = 'your_access_token_here'
const NOTION_PAGE_ID = 'your_page_id_here'
```

## 注意事項

- 現在は仮のアクセストークンを使用しています
- 実際の環境では、環境変数や安全な方法でトークンを管理してください
- セキュリティ上、アクセストークンをクライアント側に直接埋め込むことは推奨されません

## ライセンス

ISC
