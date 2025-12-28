# -*- coding: utf-8 -*-
"""
Menu関連のAPIエンドポイント
"""

from fastapi import APIRouter, HTTPException

from models.menu_models import FeatureListRequest, FeatureListResponse
from services.menu_service import get_feature_list_service

# ルーターを作成
router = APIRouter(prefix="/portal/menu/api", tags=["menu"])


@router.post("/featurelist", response_model=FeatureListResponse)
async def feature_list(request: FeatureListRequest) -> FeatureListResponse:
    """
    機能一覧要求エンドポイント
    
    Args:
        request: 機能一覧要求モデル
    
    Returns:
        FeatureListResponse: 機能一覧応答モデル
    """
    try:
        response: FeatureListResponse = get_feature_list_service(
            user=request.USER,
            seq_number=request.SEQ_NUMBER
        )
        return response
    except Exception as e:
        # 予期しないエラーが発生した場合
        raise HTTPException(
            status_code=500,
            detail=f"サーバーエラーが発生しました: {str(e)}"
        )

