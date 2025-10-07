"""pytest設定とフィクスチャー"""

import pandas as pd
import pytest


@pytest.fixture
def sample_sports_data():
    """テスト用スポーツ調査データ"""
    return pd.DataFrame(
        {
            "回答者ID": list(range(1, 21)),
            "年齢層": ["20代"] * 5 + ["30代"] * 5 + ["40代"] * 5 + ["50代"] * 5,
            "サッカー": [5, 4, 5, 4, 5, 4, 3, 4, 3, 4, 3, 5, 3, 4, 3, 2, 3, 2, 3, 2],
            "野球": [4, 5, 4, 5, 4, 5, 5, 5, 5, 4, 5, 4, 5, 4, 5, 5, 4, 5, 4, 5],
            "バスケットボール": [
                5,
                4,
                5,
                4,
                3,
                3,
                4,
                3,
                4,
                3,
                2,
                3,
                2,
                3,
                2,
                1,
                2,
                1,
                2,
                1,
            ],
            "テニス": [3, 4, 3, 4, 2, 4, 3, 4, 3, 5, 3, 4, 3, 4, 3, 4, 3, 4, 3, 4],
            "ゴルフ": [2, 1, 2, 1, 1, 3, 4, 3, 4, 4, 5, 4, 5, 4, 5, 5, 5, 5, 5, 5],
        }
    )


@pytest.fixture
def invalid_sports_data():
    """テスト用不正データ"""
    return pd.DataFrame({"年齢層": ["20代", "30代"], "サッカー": [5, 4]})  # 回答者IDが欠損


@pytest.fixture
def empty_dataframe():
    """空のDataFrame"""
    return pd.DataFrame()
