#!/usr/bin/env python3
import json
import os

# must be in dir
FOLLOWING_FILE = "following.json"
FOLLOWERS_FILE = "followers_1.json"
OUTPUT_FILE = "non_followers.txt"

def load_following(path):
    """Return a set of usernames you’re following (from relationships_following)."""
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    users = {
        sld["value"]
        for entry in data.get("relationships_following", [])
        for sld in entry.get("string_list_data", [])
        if "value" in sld
    }
    return users

def load_followers(path):
    """Return a set of usernames who follow you (from the followers list)."""
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    users = {
        sld["value"]
        for entry in data
        for sld in entry.get("string_list_data", [])
        if "value" in sld
    }
    return users

def main():
    # ensure files exist
    for fname in (FOLLOWING_FILE, FOLLOWERS_FILE):
        if not os.path.isfile(fname):
            print(f"Error: '{fname}' not found in current directory.")
            return

    following = load_following(FOLLOWING_FILE)
    followers = load_followers(FOLLOWERS_FILE)

    non_followers = sorted(following - followers)
    if not non_followers:
        print("Everyone you follow follows you back!")
    else:
        print("Profiles you follow who do NOT follow you back:\n")
        for u in non_followers:
            print(u)
        # write to file
        with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
            out.write("\n".join(non_followers))
        print(f"\nWrote {len(non_followers)} usernames to '{OUTPUT_FILE}'")

if __name__ == "__main__":
    main()
