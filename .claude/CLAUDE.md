# Streamlit データ分析画面プロジェクト

## プロジェクト概要

Python Streamlit を使用した生成 AI の PoC 開発プロジェクト。
インタラクティブなデータ可視化と分析機能を提供する。

## 技術スタック

- Python 3.12
- Streamlit (Web アプリケーションフレームワーク)
- Pandas (データ分析・処理)
- Plotly/Matplotlib (データ可視化)

## ディレクトリ構造

```
Streamlit/
├── app.py                 # メインアプリケーション
├── requirements.txt       # 依存パッケージ
├── data/                  # テストデータ
│   └── sample_data.csv
├── components/            # UIコンポーネント
│   └── __init__.py
└── utils/                 # ユーティリティ関数
    └── __init__.py
```

## 開発コマンド

- **起動**: `streamlit run app.py`
- **テスト**: `pytest tests/`
- **Lint**: `ruff check .`
- **フォーマット**: `black .`

## コーディング規約

- PEP 8 に準拠
- 関数・クラスには docstring を記載
- 型ヒントを積極的に使用
- Streamlit のベストプラクティスに従う

## 開発の進め方

1. 機能追加前に実装計画を立てる
2. 小さな単位で実装・テストを繰り返す
3. コミット前にコードフォーマットと型チェックを実行
4. コミットメッセージは Conventional Commits に従う

## ワークキーワード

- **"機能追加"**: `/feature` コマンドを実行
- **"コードレビュー"**: `/review` コマンドを実行
- **"テスト生成"**: `/test-gen` コマンドを実行
- **"ドキュメント更新"**: `/update-docs` コマンドを実行
- **"コミット"**: `/commit` コマンドを実行

## 注意事項

- 仮想環境 (venv) を必ず使用する
- requirements.txt は常に最新に保つ
- サンプルデータは data/ ディレクトリに配置
- 本番環境での使用は想定していない（学習目的）

## 参考リソース

- Streamlit 公式ドキュメント: https://docs.streamlit.io/
- Pandas Documentation: https://pandas.pydata.org/docs/
