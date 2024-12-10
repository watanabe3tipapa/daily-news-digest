import requests
from bs4 import BeautifulSoup
import datetime
import os
import json
import re

def sanitize_filename(title):
    """Create a clean filename from the title."""
    # Remove non-alphanumeric characters and replace spaces
    filename = re.sub(r'[^\w\-_\. ]', '', title)
    filename = filename.replace(' ', '_')
    return filename[:50]  # Limit filename length

def collect_news_from_sources():
    news_data = []
    
    # NHK News Web (Japanese news)
    try:
        nhk_url = 'https://www3.nhk.or.jp/news/'
        response = requests.get(nhk_url, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(response.text, 'html.parser')
        top_stories = soup.find_all('div', class_='content')[:5]
        
        nhk_news = [{
            'title': story.find('h2').text.strip() if story.find('h2') else 'Untitled',
            'link': story.find('a')['href'] if story.find('a') else '',
            'source': 'NHK News'
        } for story in top_stories if story.find('h2')]
        news_data.extend(nhk_news)
    except Exception as e:
        print(f'Error collecting NHK news: {e}')
    
    # Reuters Japan (English news)
    try:
        reuters_url = 'https://jp.reuters.com/'
        response = requests.get(reuters_url, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(response.text, 'html.parser')
        top_stories = soup.find_all('article', class_='story')[:5]
        
        reuters_news = [{
            'title': story.find('h3').text.strip() if story.find('h3') else 'Untitled',
            'link': 'https://jp.reuters.com' + story.find('a')['href'] if story.find('a') else '',
            'source': 'Reuters Japan'
        } for story in top_stories if story.find('h3')]
        news_data.extend(reuters_news)
    except Exception as e:
        print(f'Error collecting Reuters news: {e}')
    
    return news_data

def generate_markdown(news_data):
    today = datetime.date.today().strftime('%Y-%m-%d')
    markdown_content = f'# Daily News Digest - {today}\n\n'
    
    for article in news_data:
        markdown_content += f'## {article["title"]}\n'
        markdown_content += f'- **Source**: {article["source"]}\n'
        markdown_content += f'- **Link**: {article["link"]}\n\n'
    
    return markdown_content

def main():
    # Ensure news and docs directories exist
    os.makedirs('news', exist_ok=True)
    os.makedirs('docs', exist_ok=True)
    
    # Collect news
    news_data = collect_news_from_sources()
    
    # Generate markdown
    markdown_content = generate_markdown(news_data)
    
    # Save to file
    today = datetime.date.today().strftime('%Y-%m-%d')
    news_filename = f'news/{today}_news_digest.md'
    docs_filename = f'docs/{today}_news_digest.md'
    
    # Ensure index.md exists in docs for GitHub Pages
    if not os.path.exists('docs/index.md'):
        with open('docs/index.md', 'w', encoding='utf-8') as f:
            f.write('# Daily News Digest\n\n## Recent News\n')
    
    # Update index with latest news links
    with open('docs/index.md', 'r+', encoding='utf-8') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(f'## Latest News: {today}\n[{today} News Digest](/{today}_news_digest.md)\n\n{content}')
    
    # Write news files
    with open(news_filename, 'w', encoding='utf-8') as f:
        f.write(markdown_content)
    
    with open(docs_filename, 'w', encoding='utf-8') as f:
        f.write(markdown_content)
    
    # Optional: Create JSON index for easier navigation
    news_index = [
        {
            'date': today,
            'file': f'{today}_news_digest.md',
            'title': f'Daily News Digest - {today}'
        }
    ]
    
    # If index exists, read and append
    index_file = 'docs/news_index.json'
    if os.path.exists(index_file):
        with open(index_file, 'r') as f:
            existing_index = json.load(f)
        news_index.extend(existing_index)
    
    # Write updated index
    with open(index_file, 'w') as f:
        json.dump(news_index, f, indent=2)

if __name__ == '__main__':
    main()