import json
import random
import argparse
from datetime import datetime
import webbrowser

def load_repos(filename='starred_repos.json'):
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: {filename} not found. Run fetch_starred_repos.py first.")
        return []

def calculate_difficulty(repo):
    stars = repo.get('stars', 0)
    size = repo.get('size', 0)
    
    if stars > 10000:
        return 'beginner'
    elif stars > 1000:
        return 'intermediate'
    elif size < 1000:
        return 'beginner'
    else:
        return 'advanced'

def filter_repos(repos, language=None, difficulty=None, exclude_archived=True):
    filtered = repos.copy()
    
    if exclude_archived:
        filtered = [r for r in filtered if not r.get('archived', False)]
    
    if language:
        filtered = [r for r in filtered if r['language'] and r['language'].lower() == language.lower()]
    
    if difficulty:
        filtered = [r for r in filtered if calculate_difficulty(r) == difficulty.lower()]
    
    return filtered

def format_repo_info(repo):
    difficulty = calculate_difficulty(repo)
    last_update = datetime.fromisoformat(repo.get('updated_at', '2020-01-01T00:00:00Z').replace('Z', '+00:00'))
    days_ago = (datetime.now().replace(tzinfo=last_update.tzinfo) - last_update).days
    
    print(f"\n🎯 {'='*60}")
    print(f"📦 {repo.get('name', 'Unknown')} ({repo.get('full_name', 'Unknown')})")
    print(f"{'='*60}")
    print(f"📝 Description: {repo.get('description') or 'No description'}")
    print(f"💻 Language: {repo.get('language') or 'Unknown'}")
    print(f"⭐ Stars: {repo.get('stars', 0):,}")
    print(f"🍴 Forks: {repo.get('forks', 0):,}")
    print(f"📊 Difficulty: {difficulty.title()}")
    print(f"📅 Last updated: {days_ago} days ago")
    print(f"📄 License: {repo.get('license') or 'No license'}")
    
    if repo.get('topics'):
        print(f"🏷️  Topics: {', '.join(repo.get('topics', []))}")
    
    print(f"\n🔗 URL: {repo.get('url', 'Unknown')}")
    print(f"📥 Clone: git clone {repo.get('clone_url', 'Unknown')}")
    print(f"{'='*60}")

def main():
    parser = argparse.ArgumentParser(description='Pick a random starred repository to learn from')
    parser.add_argument('--language', '-l', help='Filter by programming language')
    parser.add_argument('--difficulty', '-d', choices=['beginner', 'intermediate', 'advanced'], 
                       help='Filter by difficulty level')
    parser.add_argument('--include-archived', action='store_true', 
                       help='Include archived repositories')
    parser.add_argument('--open', '-o', action='store_true', 
                       help='Open the repository URL in browser')
    parser.add_argument('--count', '-c', type=int, default=1, 
                       help='Number of repositories to pick (default: 1)')
    
    args = parser.parse_args()
    
    repos = load_repos()
    if not repos:
        return
    
    filtered_repos = filter_repos(repos, args.language, args.difficulty, 
                                 not args.include_archived)
    
    if not filtered_repos:
        print("No repositories found matching your criteria.")
        return
    
    print(f"Found {len(filtered_repos)} repositories matching your criteria.")
    
    selected_repos = random.sample(filtered_repos, min(args.count, len(filtered_repos)))
    
    for i, repo in enumerate(selected_repos):
        if len(selected_repos) > 1:
            print(f"\n--- Pick #{i+1} ---")
        
        format_repo_info(repo)
        
        if args.open:
            webbrowser.open(repo.get('url', ''))
    
    if len(selected_repos) > 1:
        print(f"\n🎲 Picked {len(selected_repos)} repositories for you to explore!")
    else:
        print(f"\n🎲 Happy learning with {selected_repos[0]['name']}!")

if __name__ == "__main__":
    main()