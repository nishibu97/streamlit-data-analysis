"""データローダーのテスト"""

import pandas as pd
import pytest

from utils.data_loader import (
    filter_by_age_group,
    get_sports_columns,
    load_csv_data,
    load_sample_data,
    validate_sports_survey_data,
)


class TestLoadCsvData:
    """CSVデータ読み込みのテスト"""

    def test_load_valid_csv(self, tmp_path):
        """正常なCSVファイルの読み込み"""
        # テスト用CSVファイル作成
        csv_file = tmp_path / "test.csv"
        csv_file.write_text("col1,col2\n1,2\n3,4\n")

        # 読み込みテスト
        df = load_csv_data(str(csv_file))

        assert isinstance(df, pd.DataFrame)
        assert len(df) == 2
        assert list(df.columns) == ["col1", "col2"]

    def test_load_nonexistent_file(self):
        """存在しないファイルの読み込み"""
        with pytest.raises(FileNotFoundError):
            load_csv_data("nonexistent_file.csv")

    def test_load_empty_csv(self, tmp_path):
        """空のCSVファイルの読み込み"""
        csv_file = tmp_path / "empty.csv"
        csv_file.write_text("")

        with pytest.raises(pd.errors.EmptyDataError):
            load_csv_data(str(csv_file))


class TestLoadSampleData:
    """サンプルデータ読み込みのテスト"""

    def test_load_sample_data_success(self):
        """サンプルデータの正常読み込み"""
        df = load_sample_data()

        assert isinstance(df, pd.DataFrame)
        assert len(df) > 0
        assert "回答者ID" in df.columns
        assert "年齢層" in df.columns

    def test_sample_data_structure(self):
        """サンプルデータの構造検証"""
        df = load_sample_data()

        # 必須カラムの存在確認
        required_columns = ["回答者ID", "年齢層"]
        for col in required_columns:
            assert col in df.columns

        # スポーツカラムの存在確認
        sports_cols = get_sports_columns(df)
        assert len(sports_cols) >= 3


class TestValidateSportsSurveyData:
    """スポーツ調査データ検証のテスト"""

    def test_validate_valid_data(self):
        """有効なデータの検証"""
        df = pd.DataFrame(
            {
                "回答者ID": [1, 2, 3],
                "年齢層": ["20代", "30代", "40代"],
                "サッカー": [5, 4, 3],
                "野球": [4, 5, 4],
                "バスケットボール": [3, 3, 5],
            }
        )

        assert validate_sports_survey_data(df) is True

    def test_validate_missing_required_column(self):
        """必須カラム欠損データの検証"""
        df = pd.DataFrame({"年齢層": ["20代", "30代"], "サッカー": [5, 4], "野球": [4, 5]})

        assert validate_sports_survey_data(df) is False

    def test_validate_insufficient_sports_columns(self):
        """スポーツカラム不足データの検証"""
        df = pd.DataFrame({"回答者ID": [1, 2], "年齢層": ["20代", "30代"], "サッカー": [5, 4]})

        assert validate_sports_survey_data(df) is False

    def test_validate_edge_case_exactly_three_sports(self):
        """境界値: ちょうど3つのスポーツカラム"""
        df = pd.DataFrame(
            {
                "回答者ID": [1, 2],
                "年齢層": ["20代", "30代"],
                "サッカー": [5, 4],
                "野球": [4, 5],
                "バスケットボール": [3, 3],
            }
        )

        assert validate_sports_survey_data(df) is True


class TestGetSportsColumns:
    """スポーツカラム取得のテスト"""

    def test_get_sports_columns_basic(self):
        """基本的なスポーツカラム取得"""
        df = pd.DataFrame(
            {
                "回答者ID": [1, 2],
                "年齢層": ["20代", "30代"],
                "サッカー": [5, 4],
                "野球": [4, 5],
            }
        )

        sports_cols = get_sports_columns(df)

        assert isinstance(sports_cols, list)
        assert "サッカー" in sports_cols
        assert "野球" in sports_cols
        assert "回答者ID" not in sports_cols
        assert "年齢層" not in sports_cols

    def test_get_sports_columns_empty(self):
        """スポーツカラムが存在しない場合"""
        df = pd.DataFrame({"回答者ID": [1, 2], "年齢層": ["20代", "30代"]})

        sports_cols = get_sports_columns(df)

        assert isinstance(sports_cols, list)
        assert len(sports_cols) == 0


class TestFilterByAgeGroup:
    """年齢層フィルタリングのテスト"""

    @pytest.fixture
    def sample_df(self):
        """テスト用データフレーム"""
        return pd.DataFrame(
            {
                "回答者ID": [1, 2, 3, 4, 5],
                "年齢層": ["20代", "20代", "30代", "30代", "40代"],
                "サッカー": [5, 4, 3, 4, 5],
            }
        )

    def test_filter_by_specific_age_group(self, sample_df):
        """特定の年齢層でフィルタリング"""
        filtered = filter_by_age_group(sample_df, "20代")

        assert len(filtered) == 2
        assert all(filtered["年齢層"] == "20代")

    def test_filter_by_none(self, sample_df):
        """Noneの場合は全データ返却"""
        filtered = filter_by_age_group(sample_df, None)

        assert len(filtered) == 5
        pd.testing.assert_frame_equal(filtered, sample_df)

    def test_filter_by_all_ages(self, sample_df):
        """'全年齢'の場合は全データ返却"""
        filtered = filter_by_age_group(sample_df, "全年齢")

        assert len(filtered) == 5
        pd.testing.assert_frame_equal(filtered, sample_df)

    def test_filter_nonexistent_age_group(self, sample_df):
        """存在しない年齢層でフィルタリング"""
        filtered = filter_by_age_group(sample_df, "50代")

        assert len(filtered) == 0
        assert isinstance(filtered, pd.DataFrame)

    def test_filter_returns_copy(self, sample_df):
        """フィルタリング結果がコピーであることを確認"""
        filtered = filter_by_age_group(sample_df, "20代")

        # 元のデータフレームを変更
        sample_df.loc[0, "サッカー"] = 999

        # フィルタリング結果は影響を受けない
        assert filtered.loc[0, "サッカー"] != 999
