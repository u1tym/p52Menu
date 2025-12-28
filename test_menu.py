# -*- coding: utf-8 -*-
"""
Menu API テストコード

期待値と合っているかを画面に表示
送信内容と受信内容を画面に表示
"""

import json
import zlib
from typing import Optional, Dict, Any
import requests


# ============================================================================
# 補助処理
# ============================================================================

def calculate_hash_pass(upass: str, magic: int) -> str:
    """
    補助処理１: ハッシュパス算出処理
    
    Args:
        upass: パスワード
        magic: マジックナンバ
    
    Returns:
        str: ハッシュ化パスワード
    """
    combined: str = f"{upass}{magic}"
    hash_pass: str = format(zlib.crc32(combined.encode()) & 0xFFFFFFFF, '08x')
    return hash_pass


def login(user: str, password: str, auth_host: str = "localhost", auth_port: int = 8000) -> Optional[int]:
    """
    補助処理２: ログイン処理
    
    Args:
        user: ユーザ名
        password: パスワード
        auth_host: 認証APIのホスト（デフォルト: localhost）
        auth_port: 認証APIのポート（デフォルト: 8000）
    
    Returns:
        Optional[int]: シーケンス管理ナンバ（失敗時はNone）
    """
    base_url: str = f"http://{auth_host}:{auth_port}"
    
    # プレ要求
    print(f"\n{'='*60}")
    print("【プレ要求】")
    print(f"{'='*60}")
    prerequest_url: str = f"{base_url}/portal/auth/api/prerequest"
    prerequest_data: Dict[str, str] = {
        "USER": user
    }
    print(f"URL: {prerequest_url}")
    print(f"送信内容: {json.dumps(prerequest_data, ensure_ascii=False, indent=2)}")
    
    try:
        prerequest_response = requests.post(prerequest_url, json=prerequest_data)
        prerequest_response.raise_for_status()
        prerequest_result: Dict[str, Any] = prerequest_response.json()
        print(f"受信内容: {json.dumps(prerequest_result, ensure_ascii=False, indent=2)}")
        
        if not prerequest_result.get("RESULT", False):
            print(f"プレ要求失敗: {prerequest_result.get('DETAIL', '不明なエラー')}")
            return None
        
        magic_number: int = prerequest_result.get("MAGIC_NUMBER")
        if magic_number is None:
            print("プレ応答にMAGIC_NUMBERが含まれていません")
            return None
        
        # 開錠要求
        print(f"\n{'='*60}")
        print("【開錠要求】")
        print(f"{'='*60}")
        unlock_url: str = f"{base_url}/portal/auth/api/unlock"
        hash_pass: str = calculate_hash_pass(password, magic_number)
        unlock_data: Dict[str, Any] = {
            "USER": user,
            "MAGIC_NUMBER": magic_number,
            "HASH_PASS": hash_pass
        }
        print(f"URL: {unlock_url}")
        print(f"送信内容: {json.dumps(unlock_data, ensure_ascii=False, indent=2)}")
        print(f"計算したHASH_PASS: {hash_pass}")
        
        unlock_response = requests.post(unlock_url, json=unlock_data)
        unlock_response.raise_for_status()
        unlock_result: Dict[str, Any] = unlock_response.json()
        print(f"受信内容: {json.dumps(unlock_result, ensure_ascii=False, indent=2)}")
        
        if not unlock_result.get("RESULT", False):
            print(f"開錠要求失敗: {unlock_result.get('DETAIL', '不明なエラー')}")
            return None
        
        seq_number: int = unlock_result.get("SEQ_NUMBER")
        if seq_number is None:
            print("開錠応答にSEQ_NUMBERが含まれていません")
            return None
        
        print(f"\nログイン成功: seq_number = {seq_number}")
        return seq_number
        
    except requests.exceptions.RequestException as e:
        print(f"HTTPリクエストエラー: {e}")
        return None
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        return None


# ============================================================================
# テストケース
# ============================================================================

