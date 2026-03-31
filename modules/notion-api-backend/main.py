"""
Notion API Backend
==================
FastAPIベースのNotion API連携バックエンド

主な機能:
- Notion APIからページデータを取得
- アクセストークンによる認証
- RESTful APIエンドポイントの提供
"""

from fastapi import FastAPI, HTTPException, Header, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
import httpx
import os
from dotenv import load_dotenv

# 環境変数の読み込み
load_dotenv()

# FastAPIアプリケーションの初期化
app = FastAPI(
    title="Notion API Backend",
    description="Notion APIからページデータを取得するバックエンドAPI",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS設定（フロントエンドからのアクセスを許可）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 本番環境では特定のオリジンのみ許可
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 定数
NOTION_API_VERSION = "2022-06-28"
NOTION_API_BASE_URL = "https://api.notion.com/v1"
NOTION_API_TOKEN = os.getenv("NOTION_API_TOKEN", "secret_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")


# リクエスト/レスポンスモデル
class PageRequest(BaseModel):
    """ページ取得リクエストモデル"""
    page_id: str = Field(
        ...,
        description="Notionページのユニークなidentifier（ハイフンあり/なし両方対応）",
        example="12345678-1234-1234-1234-123456789abc"
    )


class PageResponse(BaseModel):
    """ページ取得レスポンスモデル"""
    success: bool = Field(description="API呼び出しが成功したかどうか")
    data: Optional[Dict[str, Any]] = Field(None, description="Notionページのデータ")
    error: Optional[str] = Field(None, description="エラーメッセージ（エラー時のみ）")


class HealthResponse(BaseModel):
    """ヘルスチェックレスポンスモデル"""
    status: str = Field(description="サービスのステータス")
    message: str = Field(description="メッセージ")
    notion_api_configured: bool = Field(description="Notion APIトークンが設定されているか")


# ユーティリティ関数
def normalize_page_id(page_id: str) -> str:
    """
    ページIDを正規化（ハイフンを除去）
    
    Args:
        page_id: Notion ページID
        
    Returns:
        正規化されたページID
    """
    return page_id.replace("-", "")


async def fetch_notion_page(page_id: str, token: str) -> Dict[str, Any]:
    """
    Notion APIからページデータを取得
    
    Args:
        page_id: NotionページID
        token: Notion APIアクセストークン
        
    Returns:
        ページデータの辞書
        
    Raises:
        HTTPException: API呼び出しが失敗した場合
    """
    normalized_id = normalize_page_id(page_id)
    url = f"{NOTION_API_BASE_URL}/pages/{normalized_id}"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Notion-Version": NOTION_API_VERSION,
        "Content-Type": "application/json"
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"ページが見つかりません: {page_id}"
                )
            elif response.status_code == 401:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Notion APIトークンが無効です"
                )
            else:
                error_detail = response.json() if response.text else "不明なエラー"
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Notion API エラー: {error_detail}"
                )
                
        except httpx.TimeoutException:
            raise HTTPException(
                status_code=status.HTTP_504_GATEWAY_TIMEOUT,
                detail="Notion APIへのリクエストがタイムアウトしました"
            )
        except httpx.RequestError as e:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Notion APIへの接続エラー: {str(e)}"
            )


# APIエンドポイント
@app.get("/", response_model=Dict[str, str])
async def root():
    """
    ルートエンドポイント
    
    Returns:
        APIの基本情報
    """
    return {
        "message": "Notion API Backend",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """
    ヘルスチェックエンドポイント
    
    Returns:
        サービスの健全性情報
    """
    token_configured = bool(NOTION_API_TOKEN and NOTION_API_TOKEN != "secret_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    
    return HealthResponse(
        status="healthy",
        message="Notion API Backend is running",
        notion_api_configured=token_configured
    )


@app.post("/api/notion/page", response_model=PageResponse, status_code=status.HTTP_200_OK)
async def get_notion_page(request: PageRequest):
    """
    Notionページのデータを取得
    
    Args:
        request: ページIDを含むリクエストボディ
        
    Returns:
        ページデータを含むレスポンス
        
    Raises:
        HTTPException: ページ取得に失敗した場合
    """
    try:
        # Notion APIからページデータを取得
        page_data = await fetch_notion_page(request.page_id, NOTION_API_TOKEN)
        
        return PageResponse(
            success=True,
            data=page_data,
            error=None
        )
        
    except HTTPException as e:
        # HTTPExceptionはそのまま再送出
        raise e
    except Exception as e:
        # その他の予期しないエラー
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"内部サーバーエラー: {str(e)}"
        )


@app.get("/api/notion/page/{page_id}", response_model=PageResponse, status_code=status.HTTP_200_OK)
async def get_notion_page_by_id(page_id: str):
    """
    Notionページのデータを取得（GETメソッド）
    
    Args:
        page_id: NotionページID（パスパラメータ）
        
    Returns:
        ページデータを含むレスポンス
        
    Raises:
        HTTPException: ページ取得に失敗した場合
    """
    try:
        # Notion APIからページデータを取得
        page_data = await fetch_notion_page(page_id, NOTION_API_TOKEN)
        
        return PageResponse(
            success=True,
            data=page_data,
            error=None
        )
        
    except HTTPException as e:
        # HTTPExceptionはそのまま再送出
        raise e
    except Exception as e:
        # その他の予期しないエラー
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"内部サーバーエラー: {str(e)}"
        )


# アプリケーション起動時の処理
@app.on_event("startup")
async def startup_event():
    """アプリケーション起動時の処理"""
    print("🚀 Notion API Backend が起動しました")
    print(f"📄 API Docs: http://localhost:8000/docs")
    print(f"🔧 ReDoc: http://localhost:8000/redoc")
    if not NOTION_API_TOKEN or NOTION_API_TOKEN == "secret_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX":
        print("⚠️  警告: 有効なNotion APIトークンが設定されていません")


@app.on_event("shutdown")
async def shutdown_event():
    """アプリケーション終了時の処理"""
    print("👋 Notion API Backend を終了します")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
