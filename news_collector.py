import requests
from bs4 import BeautifulSoup
import datetime
import os

def collect_news():
    today = datetime.date.today().strftime('%Y-%m-%d')
    news_data = []
    
    # NHK News collection
    try:
        nhk_url = 'https://www3.nhk.or.jp/news/'
        response = requests.get(nhk_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        top_stories = soup.find_all('div', class_='content')[:5]
        
        for story in top_stories:
            title = story.find('h2').text.strip() if story.find('h2') else 'Untitled'
            link = story.find('a')['href'] if story.find('a') else ''
            news_data.append({
                'title': title,
                'link': link,
                'source': 'NHK News'
            })
    except Exception as e:
        print(f'NHK News collection error: {e}')
    
    # Generate Markdown
    markdown = f'# Daily News Digest - {today}\n\n'
    for article in news_data:
        markdown += f'## {article["title"]}\n'
        markdown += f'- **Source**: {article["source"]}\n'
        markdown += f'- **Link**: {article["link"]}\n\n'
    
    # Ensure directories exist
    os.makedirs('news', exist_ok=True)
    os.makedirs('docs', exist_ok=True)
    
    # Write Markdown files
    news_path = f'news/{today}_news_digest.md'
    docs_path = f'docs/{today}_news_digest.md'
    
    with open(news_path, 'w', encoding='utf-8') as f:
        f.write(markdown)
    
    with open(docs_path, 'w', encoding='utf-8') as f:
        f.write(markdown)
    
    # Update index
    index_path = 'docs/index.md'
    if not os.path.exists(index_path):
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write('# Daily News Digest\n\n## Recent News\n')
    
    with open(index_path, 'r+', encoding='utf-8') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(f'## Latest News: {today}\n[{today} News Digest](./{today}_news_digest.md)\n\n{content}')

if __name__ == '__main__':
    collect_news()