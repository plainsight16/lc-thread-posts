import tweepy
import os
class TwitterClient():
    def __init__(self):
        self.client = tweepy.Client(
        consumer_key=self._require("TWITTER_API_KEY"),
        consumer_secret=self._require("TWITTER_API_SECRET"),
        access_token=self._require("TWITTER_ACCESS_TOKEN"),
        access_token_secret=self._require("TWITTER_ACCESS_TOKEN_SECRET")
    )
    
    def start_thread(self, text:str):
        response = self.client.create_tweet(text=text)
        return response.data["id"] #type:ignore
    
    def test_credentials(self):
        me = self.client.get_me()
        return f"Logged in as: @{me.data.username}" #type:ignore
    
    def post_tweet(self, tweet_text:str, thread_id=None):
        if thread_id:
            return self.client.create_tweet(
                text=tweet_text,
                in_reply_to_tweet_id=thread_id).data["id"] #type:ignore
        return self.client.create_tweet(text=tweet_text).data["id"] #type:ignore
    
    @staticmethod
    def _require(key:str):
        value = os.getenv(key)
        if not value:
            raise ValueError(f"Missing required env: {key}")
        return value