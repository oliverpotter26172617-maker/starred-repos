#!/usr/bin/env python3
"""
Generate a markdown file with all starred repositories organized by language.
"""

import requests
import os
import re
from html import unescape
from datetime import datetime
from collections import defaultdict

# GitHub API configuration
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
GITHUB_API_BASE = 'https://api.github.com'
GITHUB_USERNAME = os.getenv('GITHUB_USERNAME') or os.getenv('GITHUB_REPOSITORY', '').split('/')[0]

def parse_stars_count(value):
    """Parse star count text into an integer."""
    cleaned = value.strip().lower().replace(',', '')
    if cleaned.endswith('k'):
        return int(float(cleaned[:-1]) * 1000)
    if cleaned.endswith('m'):
        return int(float(cleaned[:-1]) * 1000000)
    return int(cleaned) if cleaned.isdigit() else 0

def get_starred_repos_from_html():
    """Fetch starred repositories from GitHub profile HTML pages.

    Note: this fallback depends on GitHub's current stars page HTML structure.
    """
    if not GITHUB_USERNAME:
        print("Error: GITHUB_USERNAME is required for HTML fallback.")
        return []

    all_repos = []
    seen = set()
    page = 1
    # This still relies on GitHub page structure; if it breaks, inspect a stars page
    # for repository cards and update this pattern and the field regexes below.
    card_pattern = r'<div class="col-12 d-block width-full[^"]*color-border-muted"[^>]*>'

    while True:
        url = f'https://github.com/{GITHUB_USERNAME}?tab=stars&page={page}'
        response = requests.get(url, timeout=30)

        if response.status_code != 200:
            print(f"Error fetching starred repos HTML: {response.status_code}")
            break

        repos_this_page = []
        for block in re.split(card_pattern, response.text)[1:]:
            name_match = re.search(
                r'<h3>\s*<a href="/([^/"]+)/([^/"#?]+)">\s*<span class="text-normal">',
                block,
                re.S
            )
            if not name_match:
                continue

            owner, name = name_match.groups()
            full_name = f'{owner}/{name}'
            if full_name in seen:
                continue

            desc_match = re.search(r'itemprop="description">\s*(.*?)\s*</p>', block, re.S)
            lang_match = re.search(r'itemprop="programmingLanguage">(.*?)</span>', block, re.S)
            stars_match = re.search(
                rf'href="/{re.escape(owner)}/{re.escape(name)}/stargazers"[^>]*>.*?([0-9,\.kKmM]+)\s*</a>',
                block,
                re.S
            )

            description = 'No description'
            if desc_match:
                description = re.sub(r'<[^>]+>', '', unescape(desc_match.group(1))).strip() or 'No description'

            stars = parse_stars_count(stars_match.group(1)) if stars_match else 0
            language = unescape(lang_match.group(1)).strip() if lang_match else 'Other'

            repos_this_page.append({
                'name': name,
                'full_name': full_name,
                'html_url': f'https://github.com/{full_name}',
                'description': description,
                'stargazers_count': stars,
                'language': language or 'Other',
            })
            seen.add(full_name)

        if not repos_this_page:
            break

        all_repos.extend(repos_this_page)
        page += 1

    return all_repos

def get_starred_repos():
    """Fetch all starred repositories using the GitHub API."""
    headers = {}
    use_authenticated_endpoint = bool(GITHUB_TOKEN)

    if use_authenticated_endpoint:
        headers['Authorization'] = f'token {GITHUB_TOKEN}'
        url = f'{GITHUB_API_BASE}/user/starred'
    else:
        if not GITHUB_USERNAME:
            print("Error: set GITHUB_TOKEN or GITHUB_USERNAME to fetch starred repos.")
            return []
        url = f'{GITHUB_API_BASE}/users/{GITHUB_USERNAME}/starred'
    
    starred_repos = []
    page = 1
    per_page = 100
    
    while True:
        params = {'page': page, 'per_page': per_page, 'sort': 'starred_at', 'direction': 'desc'}
        
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code != 200:
            print(f"Error fetching starred repos: {response.status_code}")
            try:
                print(response.json())
            except requests.exceptions.JSONDecodeError:
                print(
                    f"Status {response.status_code}: failed to parse API error response as JSON. "
                    f"Raw response: {response.text[:500]}"
                )
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

An automatically maintained index of all my starred repositories, organized by programming language.

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
        print("GitHub API fetch failed or returned no repos. Trying HTML fallback...")
        repos = get_starred_repos_from_html()
    
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
