# ドキュメント更新ガイド

## ドキュメント管理の原則

### 常に最新状態を維持
- コード変更と同時にドキュメント更新
- 新機能追加時のドキュメント作成
- 廃止機能の削除・マーク
- APIの変更に伴う更新

### ユーザー視点での記述
- 技術的詳細よりも使用方法重視
- 具体的な例やサンプルコード
- トラブルシューティング情報
- よくある質問（FAQ）

## 更新対象ドキュメント

### プロジェクトルートドキュメント
- **README.md**: プロジェクト概要、セットアップ手順
- **CHANGELOG.md**: 変更履歴、リリースノート
- **CONTRIBUTING.md**: 開発者向けガイド
- **LICENSE**: ライセンス情報

### 技術ドキュメント
- **API仕様書**: エンドポイント、パラメータ、レスポンス
- **アーキテクチャドキュメント**: システム設計、データフロー
- **デプロイメントガイド**: 本番環境へのデプロイ手順
- **セキュリティドキュメント**: セキュリティ考慮事項

### コード内ドキュメント
- **docstring**: 関数・クラスの説明
- **インラインコメント**: 複雑なロジックの説明
- **型ヒント**: 引数・戻り値の型情報
- **設定ファイルのコメント**: 設定項目の説明

## README.md 更新ガイド

### 基本構成
```markdown
# プロジェクト名

## 概要
プロジェクトの簡潔な説明

## 機能
- 主要機能のリスト
- スクリーンショットやデモGIF

## セットアップ
### 必要な環境
### インストール手順
### 設定方法

## 使用方法
### 基本的な使い方
### サンプルコード
### 詳細オプション

## API仕様
### エンドポイント一覧
### 認証方法
### レスポンス形式

## 開発
### 開発環境セットアップ
### テスト実行方法
### ビルド手順

## トラブルシューティング
### よくある問題と解決方法
### ログの確認方法
### サポート連絡先

## ライセンス
## 貢献者
## 変更履歴
```

### Streamlit アプリ向け追加項目
```markdown
## デモ
- ライブデモURL
- デモ動画やGIF

## データ要件
- 入力データ形式
- サンプルデータの場所
- データ前処理の必要性

## デプロイメント
- Streamlit Cloud デプロイ手順
- Docker コンテナでの実行
- 環境変数設定

## カスタマイズ
- テーマ設定
- 設定ファイルの変更
- プラグイン追加
```

## API ドキュメント更新

### エンドポイント記述例
```markdown
### GET /api/data
データを取得します。

**パラメータ:**
- `limit` (optional): 取得件数の上限 (default: 100)
- `offset` (optional): 取得開始位置 (default: 0)
- `format` (optional): データ形式 [json, csv] (default: json)

**レスポンス:**
```json
{
  "status": "success",
  "data": [
    {
      "id": 1,
      "name": "sample",
      "created_at": "2023-01-01T00:00:00Z"
    }
  ],
  "total": 150,
  "limit": 100,
  "offset": 0
}
```

**エラーレスポンス:**
- `400 Bad Request`: 不正なパラメータ
- `404 Not Found`: データが見つからない
- `500 Internal Server Error`: サーバーエラー
```

### 関数ドキュメント例
```python
def process_data(data: pd.DataFrame, 
                 method: str = 'mean',
                 columns: Optional[List[str]] = None) -> pd.DataFrame:
    """データを処理します.
    
    Args:
        data: 処理対象のDataFrame
        method: 処理方法 ('mean', 'median', 'sum' のいずれか)
        columns: 処理対象の列名リスト (Noneの場合全列)
        
    Returns:
        処理済みのDataFrame
        
    Raises:
        ValueError: 不正なmethodが指定された場合
        KeyError: 指定された列が存在しない場合
        
    Example:
        >>> df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
        >>> result = process_data(df, method='mean')
        >>> print(result)
           A    B
        0  2.0  5.0
    """
```

## チェンジログ更新

### 形式
```markdown
# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]
### Added
- 新機能の説明
### Changed
- 変更された機能の説明
### Deprecated
- 廃止予定の機能
### Removed
- 削除された機能
### Fixed
- 修正されたバグ
### Security
- セキュリティに関する修正

## [1.2.0] - 2023-12-01
### Added
- CSVファイルアップロード機能
- データフィルタリング機能
- エクスポート機能

### Fixed
- グラフ表示のメモリリーク問題
- セッション状態の不整合問題
```

## ドキュメント品質チェック

### 内容の妥当性
- [ ] 最新コードとの整合性
- [ ] 手順の実行可能性
- [ ] サンプルコードの動作確認
- [ ] リンクの有効性

### 読みやすさ
- [ ] 構成の論理性
- [ ] 見出しの階層化
- [ ] コードブロックの適切な使用
- [ ] 図表の活用

### 完全性
- [ ] 必要な情報の網羅
- [ ] エラーケースの説明
- [ ] 前提条件の明記
- [ ] 参考資料の提供

## 自動化ツール

### ドキュメント生成
```python
# docs/generate_api_docs.py
import inspect
import sys
sys.path.append('..')

from your_module import your_function

def generate_function_docs(func):
    """関数のドキュメントを自動生成"""
    signature = inspect.signature(func)
    docstring = inspect.getdoc(func)
    
    docs = f"### {func.__name__}\n"
    docs += f"```python\n{func.__name__}{signature}\n```\n"
    if docstring:
        docs += f"{docstring}\n"
    
    return docs
```

### リンクチェック
```bash
# scripts/check_links.sh
#!/bin/bash

# README内のリンクをチェック
markdown-link-check README.md

# 全markdownファイルのリンクをチェック
find . -name "*.md" -exec markdown-link-check {} \;
```

### 自動更新スクリプト
```python
# scripts/update_version.py
import re
import sys

def update_version_in_docs(new_version):
    """ドキュメント内のバージョン情報を更新"""
    files_to_update = [
        'README.md',
        'docs/installation.md',
        'pyproject.toml'
    ]
    
    for file_path in files_to_update:
        with open(file_path, 'r') as f:
            content = f.read()
        
        # バージョン番号を更新
        content = re.sub(
            r'version\s*=\s*"[\d\.]+"',
            f'version = "{new_version}"',
            content
        )
        
        with open(file_path, 'w') as f:
            f.write(content)
```

## メンテナンススケジュール

### 定期更新タスク
- **毎リリース**: CHANGELOG.md更新、バージョン情報更新
- **月次**: README.mdの内容確認、リンクチェック
- **四半期**: 全ドキュメントの見直し、構成の最適化
- **年次**: アーキテクチャドキュメントの大幅更新

### 更新トリガー
- 新機能リリース時
- APIの変更時
- バグ修正時
- セキュリティアップデート時
- ユーザーからのフィードバック受領時

## 多言語対応

### 国際化対応
```
docs/
├── en/          # 英語版
│   ├── README.md
│   └── api.md
├── ja/          # 日本語版
│   ├── README.md
│   └── api.md
└── template/    # テンプレート
    ├── README.template.md
    └── api.template.md
```

### 翻訳管理
- 原文（日本語）の更新
- 翻訳版の同期更新
- 翻訳品質の確認
- 文化的適応の考慮