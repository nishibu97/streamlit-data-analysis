---
description: CSVファイルのアップロード履歴機能を追加
model: claude-sonnet-4-5-20250929
---

# CSV ファイル履歴管理機能の追加

アップロードした CSV ファイルの履歴を保持し、過去のデータを再選択できる機能を実装します。

## 機能要件

### 1. 履歴データ構造

各履歴エントリは以下の情報を保持：

```python
{
    'id': str,              # 一意のID（UUID）
    'filename': str,        # ファイル名
    'upload_time': datetime, # アップロード日時
    'row_count': int,       # 行数
    'column_count': int,    # 列数
    'columns': list,        # 列名リスト
    'data': pd.DataFrame,   # データ本体
    'file_size': str        # ファイルサイズ
}
```

### 2. 履歴管理クラス

`utils/history_manager.py` を作成：

```python
import streamlit as st
import pandas as pd
from datetime import datetime
import uuid

class HistoryManager:
    """CSVファイルのアップロード履歴を管理するクラス"""

    def __init__(self, max_history=5):
        self.max_history = max_history
        if 'upload_history' not in st.session_state:
            st.session_state.upload_history = []
        if 'current_data_id' not in st.session_state:
            st.session_state.current_data_id = None

    def add_history(self, filename: str, df: pd.DataFrame, file_size: str):
        """履歴に新しいエントリを追加"""
        history_entry = {
            'id': str(uuid.uuid4()),
            'filename': filename,
            'upload_time': datetime.now(),
            'row_count': len(df),
            'column_count': len(df.columns),
            'columns': df.columns.tolist(),
            'data': df.copy(),
            'file_size': file_size
        }

        # 履歴の先頭に追加
        st.session_state.upload_history.insert(0, history_entry)

        # 最大件数を超えたら古いものを削除
        if len(st.session_state.upload_history) > self.max_history:
            st.session_state.upload_history = st.session_state.upload_history[:self.max_history]

        # 現在のデータIDを更新
        st.session_state.current_data_id = history_entry['id']

        return history_entry['id']

    def get_history(self):
        """履歴一覧を取得"""
        return st.session_state.upload_history

    def get_data_by_id(self, data_id: str):
        """IDからデータを取得"""
        for entry in st.session_state.upload_history:
            if entry['id'] == data_id:
                return entry['data']
        return None

    def get_entry_by_id(self, data_id: str):
        """IDから履歴エントリ全体を取得"""
        for entry in st.session_state.upload_history:
            if entry['id'] == data_id:
                return entry
        return None

    def delete_history(self, data_id: str):
        """特定の履歴を削除"""
        st.session_state.upload_history = [
            entry for entry in st.session_state.upload_history
            if entry['id'] != data_id
        ]

        # 削除したのが現在のデータだった場合
        if st.session_state.current_data_id == data_id:
            if st.session_state.upload_history:
                st.session_state.current_data_id = st.session_state.upload_history[0]['id']
            else:
                st.session_state.current_data_id = None

    def clear_all_history(self):
        """全ての履歴を削除"""
        st.session_state.upload_history = []
        st.session_state.current_data_id = None

    def get_current_data(self):
        """現在選択中のデータを取得"""
        if st.session_state.current_data_id:
            return self.get_data_by_id(st.session_state.current_data_id)
        return None

    def set_current_data(self, data_id: str):
        """現在のデータを設定"""
        st.session_state.current_data_id = data_id
```

### 3. 履歴表示 UI（サイドバー）

サイドバーに履歴セクションを追加：

```python
def render_history_sidebar(history_manager: HistoryManager):
    """サイドバーに履歴一覧を表示"""

    st.sidebar.divider()

    # ヘッダー
    history_list = history_manager.get_history()
    st.sidebar.markdown(f"### 📂 データ履歴 ({len(history_list)}/{history_manager.max_history})")

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
        is_current = entry['id'] == st.session_state.current_data_id

        # カード風のコンテナ
        with st.sidebar.container():
            # 選択中の場合は背景色を変える
            if is_current:
                st.markdown("""
                    <div style="
                        background: rgba(102, 126, 234, 0.2);
                        padding: 1rem;
                        border-radius: 8px;
                        border-left: 4px solid #667eea;
                        margin-bottom: 0.5rem;
                    ">
                """, unsafe_allow_html=True)

            # ファイル情報
            st.markdown(f"**📄 {entry['filename']}**")
            st.caption(f"⏰ {entry['upload_time'].strftime('%Y-%m-%d %H:%M')}")
            st.caption(f"📊 {entry['row_count']:,}行 × {entry['column_count']}列")
            st.caption(f"💾 {entry['file_size']}")

            # ボタン
            col1, col2 = st.columns(2)
            with col1:
                if not is_current:
                    if st.button("選択", key=f"select_{entry['id']}", use_container_width=True):
                        history_manager.set_current_data(entry['id'])
                        st.success(f"✅ {entry['filename']} を読み込みました")
                        st.rerun()
                else:
                    st.button("選択中", key=f"current_{entry['id']}",
                             disabled=True, use_container_width=True)

            with col2:
                if st.button("削除", key=f"delete_{entry['id']}", use_container_width=True):
                    history_manager.delete_history(entry['id'])
                    st.rerun()

            if is_current:
                st.markdown("</div>", unsafe_allow_html=True)

            st.divider()
```

