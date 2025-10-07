"""データ分析画面コンポーネント"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from components.export_ui import render_export_section
from utils.data_loader import (
    filter_by_age_group,
    get_sports_columns,
    load_sample_data,
    validate_sports_survey_data,
)


def render_data_analysis_page():
    """データ分析画面のメインコンポーネント"""
    st.title("🏃 スポーツ関心度調査 データ分析")

    # データ読み込みセクション
    df = _render_data_loading_section()

    if df is not None and not df.empty:
        # データ検証
        if not validate_sports_survey_data(df):
            st.error(
                "⚠️ データ形式が正しくありません。必須カラム: 回答者ID, 年齢層, スポーツ種目(3つ以上)"
            )
            return

        # サイドバーでフィルタリングオプション
        filtered_df = _render_sidebar_filters(df)

        # データプレビューセクション
        _render_data_preview_section(filtered_df)

        # データエクスポートセクション
        render_export_section(filtered_df, prefix="sports_data")

        # 可視化セクション
        _render_visualization_section(filtered_df)


def _render_data_loading_section() -> pd.DataFrame | None:
    """データ読み込みセクションの描画"""
    st.header("📁 データ読み込み")

    col1, col2 = st.columns(2)

    with col1:
        use_sample = st.button("サンプルデータを使用", type="primary", use_container_width=True)

    with col2:
        uploaded_file = st.file_uploader(
            "CSVファイルをアップロード",
            type=["csv"],
            help="回答者ID, 年齢層, スポーツ種目のカラムを含むCSVファイル",
        )

    # データの読み込み
    if use_sample:
        try:
            df = load_sample_data()
            st.success(f"📊 サンプルデータを読み込みました（{len(df)}件）")
            return df
        except Exception as e:
            st.error(f"⚠️ エラー: {str(e)}")
            return None

    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.success(f"📊 ファイルを読み込みました（{len(df)}件）")
            return df
        except Exception as e:
            st.error(f"⚠️ ファイルの読み込みに失敗: {str(e)}")
            return None

    return None


def _render_sidebar_filters(df: pd.DataFrame) -> pd.DataFrame:
    """サイドバーでフィルタリングオプションを提供"""
    st.sidebar.header("🔍 フィルター")

    # 年齢層フィルター
    age_groups = ["全年齢"] + sorted(df["年齢層"].unique().tolist())
    selected_age = st.sidebar.selectbox("年齢層", age_groups, index=0)

    # フィルタリング適用
    filtered_df = filter_by_age_group(df, selected_age if selected_age != "全年齢" else None)

    st.sidebar.metric("表示データ数", len(filtered_df))

    return filtered_df


def _render_data_preview_section(df: pd.DataFrame):
    """データプレビューセクションの描画"""
    st.header("📊 データプレビュー")

    # タブで表示を切り替え
    tab1, tab2, tab3 = st.tabs(["データ一覧", "基本統計量", "データ情報"])

    with tab1:
        st.dataframe(df, use_container_width=True, height=400)

    with tab2:
        sports_cols = get_sports_columns(df)
        st.dataframe(df[sports_cols].describe(), use_container_width=True)

    with tab3:
        col1, col2 = st.columns(2)
        with col1:
            st.metric("総回答数", len(df))
            st.metric("年齢層数", df["年齢層"].nunique())

        with col2:
            st.metric("スポーツ種目数", len(get_sports_columns(df)))
            st.metric("欠損値数", df.isnull().sum().sum())


def _render_visualization_section(df: pd.DataFrame):
    """データ可視化セクションの描画"""
    st.header("📈 データ可視化")

    sports_cols = get_sports_columns(df)

    # 1. スポーツ種目別の平均関心度（棒グラフ）
    st.subheader("1️⃣ スポーツ種目別 平均関心度")
    avg_interest = df[sports_cols].mean().sort_values(ascending=False)

    # 青系グラデーションカラーパレット
    fig_bar = px.bar(
        x=avg_interest.index,
        y=avg_interest.values,
        labels={"x": "スポーツ種目", "y": "平均関心度"},
        title="スポーツ種目別の平均関心度",
        color=avg_interest.values,
        color_continuous_scale=["#1E3A8A", "#3B82F6", "#60A5FA", "#93C5FD"],
    )
    fig_bar.update_layout(
        showlegend=False,
        height=400,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font={"color": "#1E3A8A", "size": 12},
        title_font={"size": 16, "color": "#1E3A8A", "family": "Arial, sans-serif"},
    )
    st.plotly_chart(fig_bar, use_container_width=True)

    # 2. 年齢層別の関心度傾向（折れ線グラフ）
    st.subheader("2️⃣ 年齢層別 関心度傾向")

    # スポーツ選択
    selected_sports = st.multiselect(
        "表示するスポーツを選択",
        sports_cols,
        default=sports_cols[:3],
        max_selections=5,
    )

    if selected_sports:
        age_sport_data = df.groupby("年齢層")[selected_sports].mean()

        # 青系カラーパレット
        blue_colors = ["#1E3A8A", "#3B82F6", "#60A5FA", "#93C5FD", "#DBEAFE"]

        fig_line = go.Figure()
        for idx, sport in enumerate(selected_sports):
            fig_line.add_trace(
                go.Scatter(
                    x=age_sport_data.index,
                    y=age_sport_data[sport],
                    mode="lines+markers",
                    name=sport,
                    line={"width": 3, "color": blue_colors[idx % len(blue_colors)]},
                    marker={"size": 10, "color": blue_colors[idx % len(blue_colors)]},
                )
            )

        fig_line.update_layout(
            title="年齢層別の関心度傾向",
            xaxis_title="年齢層",
            yaxis_title="平均関心度",
            height=400,
            hovermode="x unified",
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font={"color": "#1E3A8A", "size": 12},
            title_font={"size": 16, "color": "#1E3A8A", "family": "Arial, sans-serif"},
            legend={
                "bgcolor": "rgba(255,255,255,0.9)",
                "bordercolor": "#E2E8F0",
                "borderwidth": 1,
            },
        )
        st.plotly_chart(fig_line, use_container_width=True)

    # 3. 相関分析（ヒートマップ）
    st.subheader("3️⃣ スポーツ種目間の相関分析")

    correlation_matrix = df[sports_cols].corr()

    # 青・白・黒系のカラースケール（赤・黄色を使わない）
    fig_heatmap = px.imshow(
        correlation_matrix,
        labels={"x": "スポーツ種目", "y": "スポーツ種目", "color": "相関係数"},
        x=sports_cols,
        y=sports_cols,
        color_continuous_scale=[
            [0, "#0F172A"],  # 負の相関: ダークブルー/ブラック
            [0.5, "#F8FAFC"],  # 無相関: ホワイト
            [1, "#1E3A8A"],  # 正の相関: プライマリブルー
        ],
        aspect="auto",
        zmin=-1,
        zmax=1,
    )
    fig_heatmap.update_layout(
        title="スポーツ種目間の相関係数",
        height=500,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font={"color": "#1E3A8A", "size": 12},
        title_font={"size": 16, "color": "#1E3A8A", "family": "Arial, sans-serif"},
    )
    st.plotly_chart(fig_heatmap, use_container_width=True)

    # 4. 分布分析（箱ひげ図）
    st.subheader("4️⃣ 関心度の分布分析")

    selected_sport_box = st.selectbox("分析するスポーツを選択", sports_cols)

    if selected_sport_box:
        # 青系グラデーションで年齢層ごとに色分け
        fig_box = px.box(
            df,
            x="年齢層",
            y=selected_sport_box,
            title=f"{selected_sport_box}の年齢層別分布",
            labels={"年齢層": "年齢層", selected_sport_box: "関心度"},
            color="年齢層",
            color_discrete_sequence=["#1E3A8A", "#3B82F6", "#60A5FA", "#93C5FD"],
        )
        fig_box.update_layout(
            showlegend=False,
            height=400,
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font={"color": "#1E3A8A", "size": 12},
            title_font={"size": 16, "color": "#1E3A8A", "family": "Arial, sans-serif"},
        )
        st.plotly_chart(fig_box, use_container_width=True)
