#!/usr/bin/env python3
"""
GitHub Action script to update README.md with current repository statistics.
Fetches star counts for featured projects and total repository count.
"""

import requests
import re
import sys
from typing import List, Tuple

# Configuration
USERNAME = "Teach2Breach"
README_PATH = "README.md"

# List of featured repos (display_name, repo_name)
FEATURED_REPOS: List[Tuple[str, str]] = [
    ("Tempest", "Tempest"),
    ("Moonwalk", "moonwalk"),
    ("Noldr", "noldr"),
    ("Early Cascade", "early_cascade_inj_rs"),
    ("Pool Party", "pool_party_rs"),
    ("Phantom", "phantom_persist_rs"),  # Display name is "Phantom" not "Phantom Persistence"
]


def get_stars(repo_name: str) -> int:
    """Fetch star count for a repository."""
    url = f"https://api.github.com/repos/{USERNAME}/{repo_name}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json().get("stargazers_count", 0)
    except requests.RequestException as e:
        print(f"Error fetching stars for {repo_name}: {e}")
        return 0


def get_repo_count() -> int:
    """Fetch total public repository count."""
    url = f"https://api.github.com/users/{USERNAME}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json().get("public_repos", 0)
    except requests.RequestException as e:
        print(f"Error fetching repo count: {e}")
        return 0


def update_readme():
    """Update README.md with current statistics."""
    try:
        # Read current README content
        with open(README_PATH, "r", encoding="utf-8") as f:
            content = f.read()
        
        original_content = content
        
        # Update star counts for featured projects
        for display_name, repo_name in FEATURED_REPOS:
            stars = get_stars(repo_name)
            print(f"Updating {display_name}: {stars} stars")
            
            # Pattern to match the badge with current star count
            pattern = rf"(\[!\[{re.escape(display_name)}\]\([^)]+-)(\d+)(%20stars-[^)]+\)\]\([^)]+\))"
            def badge_replacement(match):
                return f"{match.group(1)}{stars}{match.group(3)}"
            
            if re.search(pattern, content):
                content = re.sub(pattern, badge_replacement, content)
            else:
                print(f"Warning: Could not find pattern for {display_name}")
        
        # Update total repository count
        repo_count = get_repo_count()
        print(f"Updating total repos: {repo_count}")
        
        # Pattern to match the "View All Repositories" badge
        repo_pattern = r"(View%20All%20Repositories-)(\d+)(%20repos-[^)]+)"

        def repo_replacement(match):
            return f"{match.group(1)}{repo_count}{match.group(3)}"

        if re.search(repo_pattern, content):
            content = re.sub(repo_pattern, repo_replacement, content)
        else:
            print("Warning: Could not find repository count pattern")
        
        # Write updated content back to file
        if content != original_content:
            with open(README_PATH, "w", encoding="utf-8") as f:
                f.write(content)
            print("README.md updated successfully!")
        else:
            print("No changes needed - stats are current.")
            
    except FileNotFoundError:
        print(f"Error: {README_PATH} not found")
        sys.exit(1)
    except Exception as e:
        print(f"Error updating README: {e}")
        sys.exit(1)


if __name__ == "__main__":
    update_readme() 