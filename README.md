# Daily News Digest

このプロジェクトは、NHKニュースのRSSフィードから毎日自動的にニュースを収集し、Markdownファイルとして保存します。

## 機能

- 📰 NHKニュースのRSSフィードから最新ニュースを自動収集
- 📝 Markdown形式でニュースダイジェストを生成
- 🌐 GitHub Pagesで公開
- ⏰ GitHub Actionsで毎日自動実行

## 使い方

### ローカルで実行

```bash
# 依存関係のインストール
uv sync

# ニュース収集を実行
uv run python news_collector.py
```

### GitHub Pagesで公開

1. GitHubリポジトリの Settings > Pages に移動
2. Source を "GitHub Actions" に設定
3. ワークフローが自動的に実行され、`docs/` フォルダの内容が公開されます

### 手動でワークフローを実行

1. GitHubリポジトリの Actions タブに移動
2. "Collect Daily News" ワークフローを選択
3. "Run workflow" をクリック

## 出力

- `news/YYYY-MM-DD_news_digest.md` - ニュースダイジェスト（アーカイブ用）
- `docs/YYYY-MM-DD_news_digest.md` - ニュースダイジェスト（GitHub Pages用）
- `docs/index.md` - インデックスページ

## 技術スタック

- Python 3.13+
- [uv](https://github.com/astral-sh/uv) - パッケージマネージャー
- requests - HTTP通信
- GitHub Actions - 自動実行
- GitHub Pages - ウェブ公開

## ライセンス

MIT
