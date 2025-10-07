"""データエクスポートUIコンポーネント"""

import logging

import pandas as pd
import streamlit as st

from utils.export import (
    ExportFormat,
    export_to_csv,
    export_to_excel,
    export_to_json,
    generate_filename,
    get_mime_type,
)

# ロガーの設定
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


def render_export_section(df: pd.DataFrame, prefix: str = "sports_data"):
    """
    データエクスポートセクションを描画

    Args:
        df: エクスポート対象のDataFrame
        prefix: ファイル名のプレフィックス（デフォルト: "sports_data"）
    """
    st.header("📥 データエクスポート")

    if df.empty:
        st.warning("⚠️ エクスポートするデータがありません。")
        return

    # データサイズチェック
    MAX_ROWS = 100000
    MAX_SIZE_MB = 50

    # メモリサイズの概算（MB）
    memory_usage_mb = df.memory_usage(deep=True).sum() / (1024 * 1024)

    if len(df) > MAX_ROWS:
        st.warning(
            f"⚠️ データ件数が{MAX_ROWS:,}件を超えています（現在: {len(df):,}件）。"
            f"処理に時間がかかる場合があります。"
        )

    if memory_usage_mb > MAX_SIZE_MB:
        st.warning(
            f"⚠️ データサイズが大きいです（約{memory_usage_mb:.1f}MB）。"
            f"エクスポートに時間がかかる場合があります。"
        )

    # エクスポート形式選択
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("📄 CSV形式", type="primary", use_container_width=True):
            _download_data(df, "csv", prefix)

    with col2:
        if st.button("📊 Excel形式", type="primary", use_container_width=True):
            _download_data(df, "excel", prefix)

    with col3:
        if st.button("📋 JSON形式", type="primary", use_container_width=True):
            _download_data(df, "json", prefix)

    # エクスポート情報の表示
    with st.expander("ℹ️ エクスポート情報"):
        st.markdown(
            f"""
            **現在のデータ件数**: {len(df):,}件
            **カラム数**: {len(df.columns)}個

            **利用可能な形式**:
            - **CSV**: Comma-Separated Values（カンマ区切り）
            - **Excel**: Microsoft Excel形式（.xlsx）
            - **JSON**: JavaScript Object Notation
            """
        )


def _download_data(df: pd.DataFrame, file_format: ExportFormat, prefix: str):
    """
    データをエクスポートしてダウンロードボタンを表示

    Args:
        df: エクスポート対象のDataFrame
        file_format: エクスポート形式（"csv", "excel", "json"）
        prefix: ファイル名のプレフィックス
    """
    try:
        logger.info(
            f"Export started: format={file_format}, rows={len(df)}, columns={len(df.columns)}"
        )

        # データの変換
        if file_format == "csv":
            data = export_to_csv(df)
        elif file_format == "excel":
            data = export_to_excel(df, sheet_name="スポーツ関心度データ")
        elif file_format == "json":
            data = export_to_json(df, orient="records")
        else:
            logger.warning(f"Unsupported format requested: {file_format}")
            st.error(f"⚠️ 未対応の形式です: {file_format}")
            return

        # ファイル名とMIMEタイプの取得
        filename = generate_filename(prefix, file_format)
        mime_type = get_mime_type(file_format)

        logger.info(f"Export successful: filename={filename}, size={len(data)} bytes")

        # ダウンロードボタンの表示
        st.download_button(
            label=f"⬇️ {filename} をダウンロード",
            data=data,
            file_name=filename,
            mime=mime_type,
            type="secondary",
            use_container_width=True,
        )

        st.success(f"✅ {file_format.upper()}形式でエクスポート準備が完了しました！")

    except Exception as e:
        logger.error(f"Export failed: format={file_format}, error={str(e)}", exc_info=True)
        st.error(f"⚠️ エクスポート中にエラーが発生しました: {str(e)}")