### 4. 既存のアップロード機能との統合

CSV アップロード処理を修正：

```python
# 初期化
history_manager = HistoryManager(max_history=5)

# CSVアップロード処理
uploaded_file = st.file_uploader("CSVファイルをアップロード", type=['csv'])

if uploaded_file is not None:
    # ファイルサイズを計算
    file_size = f"{uploaded_file.size / 1024:.1f}KB"

    # CSVを読み込み
    df = pd.read_csv(uploaded_file)

    # 履歴に追加
    history_manager.add_history(
        filename=uploaded_file.name,
        df=df,
        file_size=file_size
    )

    st.success(f"✅ {uploaded_file.name} を読み込みました")
    st.rerun()

# サイドバーに履歴を表示
render_history_sidebar(history_manager)

# 現在のデータを取得して表示
current_data = history_manager.get_current_data()
if current_data is not None:
    # 統計表示
    display_statistics(current_data)
```

### 5. メモリ最適化

大きな DataFrame の場合の対応：

```python
def optimize_dataframe_memory(df: pd.DataFrame) -> pd.DataFrame:
    """DataFrameのメモリ使用量を最適化"""
    for col in df.columns:
        col_type = df[col].dtype

        if col_type != 'object':
            c_min = df[col].min()
            c_max = df[col].max()

            if str(col_type)[:3] == 'int':
                if c_min > np.iinfo(np.int8).min and c_max < np.iinfo(np.int8).max:
                    df[col] = df[col].astype(np.int8)
                elif c_min > np.iinfo(np.int16).min and c_max < np.iinfo(np.int16).max:
                    df[col] = df[col].astype(np.int16)
                elif c_min > np.iinfo(np.int32).min and c_max < np.iinfo(np.int32).max:
                    df[col] = df[col].astype(np.int32)

            elif str(col_type)[:5] == 'float':
                if c_min > np.finfo(np.float32).min and c_max < np.finfo(np.float32).max:
                    df[col] = df[col].astype(np.float32)

    return df
```

### 6. エラーハンドリング

```python
# ファイルサイズチェック
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

if uploaded_file.size > MAX_FILE_SIZE:
    st.error(f"❌ ファイルサイズが大きすぎます（最大10MB）")
else:
    try:
        df = pd.read_csv(uploaded_file)
        # メモリ最適化
        df = optimize_dataframe_memory(df)
        # 履歴に追加
        history_manager.add_history(uploaded_file.name, df, file_size)
    except Exception as e:
        st.error(f"❌ ファイルの読み込みに失敗しました: {str(e)}")
```

## 実装手順

1. `utils/history_manager.py` を作成
2. `HistoryManager` クラスを実装
3. `render_history_sidebar()` 関数を実装
4. 既存のアップロード処理を修正して履歴管理を統合
5. サイドバーに履歴表示 UI を追加
6. テストデータで動作確認

## 追加機能（オプション）

### エクスポート機能

```python
def export_history(history_manager: HistoryManager):
    """履歴をエクスポート"""
    if st.sidebar.button("📥 履歴をエクスポート"):
        history_data = {
            'entries': [
                {k: v for k, v in entry.items() if k != 'data'}
                for entry in history_manager.get_history()
            ]
        }
        st.download_button(
            "ダウンロード",
            data=json.dumps(history_data, default=str, indent=2),
            file_name="upload_history.json"
        )
```

### 検索機能

```python
search_term = st.sidebar.text_input("🔍 ファイル名で検索")
if search_term:
    filtered_history = [
        entry for entry in history_list
        if search_term.lower() in entry['filename'].lower()
    ]
```

## 注意事項

- セッションステートはブラウザを閉じると消える
- 大量のデータはメモリを圧迫するので件数制限を設定
- 永続化が必要な場合は別途実装
- マルチユーザー環境では適切な分離が必要
