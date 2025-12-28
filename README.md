# P52Menu API

FastAPIで実装されたMenu管理Web APIです。

## 概要

P52Menu APIは、ユーザー認証と機能一覧取得を提供するRESTful APIです。PostgreSQLデータベースを使用してユーザー認証と機能情報を管理します。

## 必要な環境

- Python 3.10以上
- PostgreSQLデータベース

## セットアップ

### 1. リポジトリのクローン

```bash
git clone <repository-url>
cd p52Menu
```

### 2. 仮想環境の作成と有効化

```bash
# Windows
python -m venv env
env\Scripts\activate

# Linux/Mac
python3 -m venv env
source env/bin/activate
```

### 3. 依存パッケージのインストール

```bash
pip install -r requirements.txt
```

### 4. 環境変数の設定

`env.template`をコピーして`.env`ファイルを作成し、データベース接続情報を設定してください。

```bash
# Windows
copy env.template .env

# Linux/Mac
cp env.template .env
```

`.env`ファイルを編集して、以下の値を設定します：

```env
Auth_dbhost=localhost
Auth_dbport=5432
Auth_dbname=your_database
Auth_dbuser=your_user
Auth_dbpass=your_password
```

## 実行方法

### 開発サーバーの起動

```bash
python main.py
```

または、uvicornを直接使用：

```bash
uvicorn main:app --host 0.0.0.0 --port 8001 --reload
```

サーバーが起動すると、以下のURLでアクセスできます：

- API: http://localhost:8001
- APIドキュメント（Swagger UI）: http://localhost:8001/docs
- APIドキュメント（ReDoc）: http://localhost:8001/redoc

## APIエンドポイント

### 機能一覧要求

**エンドポイント:** `POST /portal/menu/api/featurelist`

**説明:** ユーザー認証を延長し、利用可能な機能一覧を取得します。

**リクエストボディ:**

```json
{
  "USER": "string",
  "SEQ_NUMBER": 123456
}
```

| 項目名 | 型 | 説明 |
|:---:|--- |--- |
| USER | string | 試行ユーザ名 |
| SEQ_NUMBER | number | シーケンス管理ナンバ |

**レスポンス:**

```json
{
  "RESULT": true,
  "DETAIL": "",
  "SEQ_NUMBER": 123456,
  "FEATURES": [
    {
      "NAME": "機能名",
      "URL": "https://example.com/feature",
      "ICON_DATA": "base64encodedstring",
      "ICON_TYPE": "image/png",
      "ORDER": 1
    }
  ]
}
```

| 項目名 | 型 | 説明 |
|:---:|--- |--- |
| RESULT | boolean | 結果(True/False) |
| DETAIL | string | 結果がFalseだった場合に詳細情報を設定 |
| SEQ_NUMBER | number | シーケンス管理ナンバ |
| FEATURES | list | 機能に関する情報を設定 |
| FEATURES.NAME | string | 機能名 |
| FEATURES.URL | string | URL |
| FEATURES.ICON_DATA | string | ICONデータ(BASE64) |
| FEATURES.ICON_TYPE | string | ICONデータの形式 |
| FEATURES.ORDER | number | 表示順 |

**エラーレスポンス例:**

```json
{
  "RESULT": false,
  "DETAIL": "認証不正または該当なし",
  "SEQ_NUMBER": -2,
  "FEATURES": []
}
```

## プロジェクト構成

```
p52Menu/
├── main.py                    # 制御部分（FastAPIアプリの初期化とルーター登録）
├── config.py                  # 環境変数設定モジュール
├── requirements.txt           # 依存パッケージ一覧
├── env.template               # 環境変数テンプレート
├── routers/                   # APIエンドポイント（ルーティング）
│   ├── __init__.py
│   └── menu.py               # Menu関連のAPIエンドポイント
├── services/                  # 業務ロジック
│   ├── __init__.py
│   └── menu_service.py       # Menu関連の業務ロジック
├── models/                    # リクエスト/レスポンスモデル
│   ├── __init__.py
│   └── menu_models.py        # Menu関連のモデル
└── comlibs/                   # 共通ライブラリ
     ├── authorize.py          # Authorizeクラス
     └── requirements.txt
```

## 技術スタック

- **FastAPI**: モダンなPython Webフレームワーク
- **Pydantic**: データバリデーション
- **PostgreSQL**: データベース（psycopg2経由）
- **Uvicorn**: ASGIサーバー
- **python-dotenv**: 環境変数管理

## 開発

### 型ヒント

本プロジェクトでは、Pythonの型ヒントを積極的に使用しています。すべての関数、メソッド、変数に適切な型アノテーションを付与しています。

### コードスタイル

- PEP 8に準拠
- 型ヒントの使用を推奨
- docstringによるドキュメント化

## ライセンス

（ライセンス情報を記載してください）

## 作者

（作者情報を記載してください）

