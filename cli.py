import sys
from dotenv import load_dotenv

from twitter import TwitterClient
from progress import init_thread, load_progress, save_progress
from editor import open_editor
from template import DEFAULT_TEMPLATE
from gist import create_gist



load_dotenv()

def start_thread_command():
    print("=" * 50)
    print("THREAD STARTER - POST INTRODUCTION TWEET")
    print("=" * 50)

    intro_text = input("Enter your introduction tweet (e.g., 'a thread of my daily submissions - leetcode'): ").strip()

    if not intro_text:
        print("Intro text cannot be empty")
        return
    
    print("\n" + "=" * 50)
    print("TWEET PREVIEW:")
    print("=" * 50)
    print(intro_text)
    print("=" * 50)

    confirm = input("\nPost this tweet? (yes/no): ").strip().lower()
    if confirm not in ["yes", "y"]:
        print("Cancelled!")
        return

    twitter = TwitterClient()
    thread_id = twitter.post_tweet(intro_text)
    init_thread(thread_id)

    print("Thread started successfully")
    print(f"https://x.com/user/status/{thread_id}")
    print("Thread ID saved to progress.json")
    print("You can now run 'python post_leetcode.py' to post Day 1!")


def post_leetcode_command(problem_name:str):
    markdown = open_editor(problem_name, DEFAULT_TEMPLATE)
    
    gist_url = create_gist(
        title=problem_name,
        content=markdown
    )
    progress = load_progress()
    day = progress["day"] + 1
    thread_id = progress["thread_id"]

    tweet = (
        f"Day {day}\n\n"
        f"{problem_name}\n\n"
        f"{gist_url}"
    )

    print("\n" + "=" * 50)
    print("TWEET PREVIEW:")
    print("=" * 50)
    print(tweet)
    print("=" * 50)

    confirm = input("\nPost this tweet? (yes/no): ").strip().lower()
    if confirm not in ["yes", "y"]:
        print("Cancelled!")
        return

    twitter = TwitterClient()
    res = twitter.post_tweet(tweet, thread_id)

    new_thread_id = res.data["id"]
    save_progress(day, new_thread_id)

    tweet_url = f"https://x.com/user/status/{new_thread_id}"
    print(f"Tweet: {tweet_url}")
    print(f"Gist: {gist_url}")


def main():
    if len(sys.argv) < 2:
        print("Usage")
        print("leetcode-post start-thread")
        print("leetcode-post post <problem-name>")
    
    command = sys.argv[1]

    if command == "start-thread":
        start_thread_command()
    
    elif command == "post":
        if len(sys.argv) < 3:
            print("Error: problem name required")
            sys.exit(1)
        problem_name = sys.argv[2]
        post_leetcode_command(problem_name)
    
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

    if __name__ == "__main__":
        print("\n" + "=" * 50)
        print("LEETCODE X POSTER")
        print("=" * 50 + "\n")
        main()
