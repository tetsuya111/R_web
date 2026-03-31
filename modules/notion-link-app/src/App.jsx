import React from 'react'
import './App.css'

function App() {
  // 仮のアクセストークン
  const NOTION_ACCESS_TOKEN = 'secret_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
  
  // NotionページのID（例）
  const NOTION_PAGE_ID = '12345678-1234-1234-1234-123456789abc'
  
  // Notionページへのリンク
  const notionPageUrl = `https://www.notion.so/${NOTION_PAGE_ID.replace(/-/g, '')}`
  
  const handleNotionLinkClick = (e) => {
    e.preventDefault()
    
    // アクセストークンを使用してNotionページに遷移
    // 実際の実装では、トークンをヘッダーに含めてAPIリクエストを送信しますが、
    // ここではシンプルに直接ページを開きます
    window.open(notionPageUrl, '_blank')
    
    console.log('Using access token:', NOTION_ACCESS_TOKEN)
  }

  return (
    <div className="app">
      <div className="container">
        <h1>Notion Link App</h1>
        <p className="description">
          下のボタンをクリックすると、Notionページに遷移します。
          <br />
          アクセストークンを使用して認証を行います。
        </p>
        
        <div className="card">
          <h2>Notionページへのリンク</h2>
          <button 
            className="notion-button"
            onClick={handleNotionLinkClick}
          >
            Notionページを開く
          </button>
          
          <div className="info">
            <p>
              <strong>アクセストークン:</strong> {NOTION_ACCESS_TOKEN.substring(0, 20)}...
            </p>
            <p>
              <strong>ページID:</strong> {NOTION_PAGE_ID}
            </p>
          </div>
        </div>
        
        <div className="note">
          <p>
            <strong>注意:</strong> このアプリケーションは仮のアクセストークンを使用しています。
            実際の環境では、環境変数や安全な方法でトークンを管理してください。
          </p>
        </div>
      </div>
    </div>
  )
}

export default App
