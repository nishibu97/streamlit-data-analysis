"""サイドバーメニューコンポーネント"""

import streamlit as st


def render_sidebar_menu() -> str:
    """
    サイドバーにナビゲーションメニューを表示

    Returns:
        str: 選択されたページ名
    """
    st.sidebar.title("📋 メニュー")

    # ページ選択
    pages = {
        "🏠 ホーム": "home",
        "📊 データ分析": "analysis",
        "ℹ️ About": "about",
    }

    # セッション状態の初期化
    if "current_page" not in st.session_state:
        st.session_state.current_page = "home"

    # ラジオボタンでページ選択
    selected_label = st.sidebar.radio(
        "ページを選択",
        options=list(pages.keys()),
        index=list(pages.values()).index(st.session_state.current_page),
        label_visibility="collapsed",
    )

    # 選択されたページを更新
    st.session_state.current_page = pages[selected_label]

    return st.session_state.current_page
