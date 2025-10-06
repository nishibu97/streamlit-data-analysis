"""データ読み込みユーティリティモジュール"""

import pandas as pd
from pathlib import Path
from typing import Optional


def load_csv_data(file_path: str) -> pd.DataFrame:
    """
    CSVファイルを読み込んでDataFrameを返す

    Args:
        file_path: CSVファイルのパス

    Returns:
        pd.DataFrame: 読み込んだデータ

    Raises:
        FileNotFoundError: ファイルが存在しない場合
        pd.errors.EmptyDataError: ファイルが空の場合
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"ファイルが見つかりません: {file_path}")

    return pd.read_csv(file_path)


def load_sample_data() -> pd.DataFrame:
    """
    サンプルデータ(男性スポーツ関心度調査)を読み込む

    Returns:
        pd.DataFrame: サンプルデータ
    """
    sample_path = Path(__file__).parent.parent / "data" / "sample_data.csv"
    return load_csv_data(str(sample_path))


def validate_sports_survey_data(df: pd.DataFrame) -> bool:
    """
    スポーツ関心度調査データの形式を検証する

    Args:
        df: 検証するDataFrame

    Returns:
        bool: データが有効な形式であればTrue
    """
    required_columns = ["回答者ID", "年齢層"]

    # 必須カラムの存在確認
    for col in required_columns:
        if col not in df.columns:
            return False

    # スポーツカラムが3つ以上存在するか確認
    sports_columns = [col for col in df.columns if col not in required_columns]
    if len(sports_columns) < 3:
        return False

    return True


def get_sports_columns(df: pd.DataFrame) -> list[str]:
    """
    スポーツ種目のカラム名リストを取得

    Args:
        df: DataFrameオブジェクト

    Returns:
        list[str]: スポーツ種目のカラム名リスト
    """
    excluded_columns = ["回答者ID", "年齢層"]
    return [col for col in df.columns if col not in excluded_columns]


def filter_by_age_group(df: pd.DataFrame, age_group: Optional[str] = None) -> pd.DataFrame:
    """
    年齢層でデータをフィルタリング

    Args:
        df: フィルタリング対象のDataFrame
        age_group: フィルタリングする年齢層（Noneの場合は全データ）

    Returns:
        pd.DataFrame: フィルタリングされたデータ
    """
    if age_group is None or age_group == "全年齢":
        return df

    return df[df["年齢層"] == age_group].copy()
