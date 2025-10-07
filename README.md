# Streamlit データ分析画面 - 生成 AI PoC

## 概要

このプロジェクトは、Python Streamlit を使用した生成 AI の PoC（Proof of Concept）開発を想定したデータ分析画面の実装です。テストデータを用いて、インタラクティブなデータ可視化と分析機能を提供します。

### 主な機能（予定）

- データのアップロードと表示
- インタラクティブなデータ可視化
- 統計情報の表示
- データフィルタリング機能
- 生成 AI との連携機能（予定）

## 技術スタック

- **Python**: 3.8 以上
- **Streamlit**: Web アプリケーションフレームワーク
- **Pandas**: データ分析・処理
- **Plotly/Matplotlib**: データ可視化
- **その他**: 必要に応じて追加

## 初期セットアップ手順

### 1. 前提条件

以下がインストールされていることを確認してください：

- Python 3.8 以上
- pip（Python パッケージマネージャー）

### 2. リポジトリのクローン

```bash
cd /path/to/your/workspace
```

### 3. 仮想環境の作成（推奨）

```bash
# 仮想環境を作成
python -m venv venv

# 仮想環境を有効化
# macOS/Linux:
source venv/bin/activate

# Windows:
# venv\Scripts\activate
```

### 4. 依存パッケージのインストール

```bash
pip install -r requirements.txt
```

### 5. アプリケーションの起動

```bash
streamlit run app.py
```

ブラウザが自動的に開き、`http://localhost:8501` でアプリケーションにアクセスできます。

## Docker を使用した実行

### Docker Compose で起動（推奨）

```bash
# イメージのビルドとコンテナの起動
docker compose up -d

# ログの確認
docker compose logs -f

# 停止
docker compose down
```

### Docker コマンドで起動

```bash
# イメージのビルド
docker build -t streamlit-data-analysis .

# コンテナの実行
docker run -p 8501:8501 streamlit-data-analysis

# Docker Hub からプル（リリース版）
docker pull nishibu97/streamlit-data-analysis:latest
docker run -p 8501:8501 nishibu97/streamlit-data-analysis:latest
```

アプリケーションは `http://localhost:8501` でアクセス可能です。

## プロジェクト構造

```
Streamlit/
│
├── README.md              # プロジェクトドキュメント
├── requirements.txt       # 依存パッケージリスト
├── app.py                # メインアプリケーションファイル
├── data/                 # テストデータディレクトリ
│   └── sample_data.csv
├── components/           # UIコンポーネント（予定）
│   └── __init__.py
└── utils/               # ユーティリティ関数（予定）
    └── __init__.py
```

## 開発環境

### 開発用依存関係のインストール

```bash
pip install -r requirements-dev.txt
```

### エディタ推奨設定

- VS Code + Python 拡張機能
- PyCharm

### コーディング規約

- PEP 8 に準拠
- 関数・クラスには適切な docstring を記載

### コード品質チェック

```bash
# Lint チェック
ruff check .

# フォーマットチェック
black --check .

# 型チェック
mypy . --config-file=pyproject.toml

# テスト実行
pytest tests/ -v

# カバレッジ付きテスト
pytest tests/ --cov=. --cov-report=html
```

## CI/CD パイプライン

このプロジェクトは GitHub Actions を使用した CI/CD パイプラインを実装しています。

### CI (継続的インテグレーション)

**トリガー**: `main`, `develop`, `feature/**` ブランチへの push、または PR

- **マルチバージョンテスト**: Python 3.10, 3.11, 3.12
- **コード品質チェック**: ruff, black, mypy
- **テスト実行**: pytest + カバレッジ
- **セキュリティチェック**: safety, bandit
- **カバレッジレポート**: Codecov へ自動アップロード

### CD (継続的デプロイ)

**トリガー**: `v*.*.*` 形式のタグ push

- Docker イメージのビルド（マルチアーキテクチャ: amd64, arm64）
- Docker Hub および GitHub Container Registry へ push
- GitHub Release の自動作成

### リリース手順

```bash
# バージョンタグを作成
git tag v1.0.0
git push origin v1.0.0

# 自動的に以下が実行されます：
# 1. Docker イメージのビルド
# 2. Docker Hub / GHCR へのプッシュ
# 3. GitHub Release の作成
```

### 必要な GitHub Secrets

CI/CD パイプラインを使用するには、以下の Secrets を設定してください：

- `DOCKER_USERNAME`: Docker Hub ユーザー名
- `DOCKER_PASSWORD`: Docker Hub パスワード/アクセストークン
- `CODECOV_TOKEN`: Codecov トークン（オプション）

## トラブルシューティング

### Streamlit が起動しない場合

```bash
# Streamlitのバージョン確認
streamlit version

# パッケージの再インストール
pip install --upgrade streamlit
```

### ポート 8501 が使用中の場合

```bash
streamlit run app.py --server.port 8502
```

## 今後の拡張予定

- [ ] CSV データのアップロード機能
- [ ] 複数のグラフタイプでのデータ可視化
- [ ] 生成 AI モデルとの連携
- [ ] データの前処理機能
- [ ] レポート出力機能

## 参考リソース

- [Streamlit 公式ドキュメント](https://docs.streamlit.io/)
- [Streamlit Gallery](https://streamlit.io/gallery)
- [Pandas Documentation](https://pandas.pydata.org/docs/)

## ライセンス

このプロジェクトは学習・キャッチアップ目的で作成されています。

## 作成者

- キャッチアップ用プロジェクト

---

**Note**: このプロジェクトは学習目的で作成されており、本番環境での使用は想定していません。
