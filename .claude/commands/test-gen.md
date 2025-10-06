# テストケース自動生成ガイド

## テスト生成の基本原則

### テスト対象の特定
- 新規追加した機能・関数
- 修正した既存機能
- 重要なビジネスロジック
- エラーハンドリング処理

### テストタイプの選択
- **単体テスト**: 個別の関数・メソッド
- **統合テスト**: コンポーネント間の連携
- **E2Eテスト**: ユーザーシナリオ全体
- **パフォーマンステスト**: レスポンス時間・負荷

## Streamlit アプリケーションのテスト

### セットアップ
```python
import pytest
import streamlit as st
from streamlit.testing.v1 import AppTest

def test_app_basic():
    """基本的なアプリケーション動作テスト"""
    at = AppTest.from_file("app.py")
    at.run()
    assert not at.exception
```

### UI コンポーネントテスト
```python
def test_sidebar_components():
    """サイドバーコンポーネントのテスト"""
    at = AppTest.from_file("app.py")
    at.run()
    
    # サイドバーの要素確認
    assert len(at.sidebar.selectbox) > 0
    assert len(at.sidebar.slider) > 0
    
def test_file_uploader():
    """ファイルアップロード機能のテスト"""
    at = AppTest.from_file("app.py")
    
    # テストファイルのアップロード
    test_data = b"test,data\n1,2\n3,4"
    at.file_uploader[0].upload(test_data, "test.csv")
    at.run()
    
    assert not at.exception
    assert "データが正常に読み込まれました" in str(at.markdown)
```

### データ処理関数のテスト
```python
import pandas as pd
import numpy as np

def test_data_processing_function():
    """データ処理関数のテスト"""
    # テストデータの作成
    test_df = pd.DataFrame({
        'A': [1, 2, 3, 4, 5],
        'B': [10, 20, 30, 40, 50]
    })
    
    # 関数の実行
    result = your_data_function(test_df)
    
    # 結果の検証
    assert isinstance(result, pd.DataFrame)
    assert len(result) == 5
    assert 'processed_column' in result.columns
    
def test_data_validation():
    """データバリデーション関数のテスト"""
    # 正常なデータ
    valid_data = pd.DataFrame({'value': [1, 2, 3]})
    assert validate_data(valid_data) == True
    
    # 異常なデータ
    invalid_data = pd.DataFrame({'value': [None, None, None]})
    assert validate_data(invalid_data) == False
```

### 可視化コンポーネントのテスト
```python
def test_chart_generation():
    """グラフ生成機能のテスト"""
    at = AppTest.from_file("app.py")
    
    # データ入力のシミュレーション
    test_data = pd.DataFrame({
        'x': range(10),
        'y': np.random.random(10)
    })
    
    # チャート生成の確認
    at.run()
    assert len(at.plotly_chart) > 0 or len(at.pyplot) > 0
```

## エラーハンドリングのテスト

### 例外処理テスト
```python
def test_error_handling():
    """エラーハンドリングのテスト"""
    at = AppTest.from_file("app.py")
    
    # 不正なファイルのアップロード
    invalid_data = b"invalid,csv,format"
    at.file_uploader[0].upload(invalid_data, "invalid.txt")
    at.run()
    
    # エラーメッセージの確認
    assert "エラー" in str(at.error) or "Error" in str(at.error)

def test_empty_data_handling():
    """空データの処理テスト"""
    empty_df = pd.DataFrame()
    
    with pytest.raises(ValueError):
        process_empty_data(empty_df)
```

## パフォーマンステスト

### 実行時間テスト
```python
import time

def test_processing_performance():
    """処理時間のテスト"""
    large_data = pd.DataFrame({
        'A': np.random.random(10000),
        'B': np.random.random(10000)
    })
    
    start_time = time.time()
    result = heavy_processing_function(large_data)
    end_time = time.time()
    
    # 5秒以内で処理が完了することを確認
    assert (end_time - start_time) < 5.0
    assert result is not None
```

### メモリ使用量テスト
```python
import psutil
import os

def test_memory_usage():
    """メモリ使用量のテスト"""
    process = psutil.Process(os.getpid())
    initial_memory = process.memory_info().rss
    
    # 大量データの処理
    large_data = create_large_dataset()
    process_data(large_data)
    
    final_memory = process.memory_info().rss
    memory_increase = final_memory - initial_memory
    
    # メモリ増加が100MB以下であることを確認
    assert memory_increase < 100 * 1024 * 1024
```

## モックとフィクスチャー

### データフィクスチャー
```python
@pytest.fixture
def sample_dataframe():
    """テスト用データフレーム"""
    return pd.DataFrame({
        'date': pd.date_range('2023-01-01', periods=100),
        'value': np.random.random(100),
        'category': np.random.choice(['A', 'B', 'C'], 100)
    })

@pytest.fixture
def mock_api_response():
    """APIレスポンスのモック"""
    return {
        'status': 'success',
        'data': [{'id': 1, 'name': 'test'}]
    }
```

### 外部依存のモック
```python
from unittest.mock import patch, MagicMock

@patch('requests.get')
def test_api_call(mock_get, mock_api_response):
    """API呼び出しのテスト"""
    mock_get.return_value.json.return_value = mock_api_response
    
    result = fetch_data_from_api()
    
    assert result['status'] == 'success'
    mock_get.assert_called_once()
```

## テスト実行とレポート

### テスト実行コマンド
```bash
# 全テスト実行
pytest

# カバレッジ付きテスト
pytest --cov=. --cov-report=html

# 特定のテストファイル実行
pytest tests/test_data_processing.py

# テスト結果の詳細表示
pytest -v
```

### 継続的テスト
```python
# conftest.py
import pytest

def pytest_configure(config):
    """テスト設定"""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow"
    )

@pytest.fixture(autouse=True)
def cleanup():
    """テスト後のクリーンアップ"""
    yield
    # クリーンアップ処理
```

## テスト品質の指標

### カバレッジ目標
- **行カバレッジ**: 80%以上
- **分岐カバレッジ**: 70%以上
- **関数カバレッジ**: 90%以上

### テストケース品質
- [ ] 正常系テストが網羅されている
- [ ] 異常系テストが実装されている
- [ ] 境界値テストが含まれている
- [ ] パフォーマンステストが実装されている
- [ ] テストが独立して実行可能
- [ ] テストデータが適切に管理されている
- [ ] モックが適切に使用されている
- [ ] テストの実行時間が妥当