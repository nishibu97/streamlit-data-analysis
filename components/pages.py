"""アプリケーションページコンポーネント"""

import streamlit as st


def render_home_page():
    """ホームページの表示"""
    st.title("🏠 ホーム")

    st.markdown(
        """
        ## スポーツ関心度調査 データ分析アプリへようこそ

        このアプリケーションは、男性のスポーツ関心度調査データを分析・可視化するツールです。

        ### 📊 主な機能

        #### データ分析
        - **データ読み込み**: サンプルデータまたは独自のCSVファイルをアップロード
        - **データプレビュー**: データの一覧、統計情報、データ情報を表示
        - **データ可視化**: 4種類のインタラクティブなグラフで分析
          - スポーツ種目別の平均関心度（棒グラフ）
          - 年齢層別の関心度傾向（折れ線グラフ）
          - スポーツ種目間の相関分析（ヒートマップ）
          - 関心度の分布分析（箱ひげ図）
        - **フィルタリング**: 年齢層でデータを絞り込み

        ### 🚀 使い方

        1. 左側のメニューから **📊 データ分析** を選択
        2. サンプルデータを使用するか、独自のCSVファイルをアップロード
        3. サイドバーのフィルターで年齢層を絞り込み
        4. 各種グラフでデータを分析

        ### 📈 データ形式

        アップロードするCSVファイルは以下の形式である必要があります:
        - **必須カラム**: 回答者ID、年齢層
        - **スポーツカラム**: 3つ以上のスポーツ種目（関心度: 1-5）

        ### 💡 ヒント

        - グラフ上にマウスを乗せると詳細情報が表示されます
        - 折れ線グラフでは最大5つのスポーツを選択できます
        - 箱ひげ図でスポーツを選択すると年齢層別の分布が確認できます
        """
    )

    # クイックアクセスボタン
    st.markdown("---")
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("📊 データ分析を開始", use_container_width=True, type="primary"):
            st.session_state.current_page = "analysis"
            st.rerun()

    with col2:
        st.link_button(
            "📖 Streamlit公式ドキュメント",
            "https://docs.streamlit.io/",
            use_container_width=True,
        )

    with col3:
        st.link_button(
            "🐙 GitHubリポジトリ",
            "https://github.com/streamlit/streamlit",
            use_container_width=True,
        )


def render_about_page():
    """Aboutページの表示"""
    st.title("ℹ️ About")

    st.markdown(
        """
        ## アプリケーション情報

        ### 📌 プロジェクト概要

        Python Streamlitを使用した生成AIのPoC開発プロジェクトです。
        インタラクティブなデータ可視化と分析機能を提供します。

        ### 🛠️ 技術スタック

        - **Python**: 3.10+
        - **Streamlit**: 1.28.0+ (Webアプリケーションフレームワーク)
        - **Pandas**: 2.0.0+ (データ分析・処理)
        - **Plotly**: 5.17.0+ (インタラクティブなデータ可視化)
        - **NumPy**: 1.24.0+ (数値計算)

        ### 🎨 デザインシステム

        **カラースキーム**:
        - プライマリブルー: `#1E3A8A`
        - セカンダリブルー: `#3B82F6`
        - ライトブルー: `#60A5FA`, `#93C5FD`
        - 背景: ホワイト/ライトブルーグラデーション

        ### 📂 プロジェクト構成

        ```
        Streamlit/
        ├── app.py                 # メインアプリケーション
        ├── requirements.txt       # 依存パッケージ
        ├── pyproject.toml         # 開発ツール設定
        ├── .gitignore            # Git除外設定
        ├── data/                  # テストデータ
        │   └── sample_data.csv
        ├── components/            # UIコンポーネント
        │   ├── data_analysis.py
        │   ├── sidebar.py
        │   └── pages.py
        ├── utils/                 # ユーティリティ関数
        │   └── data_loader.py
        └── tests/                 # テストコード
            ├── test_data_loader.py
            └── test_data_analysis.py
        ```

        ### 🔧 開発ツール

        - **Ruff**: 高速Python Linter
        - **Black**: コードフォーマッター
        - **pytest**: テストフレームワーク
        - **mypy**: 静的型チェッカー

        ### 📊 テストカバレッジ

        - **utils/data_loader.py**: 100%
        - **全体テスト数**: 26件
        - **テスト実行時間**: 0.06秒

        ### 📝 開発規約

        - PEP 8準拠
        - 関数・クラスにdocstring記載
        - 型ヒントを積極的に使用
        - Streamlitのベストプラクティスに従う

        ### 📄 ライセンス

        このプロジェクトは学習目的で作成されたPoCです。

        ### 👨‍💻 開発者

        Claude Code + 開発チーム

        ---

        **バージョン**: 1.0.0
        **最終更新**: 2025-10-06
        """
    )
