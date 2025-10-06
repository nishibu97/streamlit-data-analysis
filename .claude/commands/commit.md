# Conventional Commits ガイド

## コミットメッセージの基本構造

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

## コミットタイプ

### 主要タイプ
- **feat**: 新機能の追加
- **fix**: バグ修正
- **docs**: ドキュメントのみの変更
- **style**: コードの意味に影響しない変更（空白、フォーマット、セミコロンなど）
- **refactor**: バグ修正や機能追加ではないコード変更
- **perf**: パフォーマンス向上のためのコード変更
- **test**: テストの追加や既存テストの修正
- **build**: ビルドシステムや外部依存関係に関する変更
- **ci**: CI設定ファイルやスクリプトの変更
- **chore**: その他の変更（依存関係更新など）

### Streamlit特有タイプ
- **ui**: UIコンポーネントの変更
- **data**: データ処理ロジックの変更
- **viz**: 可視化・グラフ関連の変更
- **cache**: キャッシュ機能の変更

## スコープ例

### 機能別スコープ
- **auth**: 認証関連
- **dashboard**: ダッシュボード機能
- **upload**: ファイルアップロード機能
- **analysis**: データ分析機能
- **export**: データエクスポート機能

### ファイル/モジュール別スコープ
- **app**: メインアプリケーション
- **components**: UIコンポーネント
- **utils**: ユーティリティ関数
- **tests**: テスト関連

## コミットメッセージ例

### 新機能追加
```
feat(dashboard): CSVファイルアップロード機能を追加

- ドラッグ&ドロップでのファイルアップロード対応
- ファイル形式検証機能
- プレビュー表示機能
- エラーハンドリング強化

Closes #123
```

### バグ修正
```
fix(viz): グラフ表示時のメモリリークを修正

- plotlyチャートの適切なクリーンアップ
- 大量データ処理時のメモリ最適化
- セッション状態の適切な管理

Fixes #456
```

### ドキュメント更新
```
docs: README.mdにデプロイ手順を追加

- Streamlit Cloud デプロイメント手順
- 環境変数設定方法
- トラブルシューティング情報
```

### リファクタリング
```
refactor(utils): データ処理関数をモジュール化

- 共通処理の関数化
- 型ヒントの追加
- docstringの充実
- テスタビリティの向上
```

### パフォーマンス改善
```
perf(cache): データキャッシュ戦略を最適化

- @st.cache_data の適切な使用
- キャッシュキーの最適化
- メモリ使用量30%削減
```

### テスト追加
```
test(analysis): データ分析機能のテストを追加

- 統計計算関数のユニットテスト
- エッジケースのテスト
- パフォーマンステスト
- カバレッジ85%達成
```

## Breaking Changes

破壊的変更がある場合は、フッターに記載：

```
feat(api): データ形式をJSONに変更

BREAKING CHANGE: データエクスポート形式がCSVからJSONに変更されました。
既存のCSV処理コードは更新が必要です。

Migration Guide:
- export_to_csv() → export_to_json()
- データ形式: {'data': [...], 'metadata': {...}}
```

## コミット前チェックリスト

### コード品質
- [ ] PEP 8準拠
- [ ] 型ヒント追加
- [ ] docstring記載
- [ ] 不要なコメントやデバッグコードの削除

### テスト
- [ ] 関連テストの実行
- [ ] 新機能のテスト追加
- [ ] カバレッジ確認
- [ ] 手動テスト実行

### ドキュメント
- [ ] README更新
- [ ] APIドキュメント更新
- [ ] コメント・docstring更新
- [ ] 変更ログ記録

### Streamlit特有
- [ ] セッション状態の適切な管理
- [ ] キャッシュ機能の適切な使用
- [ ] UIの応答性確認
- [ ] エラーハンドリング確認

## コミット粒度の指針

### 適切な粒度
- 一つの論理的変更を一つのコミット
- 最小限の動作する変更
- レビューしやすいサイズ
- ロールバック可能な単位

### 避けるべきコミット
- 複数の機能を含む大きなコミット
- 動作しない中間状態のコミット
- typoや軽微な修正の大量のコミット
- 関連のない変更の混在

## Git Hooks

### pre-commit設定例
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    rev: 22.3.0
    hooks:
      - id: black
  
  - repo: https://github.com/pycqa/flake8
    rev: 4.0.1
    hooks:
      - id: flake8
  
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v0.950
    hooks:
      - id: mypy
```

### commit-msg hook
```bash
#!/bin/sh
# .git/hooks/commit-msg

# Conventional Commits形式チェック
if ! grep -qE "^(feat|fix|docs|style|refactor|perf|test|build|ci|chore|ui|data|viz|cache)(\(.+\))?: .{1,50}" "$1"; then
    echo "Error: Commit message must follow Conventional Commits format"
    echo "Example: feat(dashboard): add user authentication"
    exit 1
fi
```

## ベストプラクティス

### メッセージ作成
1. **現在形を使用**: "add" not "added"
2. **小文字で開始**: "feat: add feature" not "feat: Add feature"
3. **末尾にピリオドなし**: "fix: resolve issue" not "fix: resolve issue."
4. **50文字以内**: 簡潔で分かりやすく
5. **詳細は本文に**: 必要に応じて詳細な説明

### 継続的改善
- コミット履歴の定期的なレビュー
- チームでのコミット規約の共有
- ツールによる自動化の活用
- メッセージ品質の継続的改善