"""ファイル名サニタイゼーションのテストモジュール"""

import pytest

from utils.export import generate_filename


class TestFilenameSanitization:
    """ファイル名サニタイゼーションのテスト"""

    def test_sanitize_special_characters(self):
        """特殊文字がアンダースコアに置換されることを確認"""
        filename = generate_filename("test/data:file", "csv")
        assert "/" not in filename
        assert ":" not in filename
        assert filename.startswith("test_data_file_")

    def test_sanitize_spaces(self):
        """スペースがアンダースコアに置換されることを確認"""
        filename = generate_filename("my test data", "csv")
        assert " " not in filename
        assert filename.startswith("my_test_data_")

    def test_sanitize_empty_string(self):
        """空文字列の場合デフォルト名が使用されることを確認"""
        filename = generate_filename("", "csv")
        assert filename.startswith("export_data_")

    def test_sanitize_only_special_chars(self):
        """特殊文字のみの場合デフォルト名が使用されることを確認"""
        filename = generate_filename("///:::", "csv")
        assert filename.startswith("export_data_")

    def test_sanitize_japanese_characters(self):
        """日本語文字が保持されることを確認"""
        filename = generate_filename("スポーツデータ", "csv")
        assert "スポーツデータ" in filename
        assert filename.endswith(".csv")

    def test_sanitize_alphanumeric_preserved(self):
        """英数字とハイフン、アンダースコアが保持されることを確認"""
        filename = generate_filename("test-data_123", "csv")
        assert "test-data_123" in filename

    def test_sanitize_excel_format(self):
        """Excel形式でもサニタイゼーションが動作することを確認"""
        filename = generate_filename("危険な/ファイル:名", "excel")
        assert "/" not in filename
        assert ":" not in filename
        assert filename.endswith(".xlsx")

    def test_sanitize_json_format(self):
        """JSON形式でもサニタイゼーションが動作することを確認"""
        filename = generate_filename("test*file?name", "json")
        assert "*" not in filename
        assert "?" not in filename
        assert filename.endswith(".json")
