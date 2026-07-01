#!/usr/bin/env python3
"""
Generate a markdown file with all starred repositories organized by language.
"""

import requests
import os
from datetime import datetime
from collections import defaultdict

# GitHub API configuration
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
GITHUB_API_BASE = 'https://api.github.com'

def get_starred_repos():
    """Fetch all starred repositories using the GitHub API."""
    headers = {}
    if GITHUB_TOKEN:
        headers['Authorization'] = f'token {GITHUB_TOKEN}'
    
    starred_repos = []
    page = 1
    per_page = 100
    
    while True:
        url = f'{GITHUB_API_BASE}/user/starred'
        params = {'page': page, 'per_page': per_page, 'sort': 'starred_at', 'direction': 'desc'}
        
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code != 200:
            print(f"Error fetching starred repos: {response.status_code}")
            print(response.json())
            break
        
        repos = response.json()
        if not repos:
            break
        
        starred_repos.extend(repos)
        page += 1
    
    return starred_repos

def organize_by_language(repos):
    """Organize repositories by programming language."""
    organized = defaultdict(list)
    
    for repo in repos:
        language = repo.get('language') or 'Other'
        organized[language].append(repo)
    
    return organized

def generate_markdown(organized_repos):
    """Generate markdown content for the README."""
    markdown = """# Starred Repos

A automatically maintained index of all my starred repositories, organized by programming language.

## Overview

This repository contains an automated system that regularly fetches and organizes all of my starred GitHub repositories. The list is updated weekly and organized by programming language for easy browsing.

## How It Works

- A Python script fetches all starred repos using the GitHub API
- Repos are organized by their primary programming language
- A GitHub Action automatically runs weekly to keep the list updated
- Changes are automatically committed and pushed

## Starred Repositories

**Last updated:** {timestamp}

**Total starred repos:** {total}

""".format(
        timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC'),
        total=sum(len(repos) for repos in organized_repos.values())
    )
    
    # Sort languages alphabetically, with 'Other' at the end
    sorted_languages = sorted(organized_repos.keys(), key=lambda x: (x == 'Other', x))
    
    for language in sorted_languages:
        repos = organized_repos[language]
        markdown += f"\n### {language} ({len(repos)})\n\n"
        
        # Sort repos by stars (descending)
        sorted_repos = sorted(repos, key=lambda x: x.get('stargazers_count', 0), reverse=True)
        
        for repo in sorted_repos:
            name = repo['name']
            url = repo['html_url']
            description = repo.get('description') or 'No description'
            stars = repo.get('stargazers_count', 0)
            
            # Clean up description
            description = description.replace('\n', ' ').strip()
            if len(description) > 100:
                description = description[:97] + '...'
            
            markdown += f"- [{name}]({url}) - ⭐ {stars}\n"
            markdown += f"  > {description}\n\n"
    
    markdown += """
## Manual Update

To manually generate the starred repos list:

```bash
python scripts/generate_stars.py
```

Make sure you have the required dependencies installed:

```bash
pip install -r requirements.txt
```

## License

MIT
"""
    
    return markdown

def main():
    """Main function to generate starred repos markdown."""
    print("Fetching starred repositories...")
    repos = get_starred_repos()
    
    if not repos:
        print("No starred repositories found or error occurred.")
        return
    
    print(f"Found {len(repos)} starred repositories")
    
    print("Organizing by language...")
    organized = organize_by_language(repos)
    
    print("Generating markdown...")
    markdown_content = generate_markdown(organized)
    
    # Write to README
    readme_path = os.path.join(os.path.dirname(__file__), '..', 'README.md')
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(markdown_content)
    
    print(f"✅ README.md updated with {len(repos)} starred repositories!")

if __name__ == '__main__':
    main()
