import tweepy
from dotenv import load_dotenv
import os


load_dotenv()

# Get Twitter credentials from environment variables
API_KEY = os.getenv("TWITTER_API_KEY")
API_SECRET = os.getenv("TWITTER_API_SECRET")
ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")

# Check if all credentials are loaded
if not all([API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET, BEARER_TOKEN]):
    print("Error: Missing Twitter credentials in .env file")
    print("Please check your .env file and make sure all keys are filled in.")
    exit(1)

# Authenticate with Twitter
try:
    client = tweepy.Client(
        bearer_token=BEARER_TOKEN,
        consumer_key=API_KEY,
        consumer_secret=API_SECRET,
        access_token=ACCESS_TOKEN,
        access_token_secret=ACCESS_TOKEN_SECRET,
    )
    print("Successfully connected to X API")
except Exception as e:
    print(f"Error connecting to X: {e}")
    exit(1)