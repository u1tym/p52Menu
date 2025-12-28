# -*- coding: utf-8 -*-
"""
Menu関連の業務ロジック
"""

import base64
from typing import List

from comlibs.authorize import Authorize, FeatureInfo as AuthFeatureInfo
from models.menu_models import FeatureInfo, FeatureListResponse
from config import auth_config


def get_feature_list_service(user: str, seq_number: int) -> FeatureListResponse:
    """
    機能一覧取得サービス
    
    Args:
        user: 試行ユーザ名
        seq_number: シーケンス管理ナンバ
    
    Returns:
        FeatureListResponse: 機能一覧応答
    """
    try:
        # Authorizeのインスタンスを生成
        authorize = Authorize(
            dbhost=auth_config.dbhost,
            dbport=auth_config.dbport,
            dbname=auth_config.dbname,
            dbuser=auth_config.dbuser,
            dbpass=auth_config.dbpass
        )
        
        # try_unlock_extend()を呼び出す
        result_seq: int = authorize.try_unlock_extend(user=user, sequence=seq_number)
        
        # 戻り値が負数の場合は異常
        if result_seq < 0:
            detail: str = _get_error_detail(result_seq)
            return FeatureListResponse(
                RESULT=False,
                DETAIL=detail,
                SEQ_NUMBER=result_seq,
                FEATURES=[]
            )
        
        # 正常の場合、get_feature_list()を呼び出す
        feature_list: List[AuthFeatureInfo] = authorize.get_feature_list(user=user)
        
        # FEATURESリストを構築
        features: List[FeatureInfo] = []
        for order, feature in enumerate(feature_list, start=1):
            # ICON_DATAをBASE64エンコード
            icon_data_b64: str = ""
            if feature.get("icon_data") is not None:
                icon_data_b64 = base64.b64encode(feature["icon_data"]).decode("utf-8")
            
            # ICON_TYPEを取得（無い場合は空文字）
            icon_type: str = feature.get("icon_mime_type") or ""
            
            features.append(FeatureInfo(
                NAME=feature["fname"],
                URL=feature["feature_url"],
                ICON_DATA=icon_data_b64,
                ICON_TYPE=icon_type,
                ORDER=order
            ))
        
        return FeatureListResponse(
            RESULT=True,
            DETAIL="",
            SEQ_NUMBER=result_seq,
            FEATURES=features
        )
        
    except Exception as e:
        # 例外が発生した場合
        return FeatureListResponse(
            RESULT=False,
            DETAIL=f"処理中にエラーが発生しました: {str(e)}",
            SEQ_NUMBER=-9,
            FEATURES=[]
        )


def _get_error_detail(error_code: int) -> str:
    """
    エラーコードから詳細メッセージを取得
    
    Args:
        error_code: エラーコード
    
    Returns:
        str: エラー詳細メッセージ
    """
    error_messages: dict[int, str] = {
        -1: "該当ユーザが存在しない",
        -2: "認証不正または該当なし",
        -9: "処理異常"
    }
    return error_messages.get(error_code, f"不明なエラーコード: {error_code}")

