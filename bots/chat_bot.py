"""
Python Slack Bot class for use with the ronnie-bot app!
"""
import os
import json
from datetime import datetime
from slackclient import SlackClient
from httplib import HTTPSConnection
from chatterbot import ChatBot as CBot
# To remember which teams have authorized your app and what tokens are
# associated with each team, we can store this information in memory on
# as a global object. When your bot is out of development, it's best to
# save this in a more persistant memory store.
authed_teams = {}


class ChatBot(object):
    """ ChatBot is a chatty Kathy.  He generally annoys his teammates"""

    def __init__(self):
        super(ChatBot, self).__init__()
        self.name = "ronnie-bot"
        self.oauth = {"client_id": os.environ.get("CLIENT_ID"),
                      "client_secret": os.environ.get("CLIENT_SECRET"),
                      "bot_token": os.environ.get("BOT_TOKEN"),
                      "app_token": os.environ.get("APP_TOKEN"),
                      "scope": "bot, chat:write:bot, reactions:write, users:read"}
        self.verification = os.environ.get("VERIFICATION_TOKEN")
        self.bot_client = SlackClient(self.oauth["bot_token"])
        self.app_client = SlackClient(self.oauth["app_token"])
        self.last_insult = datetime.fromtimestamp(1521339343)
        self.chatter_bot = None
        self.processed_events = []

    def auth(self, code):
        """
        Authenticate with OAuth and assign correct scopes.
        Save a dictionary of authed team information in memory on the bot
        object. Code is a temporary authorization code sent by Slack to be
        exchanged for an OAuth token
        """
        self.bot_client = SlackClient("")
        auth_response = self.bot_client.api_call(
            "oauth.access",
            client_id=self.oauth["client_id"],
            client_secret=self.oauth["client_secret"],
            code=code
        )
        print(auth_response)
        team_id = auth_response["team_id"]
        authed_teams[team_id] = {"bot_token":
                                 auth_response["bot"]["bot_access_token"]}
        self.bot_client = SlackClient(authed_teams[team_id]["bot_token"])

    def insult_teammates(self, slack_event):
        """
        Occassionally Ronnie-bot likes to insult his team mates.
        He's a freaking jerk.
        """
        event_datetime = datetime.fromtimestamp(
            float(slack_event["event_ts"]))

        datetime_delta = event_datetime - self.last_insult
        if (datetime_delta.total_seconds() > 43200 and not
                self.event_previously_processed(slack_event["event_ts"])):
            insult = self.build_insult(slack_event["user"])
            self.app_client.api_call(
                "chat.postMessage",
                channel=slack_event["channel"],
                text=insult
            )
            self.last_insult = event_datetime

    def chatter(self, slack_event):
        """Ronnie Bot defers to Chatter-Bot for talking."""
        if not self.event_previously_processed(slack_event["event_ts"]):
            self.setup_chatter_bot()
            chatter_response = self.chatter_bot.get_response(
                slack_event["text"])
            self.app_client.api_call(
                "chat.postMessage",
                channel=slack_event["channel"],
                text=chatter_response
            )

    def react_negatively(self, slack_event):
        """Ronnie Bot likes to down vote things other people support."""
        if not self.event_previously_processed(slack_event["event_ts"]):
            self.app_client.api_call(
                "reactions.add",
                channel=slack_event["item"]["channel"],
                name="poop",
                timestamp=slack_event["item"]["ts"]
            )

    def build_insult(self, user_id):
        """mattbas.org is an awesome insult generator!"""
        response_user = self.app_client.api_call(
            "users.info",
            user=user_id
        )
        print(response_user)
        user_name = response_user["user"]["name"]
        insult_api_conn = HTTPSConnection("insult.mattbas.org")
        insult_api_conn.request("GET", "/api/insult.json?who=%s" % user_name)
        insult_api_response = json.loads(insult_api_conn.getresponse().read())
        return insult_api_response["insult"]

    def event_previously_processed(self, event_id):
        """If this event was previously processed, exit."""
        if event_id in self.processed_events:
            return True
        else:
            self.processed_events.append(event_id)
            return False

    def setup_chatter_bot(self):
        """Only Instantiate chatter_bot if necessary."""
        if self.chatter_bot is None:
            self.chatter_bot = CBot(
                'ronnie-bot',
                trainer='chatterbot.trainers.ChatterBotCorpusTrainer',
                preprocessors=['chatterbot.preprocessors.clean_whitespace'],
                logic_adapters=[
                    {
                        "import_path": "chatterbot.logic.BestMatch",
                        "statement_comparison_function":
                            "chatterbot.comparisons.levenshtein_distance",
                        "response_selection_method":
                            "chatterbot.response_selection.get_first_response"
                    },
                    {
                        'import_path': 'chatterbot.logic.LowConfidenceAdapter',
                        'threshold': 0.5,
                        'default_response':
                            'Sorry, but my AI sucks, and I do not understand.'
                    }
                ],
                storage_adapter='chatterbot.storage.SQLStorageAdapter',
                database='/tmp/database.sqlite3'
            )
            self.chatter_bot.train("chatterbot.corpus.english")
