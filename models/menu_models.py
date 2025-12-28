# -*- coding: utf-8 -*-
"""
Menu関連のリクエスト/レスポンスモデル
"""

from typing import List, Optional
from pydantic import BaseModel, Field


class FeatureListRequest(BaseModel):
    """機能一覧要求モデル"""
    USER: str = Field(..., description="試行ユーザ名")
    SEQ_NUMBER: int = Field(..., description="シーケンス管理ナンバ")


class FeatureInfo(BaseModel):
    """機能情報モデル"""
    NAME: str = Field(..., description="機能名")
    URL: str = Field(..., description="URL")
    ICON_DATA: str = Field(..., description="ICONデータ(BASE64)")
    ICON_TYPE: str = Field(..., description="ICONデータの形式")
    ORDER: int = Field(..., description="表示順")


class FeatureListResponse(BaseModel):
    """機能一覧応答モデル"""
    RESULT: bool = Field(..., description="結果(True/False)")
    DETAIL: str = Field(..., description="結果がFalseだった場合に詳細情報を設定")
    SEQ_NUMBER: int = Field(..., description="シーケンス管理ナンバ")
    FEATURES: List[FeatureInfo] = Field(..., description="機能に関する情報を設定")

