# -*- coding: utf-8 -*-
"""
FastAPIアプリケーションの制御部分
"""

from fastapi import FastAPI
from routers import menu

# FastAPIアプリケーションを作成
app = FastAPI(
    title="P52Menu API",
    description="Menu管理API",
    version="1.0.0"
)

# ルーターを登録
app.include_router(menu.router)


@app.get("/")
async def root() -> dict[str, str]:
    """ルートエンドポイント"""
    return {"message": ""}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
