# -*- coding: utf-8 -*-
"""
環境変数設定モジュール
"""

import os
from typing import Optional
from dotenv import load_dotenv

# .envファイルを読み込む
load_dotenv()


class AuthConfig:
    """認証データベース設定クラス"""
    
    def __init__(self) -> None:
        self.dbhost: str = os.getenv("Auth_dbhost", "")
        dbport_str: Optional[str] = os.getenv("Auth_dbport")
        self.dbport: int = int(dbport_str) if dbport_str else 5432
        self.dbname: str = os.getenv("Auth_dbname", "")
        self.dbuser: str = os.getenv("Auth_dbuser", "")
        self.dbpass: str = os.getenv("Auth_dbpass", "")
    
    def validate(self) -> bool:
        """設定値の検証"""
        return all([
            self.dbhost,
            self.dbport > 0,
            self.dbname,
            self.dbuser,
            self.dbpass
        ])


# グローバル設定インスタンス
auth_config = AuthConfig()