def test_feature_list(
    user: str,
    seq_number: Optional[int],
    expected_result: bool,
    test_name: str,
    menu_host: str = "localhost",
    menu_port: int = 8001
) -> bool:
    """
    機能一覧要求のテスト
    
    Args:
        user: ユーザ名
        seq_number: シーケンス管理ナンバ（Noneの場合は0を送信）
        expected_result: 期待される結果（True: 正常, False: 異常）
        test_name: テスト名
        menu_host: Menu APIのホスト（デフォルト: localhost）
        menu_port: Menu APIのポート（デフォルト: 8001）
    
    Returns:
        bool: テストが期待値通りかどうか
    """
    print(f"\n{'#'*60}")
    print(f"【テスト】{test_name}")
    print(f"{'#'*60}")
    
    base_url: str = f"http://{menu_host}:{menu_port}"
    featurelist_url: str = f"{base_url}/portal/menu/api/featurelist"
    
    # リクエストデータ
    request_data: Dict[str, Any] = {
        "USER": user,
        "SEQ_NUMBER": seq_number if seq_number is not None else 0
    }
    
    print(f"\n{'='*60}")
    print("【機能一覧要求】")
    print(f"{'='*60}")
    print(f"URL: {featurelist_url}")
    print(f"送信内容: {json.dumps(request_data, ensure_ascii=False, indent=2)}")
    
    try:
        response = requests.post(featurelist_url, json=request_data)
        response.raise_for_status()
        result: Dict[str, Any] = response.json()
        print(f"受信内容: {json.dumps(result, ensure_ascii=False, indent=2)}")
        
        # 結果の検証
        actual_result: bool = result.get("RESULT", False)
        print(f"\n{'='*60}")
        print("【検証結果】")
        print(f"{'='*60}")
        print(f"期待値: RESULT = {expected_result}")
        print(f"実際値: RESULT = {actual_result}")
        
        if actual_result == expected_result:
            print("✓ 期待値と一致しています")
            
            if expected_result:
                # 正常の場合の追加検証
                new_seq_number: int = result.get("SEQ_NUMBER", 0)
                features: list = result.get("FEATURES", [])
                print(f"新しいSEQ_NUMBER: {new_seq_number}")
                print(f"機能一覧の件数: {len(features)}")
                if new_seq_number > 0:
                    print("✓ 新しいSEQ_NUMBERが取得できました")
                else:
                    print("✗ 新しいSEQ_NUMBERが0以下です")
                    return False
                if len(features) > 0:
                    print("✓ 機能一覧が取得できました")
                else:
                    print("⚠ 機能一覧が空です")
            else:
                # 異常の場合の詳細表示
                detail: str = result.get("DETAIL", "")
                print(f"エラー詳細: {detail}")
            
            return True
        else:
            print("✗ 期待値と一致していません")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"HTTPリクエストエラー: {e}")
        if expected_result:
            print("✗ 期待値（正常）と実際（エラー）が一致していません")
            return False
        else:
            print("⚠ エラーが発生しましたが、期待値（異常）と一致する可能性があります")
            return True
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        return False


# ============================================================================
# メイン処理
# ============================================================================

def main() -> None:
    """メイン処理"""
    print("="*60)
    print("Menu API テスト開始")
    print("="*60)
    
    # テスト1: USER=xxxx で異常が返ることを確認
    print("\n" + "="*60)
    print("テスト1: USER=xxxx で異常が返ることを確認")
    print("="*60)
    test1_result: bool = test_feature_list(
        user="xxxx",
        seq_number=0,
        expected_result=False,
        test_name="テスト1: USER=xxxx（異常期待）"
    )
    
    # テスト2: USER=admin で異常が返ることを確認（SEQ_NUMBERなし）
    print("\n" + "="*60)
    print("テスト2: USER=admin で異常が返ることを確認（SEQ_NUMBERなし）")
    print("="*60)
    test2_result: bool = test_feature_list(
        user="admin",
        seq_number=0,
        expected_result=False,
        test_name="テスト2: USER=admin（異常期待）"
    )
    
    # テスト3: USER=admin, SEQ_NUMBER=準備で取得したseq_number で正常が返ることを確認
    print("\n" + "="*60)
    print("テスト3: USER=admin, SEQ_NUMBER=準備で取得したseq_number で正常が返ることを確認")
    print("="*60)
    
    # 準備: ログイン処理
    print("\n【準備】ログイン処理を実施")
    seq_number: Optional[int] = login(user="admin", password="admin")
    
    if seq_number is None:
        print("✗ ログインに失敗したため、テスト3をスキップします")
        test3_result: bool = False
    else:
        test3_result: bool = test_feature_list(
            user="admin",
            seq_number=seq_number,
            expected_result=True,
            test_name="テスト3: USER=admin, SEQ_NUMBER=準備で取得（正常期待）"
        )
    
    # テスト結果のサマリー
    print("\n" + "="*60)
    print("【テスト結果サマリー】")
    print("="*60)
    print(f"テスト1: {'✓ 成功' if test1_result else '✗ 失敗'}")
    print(f"テスト2: {'✓ 成功' if test2_result else '✗ 失敗'}")
    print(f"テスト3: {'✓ 成功' if test3_result else '✗ 失敗'}")
    
    all_passed: bool = test1_result and test2_result and test3_result
    print(f"\n全体結果: {'✓ すべてのテストが成功しました' if all_passed else '✗ 一部のテストが失敗しました'}")
    print("="*60)


if __name__ == "__main__":
    main()

