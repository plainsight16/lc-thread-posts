from twitter import client
from gist import post_gist, create_gist_from_editor
from progress import load_progress, save_progress

def post_solution(problem_name):
    """Post the LeetCode solution to X"""
    gist_url = create_gist_from_editor(problem_name)
    # Load current progress
    progress = load_progress()
    day = progress["day"] + 1
    thread_id = progress["thread_id"]

    # Create tweet text
    tweet_text = f"Day {day}\n\n{problem_name}\n\n{gist_url}"

    if len(tweet_text) > 280:
        raise ValueError("Tweet exceeds 280 characters")

    print("\n" + "=" * 50)
    print("TWEET PREVIEW:")
    print("=" * 50)
    print(tweet_text)
    print("=" * 50)

    # Confirm before posting
    confirm = input("\nPost this tweet? (yes/no): ").strip().lower()
    if confirm not in ["yes", "y"]:
        print("Cancelled. Tweet not posted.")
        return

    try:
        # Post tweet
        if thread_id is None:
            # First tweet - start the thread
            print("\nPosting Day 1 and starting thread...")
            response = client.create_tweet(
                text=tweet_text)
            new_thread_id = response.data["id"] #type:ignore
            print(f"Thread started with Day {day}!")
        else:
            # Reply to the existing thread
            print(f"\nPosting Day {day} as reply to thread...")
            response = client.create_tweet(
                text=tweet_text,
                in_reply_to_tweet_id=thread_id
            )
            new_thread_id = thread_id  # Keep the original thread ID
            print(f"Day {day} posted to thread!")

        # Save progress
        save_progress(day, new_thread_id)

        # Show tweet URL
        tweet_url = f"https://x.com/user/status/{response.data['id']}"
        print(f"\nView your tweet: {tweet_url}")

    except Exception as e:
        print(f"\nError posting tweet: {e}")
        print("Your progress was NOT saved.")


def main():
    """Main function"""
    print("\n" + "=" * 50)
    print("LEETCODE X POSTER")
    print("=" * 50 + "\n")
    
    problem_name = input("Enter Problem Name: ").strip()

    if not problem_name:
        print("Error: Problem name cannot be empty")
        return

    # Post the solution
    post_solution(problem_name)


if __name__ == "__main__":
    main()
