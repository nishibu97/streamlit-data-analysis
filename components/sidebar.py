"""サイドバーメニューコンポーネント"""

import streamlit as st


def render_sidebar_menu() -> str:
    """
    モダンなサイドバーナビゲーションメニューを表示

    Returns:
        str: 選択されたページ名
    """
    # セッション状態の初期化
    if "current_page" not in st.session_state:
        st.session_state.current_page = "home"

    # サイドバーヘッダー
    st.sidebar.markdown(
        """
        <div style='text-align: center; padding: 1.5rem 0 1rem 0; border-bottom: 1px solid rgba(255, 255, 255, 0.1);'>
            <h1 style='font-size: 1.5rem; margin: 0; color: #60A5FA;'>⚡ Data Analytics</h1>
            <p style='font-size: 0.75rem; margin: 0.5rem 0 0 0; color: #93C5FD; opacity: 0.8;'>Version 1.0.0</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.sidebar.markdown("<br>", unsafe_allow_html=True)

    # ページ定義
    pages = [
        {"id": "home", "icon": "🏠", "label": "ホーム"},
        {"id": "analysis", "icon": "📊", "label": "データ分析"},
        {"id": "visualization", "icon": "📈", "label": "データ可視化"},
        {"id": "about", "icon": "ℹ️", "label": "使い方"},
    ]

    # ページ選択UI
    for page in pages:
        is_current = st.session_state.current_page == page["id"]
        button_label = f"{page['icon']} {page['label']}"

        if st.sidebar.button(
            button_label,
            key=f"btn_{page['id']}",
            use_container_width=True,
            type="primary" if is_current else "secondary",
        ):
            st.session_state.current_page = page["id"]
            st.rerun()

    return st.session_state.current_page


def get_sidebar_css() -> str:
    """
    サイドバーメニュー用カスタムCSS

    Returns:
        str: CSS文字列
    """
    return """
    /* サイドバーボタンスタイル調整 */
    [data-testid="stSidebar"] .stButton button {
        background: transparent !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        color: white !important;
        box-shadow: none !important;
        padding: 0.75rem 1rem !important;
        font-size: 1rem !important;
        transition: all 0.2s ease !important;
    }

    [data-testid="stSidebar"] .stButton button:hover {
        background: rgba(255, 255, 255, 0.1) !important;
        transform: none !important;
        border-color: rgba(255, 255, 255, 0.3) !important;
    }

    [data-testid="stSidebar"] .stButton button[kind="primary"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        border: none !important;
        font-weight: 600 !important;
    }
    """
