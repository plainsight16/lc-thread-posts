import tweepy
from dotenv import load_dotenv
import os
import json

# Load environment variables from .env file
load_dotenv()

# Get Twitter credentials from environment variables
API_KEY = os.getenv("TWITTER_API_KEY")
API_SECRET = os.getenv("TWITTER_API_SECRET")
ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")

# Check if all credentials are loaded
if not all([API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET, BEARER_TOKEN]):
    print("❌ Error: Missing Twitter credentials in .env file")
    print("Please check your .env file and make sure all keys are filled in.")
    exit(1)

# Authenticate with Twitter
try:
    client = tweepy.Client(
        bearer_token=BEARER_TOKEN,
        consumer_key=API_KEY,
        consumer_secret=API_SECRET,
        access_token=ACCESS_TOKEN,
        access_token_secret=ACCESS_TOKEN_SECRET
    )
    print("✅ Successfully connected to Twitter API")
except Exception as e:
    print(f"❌ Error connecting to Twitter: {e}")
    exit(1)


def load_progress():
    """Load the current day number and thread ID from progress.json"""
    try:
        with open('progress.json', 'r') as f:
            data = json.load(f)
            print(f"📊 Current progress: Day {data['day']}")
            return data
    except FileNotFoundError:
        print("📊 No previous progress found. Starting fresh!")
        return {"day": 0, "thread_id": None}


def save_progress(day, thread_id):
    """Save the current day number and thread ID to progress.json"""
    with open('progress.json', 'w') as f:
        json.dump({"day": day, "thread_id": thread_id}, f, indent=2)
    print(f"💾 Progress saved: Day {day}")


def post_solution(gist_url, problem_name):
    """Post the LeetCode solution to Twitter"""
    
    # Load current progress
    progress = load_progress()
    day = progress["day"] + 1
    thread_id = progress["thread_id"]
    
    # Create tweet text
    tweet_text = f"Day {day}\n\n{problem_name}\n\n{gist_url}"
    
    print("\n" + "="*50)
    print("TWEET PREVIEW:")
    print("="*50)
    print(tweet_text)
    print("="*50)
    
    # Confirm before posting
    confirm = input("\nPost this tweet? (yes/no): ").strip().lower()
    if confirm not in ['yes', 'y']:
        print("❌ Cancelled. Tweet not posted.")
        return
    
    try:
        # Post tweet
        if thread_id is None:
            # First tweet - start the thread
            print("\n🚀 Posting Day 1 and starting thread...")
            response = client.create_tweet(text=tweet_text)
            new_thread_id = response.data['id']
            print(f"✅ Thread started with Day {day}!")
        else:
            # Reply to the existing thread
            print(f"\n🚀 Posting Day {day} as reply to thread...")
            response = client.create_tweet(
                text=tweet_text,
                in_reply_to_tweet_id=thread_id
            )
            new_thread_id = thread_id  # Keep the original thread ID
            print(f"✅ Day {day} posted to thread!")
        
        # Save progress
        save_progress(day, new_thread_id)
        
        # Show tweet URL
        tweet_url = f"https://twitter.com/user/status/{response.data['id']}"
        print(f"\n🔗 View your tweet: {tweet_url}")
        
    except Exception as e:
        print(f"\n❌ Error posting tweet: {e}")
        print("Your progress was NOT saved.")


def main():
    """Main function"""
    print("\n" + "="*50)
    print("🚀 LEETCODE TWITTER POSTER")
    print("="*50 + "\n")
    
    # Get input from user
    gist_url = input("📝 Enter Gist URL: ").strip()
    
    if not gist_url:
        print("❌ Error: Gist URL cannot be empty")
        return
    
    problem_name = input("📝 Enter Problem Name: ").strip()
    
    if not problem_name:
        print("❌ Error: Problem name cannot be empty")
        return
    
    # Post the solution
    post_solution(gist_url, problem_name)


if __name__ == "__main__":
    main()