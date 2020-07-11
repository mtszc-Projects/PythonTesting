import re
import json
import requests
from urllib.parse import urljoin


USERS_API = "https://api.github.com/users/"


class Twitter:
    version = '1.0'

    def __init__(self, backend=None, username=None):
        self.backend = backend
        self._tweets = []
        self.username = username

    @property
    def tweets(self):
        if self.backend and not self._tweets:
            backend_text = self.backend.read()
            if backend_text:
                self._tweets = json.loads(backend_text)
        return self._tweets

    @property
    def tweet_messages(self):
        return [tweet['message'] for tweet in self.tweets]

    def get_user_avatar(self):
        if not self.username:
            return None
        url = urljoin(USERS_API, self.username)
        resp = requests.get(url)
        return resp.json()['avatar_url']

    def tweet(self, message):
        if len(message) > 160:
            raise Exception("Message too long.")
        self.tweets.append({'message': message, 'avatar': self.get_user_avatar()})
        if self.backend:
            self.backend.write(json.dumps(self.tweets))

    @staticmethod
    def find_hashtags(message):
        return [m.lower() for m in re.findall(r"#(\w+)", message)]  # raw string added to avoid invalid escape sequence
