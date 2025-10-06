"""Streamlit データ分析アプリケーション メインエントリーポイント"""

import streamlit as st

from components.data_analysis import render_data_analysis_page
from components.pages import render_about_page, render_home_page
from components.sidebar import get_sidebar_css, render_sidebar_menu


def main():
    """メインアプリケーション"""
    # ページ設定
    st.set_page_config(
        page_title="スポーツ関心度調査 データ分析",
        page_icon="🏃",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # カスタムCSS - スタイリッシュな青・白・黒系デザイン
    st.markdown(
        """
        <style>
        /* カラースキーム定義 */
        :root {
            --primary-blue: #1E3A8A;
            --secondary-blue: #3B82F6;
            --light-blue: #60A5FA;
            --dark-bg: #0F172A;
            --medium-bg: #1E293B;
            --light-bg: #F8FAFC;
            --text-primary: #0F172A;
            --text-secondary: #64748B;
            --border-color: #E2E8F0;
        }

        /* メインエリア */
        .main {
            padding-top: 1rem;
            background: linear-gradient(135deg, #F8FAFC 0%, #E0F2FE 100%);
        }

        /* ヘッダー・タイトル */
        h1 {
            color: var(--primary-blue) !important;
            font-weight: 700 !important;
            letter-spacing: -0.5px !important;
        }

        h2, h3 {
            color: var(--primary-blue) !important;
            font-weight: 600 !important;
        }

        /* タブ */
        .stTabs [data-baseweb="tab-list"] {
            gap: 12px;
            background-color: white;
            padding: 8px;
            border-radius: 12px;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        }

        .stTabs [data-baseweb="tab"] {
            padding: 10px 20px;
            background-color: transparent;
            border-radius: 8px;
            color: var(--text-secondary);
            font-weight: 500;
            transition: all 0.3s ease;
        }

        .stTabs [data-baseweb="tab"]:hover {
            background-color: #EFF6FF;
            color: var(--secondary-blue);
        }

        .stTabs [aria-selected="true"] {
            background-color: var(--secondary-blue) !important;
            color: white !important;
        }

        /* ボタン */
        .stButton button {
            background: linear-gradient(135deg, var(--primary-blue) 0%, var(--secondary-blue) 100%);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 0.6rem 1.5rem;
            font-weight: 600;
            box-shadow: 0 4px 6px rgba(59, 130, 246, 0.3);
            transition: all 0.3s ease;
        }

        .stButton button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 12px rgba(59, 130, 246, 0.4);
        }

        /* メトリック */
        [data-testid="stMetricValue"] {
            color: var(--primary-blue);
            font-weight: 700;
        }

        /* サイドバー */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, var(--dark-bg) 0%, var(--medium-bg) 100%);
        }

        [data-testid="stSidebar"] * {
            color: white !important;
        }

        [data-testid="stSidebar"] .stSelectbox label {
            color: #93C5FD !important;
        }

        /* データフレーム */
        .dataframe {
            border-radius: 12px !important;
            overflow: hidden;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }

        /* カード風スタイル */
        .element-container {
            background-color: white;
            border-radius: 12px;
            padding: 1rem;
            margin-bottom: 1rem;
        }

        /* ファイルアップローダー */
        [data-testid="stFileUploader"] {
            background-color: white;
            border: 2px dashed var(--light-blue);
            border-radius: 12px;
            padding: 1.5rem;
        }

        /* セレクトボックス */
        .stSelectbox > div > div {
            background-color: white;
            border-radius: 8px;
            border-color: var(--border-color);
        }

        /* マルチセレクト */
        .stMultiSelect > div > div {
            background-color: white;
            border-radius: 8px;
        }

        /* アラート・通知 */
        .stSuccess {
            background-color: #DBEAFE;
            color: var(--primary-blue);
            border-left: 4px solid var(--secondary-blue);
        }

        .stError {
            background-color: #FEE2E2;
            color: #991B1B;
            border-left: 4px solid #DC2626;
        }

        """ + get_sidebar_css() + """
        </style>
        """,
        unsafe_allow_html=True,
    )

    # サイドバーメニューの表示
    current_page = render_sidebar_menu()

    # ページごとの表示
    if current_page == "home":
        render_home_page()
    elif current_page == "analysis":
        render_data_analysis_page()
    elif current_page == "visualization":
        # データ可視化ページ（現在は分析ページと同じ内容を表示）
        render_data_analysis_page()
    elif current_page == "about":
        render_about_page()

    # フッター
    st.sidebar.markdown("---")
    st.sidebar.markdown(
        """
        <div style='text-align: center; color: #93C5FD; font-size: 0.9em;'>
        Powered by Streamlit<br>
        © 2025 Data Analysis App
        </div>
        """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
