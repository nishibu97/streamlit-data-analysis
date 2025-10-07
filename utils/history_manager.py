"""CSVファイルのアップロード履歴を管理するモジュール"""

from datetime import datetime
from typing import Any, Optional
import uuid

import numpy as np
import pandas as pd
import streamlit as st


class HistoryManager:
    """CSVファイルのアップロード履歴を管理するクラス

    Attributes:
        max_history (int): 保持する最大履歴数
    """

    def __init__(self, max_history: int = 5):
        """HistoryManagerを初期化

        Args:
            max_history: 保持する最大履歴数（デフォルト: 5）
        """
        self.max_history = max_history
        if "upload_history" not in st.session_state:
            st.session_state.upload_history = []
        if "current_data_id" not in st.session_state:
            st.session_state.current_data_id = None

    def add_history(
        self, filename: str, df: pd.DataFrame, file_size: str
    ) -> str:
        """履歴に新しいエントリを追加

        Args:
            filename: ファイル名
            df: DataFrameデータ
            file_size: ファイルサイズ（文字列形式）

        Returns:
            追加されたエントリのID
        """
        history_entry = {
            "id": str(uuid.uuid4()),
            "filename": filename,
            "upload_time": datetime.now(),
            "row_count": len(df),
            "column_count": len(df.columns),
            "columns": df.columns.tolist(),
            "data": df.copy(),
            "file_size": file_size,
        }

        # 履歴の先頭に追加
        st.session_state.upload_history.insert(0, history_entry)

        # 最大件数を超えたら古いものを削除
        if len(st.session_state.upload_history) > self.max_history:
            st.session_state.upload_history = st.session_state.upload_history[
                : self.max_history
            ]

        # 現在のデータIDを更新
        st.session_state.current_data_id = history_entry["id"]

        return history_entry["id"]

    def get_history(self) -> list[dict[str, Any]]:
        """履歴一覧を取得

        Returns:
            履歴エントリのリスト
        """
        return st.session_state.upload_history

    def get_data_by_id(self, data_id: str) -> Optional[pd.DataFrame]:
        """IDからデータを取得

        Args:
            data_id: データID

        Returns:
            DataFrame、存在しない場合はNone
        """
        for entry in st.session_state.upload_history:
            if entry["id"] == data_id:
                return entry["data"]
        return None

    def get_entry_by_id(self, data_id: str) -> Optional[dict[str, Any]]:
        """IDから履歴エントリ全体を取得

        Args:
            data_id: データID

        Returns:
            履歴エントリ、存在しない場合はNone
        """
        for entry in st.session_state.upload_history:
            if entry["id"] == data_id:
                return entry
        return None

    def delete_history(self, data_id: str) -> None:
        """特定の履歴を削除

        Args:
            data_id: 削除するデータID
        """
        st.session_state.upload_history = [
            entry
            for entry in st.session_state.upload_history
            if entry["id"] != data_id
        ]

        # 削除したのが現在のデータだった場合
        if st.session_state.current_data_id == data_id:
            if st.session_state.upload_history:
                st.session_state.current_data_id = st.session_state.upload_history[
                    0
                ]["id"]
            else:
                st.session_state.current_data_id = None

    def clear_all_history(self) -> None:
        """全ての履歴を削除"""
        st.session_state.upload_history = []
        st.session_state.current_data_id = None

    def get_current_data(self) -> Optional[pd.DataFrame]:
        """現在選択中のデータを取得

        Returns:
            現在選択中のDataFrame、存在しない場合はNone
        """
        if st.session_state.current_data_id:
            return self.get_data_by_id(st.session_state.current_data_id)
        return None

    def set_current_data(self, data_id: str) -> None:
        """現在のデータを設定

        Args:
            data_id: 設定するデータID
        """
        st.session_state.current_data_id = data_id


def optimize_dataframe_memory(df: pd.DataFrame) -> pd.DataFrame:
    """DataFrameのメモリ使用量を最適化

    数値型の列を可能な限り小さいデータ型に変換してメモリを節約する

    Args:
        df: 最適化するDataFrame

    Returns:
        最適化されたDataFrame
    """
    for col in df.columns:
        col_type = df[col].dtype

        if col_type != "object":
            c_min = df[col].min()
            c_max = df[col].max()

            if str(col_type)[:3] == "int":
                if (
                    c_min > np.iinfo(np.int8).min
                    and c_max < np.iinfo(np.int8).max
                ):
                    df[col] = df[col].astype(np.int8)
                elif (
                    c_min > np.iinfo(np.int16).min
                    and c_max < np.iinfo(np.int16).max
                ):
                    df[col] = df[col].astype(np.int16)
                elif (
                    c_min > np.iinfo(np.int32).min
                    and c_max < np.iinfo(np.int32).max
                ):
                    df[col] = df[col].astype(np.int32)

            elif str(col_type)[:5] == "float":
                if (
                    c_min > np.finfo(np.float32).min
                    and c_max < np.finfo(np.float32).max
                ):
                    df[col] = df[col].astype(np.float32)

    return df


def render_history_sidebar(history_manager: HistoryManager) -> None:
    """サイドバーに履歴一覧を表示

    Args:
        history_manager: HistoryManagerインスタンス
    """
    st.sidebar.divider()

    # ヘッダー
    history_list = history_manager.get_history()
    st.sidebar.markdown(
        f"### 📂 データ履歴 ({len(history_list)}/{history_manager.max_history})"
    )

    if not history_list:
        st.sidebar.info("まだデータがアップロードされていません")
        return

    # 全削除ボタン
    if st.sidebar.button("🗑️ 全て削除", use_container_width=True):
        history_manager.clear_all_history()
        st.rerun()

    st.sidebar.divider()

    # 履歴一覧
    for entry in history_list:
        is_current = entry["id"] == st.session_state.current_data_id

        # カード風のコンテナ
        with st.sidebar.container():
            # 選択中の場合は背景色を変える
            if is_current:
                st.markdown(
                    """
                    <div style="
                        background: rgba(102, 126, 234, 0.2);
                        padding: 1rem;
                        border-radius: 8px;
                        border-left: 4px solid #667eea;
                        margin-bottom: 0.5rem;
                    ">
                """,
                    unsafe_allow_html=True,
                )

            # ファイル情報
            st.markdown(f"**📄 {entry['filename']}**")
            st.caption(f"⏰ {entry['upload_time'].strftime('%Y-%m-%d %H:%M')}")
            st.caption(
                f"📊 {entry['row_count']:,}行 × {entry['column_count']}列"
            )
            st.caption(f"💾 {entry['file_size']}")

            # ボタン
            col1, col2 = st.columns(2)
            with col1:
                if not is_current:
                    if st.button(
                        "選択",
                        key=f"select_{entry['id']}",
                        use_container_width=True,
                    ):
                        history_manager.set_current_data(entry["id"])
                        st.success(f"✅ {entry['filename']} を読み込みました")
                        st.rerun()
                else:
                    st.button(
                        "選択中",
                        key=f"current_{entry['id']}",
                        disabled=True,
                        use_container_width=True,
                    )

            with col2:
                if st.button(
                    "削除",
                    key=f"delete_{entry['id']}",
                    use_container_width=True,
                ):
                    history_manager.delete_history(entry["id"])
                    st.rerun()

            if is_current:
                st.markdown("</div>", unsafe_allow_html=True)

            st.divider()
