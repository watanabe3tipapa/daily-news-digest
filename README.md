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

#### 初回セットアップ

1. GitHubリポジトリページを開く
2. **Settings** タブをクリック
3. 左サイドバーの **Pages** をクリック
4. **Source** セクションで **GitHub Actions** を選択
5. 変更を保存

#### デプロイ方法

以下のいずれかの方法でデプロイされます：

- **自動**: `main` ブランチにプッシュすると自動的にデプロイ
- **手動**: GitHubの **Actions** タブ → **Deploy to GitHub Pages** → **Run workflow**

数分後、`https://<username>.github.io/daily-news-digest/` でアクセス可能になります。

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

---


