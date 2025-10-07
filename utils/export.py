"""データエクスポートユーティリティモジュール"""

import re
from datetime import datetime
from io import BytesIO
from typing import Literal

import pandas as pd
import streamlit as st

ExportFormat = Literal["csv", "excel", "json"]


@st.cache_data(ttl=300, show_spinner=False)
def export_to_csv(df: pd.DataFrame) -> bytes:
    """
    DataFrameをCSV形式のバイトデータに変換

    Args:
        df: エクスポート対象のDataFrame

    Returns:
        bytes: CSV形式のバイトデータ

    Note:
        結果は5分間キャッシュされます
    """
    return df.to_csv(index=False).encode("utf-8-sig")


@st.cache_data(ttl=300, show_spinner=False)
def export_to_excel(df: pd.DataFrame, sheet_name: str = "Data") -> bytes:
    """
    DataFrameをExcel形式のバイトデータに変換

    Args:
        df: エクスポート対象のDataFrame
        sheet_name: シート名（デフォルト: "Data"）

    Returns:
        bytes: Excel形式のバイトデータ

    Note:
        結果は5分間キャッシュされます
    """
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name=sheet_name)
    return output.getvalue()


@st.cache_data(ttl=300, show_spinner=False)
def export_to_json(df: pd.DataFrame, orient: str = "records") -> bytes:
    """
    DataFrameをJSON形式のバイトデータに変換

    Args:
        df: エクスポート対象のDataFrame
        orient: JSON形式（デフォルト: "records"）
            - "records": [{column -> value}, ... , {column -> value}]
            - "index": {index -> {column -> value}}
            - "columns": {column -> {index -> value}}

    Returns:
        bytes: JSON形式のバイトデータ

    Note:
        結果は5分間キャッシュされます
    """
    return df.to_json(orient=orient, force_ascii=False, indent=2).encode("utf-8")


def generate_filename(
    base_name: str = "export_data", file_format: ExportFormat = "csv"
) -> str:
    """
    エクスポートファイル名を生成（タイムスタンプ付き）

    Args:
        base_name: ベースとなるファイル名（デフォルト: "export_data"）
        file_format: ファイル形式（"csv", "excel", "json"）

    Returns:
        str: 生成されたファイル名（サニタイズ済み）

    Note:
        ファイル名に使用できない文字は "_" に置換されます
    """
    # ファイル名のサニタイゼーション（英数字、日本語、ハイフン、アンダースコアのみ許可）
    safe_name = re.sub(r"[^\w\-]", "_", base_name)

    # 空文字やアンダースコアのみの場合はデフォルト名を使用
    if not safe_name or safe_name.strip("_") == "":
        safe_name = "export_data"

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    extension_map = {"csv": "csv", "excel": "xlsx", "json": "json"}
    extension = extension_map.get(file_format, "csv")
    return f"{safe_name}_{timestamp}.{extension}"


def get_mime_type(file_format: ExportFormat) -> str:
    """
    ファイル形式に対応するMIMEタイプを取得

    Args:
        file_format: ファイル形式（"csv", "excel", "json"）

    Returns:
        str: MIMEタイプ
    """
    mime_types = {
        "csv": "text/csv",
        "excel": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        "json": "application/json",
    }
    return mime_types.get(file_format, "application/octet-stream")
