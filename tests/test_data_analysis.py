"""データ分析コンポーネントのテスト"""

import pandas as pd
import pytest


class TestDataAnalysisIntegration:
    """データ分析の統合テスト"""

    def test_full_analysis_workflow(self, sample_sports_data):
        """完全な分析ワークフローのテスト"""
        from utils.data_loader import (
            filter_by_age_group,
            get_sports_columns,
            validate_sports_survey_data,
        )

        # 1. データ検証
        assert validate_sports_survey_data(sample_sports_data) is True

        # 2. スポーツカラム取得
        sports_cols = get_sports_columns(sample_sports_data)
        assert len(sports_cols) == 5
        assert "サッカー" in sports_cols
        assert "野球" in sports_cols

        # 3. 年齢層フィルタリング
        filtered_20s = filter_by_age_group(sample_sports_data, "20代")
        assert len(filtered_20s) == 5
        assert all(filtered_20s["年齢層"] == "20代")

        # 4. 統計計算
        avg_interest = sample_sports_data[sports_cols].mean()
        assert len(avg_interest) == 5
        assert all(1 <= avg_interest) and all(avg_interest <= 5)

    def test_age_group_statistics(self, sample_sports_data):
        """年齢層別統計のテスト"""
        from utils.data_loader import filter_by_age_group, get_sports_columns

        sports_cols = get_sports_columns(sample_sports_data)

        for age_group in ["20代", "30代", "40代", "50代"]:
            filtered = filter_by_age_group(sample_sports_data, age_group)
            stats = filtered[sports_cols].describe()

            # 統計量が計算できることを確認
            assert "mean" in stats.index
            assert "std" in stats.index
            assert "min" in stats.index
            assert "max" in stats.index

    def test_correlation_analysis(self, sample_sports_data):
        """相関分析のテスト"""
        from utils.data_loader import get_sports_columns

        sports_cols = get_sports_columns(sample_sports_data)
        correlation_matrix = sample_sports_data[sports_cols].corr()

        # 相関行列の検証
        assert correlation_matrix.shape == (len(sports_cols), len(sports_cols))
        # 対角成分は1
        for i in range(len(sports_cols)):
            assert correlation_matrix.iloc[i, i] == pytest.approx(1.0)
        # 対称性
        for i in range(len(sports_cols)):
            for j in range(len(sports_cols)):
                assert correlation_matrix.iloc[i, j] == pytest.approx(correlation_matrix.iloc[j, i])


class TestDataVisualizationPreparation:
    """データ可視化準備のテスト"""

    def test_bar_chart_data_preparation(self, sample_sports_data):
        """棒グラフ用データ準備のテスト"""
        from utils.data_loader import get_sports_columns

        sports_cols = get_sports_columns(sample_sports_data)
        avg_interest = sample_sports_data[sports_cols].mean().sort_values(ascending=False)

        # データ形式の検証
        assert isinstance(avg_interest, pd.Series)
        assert len(avg_interest) == len(sports_cols)
        # 降順になっていることを確認
        assert all(
            avg_interest.iloc[i] >= avg_interest.iloc[i + 1] for i in range(len(avg_interest) - 1)
        )

    def test_line_chart_data_preparation(self, sample_sports_data):
        """折れ線グラフ用データ準備のテスト"""
        from utils.data_loader import get_sports_columns

        sports_cols = get_sports_columns(sample_sports_data)
        age_sport_data = sample_sports_data.groupby("年齢層")[sports_cols].mean()

        # データ形式の検証
        assert isinstance(age_sport_data, pd.DataFrame)
        assert len(age_sport_data) == 4  # 4つの年齢層
        assert all(col in age_sport_data.columns for col in sports_cols)

    def test_box_plot_data_preparation(self, sample_sports_data):
        """箱ひげ図用データ準備のテスト"""
        # 年齢層ごとのデータ分布を取得
        age_groups = sample_sports_data["年齢層"].unique()

        for age_group in age_groups:
            age_data = sample_sports_data[sample_sports_data["年齢層"] == age_group]
            assert len(age_data) > 0

            # サッカーの分布を確認
            soccer_data = age_data["サッカー"]
            assert soccer_data.min() >= 1
            assert soccer_data.max() <= 5


class TestErrorHandling:
    """エラーハンドリングのテスト"""

    def test_invalid_data_handling(self, invalid_sports_data):
        """不正データの処理テスト"""
        from utils.data_loader import validate_sports_survey_data

        # 不正データは検証失敗
        assert validate_sports_survey_data(invalid_sports_data) is False

    def test_empty_dataframe_handling(self, empty_dataframe):
        """空DataFrameの処理テスト"""
        from utils.data_loader import get_sports_columns, validate_sports_survey_data

        # 空データは検証失敗
        assert validate_sports_survey_data(empty_dataframe) is False

        # スポーツカラムは空リスト
        sports_cols = get_sports_columns(empty_dataframe)
        assert sports_cols == []

    def test_missing_age_group_filter(self, sample_sports_data):
        """存在しない年齢層でのフィルタリング"""
        from utils.data_loader import filter_by_age_group

        filtered = filter_by_age_group(sample_sports_data, "60代")

        # 結果は空だが、DataFrameとして返る
        assert isinstance(filtered, pd.DataFrame)
        assert len(filtered) == 0


class TestPerformance:
    """パフォーマンステスト"""

    def test_large_dataset_processing(self):
        """大規模データセット処理のテスト"""
        import time

        from utils.data_loader import get_sports_columns, validate_sports_survey_data

        # 大規模データ作成
        large_data = pd.DataFrame(
            {
                "回答者ID": range(1, 10001),
                "年齢層": ["20代", "30代", "40代", "50代"] * 2500,
                "サッカー": [5, 4, 3, 4, 5] * 2000,
                "野球": [4, 5, 4, 5, 4] * 2000,
                "バスケットボール": [3, 4, 5, 4, 3] * 2000,
                "テニス": [4, 3, 4, 3, 4] * 2000,
            }
        )

        # パフォーマンス測定
        start_time = time.time()
        assert validate_sports_survey_data(large_data) is True
        sports_cols = get_sports_columns(large_data)
        avg_interest = large_data[sports_cols].mean()
        end_time = time.time()

        # 処理時間が1秒以内であることを確認
        assert (end_time - start_time) < 1.0
        assert len(avg_interest) == 4
