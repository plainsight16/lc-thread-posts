import tweepy
from dotenv import load_dotenv
import os
import json

# Load environment variables
load_dotenv()

# Get Twitter credentials
API_KEY = os.getenv("TWITTER_API_KEY")
API_SECRET = os.getenv("TWITTER_API_SECRET")
ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")

# Authenticate
client = tweepy.Client(
    bearer_token=BEARER_TOKEN,
    consumer_key=API_KEY,
    consumer_secret=API_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_TOKEN_SECRET
)

print("=" * 50)
print("THREAD STARTER - POST INTRODUCTION TWEET")
print("=" * 50)

intro_text = input("\nEnter your introduction tweet (e.g., 'a thread of my daily submissions - leetcode'): ").strip()

if not intro_text:
    print("Error: Introduction text cannot be empty")
    exit(1)

print("\n" + "=" * 50)
print("TWEET PREVIEW:")
print("=" * 50)
print(intro_text)
print("=" * 50)

confirm = input("\nPost this as your thread starter? (yes/no): ").strip().lower()

if confirm not in ['yes', 'y']:
    print("Cancelled. Tweet not posted.")
    exit(0)

try:
    # Post the introduction tweet
    response = client.create_tweet(
        text=intro_text,
        reply_settings="mentionedUsers"
    )
    thread_id = response.data['id']
    
    # Create progress.json with day 0 and the thread ID
    progress = {
        "day": 0,
        "thread_id": thread_id
    }
    
    with open('progress.json', 'w') as f:
        json.dump(progress, f, indent=2)
    
    print("\nSuccess! Thread starter posted!")
    print(f"Tweet URL: https://x.com/user/status/{thread_id}")
    print(f"\nThread ID saved to progress.json")
    print("You can now run 'python post_leetcode.py' to post Day 1!")
    
except Exception as e:
    print(f"\nError posting tweet: {e}")