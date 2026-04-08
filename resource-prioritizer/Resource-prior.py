# 📁 Resource Prioritizer - Day 3 Project
# Organizes files by date and star ratings

import os
from datetime import datetime

def scan_folder(folder_path):
    """Find all files in a folder"""
    files = []
    
    for filename in os.listdir(folder_path):
        filepath = os.path.join(folder_path, filename)
        if os.path.isfile(filepath):
            # Get file info
            stat_info = os.stat(filepath)
            mtime = datetime.fromtimestamp(stat_info.st_mtime)
            
            files.append({
                'name': filename,
                'size': stat_info.st_size,
                'date': mtime.strftime('%Y-%m-%d'),
                'modified': mtime
            })
    
    return files

def calculate_star_score(file_name):
    """Assign star rating based on file content"""
    # This will be enhanced later with actual ratings
    return 0  # Start simple!

def prioritize_files(files, folder_path):
    """Sort files by date and star rating"""
    
    def sort_key(item):
        filename = item['name'].lower()
        stars = calculate_star_score(filename)
        
        # Parse date from filename or use modification date
        try:
            file_date = datetime.strptime(
                item['date'], '%Y-%m-%d'
            )
        except:
            file_date = datetime.min
        
        return (file_date, stars)  # Sort by date, then stars
    
    sorted_files = sorted(files, key=sort_key, reverse=True)
    return sorted_files

def display_prioritized_list(prioritized_files):
    """Show results in a nice format"""
    print("\n🔍 RESOURCE PRIORITY LIST\n")
    print(f"{'Rank':<5} {'File Name':<40} {'Date':<12}")
    print("-" * 60)
    
    for i, file in enumerate(prioritized_files, 1):
        print(f"{i:<5} {file['name']:<40} {file['date']}")

# 🔨 Main execution - YOUR CODE STARTS HERE
if __name__ == "__main__":
    # Ask user for folder to scan
    folder = input("Enter folder path (leave blank for current): ").strip() or "."
    
    print(f"\n🔍 Scanning: {folder}")
    
    # Scan the folder
    files = scan_folder(folder)
    print(f"Found {len(files)} files")
    
    # Prioritize them
    prioritized = prioritize_files(files, folder)
    
    # Display results
    display_prioritized_list(prioritized)
    
    print("\n💡 Tip: Update star scores to rank more specific resources!")
# 🌟 Star Rating System - Add this section above if __name__ == "__main__"

import json
from pathlib import Path

def prompt_star_rating(filename):
    """Ask user to rate a file with stars (1-5)"""
    while True:
        try:
            rating = input(f"\n🌟 Rate '{filename}': (⭐⭐⭐⭐⭐ = ? 0-5). ")
            rating = int(rating)
            if rating < 0 or rating > 5:
                print("Invalid rating. Please enter 0-5.")
                continue
            return rating
        except ValueError:
            print("Invalid input. Enter a number between 0 and 5.")

def save_ratings_to_file(ratings_file='resource_ratings.json', ratings=None):
    """Persist star ratings to JSON file so they're remembered"""
    if ratings is None:
        ratings = {}
    
    with open(ratings_file, 'w') as f:
        json.dump(ratings, f, indent=2)

def load_ratings_from_file(ratings_file='resource_ratings.json'):
    """Load saved ratings from JSON file"""
    try:
        with open(ratings_file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        return {}

def calculate_star_score_with_file(filename, ratings_file='resource_ratings.json'):
    """Check for saved rating first, otherwise prompt for new one"""
    current_ratings = load_ratings_from_file(ratings_file)
    
    if filename in current_ratings:
        # Return stored rating silently (no prompt this time)
        return current_ratings[filename]
    
    else:
        # No saved rating yet - ask user to rate it
        return prompt_star_rating(filename)
