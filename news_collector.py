import requests
import xml.etree.ElementTree as ET
import datetime
import os

def collect_news():
    today = datetime.date.today().strftime('%Y-%m-%d')
    news_data = []
    
    # HTTP headers to avoid being blocked
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    # NHK News RSS feed collection
    try:
        # NHK provides RSS feeds for different categories
        rss_url = 'https://www3.nhk.or.jp/rss/news/cat0.xml'  # Main news feed
        response = requests.get(rss_url, headers=headers, timeout=10)
        response.encoding = 'utf-8'
        
        # Parse XML
        root = ET.fromstring(response.content)
        
        # Find all items in the RSS feed
        items = root.findall('.//item')[:10]  # Get top 10 news items
        
        for item in items:
            title_elem = item.find('title')
            link_elem = item.find('link')
            
            title = title_elem.text.strip() if title_elem is not None and title_elem.text else 'Untitled'
            link = link_elem.text.strip() if link_elem is not None and link_elem.text else ''
            
            news_data.append({
                'title': title,
                'link': link,
                'source': 'NHK News'
            })
            
        print(f'Successfully collected {len(news_data)} news items from NHK RSS feed')
        
    except requests.exceptions.Timeout:
        print('NHK News collection error: Request timed out')
    except requests.exceptions.RequestException as e:
        print(f'NHK News collection error: {e}')
    except ET.ParseError as e:
        print(f'RSS feed parsing error: {e}')
    except Exception as e:
        print(f'NHK News collection error: {e}')
    
    # Check if we have any news data
    if not news_data:
        print('Warning: No news data collected')
        return
    
    # Generate Markdown
    markdown = f'# Daily News Digest - {today}\n\n'
    markdown += f'*Collected {len(news_data)} news articles from NHK News*\n\n'
    
    for i, article in enumerate(news_data, 1):
        markdown += f'## {i}. {article["title"]}\n'
        markdown += f'- **Source**: {article["source"]}\n'
        markdown += f'- **Link**: [{article["link"]}]({article["link"]})\n\n'
    
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
    
    print(f'News digest saved: {news_path} and {docs_path}')
    
    # Update index
    index_path = 'docs/index.md'
    if not os.path.exists(index_path):
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write('# Daily News Digest\n\n')
            f.write('NHKニュースの毎日のダイジェストです。\n\n')
            f.write('## Recent News\n\n')
    
    # Read existing content and check for duplicates
    with open(index_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Only add if today's entry doesn't already exist
    today_entry = f'[{today} News Digest](./{today}_news_digest.md)'
    if today_entry not in content:
        # Find the position to insert (after "## Recent News")
        recent_news_marker = '## Recent News\n\n'
        if recent_news_marker in content:
            parts = content.split(recent_news_marker, 1)
            new_entry = f'### [{today} News Digest](./{today}_news_digest.md)\n*最新のニュース*\n\n'
            updated_content = parts[0] + recent_news_marker + new_entry + parts[1]
            
            with open(index_path, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            print(f'Index updated: {index_path}')
        else:
            print('Warning: Could not find "## Recent News" marker in index.md')
    else:
        print(f'Index already contains entry for {today}')

if __name__ == '__main__':
    collect_news()